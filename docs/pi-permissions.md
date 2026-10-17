# Pi permission contract

The optional Linux `agentic-local` extension uses Pi's built-in bash/write/edit tools and bubblewrap when active. [Setup, updates and removal](pi-setup.md#linux-permissions) belong to the installer. Current CLI/T3 loading is best effort: a missing extension or initialization/reload failure can restore built-in tools. Extension exceptions, auth checks and child guards do not ensure parent activation. A mandatory profile requires a host-level activation gate before startup and tool-registry replacement/reload; unmodified hosts are not qualified.

Run `/agentic-local` after restarting Pi/T3 to inspect current roots and probe bash. A failed sandbox probe blocks this extension's bash implementation until bubblewrap or namespace support is fixed; it does not prove that the host retained the extension.

## Operations and exceptions

[profile.json](../pi/permissions/profile.json) is the writable-root authority. Only existing configured directories are enabled at startup; missing roots require creation and restart. The extension does not automatically grant the working directory or external worktree metadata. Startup `TMPDIR` is trusted operator configuration; tool environment changes cannot add roots.

Ordinary `bash` and user `!`/`!!` commands run with a read-only host filesystem and configured writable mounts, private process/user/PID namespaces, a capability drop and private `/dev` and `/proc`. Network and loopback access remain enabled. Missing bubblewrap or denied namespace creation fails the command without an unsandboxed retry.

`write` and `edit` resolve paths and symlinks and ask before an outside-root write. Reads, listing, finding and grep retain host-user access. `bash_unrestricted` explicitly requests host-user execution and requires fresh approval showing the full command and working directory. Approval applies to one invocation. Extension/MCP calls emitted through Pi's tool event also require approval of the tool and arguments; that approval does not sandbox their internals.

Confirmations use Pi's UI or RPC `extension_ui_request` (`method: "confirm"`) and the matching response ID. Missing UI, cancellation, abort or a 60-second timeout denies the exception. A client without RPC dialog support cannot approve it; live T3 rendering is not established by the synthetic RPC tests.

## Children and inherited context

The child integration targets Pi 1.3.0 and pi-subagents 0.78.0/0.79.0 in the selected agent home's `npm/node_modules` layout. Required-child registration and the updater's child allowlist serve different purposes. Neither copies parent conversation history.

Required-child paths do not establish parent activation or whole-process confinement. Treat permission loading or startup errors as loss of the expected boundary and stop guarded work. Automatic runtime self-update with mandatory `agentic-local` enforcement is unqualified.

Global/project context and skills have separate opt-ins in agent definitions: `inheritProjectContext: true`, `inheritGlobalContext: true` and `inheritSkills: true`. Global context additionally requires project-context inheritance. `skills`/`skillPath` selects explicit skills independently; `systemPromptMode: append` alone enables none of those inputs. Choose delegation authority and model/effort separately.

## Enforcement boundary

This is tool enforcement, not whole-process confinement. Pi, extension startup/background code, MCP internals, host APIs and other tool implementations run outside bubblewrap. Trusted code can bypass tool events or replace guarded tools. Do not load a second permission extension or copy this one into another auto-discovery directory.

File-tool checks happen before opening a path: concurrent path replacement and hardlinks remain escape risks. Host-readable secrets remain readable; open networking and local services/sockets can cause effects outside filesystem mounts. Writable code can affect later host processes. Do not use this profile for hostile repositories or untrusted extensions where these limits are unacceptable.

Native loader/RPC/child regressions live in `tests/pi-permissions`; host namespace qualification additionally uses `PI_TEST_BWRAP=1`. Those tests do not establish live UI behavior, model adherence or macOS enforcement.
