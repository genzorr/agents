# AGENTS.md

This repository owns generic Codex and Claude agent assets and their install, uninstall, and validation tools.

## Boundary

- This repo is the **source of truth** for generic personal/global skills, commands, subagents, rules, Codex and Claude global instructions, and the Claude notification hook (POSIX and Windows notifiers, one settings adapter). Never hand-edit installer-owned copies under `~/.claude` or `~/.codex`. The Claude auto-mode example is not installer-owned; follow `docs/claude-auto-mode.md` for operator-approved manual configuration.
- **Source ownership follows physical presence.** This repo installs, uninstalls, and prunes **only
  the assets physically present here**. It never manages, prunes, or removes assets owned by
  `repos/harness`, `repos/session-harvester`, or any foreign/unknown installed skill.
- Harness-coupled `harness-*` assets stay source-owned by `repos/harness`. The `harvest-sessions`
  skill stays source-owned by `repos/session-harvester`. Foreign installed skills such as
  `codex-primary-runtime` are visible-only and never touched.
- Maintainers may keep local work tracking in the ignored `docs/harness/` directory. It is not part of the public distribution; use it when present, and do not require it for installation or contribution.
- Use this existing checkout by default. Create a worktree only when the operator explicitly requests one.

## Same-name skills are platform twins

A same-name Codex and Claude skill are **counterparts, not automatically identical assets**. The
per-platform variants are intentional and preserved. The catalog records both; validation warns on
cross-tree presence gaps but does not force content/frontmatter parity.

## Installer contract

All install/uninstall/validate behavior follows the reusable per-repo skill installer contract in
[`docs/skill-installer-contract.md`](docs/skill-installer-contract.md). `repos/harness` and
`repos/session-harvester` follow the same contract for their own physically-present assets.
For Agents, `catalog.json` is the sole desired-state authority and each selected home records historical materialized files plus adapter reconciliation history in `.agents-install-state.json`; the shell scripts are compatibility wrappers around the shared stdlib engine.

## Stop / Ask gates

Ask the operator before:

- live mutation of the real `~/.codex` or `~/.claude` (install/update/prune outside scratch homes);
- GitHub repo creation or any remote push;
- deleting branches;
- reading app-private settings/auth/cache files, raw session logs, or private transcripts;
- moving Harness-coupled `harness-*` source into or out of this repo;
- changing the per-repo installer ownership rule (each repo manages only its own physical assets).

## Commands

```bash
python3 scripts/validate_catalog.py            # catalog schema, source/target coverage, and travel references
python3 scripts/validate_skills.py             # frontmatter, portability, and catalog-backed text checks
python3 scripts/check_cross_repo_consistency.py # cross-repo ownership split
python3 -m unittest discover -s tests          # instruction behavior contracts
bash scripts/test-prune-safety.sh              # scratch prune/uninstall ownership guard
harness check                                  # optional: local Harness state, when present
CLAUDE_HOME=... bash scripts/install-claude.sh --dry-run --diff   # scratch-home dry run
CODEX_HOME=...  bash scripts/install-codex.sh  --dry-run --diff
```

`uv` is available for consistent tooling (`uv run python ...`), but the validation scripts remain
stdlib-only and may also be run with system `python3`.

## Branching and publishing

- Default branch: `main`.
- Use short feature branches for non-trivial changes.
- GitHub changes and pushes are external-effect actions and require explicit operator approval.
