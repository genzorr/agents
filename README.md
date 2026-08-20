# agents — personal/global Codex & Claude agent assets

This repository is the source of truth and install/manage surface for **generic personal/global**
Codex and Claude agent assets: skills, slash commands, subagents, rules, global instructions, and
notification hooks that are not specific to any single project.

It is an ordinary independent Git repository living under the Personal OS ignored `repos/`
workspace (a sibling of `repos/harness` and `repos/session-harvester`), **not** a submodule.

## Ownership boundary (hybrid, per-repo source ownership)

Each repo owns and installs **only the assets physically present in that repo**. No repo manages,
prunes, or removes another repo's skills.

| Repo | Owns / installs |
|---|---|
| **agents** (this repo) | generic personal/global skills, commands, subagents, rules, Codex and Claude global instructions, Claude notification hook |
| `repos/harness` | `harness-*` skills, the `execute` command, `harness-task-bootstrap`/`task-verifier` subagents, the Codex stop-gate hook, and the Harness CLI/data-model those call |
| `repos/session-harvester` | the `harvest-sessions` Claude skill only |
| foreign (e.g. `codex-primary-runtime`) | visible-only; never installed or pruned by any repo here |

See [`docs/skill-installer-contract.md`](docs/skill-installer-contract.md) for the reusable
per-repo installer contract all three repos follow.

## Layout

```
catalog.json          # sole desired-state catalog (assets, source layers, targets, adapters, travel docs)
codex/
  AGENTS.md           # global Codex instructions (generic agent behavior)
  skills/<id>/SKILL.md
config/
  codex-permissions.toml # source-managed named Custom permission profile
  claude-auto-mode.json  # primary-macOS Claude auto-mode record (manual, not installed)
claude/
  CLAUDE.md             # global Claude instructions
  skills/<id>/SKILL.md
  commands/*.md       # generic slash commands (dual-review, plan)
  agents/*.md         # generic subagents (code-reviewer, planner)
  rules/*.md          # generic global rules
  hooks/              # generic Claude notifier: notifications.sh (POSIX) + notifications.ps1 (Windows)
  hooks.json          # Claude hook config (merged into settings.json on install; wires the host's notifier)
shared/
  skills/<id>/...     # mechanically byte-identical Codex/Claude source content
scripts/
  install-assets.py    # shared stdlib catalog/installer engine
  install-claude.sh   # compatibility wrapper for the Claude engine (POSIX)
  install-codex.sh    # compatibility wrapper for the Codex engine (POSIX)
  install-claude.ps1  # native-Windows entry point for the Claude engine
  install-codex.ps1   # native-Windows entry point for the Codex engine
  lib/python.sh       # interpreter resolution for the POSIX wrappers (probes by execution)
  lib/python.ps1      # interpreter resolution for the PowerShell wrappers (probes by execution)
  install-codex-permissions.py # backup-preserving named Custom profile installer/rollback
  test-codex-permissions.sh    # scratch-home profile/config parser check
  check_cross_repo_consistency.py # verifies Agents/Harness/session-harvester ownership split
  validate_catalog.py # catalog/source/target/travel/state-contract validation
  validate_skills.py  # frontmatter, portability, and catalog-backed text validation
docs/
  claude-auto-mode.md          # recorded Claude auto-mode config: decision, manual apply contract, drift check
  context-file-authoring.md       # craft rubric for CLAUDE.md / AGENTS.md / rules (always-on layer)
  destructive-command-guard.md # external cross-agent command guard decision and setup
  model-and-effort.md             # choosing model/effort for subagents, workflows, delegated jobs
  orchestrate-feature-prd.md      # operator entrypoint guide and feature-orchestration product contract
  orchestrate-feature-spec.md     # technical contract and verification requirements for orchestration skills
  skill-authoring-principles.md   # craft rubric for writing/reviewing skills
  skill-lifecycle-policy.md       # generic lifecycle thresholds and audit method for skill-lifecycle
  skill-installer-contract.md     # reusable per-repo installer contract (shared by all repos)
docs/harness/          # this repo's own Harness task/slice/decision tracking state (not narrative docs)
research/findings/     # source-bounded research reviews and project-specific implications
```

