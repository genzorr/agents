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
| **agents** (this repo) | generic personal/global skills, commands, subagents, rules, Codex global instructions, Claude notification hook |
| `repos/harness` | `harness-*` skills, the `execute` command, `harness-task-bootstrap`/`task-verifier` subagents, the Codex stop-gate hook, and the Harness CLI/data-model those call |
| `repos/session-harvester` | the `harvest-sessions` Claude skill only |
| foreign (e.g. `codex-primary-runtime`) | visible-only; never installed or pruned by any repo here |

See [`docs/skill-installer-contract.md`](docs/skill-installer-contract.md) for the reusable
per-repo installer contract all three repos follow.

## Layout

```
catalog.json          # authoritative catalog of agents-owned assets (identity + install targets)
codex/
  AGENTS.md           # global Codex instructions (generic agent behavior)
  skills/<id>/SKILL.md
config/
  codex-permissions.toml # source-managed named Custom permission profile
claude/
  skills/<id>/SKILL.md
  commands/*.md       # generic slash commands (dual-review, plan)
  agents/*.md         # generic subagents (code-reviewer, planner)
  rules/*.md          # generic global rules
  hooks/              # generic Claude notification hook
  hooks.json          # Claude hook config (merged into settings.json on install)
scripts/
  install-claude.sh   # install/uninstall/prune claude/ -> $CLAUDE_HOME (default ~/.claude)
  install-codex.sh    # install/uninstall/prune codex/ -> $CODEX_HOME (default ~/.codex)
  install-codex-permissions.py # backup-preserving named Custom profile installer/rollback
  test-codex-permissions.sh    # scratch-home profile/config parser check
  check_cross_repo_consistency.py # verifies Agents/Harness/session-harvester ownership split
  validate_catalog.py # catalog <-> source consistency + installer-allowlist parity
  validate_skills.py  # SKILL.md frontmatter identity + traveling-doc references
docs/
  context-file-authoring.md       # craft rubric for CLAUDE.md / AGENTS.md / rules (always-on layer)
  destructive-command-guard.md # external cross-agent command guard decision and setup
  model-and-effort.md             # choosing model/effort for subagents, workflows, delegated jobs
  skill-authoring-principles.md   # craft rubric for writing/reviewing skills
  skill-installer-contract.md     # reusable per-repo installer contract (shared by all repos)
docs/harness/          # this repo's own Harness task/slice/decision tracking state (not narrative docs)
research/findings/     # source-bounded research reviews and project-specific implications
```

Codex/Claude same-name skills are deliberate **platform twins**, not automatically identical — the
per-platform variants are preserved, never flattened.

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

## Safety

- **Install targets (`~/.codex`, `~/.claude`) are outputs, never hand-edited.** Edit source here,
  then run the install script.
- Mutating commands run against scratch homes by default in verification. **Live global
  install/update/prune requires explicit operator approval.**
- Install is copy-based and idempotent; `--prune`/`--uninstall` only remove assets this repo owns.

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
