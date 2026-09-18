# Codex Permission and Thread Bridge Configuration

The optional permission installer owns the `agentic-local` profile and can patch two narrowly scoped opt-ins. It never replaces a complete `config.toml`, owns no bridge command/source, and preserves unrelated MCP, app, and tool settings.

```bash
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-thread-bridge
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-app-defaults
```

Before an installation write, and also before reporting that a dry run would update a config, the installer strict-loads the full prospective config with `codex app-server --strict-config --listen off` in an isolated temporary `CODEX_HOME`. A missing/incompatible Codex, timeout, syntax error, unknown key, or unsupported representation leaves the target byte-identical and does not create a missing destination directory or backup. The installer prints a rollback command after a successful write, and `--rollback PATH` restores a recorded backup while preserving the current config as a new backup.

## Workspace and Git policy

The profile keeps `approval_policy = "on-request"` and `approvals_reviewer = "auto_review"`. Its `:workspace_roots` child table must remain exactly `{ "." = "write" }`: relative child selectors can be fed back as roots by the desktop app, causing recursive growth, latency, and `E2BIG` across turns. This avoids the known trigger described in [openai/codex#33479](https://github.com/openai/codex/issues/33479) and [openai/codex#37632](https://github.com/openai/codex/issues/37632); it does not claim those upstream issues are fixed.

The profile intentionally grants no `.git` write selector. If protected repository metadata blocks a necessary commit or push, Codex may request a narrow escalation handled by Auto-review. User/repository policy and remote branch protection still decide whether a feature-branch push is authorized. Do not infer that every push is reviewed: commands already allowed by the sandbox bypass Auto-review. The installer has no Git hook, wrapper, or absolute repository allowlist.

## Thread bridge opt-in

`--configure-thread-bridge` patches the existing bridge server table and its environment-default table:

```toml
[mcp_servers.codex-thread-bridge]
default_tools_approval_mode = "writes"

[mcp_servers.codex-thread-bridge.env]
CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS = "agentic-local"
CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY = "on-request"
CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER = "auto_review"
```

The environment defaults derive from the profile's `default_permissions`, `approval_policy`, and `approvals_reviewer` root values. It rejects a missing or duplicate bridge table, inline `env` value, duplicate environment table, or duplicate owned key before writing. Read tools exposed by the bridge are annotated read-only and need no approval prompt; mutation tools remain approval-eligible under the `writes` default and can be Auto-reviewed. The patch does not add redundant tool tables or alter the bridge source, command, unrelated environment variables, socket, state directory, disabled tools, timeout, or other MCP tables. Running it again is byte-idempotent.

After installation, request an MCP reload or start a fresh task, then verify the exposed schema against the [bridge README](https://github.com/genzorr/codex-thread-bridge#readme).

## Bridge counterpart contract

The public `codex-thread-bridge` repository keeps its generic `--default-permissions`, `--default-approval-policy`, and `--default-approvals-reviewer` CLI options without embedding the personal profile name. It accepts the three `CODEX_THREAD_BRIDGE_DEFAULT_*` environment fallbacks shown above: explicit CLI options take precedence over environment defaults, which take precedence over legacy built-ins. The bridge applies these effective defaults to newly created tasks only; existing task state and unrelated server configuration remain unchanged.

## Native app-default opt-in

`--configure-app-defaults` is deliberately separate from the profile and bridge flags. It creates or updates only these keys in the one canonical `[apps._default]` table:

```toml
[apps._default]
approvals_reviewer = "auto_review"
default_tools_approval_mode = "writes"
```

It preserves unrelated default fields, per-app settings, and per-tool settings. It does not set or change `destructive_enabled` or `open_world_enabled`, blanket-approve writes, or add an `apps` table to `config/codex-permissions.toml`. To avoid semantic duplicates, the conservative line patcher rejects quoted, dotted, inline, duplicate-table, and quoted-owned-key representations that it cannot safely recognize. Running it again is byte-idempotent.
