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
echo "Codex Custom profile scratch test passed"
