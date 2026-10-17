#!/usr/bin/env python3
"""Install the optional Linux Pi permission extension and retire historical account outputs explicitly."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from urllib.parse import unquote, urlsplit

if sys.platform == "linux":
    import fcntl

REPO = Path(__file__).resolve().parents[1]
OWNER = "agents-pi-setup-v1"


def resolve_install_path(value):
    raw = str(value)
    if raw == "~":
        raw = str(Path.home())
    elif raw.startswith("~/"):
        raw = str(Path.home()) + raw[1:]
    elif raw.startswith("file://"):
        if re.search(r"[\x00-\x20]$", raw):
            raise ValueError("file URI trailing whitespace/control characters must be percent-encoded")
        parsed = urlsplit(raw)
        if parsed.netloc.lower() not in {"", "localhost"} or "\\" in raw or re.search(r"%(?![0-9a-fA-F]{2})|%2f", parsed.path, re.IGNORECASE):
            raise ValueError("unsupported file URI; use a local absolute path or file:/// URI without encoded slashes")
        raw = unquote(parsed.path or "/", errors="strict")
    if "\0" in raw:
        raise ValueError("installation paths cannot contain null bytes")
    return Path(os.path.abspath(raw))


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def snapshot(path):
    if path.is_symlink():
        raise ValueError(f"symlink destination: {path}")
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"non-file destination: {path}")
    return {"data": base64.b64encode(path.read_bytes()).decode(), "mode": stat.S_IMODE(path.stat().st_mode)}


def signature(value):
    if value is None:
        return None
    return {"sha256": hashlib.sha256(base64.b64decode(value["data"])).hexdigest(), "mode": value["mode"]}


def content(data, mode=0o644):
    return {"data": base64.b64encode(data).decode(), "mode": mode}


def atomic_write(path, value):
    if value is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".pi-setup-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), value["mode"])
            stream.write(base64.b64decode(value["data"], validate=True))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)



class Setup:
    def __init__(self, home, agent_dir):
        self.home = home
        self.agent = agent_dir
        self.state = agent_dir / ".agents-pi-setup.json"
        self.journal = agent_dir / ".agents-pi-setup-journal.json"
        self.extension = str(home / ".local/lib/pi-agentic-local/permissions")

    def target(self, key, *, check_path=True):
        fixed = {"wrapper": self.home / ".local/bin/pi-accounts", "service": self.home / ".config/systemd/user/pi-accounts-refresh.service", "timer": self.home / ".config/systemd/user/pi-accounts-refresh.timer", "settings": self.agent / "settings.json", "state": self.state}
        if key in fixed:
            result = fixed[key]
        elif key in {"auth/accounts.mjs", "auth/cli.mjs", "auth/pi-sdk.mjs"}:
            result = self.home / ".local/lib/pi-accounts" / key[5:]
        elif key in {"permissions/index.ts", "permissions/policy.mjs", "permissions/profile.json", "permissions/child-inheritance.mjs"}:
            result = Path(self.extension) / key[12:]
        else:
            raise ValueError("invalid setup-owned target")
        if check_path:
            for parent in (result, *result.parents):
                if parent.is_symlink():
                    raise ValueError(f"symlink destination: {parent}")
        return result

    def desired(self):
        result = {}
        for name in ("index.ts", "policy.mjs", "profile.json", "child-inheritance.mjs"):
            result["permissions/" + name] = content((REPO / "pi/permissions" / name).read_bytes())
        return result

    def read_state(self):
        raw = snapshot(self.target("state"))
        if raw is None:
            return {"owner": OWNER, "home": str(self.home), "files": {}, "extension": False}
        state = json.loads(base64.b64decode(raw["data"]))
        if not isinstance(state, dict) or set(state) != {"owner", "home", "files", "extension"} or state["owner"] != OWNER or state["home"] != str(self.home) or not isinstance(state["files"], dict) or type(state["extension"]) is not bool:
            raise ValueError("invalid Pi setup state")
        for key, sig in state["files"].items():
            if key in {"settings", "state"}:
                raise ValueError("invalid owned file record")
            # Retained legacy outputs are metadata until explicit retirement.
            self.target(key, check_path=False)
            if not isinstance(sig, dict) or set(sig) != {"sha256", "mode"} or not re.fullmatch("[a-f0-9]{64}", str(sig["sha256"])) or type(sig["mode"]) is not int or not 0 <= sig["mode"] <= 0o777:
                raise ValueError("invalid owned file signature")
        return state

    def recover(self, dry_run):
        raw = snapshot(self.journal)
        if raw is None:
            return
        journal = json.loads(base64.b64decode(raw["data"]))
        if not isinstance(journal, dict) or set(journal) != {"owner", "home", "changes"} or journal["owner"] != OWNER or journal["home"] != str(self.home) or not isinstance(journal["changes"], dict):
            raise ValueError("invalid Pi setup recovery journal")
        for key, pair in journal["changes"].items():
            path = self.target(key)
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError("invalid recovery record")
            for value in pair:
                if value is not None:
                    if not isinstance(value, dict) or set(value) != {"data", "mode"} or type(value["mode"]) is not int or not 0 <= value["mode"] <= 0o777:
                        raise ValueError("invalid recovery snapshot")
                    base64.b64decode(value["data"], validate=True)
            if snapshot(path) not in pair:
                raise ValueError(f"recovery conflict: {path}; preserve journal for operator review")
        if dry_run:
            raise ValueError("interrupted install; rerun without --dry-run to roll back before planning")
        for key, pair in reversed(list(journal["changes"].items())):
            atomic_write(self.target(key), pair[0])
        self.journal.unlink()
        print("Recovered interrupted Pi setup transaction")

    def plan(self, uninstall=False, retire_accounts=False):
        state = self.read_state()
        desired = {} if uninstall else self.desired()
        changes = {}
        legacy = {key for key in state["files"] if key.startswith("auth/") or key in {"wrapper", "service", "timer"}}
        retained = legacy if not retire_accounts else set()
        files = {key: state["files"][key] for key in retained}
        for key in sorted((set(state["files"]) | set(desired)) - retained):
            path = self.target(key)
            old = snapshot(path)
            recorded = state["files"].get(key)
            if old is not None and (recorded is None or signature(old) != recorded):
                raise ValueError(f"modified or unmanaged destination: {path}")
            new = desired.get(key)
            if old != new:
                changes[key] = [old, new]
            if new is not None:
                files[key] = signature(new)
        old = snapshot(self.target("settings"))
        settings = {} if old is None else json.loads(base64.b64decode(old["data"]))
        if not isinstance(settings, dict):
            raise ValueError("Pi settings must be a JSON object")
        extensions = settings.get("extensions", [])
        if not isinstance(extensions, list):
            raise ValueError("Pi settings.extensions must be an array")
        count = extensions.count(self.extension)
        if count > 1 or (count and not state["extension"]):
            raise ValueError("unmanaged or duplicate Pi permission extension entry")
        if not uninstall and state["extension"] and not count:
            raise ValueError("managed Pi extension entry removed; resolve settings before reinstall")
        changed = False
        if uninstall and state["extension"] and count:
            extensions.remove(self.extension)
            changed = True
        if not uninstall and not count:
            extensions.append(self.extension)
            changed = True
        if changed:
            settings["extensions"] = extensions
            changes["settings"] = [old, content(encoded(settings), old["mode"] if old else 0o600)]
        new_state = None if uninstall and not files else content(encoded({"owner": OWNER, "home": str(self.home), "files": files, "extension": not uninstall}), 0o600)
        old_state = snapshot(self.target("state"))
        if old_state != new_state:
            changes["state"] = [old_state, new_state]
        return changes

    def apply(self, changes):
        if not changes:
            return
        atomic_write(self.journal, content(encoded({"owner": OWNER, "home": str(self.home), "changes": changes}), 0o600))
        try:
            for key, pair in changes.items():
                if snapshot(self.target(key)) != pair[0]:
                    raise ValueError(f"destination changed during install: {self.target(key)}")
                atomic_write(self.target(key), pair[1])
        except BaseException:
            self.recover(False)
            raise
        self.journal.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(Path.home()), help="task home; use a scratch directory for tests")
    parser.add_argument("--agent-dir", help="Pi agent directory (default PI_CODING_AGENT_DIR or task home/.pi/agent)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--retire-accounts", action="store_true", help="remove only unchanged historical Agents-owned account CLI and maintenance files")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("this optional installer supports Linux only")
    try:
        home = resolve_install_path(args.home)
        agent = resolve_install_path(args.agent_dir or os.environ.get("PI_CODING_AGENT_DIR") or str(home / ".pi/agent"))
    except ValueError as exc:
        parser.error(str(exc))
    setup = Setup(home, agent)
    try:
        # Lock the home directory itself: no persistent lock file or dry-run writes.
        if not args.dry_run:
            home.mkdir(parents=True, exist_ok=True)
        lock = None
        try:
            if home.exists():
                lock = os.open(home, os.O_RDONLY | os.O_DIRECTORY)
                fcntl.flock(lock, fcntl.LOCK_EX)
            setup.target("state")
            setup.recover(args.dry_run)
            changes = setup.plan(args.uninstall, args.retire_accounts)
            for key, pair in changes.items():
                print(("remove " if pair[1] is None else "write ") + str(setup.target(key)))
            if not args.dry_run:
                setup.apply(changes)
            print("Pi setup preview complete" if args.dry_run else "Pi permission setup complete; external account tooling is unchanged unless explicitly retired")
        finally:
            if lock is not None:
                os.close(lock)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Pi setup failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
