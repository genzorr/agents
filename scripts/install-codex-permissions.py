#!/usr/bin/env python3
"""Install the agents-owned Codex Custom permission profile without clobbering user config."""

from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


REPO_DIR = Path(__file__).resolve().parents[1]
PROFILE_PATH = REPO_DIR / "config" / "codex-permissions.toml"
PROFILE_NAME = "agentic-local"
PROFILE_ROOT_KEYS = {
    "default_permissions",
    "approval_policy",
    "approvals_reviewer",
}
BRIDGE_SERVER_TABLE = "mcp_servers.codex-thread-bridge"
BRIDGE_ENV_TABLE = f"{BRIDGE_SERVER_TABLE}.env"
BRIDGE_ENV_KEYS = {
    "default_permissions": "CODEX_THREAD_BRIDGE_DEFAULT_PERMISSIONS",
    "approval_policy": "CODEX_THREAD_BRIDGE_DEFAULT_APPROVAL_POLICY",
    "approvals_reviewer": "CODEX_THREAD_BRIDGE_DEFAULT_APPROVALS_REVIEWER",
}
BRIDGE_OWNED_KEY = "default_tools_approval_mode"
BRIDGE_OWNED_VALUE = "writes"
APP_DEFAULT_TABLE = "apps._default"
APP_DEFAULT_VALUES = {"approvals_reviewer": "auto_review", "default_tools_approval_mode": "writes"}
CODEX_APP_SERVER_TABLE = 'plugins."codex-app-tools@openai-bundled".mcp_servers.codex_app'
CODEX_APP_TOOL_APPROVALS = (
    "automation_update",
    "create_thread",
    "send_message_to_thread",
    "fork_thread",
    "handoff_thread",
)
VALIDATION_TIMEOUT_SECONDS = 15
TABLE_RE = re.compile(r"^\s*\[\[?([^\]]+)\]\]?\s*(?:#.*)?$")
ROOT_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*=")
ASSIGNMENT_RE = re.compile(r"^\s*([^=\s]+)\s*=")


def table_name(line: str) -> Optional[str]:
    match = TABLE_RE.match(line.rstrip("\n"))
    return match.group(1).strip() if match else None


def remove_sections(lines: list[str], predicate) -> list[str]:
    output: list[str] = []
    skipping = False
    for line in lines:
        name = table_name(line)
        if name is not None:
            skipping = predicate(name)
        if not skipping:
            output.append(line)
    return output


def remove_root_keys(lines: list[str], keys: set[str]) -> list[str]:
    output: list[str] = []
    current_table: Optional[str] = None
    for line in lines:
        name = table_name(line)
        if name is not None:
            current_table = name
        match = ROOT_KEY_RE.match(line)
        if current_table is None and match and match.group(1) in keys:
            continue
        output.append(line)
    return output


def profile_parts() -> tuple[list[str], str]:
    text = PROFILE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not any(line == f'default_permissions = "{PROFILE_NAME}"' for line in lines):
        raise ValueError(f"profile template does not select {PROFILE_NAME}")
    first_table = next((index for index, line in enumerate(lines) if table_name(line)), None)
    if first_table is None:
        raise ValueError("profile template has no permission table")
    root_lines = [line for line in lines[:first_table] if line.strip() and not line.lstrip().startswith("#")]
    found_keys = {
        match.group(1)
        for line in root_lines
        if (match := ROOT_KEY_RE.match(line)) is not None
    }
    if found_keys != PROFILE_ROOT_KEYS:
        raise ValueError(
            f"profile template root keys must be {sorted(PROFILE_ROOT_KEYS)}, got {sorted(found_keys)}"
        )
    return root_lines, "\n".join(lines[first_table:])


def profile_bridge_defaults(root_lines: list[str]) -> dict[str, str]:
    values = {
        match.group(1): match.group(2)
        for line in root_lines
        if (match := re.fullmatch(r'\s*([A-Za-z0-9_-]+)\s*=\s*"([^"]*)"\s*', line))
    }
    if set(values) != PROFILE_ROOT_KEYS:
        raise ValueError(
            f"profile template values must define {sorted(PROFILE_ROOT_KEYS)}, got {sorted(values)}"
        )
    return {env_key: values[profile_key] for profile_key, env_key in BRIDGE_ENV_KEYS.items()}