Codex/Claude same-name skills are deliberate **platform twins**, not automatically identical — the
per-platform variants are preserved, never flattened. PR B places only mechanically byte-identical
source files under `shared/skills` while keeping platform-only files as explicit catalog source layers.

## Desired state and historical state

`catalog.json` declares the desired asset identity, platform, source file or complete directory, relative install target, adapter exception, and explicit traveling document. `scripts/install-assets.py` expands that catalog for one platform; the shell wrappers do not contain asset inventories. `.agents-install-state.json` in a selected home records files Agents materialized or safely adopted plus Claude adapter history, with explicit ownership, source digest, mode, and exact managed structural hook leaves. It is historical ownership evidence, not a desired-state catalog.

Normal install adopts exact existing outputs, updates unchanged recorded outputs, and preserves modified or unmanaged conflicts. `--dry-run` and `--diff` do not create directories, write files, change modes, merge settings, or migrate state. `--prune` removes only unchanged files recorded in historical state that are absent from the current catalog; `--uninstall` reconciles every recorded Agents file, including assets removed from the catalog. Modified destinations are reported and preserved.

Traveling documents are catalog assets. Validation scans managed skills, commands, subagents, rules, and global instructions and requires each real `docs/*.md` reference to be declared for that platform; examples and run-generated paths remain explicit exceptions. Add or remove an asset by editing its authored source and catalog entry, then validate and exercise an isolated scratch home; installer code should not change.

## Validation & install (local, safe)

```bash
# Validate catalog and skill identity (no mutation):
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 scripts/check_cross_repo_consistency.py
python3 -m unittest discover -s tests
bash scripts/test-prune-safety.sh

# Consistency check of this repo's Harness state:
harness check

# Dry-run / diff an install against a scratch home (never touches real ~/.codex / ~/.claude):
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --dry-run --diff
CODEX_HOME="$PWD/.scratch-home/codex"  bash scripts/install-codex.sh  --dry-run --diff

# Install the source-managed Codex Custom profile (backs up ~/.codex/config.toml first)
python3 scripts/install-codex-permissions.py --dry-run
python3 scripts/install-codex-permissions.py
bash scripts/test-codex-permissions.sh
```

On a **native Windows** host use the PowerShell entry points instead — the `bash` on PATH is WSL and
reaches neither the Windows home nor `powershell.exe`. Homes are selected with `$env:CLAUDE_HOME` /
`$env:CODEX_HOME` and default to `%USERPROFILE%\.claude` / `%USERPROFILE%\.codex`:

```powershell
$env:CLAUDE_HOME = "$PWD\.scratch-home\claude"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-claude.ps1 --dry-run --diff
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-claude.ps1
$env:CODEX_HOME = "$PWD\.scratch-home\codex"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1 --dry-run --diff
```

## Safety

- **Installer-owned targets under `~/.codex` and `~/.claude` are outputs, never hand-edited.** Edit their source here, then run the owning install script. The record-only Claude auto-mode config is an explicit operator-managed exception; follow `docs/claude-auto-mode.md` and preserve unrelated settings.
- Mutating commands run against scratch homes by default in verification. **Live global
  install/update/prune requires explicit operator approval.**
- Install is copy-based and idempotent; `--prune`/`--uninstall` only remove assets this repo owns.
- `.agents-install-state.json` is written atomically only after a mutating reconciliation succeeds; keep it with the home when diagnosing or retrying conflicts.
- Roll back by checking out a known-good source commit and re-running the installer against the selected scratch or approved live home; no live home is touched during repository verification.

## Tooling

This repo has a minimal `uv` project for consistent local tooling:

```bash
uv run python scripts/validate_catalog.py
uv run python scripts/validate_skills.py
uv run python scripts/check_cross_repo_consistency.py
```

The scripts are still stdlib-only and also run with system `python3`.

## Branching and publishing

- Default branch: `main`.
- Use short feature branches for non-trivial changes; keep commits reviewable.
- GitHub remote: private `git@github.com:genzorr/agents.git`.
- Do not push, delete branches, create GitHub repos, or mutate live global installs without explicit
  operator approval.
