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
  check_cross_repo_consistency.py # verifies Agents/Harness/session-harvester ownership split
  validate_catalog.py # catalog <-> source consistency + installer-allowlist parity
  validate_skills.py  # SKILL.md frontmatter identity check (dir id == name, description present)
docs/
  destructive-command-guard.md # external cross-agent command guard decision and setup
  skill-authoring-principles.md   # craft rubric for writing/reviewing skills
  skill-installer-contract.md     # reusable per-repo installer contract (shared by all repos)
docs/harness/          # this repo's own Harness task/slice/decision tracking state (not narrative docs)
```

Codex/Claude same-name skills are deliberate **platform twins**, not automatically identical — the
per-platform variants are preserved, never flattened.

## Validation & install (local, safe)

```bash
# Validate catalog and skill identity (no mutation):
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 scripts/check_cross_repo_consistency.py
bash scripts/test-prune-safety.sh

# Consistency check of this repo's Harness state:
harness check

# Dry-run / diff an install against a scratch home (never touches real ~/.codex / ~/.claude):
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --dry-run --diff
CODEX_HOME="$PWD/.scratch-home/codex"  bash scripts/install-codex.sh  --dry-run --diff
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
