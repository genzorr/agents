# AGENTS.md

This repository owns generic shared Agents, Codex, Claude, and Devin assets and their install, uninstall, and validation tools.

## Boundary

- This repo is the **source of truth** for generic personal/global skills, commands, subagents, rules, provider global instructions, the Devin default-config fragment, and the Claude notification hook (POSIX and Windows notifiers, one settings adapter). Never hand-edit installer-owned copies under `~/.agents`, `~/.claude`, `~/.codex`, or `~/.config/devin`. The Claude auto-mode example is not installer-owned; follow `docs/claude-auto-mode.md` for operator-approved manual configuration.
- Manage only assets physically present in this repository and declared in its catalog. Never install, prune, or remove another repository's assets or foreign installed files. Reserved external asset identities are enforced by `scripts/agent_catalog.py`.
- Maintainers may keep local work tracking in the ignored `docs/harness/` directory. It is not part of the public distribution; use it when present, and do not require it for installation or contribution.
- Use this existing checkout by default. Create a worktree only when the operator explicitly requests one.

## Shared skills and platform twins

A skill installed under `~/.agents/skills` is a complete provider-neutral asset, not a base overlaid by a same-name provider skill. Never install a shared skill and a same-name runtime-specific skill for one runtime: discovery is not a merge operation. Same-name provider skills and global instructions remain **counterparts, not automatically identical assets**; preserve differences in tool names, frontmatter, invocation, permissions, model behavior, and runtime-specific support files.

Repository `AGENTS.md` is the common project instruction baseline. A project `CLAUDE.md` may be an import-only compatibility wrapper or carry a real Claude-specific delta; in either case import `@AGENTS.md` before any delta. This repository uses a regular import-only wrapper so Windows checkouts do not depend on Git symlink support. Working symlinks remain appropriate where the supported environment preserves them. Provider global instructions remain separate installed artifacts.

For diagnosis and investigation closure, follow README's [Diagnosis and recovery](README.md#diagnosis-and-recovery); it links the authoritative installer contract and existing work-record route. For new-project instructions, use [Context File Authoring](docs/context-file-authoring.md). For returned research, use `integrate-research` when available; otherwise compare the answer with the original question and current evidence, separate proposals from decisions, and update only authorized owners.

## Installer contract

Follow the [installer contract](docs/skill-installer-contract.md). `catalog.json` defines desired assets; `.agents-install-state.json` records ownership in each selected home. The shell scripts wrap the shared standard-library engine.

## Stop / Ask gates

Ask the operator before:

- live mutation of the real `~/.agents`, `~/.codex`, `~/.claude`, or `~/.config/devin` (install/update/prune outside scratch homes);
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
AGENTS_HOME=... bash scripts/install-agents.sh --dry-run --diff
DEVIN_HOME=...  bash scripts/install-devin.sh  --dry-run --diff
```

`uv` is available for consistent tooling (`uv run python ...`), but the validation scripts remain
stdlib-only and may also be run with system `python3`.

## Branching and publishing

- Default branch: `main`.
- Use short feature branches for non-trivial changes.
- GitHub changes and pushes are external-effect actions and require explicit operator approval.