def section_ranges(lines: list[str], name: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    current_name: Optional[str] = None
    current_start: Optional[int] = None
    for index, line in enumerate(lines):
        table = table_name(line)
        if table is None:
            continue
        if current_name == name and current_start is not None:
            ranges.append((current_start, index))
        current_name = table
        current_start = index
    if current_name == name and current_start is not None:
        ranges.append((current_start, len(lines)))
    return ranges


def toml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def reject_unrecognized_app_defaults(lines: list[str]) -> None:
    """Reject equivalent app-default syntax that this conservative line patcher cannot own."""
    for line in lines:
        table = table_name(line)
        if table is not None and (table.startswith('apps."_default"') or table.startswith("apps.'_default'")):
            raise ValueError(f"unsupported apps table representation [{table}]")
        if re.match(r"^\s*apps(?:\s*=|\._default(?:\.|\s*=))", line):
            raise ValueError("unsupported inline or dotted apps._default representation")


def patch_table_values(
    existing: str,
    *,
    table: str,
    values: dict[str, str],
    missing_table_error: Optional[str] = None,
) -> str:
    lines = existing.splitlines()
    ranges = section_ranges(lines, table)
    if not ranges:
        if missing_table_error:
            raise ValueError(missing_table_error)
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"[{table}]")
        lines.extend(f'{key} = "{toml_string(value)}"' for key, value in values.items())
        return "\n".join(lines) + "\n"
    if len(ranges) != 1:
        raise ValueError(f"table [{table}] is ambiguous: found {len(ranges)} entries")
    start, end = ranges[0]
    owned_indices: dict[str, int] = {}
    for index in range(start + 1, end):
        match = ASSIGNMENT_RE.match(lines[index])
        if match is None:
            continue
        raw_key = match.group(1)
        if raw_key in values:
            if raw_key in owned_indices:
                raise ValueError(f"key {raw_key} is ambiguous in [{table}]")
            owned_indices[raw_key] = index
        elif raw_key.strip('"') in values:
            raise ValueError(f"unsupported quoted key {raw_key} in [{table}]")
    rendered = {key: f'{key} = "{toml_string(value)}"' for key, value in values.items()}
    for key, index in owned_indices.items():
        lines[index] = rendered[key]
    missing = [key for key in values if key not in owned_indices]
    insert_at = end
    while insert_at > start + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines[insert_at:insert_at] = [rendered[key] for key in missing]
    return "\n".join(lines) + "\n"


def patch_bridge_defaults(existing: str) -> str:
    lines = existing.splitlines()
    server_ranges = section_ranges(lines, BRIDGE_SERVER_TABLE)
    if not server_ranges:
        raise ValueError(f"MCP server entry [{BRIDGE_SERVER_TABLE}] is absent")
    if len(server_ranges) != 1:
        raise ValueError(
            f"MCP server entry [{BRIDGE_SERVER_TABLE}] is ambiguous: found {len(server_ranges)} entries"
        )
    server_start, server_end = server_ranges[0]
    if any(
        (match := ROOT_KEY_RE.match(lines[index])) is not None and match.group(1) == "env"
        for index in range(server_start + 1, server_end)
    ):
        raise ValueError(
            f"MCP server entry [{BRIDGE_SERVER_TABLE}] has an inline env value; expected [{BRIDGE_ENV_TABLE}]"
        )
    root_lines, _ = profile_parts()
    patched = patch_table_values(
        existing,
        table=BRIDGE_SERVER_TABLE,
        values={BRIDGE_OWNED_KEY: BRIDGE_OWNED_VALUE},
        missing_table_error=f"MCP server entry [{BRIDGE_SERVER_TABLE}] is absent",
    )
    return patch_table_values(
        patched,
        table=BRIDGE_ENV_TABLE,
        values=profile_bridge_defaults(root_lines),
    )


def patch_app_defaults(existing: str) -> str:
    lines = existing.splitlines()
    reject_unrecognized_app_defaults(lines)
    return patch_table_values(existing, table=APP_DEFAULT_TABLE, values=APP_DEFAULT_VALUES)


