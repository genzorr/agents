#!/usr/bin/env python3
"""Detach explicitly identified provisional Codex links before Pi asset installation."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

# Reuse the catalog engine's path guards and atomic writer; this is a finite migration,
# not another asset installer.
SPEC = importlib.util.spec_from_file_location("pi_asset_engine", Path(__file__).with_name("install-assets.py"))
ENGINE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ENGINE
SPEC.loader.exec_module(ENGINE)

RECORD = ".agents-pi-migration.json"
OWNER = "agents-pi-migration"
LINKS = {"AGENTS.md": "AGENTS.md", "docs": "docs"}


def link_value(path):
    if path.is_symlink():
        return os.readlink(path)
    if path.exists():
        raise ValueError(f"migration conflict: {path} is not the expected provisional symlink")
    return None


def expected_link(home, name, raw, codex):
    return os.path.abspath(os.path.join(home, raw)) == str(codex / LINKS[name])


def settings_value(home):
    path = ENGINE.validate_home_target(home, "settings.json", reject_leaf_symlink=True)
    if not path.exists():
        return None, None, None
    raw = path.read_bytes()
    value = json.loads(raw)
    if not isinstance(value, dict) or ("skills" in value and not isinstance(value["skills"], list)):
        raise ValueError("migration requires object settings with an optional skills array")
    return raw, value, stat.S_IMODE(path.stat().st_mode)


def load_record(home, codex):
    path = ENGINE.validate_home_target(home, RECORD, reject_leaf_symlink=True)
    if not path.exists():
        return None
    value = json.loads(path.read_text())
    keys = {"owner", "schema_version", "pi_home", "codex_home", "links", "skill_index", "stage"}
    if not isinstance(value, dict) or set(value) != keys or value["owner"] != OWNER or value["schema_version"] != 1 or value["pi_home"] != str(home) or value["codex_home"] != str(codex) or value["stage"] not in {"prepared", "complete"}:
        raise ValueError("invalid or mismatched Pi migration record")
    if not isinstance(value["links"], dict) or not set(value["links"]).issubset(LINKS):
        raise ValueError("invalid migration link records")
    for name, raw in value["links"].items():
        if not isinstance(raw, str) or not expected_link(home, name, raw, codex):
            raise ValueError("migration record contains a foreign link")
    index = value["skill_index"]
    if index is not None and (type(index) is not int or index < 0):
        raise ValueError("invalid migration skills record")
    return value


def save_record(home, record):
    path = ENGINE.validate_home_target(home, RECORD, reject_leaf_symlink=True)
    ENGINE.atomic_write(path, ENGINE.pretty_json(record).encode(), 0o600)


def migration_plan(home, codex):
    state = ENGINE.validate_home_target(home, ENGINE.STATE_FILE, reject_leaf_symlink=True)
    if state.exists():
        raise ValueError("Pi asset ownership state already exists; use its installer before migration")
    links = {}
    for name in LINKS:
        raw = link_value(ENGINE.validate_home_target(home, name))
        if raw is not None:
            if not expected_link(home, name, raw, codex):
                raise ValueError(f"migration conflict: unexpected {name} symlink target")
            links[name] = raw
    before, settings, mode = settings_value(home)
    skills = settings.get("skills", []) if settings is not None else []
    expected = str(codex / "skills")
    if skills.count(expected) > 1:
        raise ValueError("migration conflict: duplicate provisional Codex skills entries")
    index = skills.index(expected) if expected in skills else None
    after = None
    if index is not None:
        skills.pop(index)
        after = ENGINE.pretty_json(settings).encode()
    record = {"owner": OWNER, "schema_version": 1, "pi_home": str(home), "codex_home": str(codex), "links": links, "skill_index": index, "stage": "prepared"}
    return record, before, after, mode


def rollback(home, codex, record, dry_run):
    restore = []
    for name, original in record["links"].items():
        current = link_value(ENGINE.validate_home_target(home, name))
        if current is not None and current != original:
            raise ValueError(f"rollback conflict: {name} changed; preserve migration record")
        if current is None:
            restore.append((name, original))
    before, settings, mode = settings_value(home)
    after = None
    if record["skill_index"] is not None:
        if settings is None or "skills" not in settings:
            raise ValueError("rollback conflict: settings.skills was removed; preserve migration record")
        skills = settings["skills"]
        expected = str(codex / "skills")
        if skills.count(expected) > 1:
            raise ValueError("rollback conflict: duplicate Codex skills entries")
        if expected not in skills:
            skills.insert(min(record["skill_index"], len(skills)), expected)
            after = ENGINE.pretty_json(settings).encode()
    for name, _ in restore:
        print(f"{'would restore' if dry_run else 'restore'} provisional {name} symlink")
    if after is not None:
        print(f"{'would restore' if dry_run else 'restore'} exact Codex skills entry")
    if dry_run:
        return
    if after is not None:
        if settings_value(home)[0] != before:
            raise ValueError("rollback conflict: settings changed during rollback")
        ENGINE.atomic_write(home / "settings.json", after, mode)
    for name, raw in restore:
        # symlink() fails rather than replacing a concurrently created destination.
        os.symlink(raw, ENGINE.validate_home_target(home, name))
    ENGINE.validate_home_target(home, RECORD, reject_leaf_symlink=True).unlink()


def migrate(home, codex, dry_run=False, undo=False):
    record = load_record(home, codex)
    if undo:
        if record is not None:
            rollback(home, codex, record, dry_run)
        return
    if record is not None:
        if record["stage"] == "prepared":
            raise ValueError("interrupted migration; run --rollback, then preview and retry")
        print("Provisional Pi migration already recorded; no changes")
        return
    record, before, after, mode = migration_plan(home, codex)
    if not record["links"] and after is None:
        print("No matching provisional Pi links or Codex skills entry")
        return
    for name in record["links"]:
        print(f"{'would detach' if dry_run else 'detach'} provisional {name} symlink")
    if after is not None:
        print(f"{'would remove' if dry_run else 'remove'} exact Codex skills entry")
    if dry_run:
        return
    save_record(home, record)
    try:
        for name, raw in record["links"].items():
            path = ENGINE.validate_home_target(home, name)
            if link_value(path) != raw:
                raise ValueError(f"migration conflict: {name} changed during migration")
            path.unlink()
        if after is not None:
            if settings_value(home)[0] != before:
                raise ValueError("migration conflict: settings changed during migration")
            ENGINE.atomic_write(home / "settings.json", after, mode)
        record["stage"] = "complete"
        save_record(home, record)
    except (OSError, ValueError):
        # The prepared record remains sufficient for an explicit narrow rollback.
        raise ValueError("migration interrupted; preserve its record and run --rollback before retrying") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pi-home", required=True)
    parser.add_argument("--codex-home", required=True, help="explicit expected provisional-link destination; never read")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("this provisional Pi migration is qualified for Linux only")
    try:
        home = ENGINE.resolve_pi_home(args.pi_home)
        codex = ENGINE.resolve_pi_home(args.codex_home)
        if home == codex:
            raise ValueError("Pi and expected Codex homes must differ")
        migrate(home, codex, args.dry_run, args.rollback)
    except (ENGINE.CatalogError, OSError, ValueError) as exc:
        print(f"Pi migration failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
