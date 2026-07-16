#!/usr/bin/env python3
"""Install the agents-owned Codex Custom permission profile without clobbering user config."""

from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
PROFILE_PATH = REPO_DIR / "config" / "codex-permissions.toml"
PROFILE_NAME = "agentic-local"
PROFILE_ROOT_KEYS = {
    "default_permissions",
    "approval_policy",
    "approvals_reviewer",
}
TABLE_RE = re.compile(r"^\s*\[\[?([^\]]+)\]\]?\s*(?:#.*)?$")
ROOT_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*=")


def table_name(line: str) -> str | None:
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
    current_table: str | None = None
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


def render_config(existing: str) -> str:
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
    rendered = "\n".join(
        root_lines
        + [""]
        + lines
        + ["", body.rstrip(), ""]
    )
    validate_config(rendered)
    return rendered


def validate_config(text: str) -> None:
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


def install(config_path: Path, *, dry_run: bool) -> int:
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    rendered = render_config(existing)
    if rendered == existing:
        print(f"Codex Custom profile already installed: {PROFILE_NAME}")
        return 0
    if dry_run:
        changed = list(
            difflib.unified_diff(existing.splitlines(), rendered.splitlines(), lineterm="")
        )
        print(f"Dry run: would update {config_path} ({len(changed)} diff lines; content omitted)")
        return 0
    config_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    backup: Path | None = None
    if config_path.exists():
        backup = backup_path(config_path)
        shutil.copy2(config_path, backup)
        print(f"Backup: {backup}")
    write_atomic(config_path, rendered)
    print(f"Installed Codex Custom profile: {PROFILE_NAME}")
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
    parser.add_argument("--rollback", type=Path)
    args = parser.parse_args()
    config_path = Path(args.codex_home).expanduser() / "config.toml"
    try:
        if args.rollback:
            return rollback(config_path, args.rollback.expanduser())
        return install(config_path, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
