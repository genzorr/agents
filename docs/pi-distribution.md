# Legacy Pi migration and recovery

Ordinary installation and updates belong in [Pi setup](pi-setup.md). Use this reference only for provisional Codex links, historical Agents-owned account outputs or recovery of those migrations. Close Pi/T3 and other settings writers first; preview each operation and apply only within operator-authorized scope.

## Provisional Codex references

The Linux migration handles only `AGENTS.md` and `docs` symlinks pointing lexically to the explicitly supplied Codex home, plus one exact absolute Codex skills entry in Pi settings. It never reads those Codex destinations. Foreign files/links, malformed settings, duplicate entries or an existing Agents asset ledger are conflicts.

```bash
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex" --dry-run
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex"
```

Install current assets through their owning repositories afterward. Migration records original link text and the removed entry's position in `.agents-pi-migration.json` before effects. Repeated completion is a no-op. An interrupted prepared transaction requires explicit rollback before retrying; preserve its record.

## Narrow migration rollback

A composed installation has two asset owners. Harness leaves its own documents in `docs/`, so remove its unchanged outputs first, then Agents outputs, before restoring the old docs symlink. Substitute the actual Harness checkout for `HARNESS_REPO`:

```bash
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash "$HARNESS_REPO/scripts/install-pi.sh" --uninstall --dry-run
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash "$HARNESS_REPO/scripts/install-pi.sh" --uninstall
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh --uninstall --dry-run
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh --uninstall
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex" --rollback --dry-run
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex" --rollback
```

Stop at an unresolved owner conflict; never delete foreign/modified files or rewrite ownership records to clear the directory. If Harness was never installed, omit its two commands. Rollback restores only recorded links into absent or already-matching destinations and reinserts only the recorded skills entry, preserving unrelated settings. A foreign document still occupying `docs/` blocks restoration even after both uninstallers run. Changed/invalid `settings.skills` also blocks it. Partial restoration is retryable; successful rollback removes the migration record.

Installers, migration and rollback run sequentially, without coordination with external settings writers. Generic asset failure before ledger commit may leave exact outputs: rerun to adopt unchanged matches before uninstalling. Permission setup has its own journal and recovery in [Pi setup](pi-setup.md#linux-permissions). These are process-interruption bounds, not disk-corruption guarantees.

## Historical account outputs

Earlier Agents setup owned `~/.local/bin/pi-accounts`, three `~/.local/lib/pi-accounts` modules and `pi-accounts-refresh.service`/`.timer`. Normal permission updates/uninstalls retain them. Explicit retirement removes only unchanged recorded outputs; foreign, modified or symlink replacements conflict. It preserves auth, pool, selection, sessions and unrelated settings.

Finish OAuth/switch activity. Pause the timer and let any running refresh finish; never stop the refresh service during token rotation:

```bash
systemctl --user disable --now pi-accounts-refresh.timer
systemctl --user show pi-accounts-refresh.service --property=ActiveState --property=Result --property=ExecMainStatus
# Continue only when no refresh is running.
python3 scripts/install-pi.py --retire-accounts --dry-run
python3 scripts/install-pi.py --retire-accounts
systemctl --user daemon-reload
```

Retirement also reconciles permissions in the reviewed transaction. Then install the standalone [pi-accounts package](https://github.com/genzorr/pi-accounts#readme) and its maintenance service using that owner's instructions. Do not overwrite a still-owned legacy wrapper with npm or run an older all-in-one Agents installer afterward. No re-login is required solely to change distribution. The standalone package owns its update, safe maintenance disable/uninstall and rollback procedures.
