# Destructive Command Guard

DCG is an external, user-installed defense-in-depth hook for accidental destructive shell and Git
commands across Codex, Claude Code, and other supported agents. This repository records the setup;
it does not vendor the binary or manage it through the agents asset installers.

## Decision

- Adopt pinned release `v0.6.7` with only its default core filesystem, Git, and disk packs.
- Do not run `dcg init`, enable optional infrastructure/cloud/database packs, or add shell-startup
  modifications without separate review.
- Keep Codex Custom Auto-review and Claude permissions as the actual permission layers. DCG does not
  replace them.

DCG assumes a well-intentioned but fallible agent and fails open on some parse errors, timeouts, direct
interpreter operations, scripts, and Codex execution paths not intercepted by `PreToolUse`. Treat it as
mistake reduction, not containment. Its custom MIT-derived license includes an OpenAI/Anthropic rider;
do not copy or redistribute the binary from this repository.

Sources:

- <https://github.com/Dicklesworthstone/destructive_command_guard>
- <https://github.com/Dicklesworthstone/destructive_command_guard/blob/main/docs/codex-integration.md>
- <https://github.com/Dicklesworthstone/destructive_command_guard/blob/main/LICENSE>

## Installation contract

1. Back up `~/.codex/hooks.json` and `~/.claude/settings.json`.
2. Download the pinned release installer and adjacent SHA-256 file, then verify the checksum before
   execution. Do not pipe the moving `main` installer directly into a shell.
3. Run the verified local installer with `--version v0.6.7 --easy-mode`.
4. Do not run `dcg init`.

## Verification

- `dcg --version` reports the pinned version.
- Existing Codex and Claude hooks remain present alongside DCG.
- `dcg doctor` reports no blocking integration error.
- Direct, non-executing Codex-shaped and Claude-shaped hook payloads allow a safe command and deny
  `git reset --hard HEAD~1`.
- Never validate by executing a real destructive command outside a disposable repository.

## Rollback

Use DCG's uninstaller or restore the timestamped hook backups, then verify that unrelated hooks remain.
Do not delete whole Codex or Claude settings files.

## Current status

Installed and verified on 2026-07-16. `dcg --version` reports `0.6.7`; `dcg doctor` passes with the
two default packs; Codex-shaped and Claude-shaped payload probes allow a safe command and deny
`git reset --hard HEAD~1`. Existing Codex and Claude hooks were preserved. Easy mode also added a
shell-startup check and Copilot hook; both out-of-scope additions were removed, leaving only the
approved Codex and Claude integrations.
