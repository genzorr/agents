# Pi permission contract

The optional Linux `agentic-local` extension uses Pi's built-in bash/write/edit tools and bubblewrap when active. [Setup, updates and removal](pi-setup.md#linux-permissions) belong to the installer. The selected default uses Pi’s normal extension loading with best-effort enforcement: a missing extension or initialization/reload failure can restore built-in tools. Extension exceptions, auth checks and child guards do not ensure parent activation. Strong mandatory host enforcement is not provided.

Run `/agentic-local` after restarting Pi/T3 to inspect current roots and probe bash. A failed sandbox probe blocks this extension's bash implementation until bubblewrap or namespace support is fixed; it does not prove that the host retained the extension.

## Operations and exceptions

[profile.json](../pi/permissions/profile.json) is the writable-root authority. Only existing configured directories are enabled at startup; missing roots require creation and restart. The extension does not automatically grant the working directory or external worktree metadata. Startup `TMPDIR` is trusted operator configuration; tool environment changes cannot add roots.

Ordinary `bash` and user `!`/`!!` commands run with a read-only host filesystem and configured writable mounts, private process/user/PID namespaces, a capability drop and private `/dev` and `/proc`. Network and loopback access remain enabled. Missing bubblewrap or denied namespace creation fails the command without an unsandboxed retry.

`write` and `edit` resolve paths and symlinks and ask before an outside-root write. Reads, listing, finding and grep retain host-user access. `bash_unrestricted` explicitly requests host-user execution and requires fresh approval showing the full command and working directory. Approval applies to one invocation. Other extension/MCP calls emitted through Pi's tool event require approval of the tool and arguments; that approval does not sandbox their internals.

Confirmations use Pi's UI or RPC `extension_ui_request` (`method: "confirm"`) and the matching response ID. Missing UI, cancellation, abort or a 60-second timeout denies the exception. A client without RPC dialog support cannot approve it; live T3 rendering is not established by the synthetic RPC tests.

## Children and inherited context

The child integration targets Pi 1.3.0 and pi-subagents 0.78.0/0.79.0 in the selected agent home's `npm/node_modules` layout. Required-child registration and the updater's child allowlist serve different purposes. Neither copies parent conversation history.

New unattended controls require pi-subagents 0.79.0; the legacy 0.78.0 required-child integration remains manual and does not qualify the worker helper. The policy admits native read-only `list`, `get`, `models` and `guide` queries without approval; capability probes, extra execution/configuration arguments and foreign tools remain manual. It admits fresh native worker launches with the required profile. Named status, steer, interrupt, resume, stop and blocking `bg_wait` additionally require an exact admitted-worker receipt stamped with the current coordinator UUID. Bound child `contact_supervisor` uses only its immediate-parent channel. Raw workflows/host commands, bare/fleet listings, alternate child selectors, nonblocking subscriptions, foreign targets and other extension/MCP calls receive no automatic exception. Manually approved foreign or legacy-workflow resumes do not mint unattended authority. Headless children still have no confirmation UI: an outside-scope operation must return blocked, never self-approve or bypass the profile. Native required-profile qualification is complete for this source; human parent UI behavior remains untested, and source qualification does not change installed behavior.

The source worker helper runs under the current ordinary interactive coordinator. Workers return blocked/partial/final outcomes; launch and retained resume expose exact run IDs in native text. Prefer native completion notifications in the running coordinator, using exact owned blocking waits when needed before inspecting status/result. Status requires a known ID; hidden metadata and guessed targets are not a supported recovery route. After restart, recover recorded native status/session state; do not promise automatic wake, exactly-once execution or process-exit observation by an observer that no longer exists. The ordinary-owner helper uses existing T3 tools and retains per-call MCP approval, including return to the fixed main conversation. Native child supervisor contact is not that ordinary return route. Native source-consumer/adapter tests establish separate thread/control/approval interfaces; live authenticated exposure, the combined ordinary Pi-to-worker path and human UI remain unqualified. Retry keys do not survive a caller-session restart as global deduplication.

Required-child paths do not establish parent activation or whole-process confinement. Treat permission loading or startup errors as loss of the expected boundary and stop guarded work. Automatic runtime self-update with mandatory `agentic-local` enforcement is unqualified.

Global/project context and skills have separate opt-ins in agent definitions: `inheritProjectContext: true`, `inheritGlobalContext: true` and `inheritSkills: true`. Global context additionally requires project-context inheritance. `skills`/`skillPath` selects explicit skills independently; `systemPromptMode: append` alone enables none of those inputs. Choose delegation authority and model/effort separately.

## Enforcement boundary

This is tool enforcement, not whole-process confinement. Pi, extension startup/background code, MCP internals, host APIs and other tool implementations run outside bubblewrap. Trusted code can bypass tool events or replace guarded tools. Do not load a second permission extension or copy this one into another auto-discovery directory.

File-tool checks happen before opening a path: concurrent path replacement and hardlinks remain escape risks. Host-readable secrets remain readable; open networking and local services/sockets can cause effects outside filesystem mounts. Writable code can affect later host processes. Do not use this profile for hostile repositories or untrusted extensions where these limits are unacceptable.

Native loader/RPC/child regressions live in `tests/pi-permissions`; host namespace qualification additionally uses `PI_TEST_BWRAP=1`. Those tests do not establish live UI behavior, model adherence or macOS enforcement.
