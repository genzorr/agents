# Personal Codex Thread Bridge Configuration

The optional permission installer owns the personal defaults for bridge-created Codex tasks. It does not own the bridge command or a complete `config.toml`; it patches only the existing `[mcp_servers.codex-thread-bridge.env]` table.

Run this locally on both the laptop and `genzorr-pc` after installing or updating the bridge configuration:

```bash
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-thread-bridge
```

The command derives these values from `config/codex-permissions.toml` and writes them as MCP environment variables:

| Environment variable | Source-owned value |
| --- | --- |
| `CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS` | `default_permissions` |
| `CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY` | `approval_policy` |
| `CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER` | `approvals_reviewer` |

The patch preserves the existing bridge `command`, `args`, socket, state directory, disabled tools, timeouts, other MCP environment variables, and unrelated Codex settings. It fails before writing when the exact `codex-thread-bridge` MCP entry is absent or appears more than once. Running it again is idempotent.

The expected laptop entry after installation is:

```toml
[mcp_servers.codex-thread-bridge]
command = "/Users/genzorr/dev/tools/codex-thread-bridge/.venv/bin/codex-thread-bridge"
args = ["--socket", "/Users/genzorr/.codex/app-server-control/app-server-control.sock", "--state-dir", "/Users/genzorr/.local/state/codex-thread-bridge"]
disabled_tools = ["create_worktree_thread"]
tool_timeout_sec = 60

[mcp_servers.codex-thread-bridge.env]
CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS = "agentic-local"
CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY = "on-request"
CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER = "auto_review"
```

The expected `genzorr-pc` entry after installation is:

```toml
[mcp_servers.codex-thread-bridge]
command = "/home/genzorr/dev/tools/codex-thread-bridge/.venv/bin/codex-thread-bridge"
args = ["--socket", "/home/genzorr/.codex/app-server-control/app-server-control.sock", "--state-dir", "/home/genzorr/.local/state/codex-thread-bridge"]
disabled_tools = ["create_worktree_thread"]
tool_timeout_sec = 60

[mcp_servers.codex-thread-bridge.env]
CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS = "agentic-local"
CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY = "on-request"
CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER = "auto_review"
```

## Bridge counterpart contract

The public `codex-thread-bridge` repository should keep its generic CLI options `--default-permissions`, `--default-approval-policy`, and `--default-approvals-reviewer`, without embedding the personal profile name. To consume this personal MCP configuration, the bridge needs three optional generic environment fallbacks with the same names shown above. Explicit CLI options must take precedence over environment defaults, and environment defaults must take precedence over the bridge's legacy built-in defaults. The bridge should apply the effective values to newly created tasks only; existing task state and unrelated server configuration remain unchanged.
