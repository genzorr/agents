#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
scratch_home="$(mktemp -d "${TMPDIR:-/tmp}/agents-codex-permissions.XXXXXX")"
trap 'rm -rf "$scratch_home"' EXIT

installer=(python3 "$repo_dir/scripts/install-codex-permissions.py")

assert_workspace_selector() {
    local config_path=$1
    awk '
        $0 == "[permissions.agentic-local.filesystem.\":workspace_roots\"]" { active = 1; next }
        active && /^\[/ { active = 0 }
        active && /^[[:space:]]*[^#[:space:]][^=]*=/ {
            entries++
            if ($0 != "\".\" = \"write\"") bad = 1
        }
        END { exit !(entries == 1 && !bad) }
    ' "$config_path"
}

run_install() {
    CODEX_HOME="$1" "${installer[@]}" "${@:2}"
}

file_mode() {
    python3 -c 'import os, stat, sys; print(stat.S_IMODE(os.stat(sys.argv[1]).st_mode))' "$1"
}

insert_before() {
    python3 - "$1" "$2" "$3" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
marker = sys.argv[2]
insertion = sys.argv[3]
text = path.read_text(encoding="utf-8")
if text.count(marker) != 1:
    raise SystemExit(f"expected one marker: {marker}")
path.write_text(text.replace(marker, f"{insertion}\n{marker}", 1), encoding="utf-8")
PY
}

insert_after() {
    python3 - "$1" "$2" "$3" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
marker = sys.argv[2]
insertion = sys.argv[3]
text = path.read_text(encoding="utf-8")
if text.count(marker) != 1:
    raise SystemExit(f"expected one marker: {marker}")
path.write_text(text.replace(marker, f"{marker}\n{insertion}", 1), encoding="utf-8")
PY
}

mkdir -p "$scratch_home/base"
cp "$repo_dir/tests/fixtures/legacy-codex-config.toml" "$scratch_home/base/config.toml"
base_mode_before="$(file_mode "$scratch_home/base/config.toml")"
run_install "$scratch_home/base"
rg -n '^default_permissions = "agentic-local"$|^approval_policy = "on-request"$|^approvals_reviewer = "auto_review"$' "$scratch_home/base/config.toml" >/dev/null
! rg -n '^\[apps\._default\]$|^default_tools_approval_mode = "writes"$' "$scratch_home/base/config.toml"
assert_workspace_selector "$scratch_home/base/config.toml"
base_mode="$(file_mode "$scratch_home/base/config.toml")"
[[ "$base_mode" == "$base_mode_before" ]]
[[ "$(run_install "$scratch_home/base" --dry-run)" == *"already installed"* ]]

dry_missing="$scratch_home/dry-missing"
[[ ! -e "$dry_missing" ]]
[[ "$(run_install "$dry_missing" --dry-run)" == *"would update"* ]]
[[ ! -e "$dry_missing" ]]

for machine in laptop genzorr-pc; do
    bridge_home="$scratch_home/bridge-$machine"
    mkdir -p "$bridge_home"
    cp "$repo_dir/tests/fixtures/codex-thread-bridge-$machine.toml" "$bridge_home/config.toml"
    if [[ "$machine" == "laptop" ]]; then
        insert_after "$bridge_home/config.toml" 'tool_timeout_sec = 60' 'default_tools_approval_mode = "auto"'
    fi
    run_install "$bridge_home" --configure-thread-bridge
    rg -n '^default_tools_approval_mode = "writes"$' "$bridge_home/config.toml" >/dev/null
    [[ "$(rg -c '^default_tools_approval_mode = "writes"$' "$bridge_home/config.toml")" == "1" ]]
    rg -n '^CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS = "agentic-local"$|^CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY = "on-request"$|^CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER = "auto_review"$' "$bridge_home/config.toml" >/dev/null
    [[ "$(rg -c '^CODEX_THREAD_BRIDGE_DEFAULT_(PERMISSIONS|APPROVAL_POLICY|APPROVALS_REVIEWER) =' "$bridge_home/config.toml")" == "3" ]]
    rg -F 'disabled_tools = ["create_worktree_thread"]' "$bridge_home/config.toml" >/dev/null
    rg -n '^tool_timeout_sec = 60$' "$bridge_home/config.toml" >/dev/null
    if [[ "$machine" == "laptop" ]]; then
        rg -F 'CODEX_THREAD_BRIDGE_MACHINE_LABEL = "laptop"' "$bridge_home/config.toml" >/dev/null
    else
        rg -F '[mcp_servers.other-server]' "$bridge_home/config.toml" >/dev/null
    fi
    cp "$bridge_home/config.toml" "$bridge_home/once.toml"
    run_install "$bridge_home" --configure-thread-bridge
    cmp "$bridge_home/once.toml" "$bridge_home/config.toml"
done

for rejected in missing ambiguous-bridge inline-bridge malformed unknown quoted-app inline-app dotted-app duplicate-app duplicate-key duplicate-app-key duplicate-bridge-key; do
    rejected_home="$scratch_home/$rejected"
    mkdir -p "$rejected_home"
    cp "$repo_dir/tests/fixtures/legacy-codex-config.toml" "$rejected_home/config.toml"
    case "$rejected" in
        missing) args=(--configure-thread-bridge) ;;
        ambiguous-bridge) cp "$repo_dir/tests/fixtures/codex-thread-bridge-ambiguous.toml" "$rejected_home/config.toml"; args=(--configure-thread-bridge) ;;
        inline-bridge) cp "$repo_dir/tests/fixtures/codex-thread-bridge-laptop.toml" "$rejected_home/config.toml"; insert_after "$rejected_home/config.toml" 'tool_timeout_sec = 60' 'env = { BRIDGE_LABEL = "laptop" }'; args=(--configure-thread-bridge) ;;
        malformed) cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$rejected_home/config.toml"; printf 'model = [\n' >> "$rejected_home/config.toml"; args=() ;;
        unknown) cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$rejected_home/config.toml"; printf 'unknown_thing = true\n' >> "$rejected_home/config.toml"; args=() ;;
        quoted-app) cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$rejected_home/config.toml"; printf '\n[apps."_default"]\napprovals_reviewer = "user"\n' >> "$rejected_home/config.toml"; args=(--configure-app-defaults) ;;
        inline-app) insert_before "$rejected_home/config.toml" '[sandbox_workspace_write]' 'apps = { _default = { approvals_reviewer = "user" } }'; args=(--configure-app-defaults) ;;
        dotted-app) insert_before "$rejected_home/config.toml" '[sandbox_workspace_write]' 'apps._default.approvals_reviewer = "user"'; args=(--configure-app-defaults) ;;
        duplicate-app) cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$rejected_home/config.toml"; printf '\n[apps._default]\n[apps._default]\n' >> "$rejected_home/config.toml"; args=(--configure-app-defaults) ;;
        duplicate-key) cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$rejected_home/config.toml"; printf '\n[apps._default]\n"approvals_reviewer" = "user"\n' >> "$rejected_home/config.toml"; args=(--configure-app-defaults) ;;
        duplicate-app-key) cp "$repo_dir/tests/fixtures/inline-codex-config.toml" "$rejected_home/config.toml"; printf '\n[apps._default]\napprovals_reviewer = "user"\napprovals_reviewer = "auto_review"\n' >> "$rejected_home/config.toml"; args=(--configure-app-defaults) ;;
        duplicate-bridge-key) cp "$repo_dir/tests/fixtures/codex-thread-bridge-laptop.toml" "$rejected_home/config.toml"; insert_after "$rejected_home/config.toml" 'tool_timeout_sec = 60' $'default_tools_approval_mode = "auto"\ndefault_tools_approval_mode = "writes"'; args=(--configure-thread-bridge) ;;
    esac
    cp "$rejected_home/config.toml" "$rejected_home/original.toml"
    if run_install "$rejected_home" "${args[@]}" 2>"$rejected_home/error.log"; then
        echo "$rejected unexpectedly succeeded" >&2
        exit 1
    fi
    cmp "$rejected_home/original.toml" "$rejected_home/config.toml"
