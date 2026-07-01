# Skill Installer Contract

A durable, repo-neutral contract for how `repos/agents`, `repos/harness`, and
`repos/session-harvester` each install, uninstall, update, and prune the Codex/Claude
assets they own. It defines the shared shape; it does not implement it. Later
implementation tasks (Agents installer, Harness installer reconciliation,
session-harvester install/uninstall) build against this contract instead of
inventing per-repo behavior.

This contract was written against the existing Harness installers
(`repos/harness/scripts/install-claude.sh`, `install-codex.sh`) as the load-bearing
precedent for hook/config safety and doc-manifest behavior. Where those scripts'
actual behavior differs from an idealized command shape, this doc says so explicitly
(see §2 and §9) rather than silently describing something that doesn't exist yet.

## 1. Purpose & scope

One installer *surface shape* is shared across three repos; there is no global,
cross-repo installer. Each repo:

- installs, uninstalls, updates, and prunes **only the assets physically present in
  that repo's own source tree** (`agents/{codex,claude}/...`,
  `harness/{codex,claude}/...`, `session-harvester/...`);
- never manages, prunes, or removes another repo's assets, even if that repo's
  install target lives in the same global `~/.codex` or `~/.claude` directory;
- never manages, prunes, or removes a foreign/unknown installed asset (e.g.
  `codex-primary-runtime`) that isn't sourced from any of these three repos.

Ownership is determined by **physical presence in the repo's own source tree**, not
by naming convention. A repo's catalog/allowlist (§7) is the authoritative
enumeration of that presence — it is generated from or checked against the source
tree, never hand-maintained as a separate claim.

## 2. Command surface

The target shape below is what future implementations may converge on. **Current
repo support is intentionally uneven and documented in §10**: Agents implements
install/prune/uninstall flags, Harness has single-mode scripts with
`--dry-run`/`--diff`/`--prune`, and session-harvester has a single-skill
install/uninstall script. This contract describes semantics and ownership
invariants first; it does not claim every repo already exposes every verb.

| Command | Mutates? | Idempotent? | What it does |
|---|---|---|---|
| `validate` | no | yes | Checks source-tree identity/coverage (see §8). Never touches install targets. |
| `status` / `diff` | no | yes | Reports source-vs-installed drift: new (in source, not installed), changed (differs), removed (installed, not in source), unmanaged (installed, not owned by this repo). Read-only equivalent of what `install --dry-run --diff` would do. |
| `install` | yes | yes | Copies source → install target for this repo's owned assets. Creates missing dirs/files, updates changed ones, never touches assets it doesn't own. Re-running with no source changes is a no-op. |
| `uninstall` | yes | yes | Removes install targets for **all** of this repo's owned assets, regardless of current source-tree state (a stronger, explicit "take my stuff out" — distinct from `prune`, which only removes what source no longer has). |
| `update` | yes | yes | Alias/shorthand for re-running `install` after a source change; same semantics, framed for the "I changed source, now sync it" workflow. |
| `prune` | yes | yes | Removes install targets that are (a) in this repo's managed set and (b) absent from this repo's current source tree. See the prune invariant in §3. Never removes an unmanaged or foreign target. |

A repo may mark any command **non-applicable** if its owned asset set doesn't need
it — e.g. session-harvester manages exactly one Claude skill file, so it may
implement only `install`/`uninstall`/`validate` and document `status`, `update`, and
`prune` as "not applicable: single-asset repo, re-run install to update, delete
manually to uninstall" rather than building unused machinery. Non-applicability must
be **stated in that repo's install docs**, not silently omitted — a missing command
with no note is a gap; a missing command with a one-line "not applicable because…"
is a conforming implementation of this contract.

## 3. Ownership rule (the prune invariant)

Each repo installs, uninstalls, and prunes only assets physically present in its own
source tree. The catalog/allowlist (§7) is the authoritative managed-set for that
repo — nothing is managed by convention or naming pattern alone.

**Prune invariant, stated precisely:** `prune` removes an install target **if and
only if** both hold:

1. the target's name is in this repo's managed set (catalog/allowlist), **and**
2. the corresponding source no longer exists in this repo's source tree.

`prune` never removes a target for any other reason. In particular:

- an installed asset owned by a *different* repo (even one following this same
  contract) is never in this repo's managed set, so it is never touched;
- a foreign/unknown installed asset (`codex-primary-runtime`) is never in any
  repo's managed set, so it is never touched — Harness's Codex installer belt-and-
  suspenders skips it by exact name in addition to it already failing the
  allowlist check;
- an asset that IS in the managed set but whose source still exists is never
  removed by `prune` — only `uninstall` removes those.

This is the invariant that prevents the cross-repo violation named in the S-17
board: after the generic personal/global assets move from Harness to Agents, the
Harness allowlist **must** drop those names, or Harness's own `--prune` would
delete Agents-installed assets it no longer sources.