def approve_codex_app_tools(existing: str) -> str:
    patched = patch_table_values(
        existing,
        table=CODEX_APP_SERVER_TABLE,
        values={"default_tools_approval_mode": "approve"},
    )
    for tool in CODEX_APP_TOOL_APPROVALS:
        patched = patch_table_values(
            patched,
            table=f"{CODEX_APP_SERVER_TABLE}.tools.{tool}",
            values={"approval_mode": "approve"},
        )
    return patched


def render_config(
    existing: str,
    *,
    configure_thread_bridge: bool = False,
    configure_app_defaults: bool = False,
    approve_codex_app_tools_enabled: bool = False,
) -> str:
    root_lines, body = profile_parts()
    lines = remove_root_keys(
        existing.splitlines(),
        PROFILE_ROOT_KEYS | {"sandbox_mode", "sandbox_workspace_write"},
    )
    lines = remove_sections(
        lines,
        lambda name: name == "sandbox_workspace_write"
        or name == f"permissions.{PROFILE_NAME}"
        or name.startswith(f"permissions.{PROFILE_NAME}."),
    )
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    prefix = "\n".join(root_lines + [""] + lines).rstrip("\n")
    if configure_thread_bridge:
        prefix = patch_bridge_defaults(prefix + "\n").rstrip("\n")
    if configure_app_defaults:
        prefix = patch_app_defaults(prefix + "\n").rstrip("\n")
    if approve_codex_app_tools_enabled:
        prefix = approve_codex_app_tools(prefix + "\n").rstrip("\n")
    rendered = "\n".join([prefix, "", body.rstrip(), ""])
    validate_rendered_config(rendered)
    return rendered


def validate_rendered_config(text: str) -> None:
    if re.search(r"^\s*sandbox_mode\s*=", text, re.MULTILINE):
        raise ValueError("legacy sandbox_mode remains in rendered config")
    if re.search(r"^\s*\[sandbox_workspace_write\]", text, re.MULTILINE):
        raise ValueError("legacy sandbox_workspace_write remains in rendered config")
    if re.search(r"^\s*sandbox_workspace_write\s*=", text, re.MULTILINE):
        raise ValueError("legacy inline sandbox_workspace_write remains in rendered config")
    if f'default_permissions = "{PROFILE_NAME}"' not in text:
        raise ValueError(f"default_permissions is not {PROFILE_NAME}")
    if 'approval_policy = "on-request"' not in text:
        raise ValueError("approval_policy is not on-request")
    if 'approvals_reviewer = "auto_review"' not in text:
        raise ValueError("approvals_reviewer is not auto_review")
    if f"[permissions.{PROFILE_NAME}]" not in text:
        raise ValueError(f"permissions.{PROFILE_NAME} is missing")


