# Pi automatic updates

Use the existing [pi-auto-update](https://github.com/eiei114/pi-auto-update) extension and Pi's native updater. It runs `pi update --extensions`, then `pi update`, for a parent startup event. It does not update Agents/Harness assets or the separate account package; use their owning installers and `pi-accounts update`.

## Setup

Finish active Pi/T3 work first. Install the reviewed permission integration through [its owning setup](pi-setup.md), where applicable. Before enabling the updater, set the documented `subagents.defaultExtensions` allowlist in Pi's existing settings. Include every existing child extension capability except the updater; for the Linux profile these are the absolute installed paths to `pi-subagents/index.js` and `permissions/index.ts`:

```json
{
  "subagents": {
    "defaultExtensions": [
      "/absolute/agent-home/npm/node_modules/pi-subagents/index.js",
      "/absolute/permission-directory/index.ts"
    ]
  }
}
```

Merge this setting while preserving unrelated fields and any additional existing child capabilities. On macOS omit the Linux-only permission entry; use the actual selected agent home. `defaultSubagentOnlyExtensions` preserves ambient discovery and cannot exclude the updater. Explicit per-agent `extensions` overrides the default, so inspect those before using that route. Built-in MCP selection remains separate. New ambient child extensions need explicit inclusion in this allowlist.

For an already-installed qualified subagent package, replace only its exact old npm source in `settings.packages` with `npm:pi-subagents@0.78.0 || 0.79.0`; preserve every other entry. Native extension update can then advance it. For a new installation use the first command below; install the reviewed addon after the child allowlist is configured:

```bash
pi install 'npm:pi-subagents@0.78.0 || 0.79.0'
pi install npm:pi-auto-update@0.1.6
```

The union is a native npm range: extension update advances eligible 0.78.0 to qualified 0.79.0, while excluding future versions. The updater addon itself stays at its reviewed release. [Child compatibility](pi-child-inheritance.md) and the account tool's reference own their compatibility bounds; missing or future APIs fail closed. Pi self-update follows upstream latest, so a later unqualified Pi release may require source requalification before auth/child operations work. Native npm Pi infers its actual installation prefix; no managed-layout migration or npm wrapper is required.

## Operation and rollback

Start a fresh idle Pi process to load the extension. `/auto-update-now` explicitly runs both checks. Automatic startup skips when `PI_AUTO_UPDATE=0` or `PI_OFFLINE=1`; the manual command bypasses those skips. The addon deduplicates concurrent requests within one extension instance, not across all parent sessions/processes. Reload/new/resume/fork events skip automatic updates, but another startup instance can run them again. Child ambient exclusion prevents that path in ordinary configured children; it is not a general update lock or a restriction on explicit operator overrides.

For removal, prevent new starts, let an active updater finish, and use `pi remove npm:pi-auto-update@0.1.6`. Restore only the allowlist/package entries you deliberately changed, preserving foreign settings. Removal does not undo completed updates; use the owning native package manager to restore a known-good release if needed. No extra daemon, scheduler, proxy or account rotation is added. Hourly token renewal remains independently owned by pi-accounts.

Qualification uses actual published artifacts, native startup/child APIs and updater shims without inference. Actual macOS execution, human T3 dialogs and model behavior remain unverified. Do not describe shim checks as live updater execution.
