# Pi setup

Install Pi first. This checkout manages instructions, skills and an optional Linux permission extension. [pi-accounts](https://github.com/genzorr/pi-accounts#readme) independently owns account login, selection, quota checks and hourly token maintenance. Its README owns installation, compatibility and `pi-accounts update`.

Close Pi/T3 processes that may save settings before changing an installation, review each preview, then start a fresh backend afterward. Use an isolated `PI_CODING_AGENT_DIR` to try asset commands without changing the real home. Permissions, native packages and accounts have separate owners; none of these asset commands migrates credentials.

## Instructions and skills

From this checkout:

```bash
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh --dry-run --diff
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh
```

For an update, preview and apply `--update`. Add `--prune` only when removing unchanged stale owned outputs is intended. For removal, preview `--uninstall --dry-run`, then apply `--uninstall`. Modified or foreign files remain conflicts; keep the ownership record rather than forcing deletion. The [installer contract](skill-installer-contract.md) owns recovery details.

[catalog.json](../catalog.json) is the membership and source authority. The installer copies complete skills and their references, global `AGENTS.md` and guidance documents; it preserves the normal system prompt. Pi also discovers the separately managed shared Agents home: update it with `scripts/install-agents.sh`, reviewing that separate preview because other runtimes discover it too. Harness workflows use the [Harness owner's installer](https://github.com/genzorr/harness/tree/main/pi), never the Agents installer.

A fresh Pi process should list the installed skills. `/skill:name` explicitly invokes one; model-facing metadata does not override a skill's trigger or authority. Each skill owns its prerequisites and conditional external capabilities. Project `AGENTS.md` needs no conversion; project skill discovery depends on Pi's project trust setting. For old Codex links or historical account files, use [legacy migration and recovery](pi-distribution.md).

The explicit-only `orchestrate-feature` helper uses exposed T3 tools to create or reuse a separate ordinary owner conversation; that owner uses `orchestrate-workers` for native leaves and handles routine iterations locally. Blockers, decisions and final handoffs return through per-call-approved `t3_thread_send` to the fixed main conversation. Denied/unavailable approval leaves manual open/read recovery, not an automatic notification. Ordinary creation and messaging retry keys are caller-session scoped, not restart-global.

The worker route uses pi-subagents 0.79.0 and the source permission update: fresh launches, exact owned lifecycle receipts, completion notifications and blocking waits when needed. Independent review requires an operator request. Native source-consumer/adapter tests qualify these interfaces separately; installed authenticated T3 exposure, an ordinary Pi owner running its leaves, and human UI/model behavior remain unqualified. See the [permission and delivery boundary](pi-permissions.md#children-and-inherited-context). Source qualification does not install either helper.

After review, preview and reconcile assets with the commands above and permissions with their separate installer below, then restart an idle Pi/T3 backend. Before rollback/removal, finish owned runs; use the owning installers and preserve modified/foreign files and ownership records. Older permission source may again block unattended lifecycle operations. The helper preserves the coordinator's profile and external-write authority and creates no watcher.

## Linux permissions

Requires `/bin/bash`, `/usr/bin/bwrap` and working unprivileged namespaces. This extension does not support macOS or Windows. Default installation uses Pi’s normal extension loading. This is the selected best-effort scope: missing or failed startup/reload can leave built-in tools available. Strong mandatory host enforcement is not provided.

```bash
python3 scripts/install-pi.py --dry-run
python3 scripts/install-pi.py
```

Use the same commands to update unchanged owned files. To remove, preview `--uninstall --dry-run`, then apply `--uninstall`. `--home /tmp/pi-permission-trial` selects a scratch task home; explicitly pass `--agent-dir` if the shell already exports another `PI_CODING_AGENT_DIR`. Tilde expansion always uses the process home. Both installers accept relative paths, `~/...` and local file URLs; remote hosts and unsafe URL spellings are rejected.

The permission installer owns only `~/.local/lib/pi-agentic-local/permissions`, its exact settings extension entry, and `.agents-pi-setup.json` plus a temporary recovery journal. It preserves unrelated settings and never reads auth, account pools or sessions. Modified files, symlinks and duplicate entries are conflicts. It recovers interrupted transactions before replanning and refuses externally changed recovery destinations; retain the journal for resolution. For source rollback, uninstall with the current version before installing a known-good permission version. Older all-in-one installers must not recreate retired account tooling.

After restart, run `/agentic-local` to inspect current writable roots and test bash availability. This status is not a persistent host activation guarantee. Read the [permission contract](pi-permissions.md) before relying on enforcement or approving exceptions.

## Optional automatic updates for unprofiled hosts

Automatic runtime self-update has not been qualified with `agentic-local`; this source setup does not certify an enabled live updater. The native option below applies to unprofiled hosts, including macOS.

[pi-auto-update](https://github.com/eiei114/pi-auto-update) runs `pi update --extensions`, then `pi update` at startup. It does not update Agents/Harness assets or pi-accounts.

Before installing it, merge this child policy into existing Pi settings, using actual absolute paths and retaining every existing child extension capability except the updater:

```json
{
  "subagents": {
    "defaultExtensions": [
      "/absolute/agent-home/npm/node_modules/pi-subagents/index.js"
    ]
  }
}
```

Preserve any other required child extensions in this list; adding a permission entry does not qualify mandatory enforcement. `defaultExtensions` disables ambient child extensions; `defaultSubagentOnlyExtensions` does not. Explicit agent `extensions` overrides the default. Built-in MCP selection is separate. Include future child capabilities explicitly instead of silently dropping them.

```bash
pi install 'npm:pi-subagents@0.78.0 || 0.79.0'
pi install npm:pi-auto-update@0.1.6
```

For an existing subagents installation, replace only its old source entry with that bounded range, preserving other packages. An exact version pin is skipped by native updates. Pi self-update follows upstream latest; a future release may require compatibility requalification. Native npm Pi preserves its installation prefix; no managed-layout migration is needed.

Restart Pi to load the updater. `/auto-update-now` runs explicitly. `PI_AUTO_UPDATE=0` or `PI_OFFLINE=1` skips automatic startup only; the manual command bypasses those flags. Concurrent requests deduplicate within one extension instance, not across processes or children. Reload/new/resume/fork skip automatic runs. The child allowlist prevents ordinary child startups from loading the updater.

To remove, prevent new starts, let active updates finish, then run `pi remove npm:pi-auto-update@0.1.6`. Restore only the package/allowlist entries deliberately changed. Removal does not undo completed updates; restore known-good versions through their owning package managers when needed.
