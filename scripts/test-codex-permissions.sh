#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
scratch_home="$(mktemp -d "${TMPDIR:-/tmp}/agents-codex-permissions.XXXXXX")"
trap 'rm -rf "$scratch_home"' EXIT

mkdir -p "$scratch_home"
cp "$repo_dir/tests/fixtures/legacy-codex-config.toml" "$scratch_home/config.toml"

CODEX_HOME="$scratch_home" python3 "$repo_dir/scripts/install-codex-permissions.py"
! rg -n '^\s*sandbox_mode\s*=|^\s*\[sandbox_workspace_write\]' "$scratch_home/config.toml"
rg -n '^default_permissions = "agentic-local"$|^\[permissions\.agentic-local\]$|^enabled = true$' "$scratch_home/config.toml" >/dev/null
rg -n '^approval_policy = "on-request"$|^approvals_reviewer = "auto_review"$' "$scratch_home/config.toml" >/dev/null
! rg -n '^"\.(git|codex)" = "write"$' "$scratch_home/config.toml"
rg -n '^\[permissions\.agentic-local\.filesystem\."~/.cache/uv"\]$' "$scratch_home/config.toml" >/dev/null
[[ "$(CODEX_HOME="$scratch_home" python3 "$repo_dir/scripts/install-codex-permissions.py" --dry-run)" == *"already installed"* ]]
CODEX_HOME="$scratch_home" codex --strict-config --cd "$repo_dir" --help >/dev/null

inline_home="$scratch_home/inline"
mkdir -p "$inline_home"
cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$inline_home/config.toml"
CODEX_HOME="$inline_home" python3 "$repo_dir/scripts/install-codex-permissions.py"
! rg -n '^\s*sandbox_workspace_write\s*=' "$inline_home/config.toml"
rg -n '^approval_policy = "on-request"$|^approvals_reviewer = "auto_review"$' "$inline_home/config.toml" >/dev/null
CODEX_HOME="$inline_home" codex --strict-config --cd "$repo_dir" --help >/dev/null

empty_home="$scratch_home/empty"
mkdir -p "$empty_home"
CODEX_HOME="$empty_home" python3 "$repo_dir/scripts/install-codex-permissions.py"
rg -n '^approval_policy = "on-request"$|^approvals_reviewer = "auto_review"$' "$empty_home/config.toml" >/dev/null
CODEX_HOME="$empty_home" codex --strict-config --cd "$repo_dir" --help >/dev/null

for machine in laptop genzorr-pc; do
    bridge_home="$scratch_home/$machine"
    mkdir -p "$bridge_home"
    cp "$repo_dir/tests/fixtures/codex-thread-bridge-$machine.toml" "$bridge_home/config.toml"

    CODEX_HOME="$bridge_home" python3 "$repo_dir/scripts/install-codex-permissions.py" --configure-thread-bridge
    rg -n '^default_permissions = "agentic-local"$|^approval_policy = "on-request"$|^approvals_reviewer = "auto_review"$' "$bridge_home/config.toml" >/dev/null
    rg -n '^CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS = "agentic-local"$|^CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY = "on-request"$|^CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER = "auto_review"$' "$bridge_home/config.toml" >/dev/null
    [[ "$(rg -c '^CODEX_THREAD_BRIDGE_DEFAULT_(PERMISSIONS|APPROVAL_POLICY|APPROVALS_REVIEWER) =' "$bridge_home/config.toml")" == "3" ]]
    if [[ "$machine" == "laptop" ]]; then
        rg -F 'command = "/Users/genzorr/dev/tools/codex-thread-bridge/.venv/bin/codex-thread-bridge"' "$bridge_home/config.toml" >/dev/null
        rg -F 'args = ["--socket", "/Users/genzorr/.codex/app-server-control/app-server-control.sock", "--state-dir", "/Users/genzorr/.local/state/codex-thread-bridge"]' "$bridge_home/config.toml" >/dev/null
        rg -F 'disabled_tools = ["create_worktree_thread"]' "$bridge_home/config.toml" >/dev/null
        rg -F 'CODEX_THREAD_BRIDGE_MACHINE_LABEL = "laptop"' "$bridge_home/config.toml" >/dev/null
    else
        rg -F 'command = "/home/genzorr/dev/tools/codex-thread-bridge/.venv/bin/codex-thread-bridge"' "$bridge_home/config.toml" >/dev/null
        rg -F 'args = ["--socket", "/home/genzorr/.codex/app-server-control/app-server-control.sock", "--state-dir", "/home/genzorr/.local/state/codex-thread-bridge"]' "$bridge_home/config.toml" >/dev/null
        rg -F 'disabled_tools = ["create_worktree_thread"]' "$bridge_home/config.toml" >/dev/null
        rg -F '[mcp_servers.other-server]' "$bridge_home/config.toml" >/dev/null
    fi
    rg -n '^tool_timeout_sec = 60$' "$bridge_home/config.toml" >/dev/null
    [[ "$(CODEX_HOME="$bridge_home" python3 "$repo_dir/scripts/install-codex-permissions.py" --configure-thread-bridge --dry-run)" == *"already installed"* ]]
    CODEX_HOME="$bridge_home" codex --strict-config --cd "$repo_dir" --help >/dev/null
done

missing_home="$scratch_home/missing-bridge"
mkdir -p "$missing_home"
cp "$repo_dir/tests/fixtures/legacy-codex-config.toml" "$missing_home/config.toml"
if CODEX_HOME="$missing_home" python3 "$repo_dir/scripts/install-codex-permissions.py" --configure-thread-bridge 2>"$missing_home/error.log"; then
    echo "missing MCP entry unexpectedly succeeded" >&2
    exit 1
fi
rg -n 'MCP server entry \[mcp_servers\.codex-thread-bridge\] is absent' "$missing_home/error.log" >/dev/null
cmp "$repo_dir/tests/fixtures/legacy-codex-config.toml" "$missing_home/config.toml"

ambiguous_home="$scratch_home/ambiguous-bridge"
mkdir -p "$ambiguous_home"
cp "$repo_dir/tests/fixtures/codex-thread-bridge-ambiguous.toml" "$ambiguous_home/config.toml"
if CODEX_HOME="$ambiguous_home" python3 "$repo_dir/scripts/install-codex-permissions.py" --configure-thread-bridge 2>"$ambiguous_home/error.log"; then
    echo "ambiguous MCP entry unexpectedly succeeded" >&2
    exit 1
fi
rg -n 'MCP server entry \[mcp_servers\.codex-thread-bridge\] is ambiguous' "$ambiguous_home/error.log" >/dev/null
cmp "$repo_dir/tests/fixtures/codex-thread-bridge-ambiguous.toml" "$ambiguous_home/config.toml"

echo "Codex Custom profile scratch test passed"
