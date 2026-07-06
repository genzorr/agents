#!/usr/bin/env bash
# Install agents Claude config (agents, commands, rules, skills, hooks) to $CLAUDE_HOME (defaults to ~/.claude)
# Usage: ./scripts/install-claude.sh [--dry-run] [--diff] [--prune] [--uninstall]
#
# Adapted from repos/harness/scripts/install-claude.sh for this repo's owned assets
# (generic personal/global skills, commands, subagents, rules, notification hook).
# Follows docs/skill-installer-contract.md. Preserves the Harness script's hook/
# config safety guards (settings.json hooks merge) unchanged.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_ROOT="$REPO_DIR/claude"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
# Records which static repo docs the installer copied, so --prune can reconcile
# stale repo-managed copied docs without touching unmanaged user docs.
DOC_MANIFEST="$CLAUDE_HOME/.agents-doc-manifest"

DRY_RUN=false
SHOW_DIFF=false
PRUNE=false
UNINSTALL=false

for arg in "$@"; do
    case "$arg" in
        --dry-run)    DRY_RUN=true ;;
        --diff)       SHOW_DIFF=true ;;
        --prune)      PRUNE=true ;;
        --uninstall)  UNINSTALL=true ;;
        --help|-h)
            echo "Usage: $0 [--dry-run] [--diff] [--prune] [--uninstall]"
            echo "  --dry-run    Show what would be copied without writing"
            echo "  --diff       Show diffs between source and installed files"
            echo "  --prune      Remove repo-managed installed entries not present in source"
            echo "  --uninstall  Remove ALL repo-owned install targets, regardless of source state"
            exit 0
            ;;
        *) echo "Unknown option: $arg"; exit 1 ;;
    esac
done

changed=0
skipped=0
added=0
removed=0

# Repo-managed allowlists. Anything not on these lists is left alone even with
# --prune/--uninstall. This repo owns no harness-* skills, so there is no
# harness-* prefix branch (that stays Harness's own allowlist).
is_repo_managed_skill() {
    case "$1" in
        architecture-review|archify|ask-chatgpt-pro|ask-oracle|babysit-pr|custom-init|diagnose|distill-source|doc-audit|docker-optimize|fix-build|goal-prompt|grill-with-docs|gtsam-doc|integrate-research|prepare-dynamic-workflow|prototype|research-prompt|review-change|session-handoff|skill-lifecycle|thermo-nuclear-code-quality-review|tdd|zoom-out) return 0 ;;
        *) return 1 ;;
    esac
}

is_repo_managed_agent() {
    case "$1" in
        code-reviewer.md|planner.md) return 0 ;;
        *) return 1 ;;
    esac
}

is_repo_managed_command() {
    case "$1" in
        dual-review.md|plan.md) return 0 ;;
        *) return 1 ;;
    esac
}

is_repo_managed_rule() {
    case "$1" in
        conciseness.md|reading-discipline.md|surgical-changes.md|think-before-coding.md) return 0 ;;
        *) return 1 ;;
    esac
}

is_repo_managed_hook() {
    case "$1" in
        notifications.sh) return 0 ;;
        *) return 1 ;;
    esac
}

sync_file() {
    local src_file="$1"
    local dst_file="$2"
    local rel="$3"

    if [[ ! -f "$dst_file" ]]; then
        if $SHOW_DIFF; then echo "NEW  $rel"; fi
        if $DRY_RUN; then
            echo "  would create: $dst_file"
        else
            mkdir -p "$(dirname "$dst_file")"
            cp "$src_file" "$dst_file"
            echo "  added: $rel"
        fi
        added=$((added + 1))
    elif ! diff -q "$src_file" "$dst_file" > /dev/null 2>&1; then
        if $SHOW_DIFF; then
            echo "CHANGED  $rel"
            diff --color=auto -u "$dst_file" "$src_file" || true
            echo
        fi
        if $DRY_RUN; then
            echo "  would update: $dst_file"
        else
            cp "$src_file" "$dst_file"
            echo "  updated: $rel"
        fi
        changed=$((changed + 1))
    else
        skipped=$((skipped + 1))
    fi
}