def validate_with_codex(text: str) -> None:
    """Strict-load only the prospective config in a disposable Codex home before mutation."""
    with tempfile.TemporaryDirectory(prefix="agents-codex-config-validation-") as temporary_home:
        home = Path(temporary_home)
        (home / "config.toml").write_text(text, encoding="utf-8")
        for name in ("cache", "config", "data", "state"):
            (home / name).mkdir()
        environment = os.environ.copy()
        environment.update(
            {
                "CODEX_HOME": str(home),
                "HOME": str(home),
                "XDG_CACHE_HOME": str(home / "cache"),
                "XDG_CONFIG_HOME": str(home / "config"),
                "XDG_DATA_HOME": str(home / "data"),
                "XDG_STATE_HOME": str(home / "state"),
            }
        )
        try:
            result = subprocess.run(
                ["codex", "app-server", "--strict-config", "--listen", "off"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
                timeout=VALIDATION_TIMEOUT_SECONDS,
                check=False,
            )
        except FileNotFoundError as exc:
            raise ValueError("Codex is unavailable for strict configuration validation") from exc
        except subprocess.TimeoutExpired as exc:
            raise ValueError("Codex strict configuration validation timed out") from exc
    output = result.stdout + result.stderr
    # Some Codex releases validate successfully, then exit 1 because --listen off selects no transport.
    # Treat only that documented terminal condition as a valid strict load; all other nonzero exits reject.
    no_transport = "Error: no transport configured; use --listen or enable remote control" in output
    if result.returncode != 0 and not (result.returncode == 1 and no_transport):
        detail = output.strip().splitlines()[-1] if output.strip() else f"exit status {result.returncode}"
        raise ValueError(f"Codex strict configuration validation failed: {detail}")


def backup_path(config_path: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = config_path.with_name(f"{config_path.name}.bak.agentic-permissions-{stamp}")
    suffix = 1
    while candidate.exists():
        candidate = config_path.with_name(
            f"{config_path.name}.bak.agentic-permissions-{stamp}-{suffix}"
        )
        suffix += 1
    return candidate


def write_atomic(path: Path, content: str) -> None:
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    os.chmod(temp_path, mode)
    os.replace(temp_path, path)


def install(
    config_path: Path,
    *,
    dry_run: bool,
    configure_thread_bridge: bool,
    configure_app_defaults: bool,
    approve_codex_app_tools_enabled: bool,
) -> int:
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    rendered = render_config(
        existing,
        configure_thread_bridge=configure_thread_bridge,
        configure_app_defaults=configure_app_defaults,
        approve_codex_app_tools_enabled=approve_codex_app_tools_enabled,
    )
    validate_with_codex(rendered)
    suffixes = []
    if configure_thread_bridge:
        suffixes.append("codex-thread-bridge defaults")
    if configure_app_defaults:
        suffixes.append("app defaults")
    if approve_codex_app_tools_enabled:
        suffixes.append("Codex App tool approvals")
    suffix = f" and {', '.join(suffixes)}" if suffixes else ""
    if rendered == existing:
        print(f"Codex Custom profile{suffix} already installed: {PROFILE_NAME}")
        return 0
    if dry_run:
        changed = list(
            difflib.unified_diff(existing.splitlines(), rendered.splitlines(), lineterm="")
        )
        print(f"Dry run: would update {config_path} ({len(changed)} diff lines; content omitted)")
        return 0
    config_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    backup: Optional[Path] = None
    if config_path.exists():
        backup = backup_path(config_path)
        shutil.copy2(config_path, backup)
        print(f"Backup: {backup}")
    write_atomic(config_path, rendered)
    print(f"Installed Codex Custom profile: {PROFILE_NAME}")
    if configure_thread_bridge:
        print(f"Configured MCP server approval mode and created-task defaults: {BRIDGE_SERVER_TABLE}")
    if configure_app_defaults:
        print(f"Configured native app default approval modes: {APP_DEFAULT_TABLE}")
    if approve_codex_app_tools_enabled:
        print(f"Approved Codex App MCP tools without prompts: {CODEX_APP_SERVER_TABLE}")
    if backup is not None:
        print(f"Rollback: {Path(__file__).name} --rollback {backup}")
    else:
        print(f"Rollback: remove newly created {config_path}")
    return 0


def rollback(config_path: Path, source: Path) -> int:
    if not source.is_file():
        raise FileNotFoundError(source)
    backup = backup_path(config_path)
    if config_path.exists():
        shutil.copy2(config_path, backup)
        print(f"Current config backup: {backup}")
    shutil.copy2(source, config_path)
    print(f"Restored Codex config from: {source}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--configure-thread-bridge",
        action="store_true",
        help=f"patch [{BRIDGE_SERVER_TABLE}] approval mode and created-task defaults",
    )
    parser.add_argument(
        "--configure-app-defaults",
        action="store_true",
        help=f"patch [{APP_DEFAULT_TABLE}] only",
    )
    parser.add_argument(
        "--approve-codex-app-tools",
        action="store_true",
        help="approve the bundled Codex App MCP tools that otherwise prompt",
    )
    parser.add_argument("--rollback", type=Path)
    args = parser.parse_args()
    config_path = Path(args.codex_home).expanduser() / "config.toml"
    try:
        if args.rollback:
            return rollback(config_path, args.rollback.expanduser())
        return install(
            config_path,
            dry_run=args.dry_run,
            configure_thread_bridge=args.configure_thread_bridge,
            configure_app_defaults=args.configure_app_defaults,
            approve_codex_app_tools_enabled=args.approve_codex_app_tools,
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
