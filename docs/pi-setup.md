# Optional Linux Pi permission setup

This installer owns the `agentic-local` permission extension and its exact Pi settings entry. Account management is an independent [pi-accounts package](https://github.com/genzorr/pi-accounts); Agents no longer installs its CLI, modules or maintenance units. The catalog instruction/skill installer remains separate. Install Pi first; the permission extension requires Linux, `bwrap`, and `bash`, with no additional npm dependencies or `socat`.

## Preview, install and remove permissions

```bash
python3 scripts/install-pi.py --dry-run
python3 scripts/install-pi.py
python3 scripts/install-pi.py --uninstall --dry-run
python3 scripts/install-pi.py --uninstall
```

Use `--home /tmp/pi-permission-trial` for a scratch installation. `--agent-dir` selects the Pi agent directory, defaulting to `PI_CODING_AGENT_DIR` or `<home>/.pi/agent`; explicitly set it when your shell exports a different home. Paths support `~`, `~/...`, relative paths and local file URLs with percent-encoded spaces. Tilde means the process home, independently of `--home`. Remote URL hosts, encoded slashes, malformed escapes and backslashes in file URLs are rejected. The installer does not require Node to retire historical files or uninstall permissions.

The installer writes only the permission directory `~/.local/lib/pi-agentic-local/permissions/{index.ts,policy.mjs,profile.json,child-inheritance.mjs}`, one absolute directory string in Pi `settings.json` `extensions`, and its private `.agents-pi-setup.json` ownership record and temporary recovery journal. It preserves unrelated settings, including skills, packages, providers, model and effort. It never owns or reads `auth.json`, `accounts/pool.json`, sessions or standalone npm package files.

Existing unmanaged permission files, modified owned files, duplicate extension entries and symlink destinations are conflicts. Reinstallation updates unchanged owned permission outputs. Uninstall removes unchanged owned permissions and only the exact managed extension entry; it leaves unrelated settings and empty directories intact. Start a fresh idle Pi/T3 process to load an extension update. See [permission boundaries](pi-permissions.md) and [required child-extension qualification](pi-child-inheritance.md); this is tool enforcement rather than whole-process confinement or Codex's AI approval reviewer.

## Historical account outputs and explicit migration

Earlier Agents setup versions owned `~/.local/bin/pi-accounts`, three modules under `~/.local/lib/pi-accounts`, and `pi-accounts-refresh.service` / `.timer`. A normal permission install/update/uninstall preserves these historical outputs and their ownership records, including modified files. It does not silently interrupt a user testing accounts. `--retire-accounts` explicitly removes only unchanged historical outputs recorded in this installer's state; differing files, changed modes or symlinks cause a conflict before applying any planned change. Unrecorded files and standalone npm files are never adopted or removed.

The following migration requires explicit operator authorization. Finish human OAuth/switch operations and idle Pi/T3 first. Pause only the timer, then let any active oneshot refresh finish: stopping a refresh during provider token rotation can lose credentials. Do not run `systemctl stop pi-accounts-refresh.service`.

```bash
systemctl --user disable --now pi-accounts-refresh.timer
systemctl --user show pi-accounts-refresh.service --property=ActiveState --property=Result --property=ExecMainStatus
# Wait for ActiveState=inactive or failed and no running refresh before continuing.
python3 scripts/install-pi.py --retire-accounts --dry-run
python3 scripts/install-pi.py --retire-accounts
systemctl --user daemon-reload
npm install --global --prefix "$HOME/.local" https://github.com/genzorr/pi-accounts/releases/download/v0.1.1/pi-accounts-0.1.1.tgz
pi-accounts status
pi-accounts maintenance install --dry-run
pi-accounts maintenance install
pi-accounts maintenance enable
pi-accounts maintenance status
```

The retirement updates permissions in the same reviewed transaction and retains the existing Pi agent home, native credentials, pool and selected account. No re-login is required solely to change distribution. The standalone maintenance installer uses new dedicated service names and does not overwrite unowned legacy `pi-accounts-refresh` units. Review its package README for supported Pi versions and macOS maintenance; Linux permission enforcement is not a Mac sandbox.

Do not install the npm command over a still-owned Agents wrapper before retirement. If another tool has already replaced that wrapper, retirement reports a conflict and preserves it; resolve the exact historical ownership boundary explicitly rather than removing state or forcing overwrite. Once retirement succeeds, subsequent Agents permission updates/uninstalls ignore standalone CLI/module/unit paths.

## Recovery and rollback

The permission installer preflights all planned changes, serializes invocations for the same home with an advisory directory lock, and records original/intended bytes and modes in a private journal before writing. Ordinary write failure rolls back its transaction. After process interruption, the next non-dry run rolls back a pending journal before replanning; dry-run reports it without writing. Recovery refuses to overwrite destinations changed outside the transaction. Keep the journal for explicit conflict resolution. The lock does not coordinate Pi settings saves; close other settings writers during changes. This is process-interruption recovery, not a disk-corruption guarantee.

A source-version rollback uses the currently installed permission version to uninstall its unchanged owned outputs before installing a known-good version; older installers may reject newer file identities. After accounts have moved to the standalone package, do not run an older all-in-one Agents installer: it would try to recreate the retired external tool. Keep permissions and standalone accounts on their independent update/rollback paths. To remove standalone scheduling safely, use `pi-accounts maintenance disable`, wait for its runner to finish, then `pi-accounts maintenance uninstall` before `npm uninstall --global --prefix "$HOME/.local" pi-accounts`. Those commands preserve credentials and the pool.

This optional permission installer is Linux-only and its suite skips before importing Linux dependencies on other platforms. The separate [catalog distribution](pi-distribution.md) owns global instructions and skills and does not apply permission updates or account migration.
