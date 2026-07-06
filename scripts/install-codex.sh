#!/usr/bin/env bash
# Install agents Codex config to $CODEX_HOME (defaults to ~/.codex)
# Usage: ./scripts/install-codex.sh [--dry-run] [--diff] [--prune] [--uninstall]
#
# Adapted from repos/harness/scripts/install-codex.sh for this repo's owned assets
# (generic personal/global skills, global AGENTS.md instructions). This repo owns
# no Codex hooks — the Codex stop-gate hook (hooks.json/hooks/stop.sh) and its
# sibling notifications.sh stay Harness-owned (stop.sh sources notifications.sh as
# a sibling, so splitting them across repos would break the gate) — so all hooks
# install/prune logic is intentionally omitted here. Follows
# docs/skill-installer-contract.md.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_ROOT="$REPO_DIR/codex"
SKILLS_SRC="$SRC_ROOT/skills"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DST="$CODEX_HOME/skills"
# Records which static repo docs the installer copied, so --prune can reconcile
# stale repo-managed copied docs without touching unmanaged user docs.
DOC_MANIFEST="$CODEX_HOME/.agents-doc-manifest"

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
            echo "  --prune      Remove repo-managed installed skills not present in the source tree"
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

is_managed_agents_file() {
    local dst_file="$1"

    [[ ! -s "$dst_file" ]] && return 0
    head -n 1 "$dst_file" | grep -qx '# Global Codex Instructions'
}

# Repo-managed skill allowlist. Anything not on this list is left alone even with
# --prune/--uninstall. This repo owns no harness-* skills, so there is no
# harness-* prefix branch (that stays Harness's own allowlist).
is_repo_managed_skill() {
    local skill_name="$1"

    case "$skill_name" in
        architecture-review|archify|ask-chatgpt-pro|ask-oracle|babysit-pr|codex-project-init|diagnose|distill-source|doc-audit|docker-optimize|fix-build|goal-prompt|grill-with-docs|gtsam-doc|integrate-research|prepare-dynamic-workflow|prototype|research-prompt|review-change|session-handoff|skill-lifecycle|thermo-nuclear-code-quality-review|tdd|zoom-out) return 0 ;;
        *) return 1 ;;
    esac
}

sync_file() {
    local src_file="$1"
    local dst_file="$2"
    local rel="$3"

    if [[ ! -f "$dst_file" ]]; then
        if $SHOW_DIFF; then
            echo "NEW  $rel"
        fi
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

if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "Source directory not found: $SKILLS_SRC" >&2
    exit 1
fi

if $UNINSTALL; then
    # Uninstall: remove every repo-owned install target regardless of current
    # source-tree state (stronger than --prune, which only removes what source
    # no longer has). Never touches anything outside the owned set below.
    if [[ -d "$SKILLS_DST" ]]; then
        for installed_dir in "$SKILLS_DST"/*/; do
            [[ -d "$installed_dir" ]] || continue
            skill_name="$(basename "$installed_dir")"
            if is_repo_managed_skill "$skill_name"; then
                if $DRY_RUN; then
                    echo "  would remove: $installed_dir"
                else
                    rm -rf "$installed_dir"
                    echo "  removed: $skill_name"
                fi
                removed=$((removed + 1))
            fi
        done
    fi
    if [[ -f "$SRC_ROOT/AGENTS.md" ]] && is_managed_agents_file "$CODEX_HOME/AGENTS.md"; then
        if [[ -f "$CODEX_HOME/AGENTS.md" ]]; then
            if $DRY_RUN; then
                echo "  would remove: AGENTS.md"
            else
                rm "$CODEX_HOME/AGENTS.md"
                echo "  removed: AGENTS.md"
            fi
            removed=$((removed + 1))
        fi
    fi

    # Reconcile the doc manifest: uninstall removes everything this repo copied.
    if [[ -f "$DOC_MANIFEST" ]]; then
        while IFS= read -r doc; do
            [[ -z "$doc" ]] && continue
            installed="$CODEX_HOME/$doc"
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

mkdir -p "$SKILLS_DST"

if [[ -f "$SRC_ROOT/AGENTS.md" ]]; then
    if is_managed_agents_file "$CODEX_HOME/AGENTS.md"; then
        sync_file "$SRC_ROOT/AGENTS.md" "$CODEX_HOME/AGENTS.md" "AGENTS.md"
    else
        echo "  skipped unmanaged global file: $CODEX_HOME/AGENTS.md"
        skipped=$((skipped + 1))
    fi
fi

for skill_dir in "$SKILLS_SRC"/*/; do
    [[ -d "$skill_dir" ]] || continue
    skill_name="$(basename "$skill_dir")"
    while IFS= read -r -d '' file; do
        rel_path="${file#$skill_dir}"
        sync_file "$file" "$SKILLS_DST/$skill_name/$rel_path" "skills/$skill_name/$rel_path"
    done < <(find "$skill_dir" -type f -print0)
done

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
    [[ -d "$SKILLS_SRC" ]] || return 0
    local doc
    while IFS= read -r doc; do
        [[ -z "$doc" ]] && continue
        case "$doc" in
            *RUN_ID*|*YYYYMMDD*) continue ;;
        esac
        [[ -f "$REPO_DIR/$doc" ]] || continue
        printf '%s\n' "$doc"
    done < <(
        find "$SKILLS_SRC" -type f -print0 |
            xargs -0 perl -ne 'while (/(^|[^\/])(docs\/[A-Za-z0-9\/_.-]+\.md)/g) { print "$2\n" }' |
            sort -u
    )
}

CURRENT_DOCS="$(managed_doc_set)"

# Copy the current managed doc set into the install tree.
while IFS= read -r doc; do
    [[ -z "$doc" ]] && continue
    sync_file "$REPO_DIR/$doc" "$CODEX_HOME/$doc" "$doc"
done <<< "$CURRENT_DOCS"

if $PRUNE; then
    # Stale repo-managed copied docs: docs we previously copied (recorded in the
    # manifest) that the current skill set no longer references. Unmanaged user
    # docs are never recorded in the manifest, so they are never removed.
    if [[ -f "$DOC_MANIFEST" ]]; then
        while IFS= read -r doc; do
            [[ -z "$doc" ]] && continue
            grep -qxF "$doc" <<< "$CURRENT_DOCS" && continue
            installed="$CODEX_HOME/$doc"
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
    for installed_dir in "$SKILLS_DST"/*/; do
        [[ -d "$installed_dir" ]] || continue
        skill_name="$(basename "$installed_dir")"
        if [[ "$skill_name" == .* || "$skill_name" == "codex-primary-runtime" ]]; then
            skipped=$((skipped + 1))
            continue
        fi
        if ! is_repo_managed_skill "$skill_name"; then
            skipped=$((skipped + 1))
            continue
        fi
        if [[ ! -d "$SKILLS_SRC/$skill_name" ]]; then
            if $DRY_RUN; then
                echo "  would remove: $installed_dir"
            else
                rm -rf "$installed_dir"
                echo "  removed: $skill_name"
            fi
            removed=$((removed + 1))
        fi
    done
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