# Sync flat directories (agents, commands, rules).
sync_flat() {
    local category="$1"
    [[ -d "$SRC_ROOT/$category" ]] || return 0
    for f in "$SRC_ROOT/$category"/*.md; do
        [[ -f "$f" ]] || continue
        sync_file "$f" "$CLAUDE_HOME/$category/$(basename "$f")" "$category/$(basename "$f")"
    done
}

# The static repo docs that skills reference and should travel into the install
# tree, so a relative `docs/<name>.md` reference inside a skill resolves after
# install. The set is discovered dynamically from the source skill bodies, then
# filtered: absolute cross-repo paths (`/.../docs/<name>.md`) are not travel
# candidates for this repo; run-local templated paths (docs/harness/ops/RUN_ID/*,
# docs/audits/YYYYMMDD-*) are skipped because they are generated inside a run
# directory at runtime; and any reference that is not a real repo file
# (illustrative example paths) is skipped too. Echoes one repo-relative path per
# line, sorted and unique.
managed_doc_set() {
    [[ -d "$SRC_ROOT/skills" ]] || return 0
    local doc
    while IFS= read -r doc; do
        [[ -z "$doc" ]] && continue
        case "$doc" in
            *RUN_ID*|*YYYYMMDD*) continue ;;
        esac
        [[ -f "$REPO_DIR/$doc" ]] || continue
        printf '%s\n' "$doc"
    done < <(
        find "$SRC_ROOT/skills" -type f -print0 |
            xargs -0 perl -ne 'while (/(^|[^\/])(docs\/[A-Za-z0-9\/_.-]+\.md)/g) { print "$2\n" }' |
            sort -u
    )
}

# Merge hooks.json into settings.json. Claude Code reads hooks from settings.json;
# we never overwrite the file, only set/replace the `hooks` key — and only if the
# existing hooks block is empty or already points at our managed hook scripts.
merge_hooks_into_settings() {
    local src="$SRC_ROOT/hooks.json"
    local dst="$CLAUDE_HOME/settings.json"
    [[ -f "$src" ]] || return 0

    if ! command -v jq >/dev/null 2>&1; then
        echo "  skipped settings.json merge: jq not available"
        skipped=$((skipped + 1))
        return 0
    fi

    local rendered
    rendered="$(sed "s#__CLAUDE_HOME__#$CLAUDE_HOME#g" "$src")"

    if [[ ! -f "$dst" ]]; then
        if $DRY_RUN; then
            echo "  would create: $dst (with hooks block)"
            added=$((added + 1))
            return 0
        fi
        echo "{}" > "$dst"
    fi

    local managed existing_empty
    existing_empty="$(jq '(.hooks // {}) | (type == "object" and length == 0) or (type == "array" and length == 0) or . == null' "$dst")"
    managed=true
    if [[ "$existing_empty" != "true" ]]; then
        # Managed = every leaf command invokes our notifications.sh script.
        # Matches both literal paths and "$HOME/.claude/hooks/notifications.sh ..." forms.
        while IFS= read -r cmd; do
            [[ -z "$cmd" ]] && continue
            case "$cmd" in
                *"/hooks/notifications.sh"*) ;;
                *) managed=false; break ;;
            esac
        done < <(jq -r '.hooks // {} | to_entries[] | .value[]? | .hooks[]?.command // empty' "$dst")
    fi

    if ! $managed; then
        echo "  skipped settings.json hooks merge: unmanaged hook entries present in $dst"
        skipped=$((skipped + 1))
        return 0
    fi

    local merged
    merged="$(jq --argjson new "$rendered" '. + {hooks: $new.hooks}' "$dst")"
    if [[ "$merged" == "$(cat "$dst")" ]]; then
        skipped=$((skipped + 1))
        return 0
    fi

    if $SHOW_DIFF; then
        echo "CHANGED  settings.json (hooks key)"
        diff --color=auto -u "$dst" <(echo "$merged") || true
        echo
    fi
    if $DRY_RUN; then
        echo "  would update: $dst (hooks key)"
    else
        echo "$merged" > "$dst"
        echo "  updated: settings.json (hooks key)"
    fi
    changed=$((changed + 1))
}

# Remove the hooks key from settings.json on --uninstall, but only if it is
# entirely managed (every leaf command points at our notifications.sh) — an
# unmanaged hooks block is left untouched, same guard direction as the merge.
unmerge_hooks_from_settings() {
    local dst="$CLAUDE_HOME/settings.json"
    [[ -f "$dst" ]] || return 0

    if ! command -v jq >/dev/null 2>&1; then
        echo "  skipped settings.json hooks removal: jq not available"
        skipped=$((skipped + 1))
        return 0
    fi

    local existing_empty managed
    existing_empty="$(jq '(.hooks // {}) | (type == "object" and length == 0) or (type == "array" and length == 0) or . == null' "$dst")"
    if [[ "$existing_empty" == "true" ]]; then
        return 0
    fi

    managed=true
    while IFS= read -r cmd; do
        [[ -z "$cmd" ]] && continue
        case "$cmd" in
            *"/hooks/notifications.sh"*) ;;
            *) managed=false; break ;;
        esac
    done < <(jq -r '.hooks // {} | to_entries[] | .value[]? | .hooks[]?.command // empty' "$dst")

    if ! $managed; then
        echo "  skipped settings.json hooks removal: unmanaged hook entries present in $dst"
        skipped=$((skipped + 1))
        return 0
    fi

    local merged
    merged="$(jq 'del(.hooks)' "$dst")"
    if $SHOW_DIFF; then
        echo "CHANGED  settings.json (hooks key removed)"
        diff --color=auto -u "$dst" <(echo "$merged") || true
        echo
    fi
    if $DRY_RUN; then
        echo "  would remove: $dst (hooks key)"
    else
        echo "$merged" > "$dst"
        echo "  removed: settings.json (hooks key)"
    fi
    removed=$((removed + 1))
}

if $UNINSTALL; then
    # Uninstall: remove every repo-owned install target regardless of current
    # source-tree state (stronger than --prune, which only removes what source
    # no longer has). Never touches anything outside the owned sets below.
    if [[ -d "$CLAUDE_HOME/skills" ]]; then
        for installed_dir in "$CLAUDE_HOME/skills"/*/; do
            [[ -d "$installed_dir" ]] || continue
            name="$(basename "$installed_dir")"
            [[ "$name" == .* ]] && continue
            if is_repo_managed_skill "$name"; then
                if $DRY_RUN; then
                    echo "  would remove: skills/$name"
                else
                    rm -rf "$installed_dir"
                    echo "  removed: skills/$name"
                fi
                removed=$((removed + 1))
            fi
        done
    fi
    for category in agents commands rules; do
        [[ -d "$CLAUDE_HOME/$category" ]] || continue
        check_fn="is_repo_managed_${category%s}"
        for installed_file in "$CLAUDE_HOME/$category"/*.md; do
            [[ -f "$installed_file" ]] || continue
            name="$(basename "$installed_file")"
            if $check_fn "$name"; then
                if $DRY_RUN; then
                    echo "  would remove: $category/$name"
                else
                    rm "$installed_file"
                    echo "  removed: $category/$name"
                fi
                removed=$((removed + 1))
            fi
        done
    done
    if [[ -d "$CLAUDE_HOME/hooks" ]]; then
        for installed_file in "$CLAUDE_HOME/hooks"/*; do
            [[ -f "$installed_file" ]] || continue
            name="$(basename "$installed_file")"
            if is_repo_managed_hook "$name"; then
                if $DRY_RUN; then
                    echo "  would remove: hooks/$name"
                else
                    rm "$installed_file"
                    echo "  removed: hooks/$name"
                fi
                removed=$((removed + 1))
            fi
        done
    fi
    unmerge_hooks_from_settings

    # Reconcile the doc manifest: uninstall removes everything this repo copied.
    if [[ -f "$DOC_MANIFEST" ]]; then
        while IFS= read -r doc; do
            [[ -z "$doc" ]] && continue
            installed="$CLAUDE_HOME/$doc"
            [[ -f "$installed" ]] || continue
            if $DRY_RUN; then
                echo "  would remove: $doc"
            else
                rm "$installed"
                echo "  removed: $doc"
            fi
            removed=$((removed + 1))
        done < "$DOC_MANIFEST"
        if ! $DRY_RUN; then
            rm -f "$DOC_MANIFEST"
        fi
    fi

    echo
    if $DRY_RUN; then
        echo "Dry run (uninstall): $removed would be removed, $skipped unchanged"
    else
        echo "Uninstalled: $removed removed, $skipped unchanged"
    fi
    exit 0
fi

sync_flat agents
sync_flat commands
sync_flat rules

CURRENT_DOCS="$(managed_doc_set)"

# Copy the current managed doc set into the install tree.
sync_referenced_docs() {
    local doc
    while IFS= read -r doc; do
        [[ -z "$doc" ]] && continue
        sync_file "$REPO_DIR/$doc" "$CLAUDE_HOME/$doc" "$doc"
    done <<< "$CURRENT_DOCS"
}

# Sync skills (nested directories).
if [[ -d "$SRC_ROOT/skills" ]]; then
    for skill_dir in "$SRC_ROOT/skills"/*/; do
        [[ -d "$skill_dir" ]] || continue
        skill_name="$(basename "$skill_dir")"
        while IFS= read -r -d '' file; do
            rel_path="${file#$skill_dir}"
            sync_file "$file" "$CLAUDE_HOME/skills/$skill_name/$rel_path" "skills/$skill_name/$rel_path"
        done < <(find "$skill_dir" -type f -print0)
    done
    if [[ -f "$SRC_ROOT/skills/README.md" ]]; then
        sync_file "$SRC_ROOT/skills/README.md" "$CLAUDE_HOME/skills/README.md" "skills/README.md"
    fi
fi

sync_referenced_docs

# Sync top-level claude/README.md to the install root for parity with codex/.
if [[ -f "$SRC_ROOT/README.md" ]]; then
    sync_file "$SRC_ROOT/README.md" "$CLAUDE_HOME/README.md" "README.md"
fi

# Sync hook scripts and make them executable.
if [[ -d "$SRC_ROOT/hooks" ]]; then
    while IFS= read -r -d '' file; do
        rel_path="${file#$SRC_ROOT/}"
        sync_file "$file" "$CLAUDE_HOME/$rel_path" "$rel_path"
        if ! $DRY_RUN && [[ "$file" == *.sh ]]; then
            chmod +x "$CLAUDE_HOME/$rel_path"
        fi
    done < <(find "$SRC_ROOT/hooks" -type f -print0)
fi

merge_hooks_into_settings

# Prune: remove repo-managed installed entries not present in source.
if $PRUNE; then
    # Stale repo-managed copied docs: docs we previously copied (recorded in the
    # manifest) that the current skill set no longer references. Unmanaged user
    # docs are never recorded in the manifest, so they are never removed.
    if [[ -f "$DOC_MANIFEST" ]]; then
        while IFS= read -r doc; do
            [[ -z "$doc" ]] && continue
            grep -qxF "$doc" <<< "$CURRENT_DOCS" && continue
            installed="$CLAUDE_HOME/$doc"
            [[ -f "$installed" ]] || continue
            if $DRY_RUN; then
                echo "  would remove: $doc"
            else
                rm "$installed"
                echo "  removed: $doc"
            fi
            removed=$((removed + 1))
        done < "$DOC_MANIFEST"
    fi
    if [[ -d "$CLAUDE_HOME/skills" ]]; then
        for installed_dir in "$CLAUDE_HOME/skills"/*/; do
            [[ -d "$installed_dir" ]] || continue
            name="$(basename "$installed_dir")"
            [[ "$name" == .* ]] && continue
            if is_repo_managed_skill "$name" && [[ ! -d "$SRC_ROOT/skills/$name" ]]; then
                if $DRY_RUN; then
                    echo "  would remove: skills/$name"
                else
                    rm -rf "$installed_dir"
                    echo "  removed: skills/$name"
                fi
                removed=$((removed + 1))
            fi
        done
    fi
    for category in agents commands rules; do
        [[ -d "$CLAUDE_HOME/$category" ]] || continue
        check_fn="is_repo_managed_${category%s}"
        for installed_file in "$CLAUDE_HOME/$category"/*.md; do
            [[ -f "$installed_file" ]] || continue
            name="$(basename "$installed_file")"
            if $check_fn "$name" && [[ ! -f "$SRC_ROOT/$category/$name" ]]; then
                if $DRY_RUN; then
                    echo "  would remove: $category/$name"
                else
                    rm "$installed_file"
                    echo "  removed: $category/$name"
                fi
                removed=$((removed + 1))
            fi
        done
    done
    if [[ -d "$CLAUDE_HOME/hooks" ]]; then
        for installed_file in "$CLAUDE_HOME/hooks"/*; do
            [[ -f "$installed_file" ]] || continue
            name="$(basename "$installed_file")"
            if is_repo_managed_hook "$name" && [[ ! -f "$SRC_ROOT/hooks/$name" ]]; then
                if $DRY_RUN; then
                    echo "  would remove: hooks/$name"
                else
                    rm "$installed_file"
                    echo "  removed: hooks/$name"
                fi
                removed=$((removed + 1))
            fi
        done
    fi
fi

# Reconcile the doc manifest with what is now installed. A --prune run removed
# stale docs, so the manifest becomes exactly the current set; a normal run only
# adds docs, so the manifest accumulates (union) to keep a record of anything a
# later --prune may need to reconcile. Written via a temp file because the union
# branch reads the existing manifest in the same step (a `... > $DOC_MANIFEST`
# redirect would truncate it before `cat` could read it).
if ! $DRY_RUN; then
    manifest_tmp="$(mktemp "${DOC_MANIFEST}.XXXXXX")"
    {
        [[ -n "$CURRENT_DOCS" ]] && printf '%s\n' "$CURRENT_DOCS"
        if ! $PRUNE && [[ -f "$DOC_MANIFEST" ]]; then cat "$DOC_MANIFEST"; fi
    } | sort -u | grep -v '^$' > "$manifest_tmp" || true
    mv "$manifest_tmp" "$DOC_MANIFEST"
fi

echo
if $DRY_RUN; then
    echo "Dry run: $added new, $changed changed, $removed removed, $skipped unchanged"
else
    echo "Installed: $added new, $changed updated, $removed removed, $skipped unchanged"
fi