done
rg -n 'unknown configuration field|expected' "$scratch_home/malformed/error.log" >/dev/null
rg -n 'unknown configuration field .*unknown_thing' "$scratch_home/unknown/error.log" >/dev/null
rg -n 'MCP server entry \[mcp_servers\.codex-thread-bridge\] is ambiguous' "$scratch_home/ambiguous-bridge/error.log" >/dev/null
rg -n 'MCP server entry \[mcp_servers\.codex-thread-bridge\] has an inline env value' "$scratch_home/inline-bridge/error.log" >/dev/null
rg -n 'unsupported apps table representation' "$scratch_home/quoted-app/error.log" >/dev/null
rg -n 'unsupported inline or dotted apps._default representation' "$scratch_home/inline-app/error.log" >/dev/null
rg -n 'ambiguous' "$scratch_home/duplicate-app/error.log" >/dev/null
rg -n 'unsupported quoted key' "$scratch_home/duplicate-key/error.log" >/dev/null
rg -n 'key approvals_reviewer is ambiguous' "$scratch_home/duplicate-app-key/error.log" >/dev/null
rg -n 'key default_tools_approval_mode is ambiguous' "$scratch_home/duplicate-bridge-key/error.log" >/dev/null

app_home="$scratch_home/app-defaults"
mkdir -p "$app_home"
cp "$repo_dir/tests/fixtures/app-defaults.toml" "$app_home/config.toml"
run_install "$app_home" --configure-app-defaults
rg -n '^\[apps\._default\]$|^approvals_reviewer = "auto_review"$|^default_tools_approval_mode = "writes"$|^destructive_enabled = false$' "$app_home/config.toml" >/dev/null
rg -F '[apps.google_drive.tools."files/delete"]' "$app_home/config.toml" >/dev/null
rg -n '^open_world_enabled = false$|^default_tools_approval_mode = "approve"$' "$app_home/config.toml" >/dev/null
cp "$app_home/config.toml" "$app_home/once.toml"
run_install "$app_home" --configure-app-defaults
cmp "$app_home/once.toml" "$app_home/config.toml"

app_create_home="$scratch_home/app-create"
mkdir -p "$app_create_home"
cp "$repo_dir/tests/fixtures/legacy-codex-config.toml" "$app_create_home/config.toml"
run_install "$app_create_home" --configure-app-defaults
rg -n '^\[apps\._default\]$|^approvals_reviewer = "auto_review"$|^default_tools_approval_mode = "writes"$' "$app_create_home/config.toml" >/dev/null

echo "Codex Custom profile scratch test passed"
