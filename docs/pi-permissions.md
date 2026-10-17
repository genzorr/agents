# Pi agentic-local permissions

`pi/permissions` is a Linux Pi extension that restricts ordinary bash filesystem writes and gates file writes outside the configured roots. It uses Pi 1.3.0's built-in bash/write/edit implementations and `/usr/bin/bwrap`; there is no npm permission package, AI approval service, proxy, or inference hook. Network access and local binding remain enabled. File reads retain the host user's access.

The installer copies `pi/permissions/{index.ts,policy.mjs,profile.json,child-inheritance.mjs}` to `~/.local/lib/pi-agentic-local/permissions/` and adds that absolute directory as one `settings.json` `extensions` entry in the selected Pi agent home (normally `~/.pi/agent`). It preserves unrelated settings, extensions, providers and MCP configuration. Restart an idle Pi/T3 backend after installation or removal so it discovers the new extension. Do not also copy it into Pi's auto-discovered `extensions` directory: loading two permission extensions creates conflicting tool replacements. Existing tool-replacing extensions need operator review; this feature does not unload them.

## Allowed operations and manual exceptions

`profile.json` mirrors the explicitly writable paths in the operator's existing Codex `permissions.agentic-local` profile: `~/dev`, `/tmp`, the process's temporary directory, `~/.cache/uv`, the listed Claude runtime/cache directories, and `~/.local/state/claude-headless/jobs`. Only existing directories are enabled at Pi startup. Missing roots are skipped; create an intended directory manually and restart Pi to enable it. The extension resolves configured roots once at startup and does not automatically add the current working directory or Git worktree metadata outside those roots. The startup `TMPDIR` is trusted operator configuration; tool-supplied environment changes cannot add roots.

Ordinary `bash` and user `!`/`!!` commands run under a read-only host filesystem mount with writable mounts for the configured roots. A separate process/user/PID namespace, capability drop, private `/dev`, and private `/proc` reduce filesystem escapes. The network namespace is shared, allowing normal network access and loopback binding without a proxy or `socat`. Bash command text remains shell-quoted, and the host launcher clears `BASH_ENV` and `ENV`. Missing bubblewrap or denied namespace creation fails the command; it never silently runs unsandboxed.

The `write` and `edit` tools normalize paths like Pi, resolve symlinks including missing targets, and ask before an outside-scope write. Traversal and directory-name-prefix lookalikes do not grant writes. An approval applies to one invocation. Reads, listing, finding and grep do not require approval.

To run an outside-scope command, the model must explicitly call `bash_unrestricted`. The confirmation displays the working directory and complete command and explains that the command receives the Pi process's host-user permissions. Every call requires fresh approval; a denied sandbox command never authorizes a retry. Extension/MCP tools exposed through Pi's `tool_call` event also require confirmation of their tool name and arguments for each invocation. Approval grants the invocation's full privileges, not filesystem confinement for the tool's internals.

Confirmations use Pi's `ctx.ui.confirm`, which maps to RPC `extension_ui_request` with `method: "confirm"`; the client answers `extension_ui_response` with the same `id` and `confirmed: true` or `false`. Cancellation, an absent UI, an aborted tool invocation, or a 60-second timeout denies the exception. A client that does not implement RPC dialogs cannot approve outside-scope actions. The synthetic integration test exercises actual Pi RPC denial followed by approval without invoking a model. T3's own dialog rendering still needs a live UI check.

## Enforcement boundary

This is a bash filesystem sandbox plus direct file-tool approval gates, not whole-process confinement or identical Codex enforcement. The Pi process, extension startup code, MCP servers, other tools' internal implementations and their subprocesses remain outside bubblewrap. Extension/MCP confirmation covers calls emitted through Pi's tool event; it cannot contain background work, extension code that invokes host APIs directly, or another extension that replaces these tools or `user_bash` operations. Other shell tools require the generic manual tool approval but do not gain this bash sandbox. Operator-loaded code and settings remain trusted.

For the qualified `pi-subagents` releases, this extension registers its canonical entrypoint through the public required-child-extensions API at each session start and disposes that registration at shutdown. Native foreground/background children retain the permission extension even when ambient extensions are disabled or the agent sets `extensions: []`; a conflicting capability ceiling rejects the launch. Unsupported external runners and machine placement are rejected by the API's `requireForAllRunners` option. Missing/incompatible APIs or an existing foreign registration leave the `subagent` tool blocked while parent file/bash guards remain active. The complete version, lifecycle, instruction/skill inheritance and test qualifications are in [Pi child inheritance](pi-child-inheritance.md).

Direct file tools use a check before opening the file, not an OS sandbox. A concurrent attacker can race path replacement after the check, and hardlinks can refer to the same inode through paths on both sides of a boundary. Allowed bash writes to an existing hardlink can also change that inode. Read access includes secrets available to the host user; open network access permits sending them, and access to local services/Unix sockets can cause effects outside the filesystem mounts. Writable project code can influence later host processes. Do not use this profile for hostile repositories or untrusted extensions where those limitations are unacceptable.

## Status, verification and recovery

Requirements are Linux, the supported Pi SDK (tested with `@earendil-works/pi-coding-agent` 1.3.0), `/bin/bash`, and `/usr/bin/bwrap` with working unprivileged namespaces. `socat` is not required.

Run `/agentic-local` in Pi or T3 to execute a harmless `true` sandbox probe and show effective writable roots. A failed probe means bash is unavailable until the dependency or namespace problem is fixed. The profile remains active for file-tool checks. Do not disable namespace restrictions globally merely to bypass this error; inspect the host's bubblewrap/AppArmor configuration with the operator. macOS requires a separate sandbox implementation and is not supported by this extension.

From the source checkout:

```bash
node --test tests/pi-permissions/*.test.mjs
PI_TEST_BWRAP=1 node --test tests/pi-permissions/policy.test.mjs
```

The first command runs path, approval, shell-transport, real Pi loader, and real RPC tests; it skips the host namespace test unless enabled. Child-inheritance tests additionally require a qualified `pi-subagents` release and discover it under `~/.pi/agent/npm/node_modules/pi-subagents` by default; set `PI_SUBAGENTS_ROOT` for a different source installation. Pi integration tests discover the target machine's installed SDK at `~/.local/lib/node_modules/@earendil-works/pi-coding-agent`; set `PI_SDK_ROOT` to test another SDK installation. They use isolated temporary homes and synthetic operations, with no login or model request. The second command checks actual reads, allowed writes, blocked direct/traversal/symlink writes, DNS and loopback binding. A host that denies nested namespace creation cannot qualify this test inside its enclosing sandbox; use an appropriately authorized host shell.

For activation and removal, use the feature installer's documented commands. Removal must delete only its managed extension entry and unchanged owned files; preserve unrelated Pi settings. Restart the backend after removal. No Codex, Claude, or shared-Agents installation is part of this profile.