Legacy cleanup is outside the normal managed set. If an operator wants to remove
pre-extraction names such as `dynamic-workflow-prompt`,
`gpt-pro-context-prompt`, `add-tasks`, `investigate`, `session-start`,
`task-checkpoint`, `task-done`, `task-start`, `branching-and-prs.md`, or
`adversarial-review.md`, do it through a separate explicit migration run after a
dry-run review and operator approval. Do not place those names in ordinary
install/prune/uninstall allowlists unless their source exists in the owning repo.

## 4. Scratch-home testing

`CODEX_HOME` and `CLAUDE_HOME` environment variables redirect all install targets
(read and write) away from the real `~/.codex` / `~/.claude`. Every mutation-capable
command (`install`, `uninstall`, `update`, `prune`) **must** be exercised against a
scratch home before any live run, using this invocation pattern:

```bash
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --dry-run --diff
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --prune --dry-run

CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh --dry-run --diff
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh --prune --dry-run
```

`--dry-run` reports what would change without writing; `--diff` shows the actual
content diff for changed files. A scratch-home run against a *fresh* directory
proves an install/prune from empty; a scratch-home run seeded with a prior install
(or a copy of the real home) proves idempotency and correct drift/prune detection
without any risk to the live environment.

## 5. Live-mutation approval gate

Running `install`, `uninstall`, `update`, or `prune` against the **real** `~/.codex`
or `~/.claude` (i.e. without `CODEX_HOME`/`CLAUDE_HOME` redirected to a scratch
path) is an explicit operator-approval gate. No repo's installer may perform a live
global mutation autonomously — an agent must stop and ask before running any
mutating command against the real home, every time, regardless of how many times
approval was granted for scratch-home or prior live runs in the same session.
`validate`, `status`, and `diff` are read-only and do not require this gate even
against the real home.

## 6. Hook/config safety

These are the **existing** guards implemented in the Harness scripts today. Any
repo's installer implementation must preserve this behavior exactly — it is what
makes install idempotent and non-destructive to a user's own configuration.

**Claude (`hooks.json` → `~/.claude/settings.json`):**

- Claude Code reads hooks from `settings.json`; the installer never overwrites that
  file wholesale — it only sets/replaces the `hooks` key via `jq`.
- The merge is skipped (with a "skipped… unmanaged hook entries present" message)
  unless the existing `hooks` block in `settings.json` is **empty** or **every leaf
  hook command already points at the managed `notifications.sh`** (matched by
  `*/hooks/notifications.sh*` substring, so both literal and `$HOME`-relative
  forms count as managed). Any other unmanaged hook command present blocks the
  merge entirely — the installer does not selectively merge around it.
  If `jq` is not on `PATH`, the merge is skipped outright.
- The hook source's `__CLAUDE_HOME__` placeholder is rendered to the real
  `$CLAUDE_HOME` value (`sed` substitution) before merging, so the resulting
  hook commands are absolute paths into the install target.

**Codex (`AGENTS.md` and `hooks.json`):**

