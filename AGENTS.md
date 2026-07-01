# AGENTS.md

This repository owns **generic personal/global** Codex and Claude agent assets and the surface that
installs/uninstalls/validates them. It was extracted from `repos/harness` under Personal OS slice
S-17.

## Boundary

- This repo is the **source of truth** for generic personal/global skills, commands, subagents,
  rules, Codex global instructions, and the Claude notification hook. Edit those here; never edit
  the installed copies under `~/.claude` or `~/.codex` directly.
- **Source ownership follows physical presence.** This repo installs, uninstalls, and prunes **only
  the assets physically present here**. It never manages, prunes, or removes assets owned by
  `repos/harness`, `repos/session-harvester`, or any foreign/unknown installed skill.
- Harness-coupled `harness-*` assets stay source-owned by `repos/harness`. The `harvest-sessions`
  skill stays source-owned by `repos/session-harvester`. Foreign installed skills such as
  `codex-primary-runtime` are visible-only and never touched.
- Treat `/Users/example/dev/os` (Personal OS) as the source of truth for cross-project governance:
  the OS/Harness boundary policy, the agents extraction plan, and the project registry. Use this
  repo's `docs/harness/` for agents-local backlog and follow-up work; Personal OS Harness tracks the
  original extraction (S-17).

## Same-name skills are platform twins

A same-name Codex and Claude skill are **counterparts, not automatically identical assets**. The
per-platform variants are intentional and preserved. The catalog records both; validation warns on
cross-tree presence gaps but does not force content/frontmatter parity.

## Installer contract

All install/uninstall/validate behavior follows the reusable per-repo skill installer contract in
[`docs/skill-installer-contract.md`](docs/skill-installer-contract.md). `repos/harness` and
`repos/session-harvester` follow the same contract for their own physically-present assets.

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
python3 scripts/validate_catalog.py            # catalog <-> source + allowlist parity
python3 scripts/validate_skills.py             # SKILL.md frontmatter identity
bash scripts/test-prune-safety.sh              # scratch prune/uninstall ownership guard
harness check                                  # Harness state consistency
CLAUDE_HOME=... bash scripts/install-claude.sh --dry-run --diff   # scratch-home dry run
CODEX_HOME=...  bash scripts/install-codex.sh  --dry-run --diff
```
