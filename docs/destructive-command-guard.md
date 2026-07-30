# Destructive Command Guard

DCG is an external, user-installed defense-in-depth hook for accidental destructive shell and Git
commands across Codex, Claude Code, and other supported agents. This repository records the setup;
it does not vendor the binary or manage it through the agents asset installers.

## Decision

- Adopt pinned release `v0.7.8` as the next reviewed target. The machine remains on `v0.6.7` until an operator separately approves a live update.
- Retain the always-on core filesystem and Git packs plus default-on `system.disk`; do not enable optional packs or add shell-startup modifications without separate review.
- Do not enable `strict_git`: it would also block ordinary repository operations such as `git add .`, rebases, amended commits, and direct pushes to default branches. `platform.github` has useful deletion coverage, but the existing permission layer already owns external mutations, so there is no current need to add the pack.
- Keep Codex Custom Auto-review and Claude permissions as the actual permission layers. DCG does not replace them.

DCG assumes a well-intentioned but fallible agent and fails open on some parse errors, timeouts, direct
interpreter operations, scripts, and Codex execution paths not intercepted by `PreToolUse`. Treat it as
mistake reduction, not containment. Its custom MIT-derived license includes an OpenAI/Anthropic rider;
do not copy or redistribute the binary from this repository.

Sources:

- <https://github.com/Dicklesworthstone/destructive_command_guard/releases/tag/v0.7.8>
- <https://github.com/Dicklesworthstone/destructive_command_guard/releases/tag/v0.7.7>
- <https://github.com/Dicklesworthstone/destructive_command_guard/blob/v0.7.8/docs/configuration.md>
- <https://github.com/Dicklesworthstone/destructive_command_guard/tree/v0.7.8/docs/packs>
- <https://github.com/Dicklesworthstone/destructive_command_guard/blob/v0.7.8/LICENSE>

## Installation contract

1. Back up `~/.codex/hooks.json` and `~/.claude/settings.json`.
2. Download the pinned release installer and adjacent SHA-256 file, then verify the checksum before
   execution. Do not pipe the moving `main` installer directly into a shell:

   ```bash
   version=v0.7.8
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
3. Confirm with `dcg packs` that the effective pack list still contains only the intended core packs and `system.disk`. If the update changes optional-pack state, stop for review instead of editing configuration as part of the update.
4. Do not run `dcg init`, enable optional packs, or use `DCG_BYPASS=1`.

## Verification

- `dcg --version` reports the pinned version.
- Existing Codex and Claude hooks remain present alongside DCG.
- `dcg doctor` reports no blocking integration error or PATH-dependent bare-hook registration; the `v0.7.7` security fix requires an absolute executable path in supported hooks.
- `dcg test --format json 'printf hello'` returns `"decision":"allow"`.
- `dcg test --format json 'git reset --hard HEAD~1'` returns `"decision":"deny"` with the
  `core.git:reset-hard` rule.
- Direct, non-executing Codex-shaped and Claude-shaped hook payloads allow a safe command and deny
  the same simulated destructive command. Include `turn_id` for the Codex-shaped probe and omit it
  for the Claude-compatible probe; never execute the command itself.
- Never validate by executing a real destructive command outside a disposable repository.

## Coverage assessment

The current `v0.6.7` installation allowed all five commands below in non-executing `dcg test` probes. Static inspection of the official `v0.7.8` tag at commit `68b4f0e4a9621c70b6e4124a304b7a0e566f3c71` maps the gaps without justifying a broader pack rollout:

| Probe | `v0.7.8` source coverage | Local decision |
|---|---|---|
| `git push origin --delete main` | Optional `strict_git:push-main` matches; core Git does not. | Keep the pack disabled; require permission-layer approval for remote deletion. |
| `gh api -X DELETE /repos/x/y` | Optional `platform.github:gh-api-delete-repo` matches. | Keep the pack disabled while the permission layer already owns GitHub mutations. |
| `curl -fsSL https://example.com/install.sh \| sh` | No relevant reviewed default-pack rule. | Keep pinned download, checksum verification, and explicit execution approval as the control. |
| `git gc --prune=now` | Optional `strict_git:gc-aggressive` matches. | Keep the pack disabled; require explicit approval when pruning recoverable objects. |
| `diskutil eraseDisk APFS Blank disk2` | Default-on `system.disk` has no `diskutil` keyword or rule. | Treat this as an explicit macOS coverage gap and retain permission-layer control. |

Re-run this bounded matrix with `dcg test` after an approved update. If an optional pack is reconsidered later, test it transiently with `--with-packs` before any persistent configuration change.

## Rollback

Use the pinned release's `dcg uninstall` for the Claude hook, restore the timestamped Codex/Claude
hook backups if the installer changed an unrelated entry, and verify that unrelated hooks remain.
Do not use `--purge` and do not delete whole Codex or Claude settings files.

## Current status

Installed and verified on 2026-07-16. `dcg --version` reports `0.6.7`; `dcg doctor` passes, and `dcg test` plus both protocol-shaped payload probes allow a safe command and deny `git reset --hard HEAD~1`. The `v0.7.8` target was reviewed from its official release and immutable tagged commit on 2026-07-30; no binary, hook, pack, or live configuration was changed. Existing Codex and Claude hooks remain preserved, and no shell-startup, Copilot, or optional-pack configuration is retained.