- `AGENTS.md` is written only if the destination is **empty** or its **first
  line** is exactly the managed header `# Global Codex Instructions`. Any other
  first line means the destination is unmanaged and is skipped (with a "skipped
  unmanaged global file" message) — the file is never appended to or partially
  merged.
- `hooks.json` is written only if the destination **either** is byte-identical to
  the current source `hooks.json` (fast-path `diff -q` match) **or** contains
  exactly one `"command":` entry whose value matches one of the known forms of the
  managed Stop-gate command (`.../hooks/stop.sh`, `$HOME/.codex/hooks/stop.sh`, or
  the unrendered `__CODEX_HOME__/hooks/stop.sh` placeholder). Any other shape
  (extra hooks, a different single command, multiple commands that aren't the
  exact match) is treated as unmanaged and skipped.
- The `__CODEX_HOME__` placeholder in the source `hooks.json` is rendered to the
  real `$CODEX_HOME` value before comparison/write.

**Both platforms:** install targets (`~/.codex`, `~/.claude`) are **outputs only,
never hand-edited**. Any user who wants to change installed behavior edits the
owning repo's source and re-runs install; a direct edit under the install target
will be silently overwritten (for files inside a repo's owned set) or left alone
but inconsistent with source (for anything outside it) on the next install.

## 7. Manifest/catalog + doc-manifest

**Catalog** — each repo's catalog (in Agents, `catalog.json`; Harness and
session-harvester may use an equivalent structure) is the ownership source of
truth: it enumerates every asset that repo's installer is allowed to install,
update, or prune, with per-platform source path and install target. An installer's
managed-set check (the `is_repo_managed_skill`-style allowlist) must be derivable
from, or checked against, this catalog — not maintained as an independent list that
can drift from it. `scripts/validate_catalog.py` in Agents is the reference
implementation of "does the allowlist match the catalog," including tolerance for
an installer script that doesn't exist yet.

**Doc-manifest** (`.harness-doc-manifest`-style file dropped in the install home,
named per-repo, e.g. `.agents-doc-manifest`) — records which static repo docs
(`docs/*.md` files a skill's body statically references, e.g. `docs/glossary.md`)
were copied into the install tree because a currently-installed skill references
them. This mechanism is repo-neutral:

- on every install run, the current skill source is scanned for `docs/*.md`
  references (excluding run-local templated paths like `RUN_ID`/`YYYYMMDD`
  segments, and excluding references that don't resolve to a real repo file —
  those are illustrative examples, not travel candidates);
- every resolved reference is copied alongside the skill install, so a skill that
  points at a doc still finds it after install;
- on a normal (non-prune) run the manifest **accumulates** (union of past + current
  doc set) so a later prune has the full history to reconcile;
- on a `--prune` run, any manifest-recorded doc no longer in the current reference
  set is removed from the install tree, and the manifest is rewritten to exactly
  the current set;
- a doc the user placed under the install tree themselves is **never** recorded in
  the manifest (it was never copied by the installer), so it is never touched by
  prune — the manifest only ever tracks installer-copied docs.

## 8. Validation behavior

- **`SKILL.md` identity**: every skill directory's `name:` frontmatter field must
  equal its directory name (which must also equal its catalog id). Missing or
  empty `description:` is a hard failure. This is enforced by a stdlib-only,
  string-based frontmatter parser — no YAML dependency, matching the durable-
  frontmatter convention.
- **Catalog coverage**: every physically-present asset in a repo's owned locations
  (skills, commands, subagents, rules, hooks, global instructions) must have a
  catalog entry, and every catalog entry's source path must exist on disk — both
  directions are checked, so an asset can't be silently un-cataloged nor a catalog
  entry silently orphaned.
- **Cross-tree presence**: a same-id skill present on one platform (Codex) but not
  the other (Claude), or vice versa, is a **warning**, not a failure — twins are
  deliberately not forced to be identical or even mutually present. Content and
  frontmatter parity across platform twins (`model`/`effort`/`allowed-tools`/
  `argument-hint`) is deferred by design and never checked.
- **Boundary check**: a boundary/foreign id (any `harness-*` name,
  `harvest-sessions`, `codex-primary-runtime`, or another repo's owned id) must
  never appear as an installable entry in a repo's own catalog.

## 9. Idempotency & rollback

- Install is **copy-based and idempotent**: re-running `install`/`update` with an
  unchanged source is a no-op (reported as "unchanged"); with a changed source it
  updates only the changed files.
- Install **never deletes user data** it doesn't own — it only ever writes files
  under its own managed paths, and the hook/config guards in §6 mean it refuses to
  touch a destination it can't prove is already managed.
- `prune`/`uninstall` remove **only** targets in the repo's own managed set (§3);
  they never delete anything outside it, including another repo's assets or a
  foreign asset.
- **Rollback** is: re-run `install` from the current (or a prior, checked-out)
  source commit to restore a known-good install state, or restore the install
  target itself from VCS/backup if the target directory is independently tracked.
  There is no separate rollback mechanism beyond "source is the truth, re-sync
  from it" — this is why install must stay copy-based and idempotent rather than
  stateful.

## 10. Per-repo applicability

| Repo | Managed set | `validate` | `status`/`diff` | `install` | `uninstall` | `update` | `prune` |
|---|---|---|---|---|---|---|---|
| **agents** | everything in `agents/catalog.json` (generic personal/global skills, commands, subagents, rules, Codex `AGENTS.md`, Claude notification hook) | yes | yes | yes | yes | yes | yes |
| **harness** | `harness-*` skills (both platforms), Claude `execute` command, Claude `harness-task-bootstrap`/`task-verifier` subagents, the Codex Stop-gate hook (`hooks.json` + `hooks/stop.sh` + `hooks/notifications.sh`, kept together because `stop.sh` sources `notifications.sh` as a sibling) | yes (`uv run python scripts/validate_skills.py`) | partial: `--dry-run --diff` reports source-vs-installed drift | yes | unsupported/deferred; not exposed by current scripts | re-run install | yes (`--prune`) |
| **session-harvester** | `harvest-sessions` (Claude skill) only | yes | not applicable — single asset, `status` adds no value over checking one path | yes | yes | not applicable — re-run `install` | not applicable — single asset, delete manually or via `uninstall` |

session-harvester satisfies this contract with a minimal `install`/`uninstall` for
its one skill (plus any doc it statically references) and documents the three
non-applicable commands with the one-line reasons above, per the non-applicability
rule in §2 — it does not need to build `status`/`update`/`prune` machinery for a
single-asset managed set.

## References

- `catalog.json` (this repo) — the Agents catalog this contract's §7 refers to.
- `scripts/validate_catalog.py`, `scripts/validate_skills.py` (this repo) — the
  validation behavior in §8.
- `repos/harness/scripts/install-claude.sh`, `repos/harness/scripts/install-codex.sh`
  — the existing implementation this contract's §6/§7 behavior is captured from.
