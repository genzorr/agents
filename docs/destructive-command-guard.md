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

- <https://github.com/Dicklesworthstone/destructive_command_guard/releases/tag/v0.6.7>
- <https://github.com/Dicklesworthstone/destructive_command_guard/blob/v0.6.7/docs/codex-integration.md>
- <https://github.com/Dicklesworthstone/destructive_command_guard/blob/main/LICENSE>

## Installation contract

1. Back up `~/.codex/hooks.json` and `~/.claude/settings.json`.
2. Download the pinned release installer and adjacent SHA-256 file, then verify the checksum before
   execution. Do not pipe the moving `main` installer directly into a shell:

   ```bash
   version=v0.6.7
   scratch="$(mktemp -d "${TMPDIR:-/tmp}/dcg-install.XXXXXX")"
   curl -fsSL -o "$scratch/install.sh" \
     "https://github.com/Dicklesworthstone/destructive_command_guard/releases/download/$version/install.sh"
   curl -fsSL -o "$scratch/install.sh.sha256" \
     "https://github.com/Dicklesworthstone/destructive_command_guard/releases/download/$version/install.sh.sha256"
   (cd "$scratch" && shasum -a 256 -c install.sh.sha256)
   chmod +x "$scratch/install.sh"
   "$scratch/install.sh" --version "$version" --verify --no-gum
   ```

   The upstream installer configures its supported agent hooks while preserving unrelated hook
   entries. Review the resulting Codex and Claude settings and retain only those two integrations
   for this package; do not accept shell-startup, Copilot, or other agent additions.
3. Do not run `dcg init`, enable optional packs, or use `DCG_BYPASS=1`.

## Verification

- `dcg --version` reports the pinned version.
- Existing Codex and Claude hooks remain present alongside DCG.
- `dcg doctor` reports no blocking integration error.
- `dcg test --format json 'printf hello'` returns `"decision":"allow"`.
- `dcg test --format json 'git reset --hard HEAD~1'` returns `"decision":"deny"` with the
  `core.git:reset-hard` rule.
- Direct, non-executing Codex-shaped and Claude-shaped hook payloads allow a safe command and deny
  the same simulated destructive command. Include `turn_id` for the Codex-shaped probe and omit it
  for the Claude-compatible probe; never execute the command itself.
- Never validate by executing a real destructive command outside a disposable repository.

## Rollback

Use the pinned release's `dcg uninstall` for the Claude hook, restore the timestamped Codex/Claude
hook backups if the installer changed an unrelated entry, and verify that unrelated hooks remain.
Do not use `--purge` and do not delete whole Codex or Claude settings files.

## Current status

Installed and verified on 2026-07-16. `dcg --version` reports `0.6.7`; `dcg doctor` passes with the
two default packs; `dcg test` and both protocol-shaped payload probes allow a safe command and deny
`git reset --hard HEAD~1`. Existing Codex and Claude hooks were preserved, and no shell-startup,
Copilot, or optional-pack configuration is retained.
