#!/usr/bin/env python3
"""Install one platform's Agents assets from the catalog."""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import shlex
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from agent_catalog import Asset, CatalogError, DesiredFile, SourceLayer, desired_files, load_catalog, validate_asset_target, validate_catalog

STATE_FILE = ".agents-install-state.json"
LEGACY_DOC_MANIFEST = ".agents-doc-manifest"
STATE_SCHEMA_VERSION = 2
ADAPTER_KIND = "claude_settings_hooks"
STATE_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
STATE_MODE_RE = re.compile(r"^[0-7]{4}$")
SHELL_CONTROL_RE = re.compile(r"[;&|<>`$\\\\\r\n]")


@dataclass(frozen=True)
class FileAction:
    kind: str
    target: str
    desired: DesiredFile | None = None


@dataclass(frozen=True)
class AdapterAction:
    description: str
    path: Path
    target: str
    before: str
    after: str
    mode: int


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_signature(path: Path) -> tuple[str, int]:
    return digest_bytes(path.read_bytes()), stat.S_IMODE(path.stat().st_mode)


def state_signature(record: dict[str, Any]) -> tuple[str, int]:
    mode = record.get("mode")
    digest = record.get("sha256")
    if not isinstance(mode, str) or not STATE_MODE_RE.fullmatch(mode) or not isinstance(digest, str) or not STATE_DIGEST_RE.fullmatch(digest):
        raise ValueError("invalid state file signature")
    return digest, int(mode, 8)


def state_record(desired: DesiredFile) -> dict[str, Any]:
    digest, mode = file_signature(desired.source)
    return {
        "owner": "agents",
        "asset_id": desired.asset.id,
        "kind": desired.asset.kind,
        "sha256": digest,
        "mode": format(mode, "04o"),
        "baseline_known": True,
    }


def empty_state(platform: str) -> dict[str, Any]:
    return {"schema_version": STATE_SCHEMA_VERSION, "owner": "agents", "platform": platform, "files": {}, "adapters": {}}


def validate_home_target(home: Path, target: str, *, reject_leaf_symlink: bool = False) -> Path:
    """Reject symlinked or non-directory home ancestors before any access."""
    relative = PurePosixPath(target)
    if relative.is_absolute() or "\\" in target or any(part in {"", ".", ".."} for part in relative.parts):
        raise CatalogError(f"unsafe home-relative path: {target}")
    if home.is_symlink() or (home.exists() and not home.is_dir()):
        raise CatalogError(f"selected home is not a real directory: {home}")
    current = home
    parts = relative.parts
    for index, part in enumerate(parts):
        current /= part
        is_leaf = index == len(parts) - 1
        if current.is_symlink() and (not is_leaf or reject_leaf_symlink):
            raise CatalogError(f"home path contains a symlink: {current}")
        if not is_leaf and current.exists() and not current.is_dir():
            raise CatalogError(f"home path ancestor is not a directory: {current}")
    return home / relative.as_posix()


def _validate_file_record(platform: str, target: str, record: object, desired: dict[str, DesiredFile] | None) -> None:
    if not isinstance(record, dict):
        raise CatalogError(f"invalid state record for {target}")
    required = {"owner", "asset_id", "kind", "sha256", "mode", "baseline_known"}
    if not required.issubset(record):
        raise CatalogError(f"invalid state record for {target}: missing required field")
    if record["owner"] != "agents":
        raise CatalogError(f"invalid state record for {target}: foreign owner")
    validate_asset_target(platform, record["asset_id"], record["kind"], target, f"state record {target}", allow_legacy_document=True)
    if not isinstance(record["baseline_known"], bool):
        raise CatalogError(f"invalid state record for {target}: baseline_known must be boolean")
    state_signature(record)
    if desired is not None and target in desired:
        item = desired[target]
        if record["asset_id"] != item.asset.id or record["kind"] != item.asset.kind:
            raise CatalogError(f"invalid state record for {target}: asset identity does not match catalog")


def is_supported_hook_command(command: str, script_path: str) -> bool:
    """Accept only the documented direct hook invocation form."""
    if command == script_path:
        return True
    prefix = script_path + ' "'
    if not command.startswith(prefix) or not command.endswith('"'):
        return False
    argument = command[len(prefix) : -1]
    return bool(argument) and '"' not in argument and SHELL_CONTROL_RE.search(argument) is None


def rendered_hook_script_path(home: Path, script_target: str) -> str:
    validate_home_target(home, script_target, reject_leaf_symlink=True)
    return f"{shlex.quote(str(home))}/{script_target}"


def hook_leaves(value: Any, path: tuple[str | int, ...] = ()) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        if isinstance(value.get("command"), str):
            return [{"path": list(path), "leaf": copy.deepcopy(value)}]
        result: list[dict[str, Any]] = []
        for key, child in value.items():
            result.extend(hook_leaves(child, (*path, key)))
        return result
    if isinstance(value, list):
        result: list[dict[str, Any]] = []
        for index, child in enumerate(value):
            result.extend(hook_leaves(child, (*path, index)))
        return result
    return []


def leaf_identity(leaf: dict[str, Any]) -> str:
    return json.dumps(leaf, sort_keys=True, separators=(",", ":"))


def leaf_at(value: Any, path: list[object]) -> Any:
    current = value
    for part in path:
        if isinstance(part, str) and isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(part, int) and not isinstance(part, bool) and isinstance(current, list) and 0 <= part < len(current):
            current = current[part]
        else:
            return None
    return current


def validate_managed_leaves(asset_id: str, leaves: object, script_path: str) -> list[dict[str, Any]]:
    if not isinstance(leaves, list):
        raise CatalogError(f"invalid adapter state for {asset_id}: managed_leaves must be a list")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for identity in leaves:
        if not isinstance(identity, dict) or set(identity) != {"path", "leaf"} or not isinstance(identity["path"], list) or not isinstance(identity["leaf"], dict):
            raise CatalogError(f"invalid adapter state for {asset_id}: managed_leaves must contain structural identities")
        path = identity["path"]
        if not path or any(not isinstance(part, (str, int)) or isinstance(part, bool) for part in path):
            raise CatalogError(f"invalid adapter state for {asset_id}: managed_leaves path is invalid")
        leaf = identity["leaf"]
        command = leaf.get("command")
        if not isinstance(command, str) or not is_supported_hook_command(command, script_path):
            raise CatalogError(f"invalid adapter state for {asset_id}: managed_leaves must contain supported hook invocations")
        key = leaf_identity(identity)
        if key in seen:
            raise CatalogError(f"invalid adapter state for {asset_id}: duplicate managed leaf identity")
        seen.add(key)
        normalized.append({"path": path, "leaf": copy.deepcopy(leaf)})
    return normalized


def remove_managed_leaves(value: Any, leaves: list[dict[str, Any]]) -> tuple[Any, bool]:
    for identity in leaves:
        if leaf_at(value, identity["path"]) != identity["leaf"]:
            return value, False
    targets = {tuple(identity["path"]): identity["leaf"] for identity in leaves}

    def remove(current: Any, path: tuple[str | int, ...]) -> Any:
        if path in targets:
            return None
        if isinstance(current, dict):
            result: dict[str, Any] = {}
            for key, child in current.items():
                cleaned = remove(child, (*path, key))
                if cleaned is not None or key != "hooks":
                    if cleaned is not None:
                        result[key] = cleaned
            return result or None
        if isinstance(current, list):
            result = [cleaned for index, child in enumerate(current) if (cleaned := remove(child, (*path, index))) is not None]
            return result or None
        return current

    return remove(value, ()), True


def newly_managed_leaves(before: Any, after: Any) -> list[dict[str, Any]]:
    prior = {leaf_identity(identity) for identity in hook_leaves(before)}
    return [identity for identity in hook_leaves(after) if leaf_identity(identity) not in prior]


def adoptable_desired_leaves(current: Any, desired: Any) -> tuple[list[dict[str, Any]], str | None]:
    """Return exact preexisting desired leaves only when each has one stable location."""
    current_leaves = hook_leaves(current)
    adopted: list[dict[str, Any]] = []
    for desired_identity in hook_leaves(desired):
        matches = [identity for identity in current_leaves if identity["leaf"] == desired_identity["leaf"]]
        if not matches:
            continue
        if len(matches) != 1 or matches[0]["path"] != desired_identity["path"]:
            return [], "unresolved settings.json hook adapter: desired hook leaf is ambiguous or not at its expected path; preserved"
        adopted.append(copy.deepcopy(desired_identity))
    return adopted, None


def _validate_adapter_record(home: Path, asset_id: str, record: object) -> None:
    if not isinstance(record, dict):
        raise CatalogError(f"invalid adapter state for {asset_id}")
    required = {"owner", "asset_id", "kind", "platform", "target", "script_target", "managed_leaves"}
    if not required.issubset(record):
        raise CatalogError(f"invalid adapter state for {asset_id}: missing required field")
    if record["owner"] != "agents" or record["asset_id"] != asset_id or record["kind"] != ADAPTER_KIND or record["platform"] != "claude" or record["target"] != "settings.json":
        raise CatalogError(f"invalid adapter state for {asset_id}: foreign or inconsistent identity")
    script_target = record["script_target"]
    validate_asset_target("claude", asset_id, "hook", script_target, f"adapter state {asset_id}")
    validate_managed_leaves(asset_id, record["managed_leaves"], rendered_hook_script_path(home, script_target))


def load_state(
    home: Path,
    platform: str,
    desired: dict[str, DesiredFile] | None = None,
) -> tuple[dict[str, Any], bool]:
    path = validate_home_target(home, STATE_FILE, reject_leaf_symlink=True)
    if not path.exists():
        return empty_state(platform), False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError(f"invalid {STATE_FILE}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != STATE_SCHEMA_VERSION or data.get("owner") != "agents" or data.get("platform") != platform or not isinstance(data.get("files"), dict):
        raise CatalogError(f"incompatible {STATE_FILE}: expected schema {STATE_SCHEMA_VERSION} for {platform}")
    if "adapters" not in data:
        data["adapters"] = {}
    if not isinstance(data["adapters"], dict):
        raise CatalogError(f"invalid {STATE_FILE}: adapters must be an object")
    expected_targets: dict[str, set[str]] = {}
    expected_kinds: dict[str, str] = {}
    if desired is not None:
        for target, item in desired.items():
            expected_targets.setdefault(item.asset.id, set()).add(target)
            expected_kinds[item.asset.id] = item.asset.kind
    for asset_id, record in data["adapters"].items():
        _validate_adapter_record(home, asset_id, record)
    for target, record in data["files"].items():
        if not isinstance(target, str) or not target or "\\" in target or Path(target).is_absolute() or ".." in PurePosixPath(target).parts or not isinstance(record, dict):
            raise CatalogError(f"invalid state entry: {target!r}")
        validate_home_target(home, target)
        try:
            _validate_file_record(platform, target, record, desired)
        except (TypeError, ValueError) as exc:
            raise CatalogError(f"invalid state signature for {target}: {exc}") from exc
        if record["kind"] == "hook":
            catalog_match = (
                record["asset_id"] in expected_targets
                and expected_kinds[record["asset_id"]] == "hook"
                and target in expected_targets[record["asset_id"]]
            )
            adapter = data["adapters"].get(record["asset_id"])
            history_match = isinstance(adapter, dict) and adapter.get("script_target") == target
            if not catalog_match and not history_match:
                raise CatalogError(f"invalid state record for {target}: hook target is not bound to catalog or adapter history")
    return data, True


def read_legacy_manifest(home: Path) -> list[str]:
    path = validate_home_target(home, LEGACY_DOC_MANIFEST, reject_leaf_symlink=True)
    if not path.is_file():
        return []
    result: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        target = raw.strip()
        if not target:
            continue
        parts = PurePosixPath(target).parts
        if PurePosixPath(target).is_absolute() or ".." in parts or not target.startswith("docs/"):
            raise CatalogError(f"invalid legacy document manifest path: {target}")
        result.append(PurePosixPath(target).as_posix())
    return sorted(set(result))


def migrate_legacy_entries(repo: Path, home: Path, state: dict[str, Any], desired: dict[str, DesiredFile]) -> None:
    for target in read_legacy_manifest(home):
        if target in state["files"]:
            continue
        validate_home_target(home, target)
        destination = home / target
        if destination.is_symlink() or not destination.is_file():
            continue
        digest, mode = file_signature(destination)
        owner = desired.get(target)
        source = owner.source if owner is not None else repo / target
        baseline_known = source.is_file() and file_signature(source) == (digest, mode)
        state["files"][target] = {
            "owner": "agents",
            "asset_id": owner.asset.id if owner else f"legacy-document:{target}",
            "kind": owner.asset.kind if owner else "traveling_document",
            "sha256": digest,
            "mode": format(mode, "04o"),
            "baseline_known": baseline_known,
        }


def is_codex_managed_global(path: Path) -> bool:
    if not path.exists() or path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
        return True
    first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
    return first == ["# Global Codex Instructions"]


def source_text(layer: SourceLayer, repo: Path) -> str:
    return (repo / layer.path).read_text(encoding="utf-8")


def hook_asset(assets: tuple[Asset, ...], platform: str) -> tuple[Asset, SourceLayer, SourceLayer] | None:
    for asset in assets:
        if asset.handling.get(platform) != "claude_settings_hooks":
            continue
        layers = asset.sources[platform]
        script = next((layer for layer in layers if layer.target is not None), None)
        fragment = next((layer for layer in layers if layer.target is None and layer.role == "settings-hooks"), None)
        if script is None or fragment is None:
            raise CatalogError(f"{asset.id} ({platform}): settings hook adapter needs script and fragment layers")
        return asset, script, fragment
    return None


def merge_hook_values(existing: Any, desired: Any) -> Any:
    if existing is None or existing in ({}, []):
        return copy.deepcopy(desired)
    if isinstance(existing, dict) and isinstance(desired, dict):
        result = copy.deepcopy(existing)
        for key, value in desired.items():
            if key not in result:
                result[key] = copy.deepcopy(value)
            elif isinstance(result[key], (dict, list)) or isinstance(value, (dict, list)):
                if type(result[key]) is not type(value):
                    raise CatalogError("unresolved settings.json hook adapter: incompatible nonempty hook types")
                result[key] = merge_hook_values(result[key], value)
            else:
                result[key] = copy.deepcopy(value)
        return result
    if isinstance(existing, list) and isinstance(desired, list):
        result = copy.deepcopy(existing)
        result.extend(copy.deepcopy(value) for value in desired if value not in result)
        return result
    raise CatalogError("unresolved settings.json hook adapter: incompatible nonempty hook types")


def rendered_hook_fragment(repo: Path, layer: SourceLayer, home: Path) -> dict[str, Any]:
    text = source_text(layer, repo).replace("__CLAUDE_HOME__", shlex.quote(str(home)))
    value = json.loads(text)
    if not isinstance(value, dict) or not isinstance(value.get("hooks"), (dict, list)):
        raise CatalogError("Claude hook fragment must contain a hooks object or array")
    return value


def creation_mode() -> int:
    """Return the mode a normal shell-created file receives under this umask."""
    current_umask = os.umask(0)
    os.umask(current_umask)
    return 0o666 & ~current_umask


def pretty_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def plan_claude_hooks(
    repo: Path,
    home: Path,
    assets: tuple[Asset, ...],
    state: dict[str, Any],
    *,
    prune: bool,
    uninstall: bool,
) -> tuple[AdapterAction | None, str | None, dict[str, dict[str, Any] | None]]:
    configured = hook_asset(assets, "claude")
    histories = {
        asset_id: record
        for asset_id, record in state.get("adapters", {}).items()
        if isinstance(record, dict) and record.get("kind") == ADAPTER_KIND and record.get("target") == "settings.json"
    }
    if configured is not None:
        asset, script, fragment = configured
        asset_id = asset.id
        script_target = script.target
        if script_target is None:
            raise CatalogError(f"{asset_id}: settings hook adapter has no script target")
        desired_hooks = rendered_hook_fragment(repo, fragment, home)["hooks"]
    else:
        asset_id = None
        script_target = None
        desired_hooks = None

    if configured is None and not histories:
        return None, None, {}
    if uninstall and not histories:
        return None, None, {}
    if not configured and not (prune or uninstall):
        return None, None, {}
    active_histories = histories if (prune or uninstall) else ({asset_id: histories[asset_id]} if asset_id in histories else {})

    destination = validate_home_target(home, "settings.json", reject_leaf_symlink=True)
    if not destination.exists():
        if uninstall:
            return None, None, {history_id: None for history_id in active_histories}
        settings: dict[str, Any] = {}
        before = ""
    else:
        try:
            before = destination.read_text(encoding="utf-8")
            settings = json.loads(before)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            return None, f"unresolved settings.json hook adapter: invalid JSON ({exc})", {}
        if not isinstance(settings, dict):
            return None, "unresolved settings.json hook adapter: settings root is not an object", {}
    current_hooks = settings.get("hooks")
    if current_hooks not in (None, {}, []) and not isinstance(current_hooks, (dict, list)):
        return None, "unresolved settings.json hook adapter: hooks value is not an object or array", {}
    historical_leaves = [leaf for history in active_histories.values() for leaf in history["managed_leaves"]]
    cleaned_hooks, matched = remove_managed_leaves(current_hooks, historical_leaves)
    if not matched:
        return None, "unresolved settings.json hook adapter: recorded hook leaves were modified or moved; preserved", {}
    if uninstall or (prune and configured is None):
        if "hooks" not in settings:
            return None, None, {history_id: None for history_id in active_histories}
        updated_hooks = cleaned_hooks
        updated = dict(settings)
        if updated_hooks is None:
            del updated["hooks"]
        else:
            updated["hooks"] = updated_hooks
        description = "remove Agents hooks from settings.json"
        history_updates = {history_id: None for history_id in active_histories}
    else:
        if configured is None or asset_id is None or script_target is None or desired_hooks is None:
            return None, "unresolved Claude hook adapter: catalog history has no current fragment", {}
        adopted_leaves: list[dict[str, Any]] = []
        if asset_id not in histories:
            adopted_leaves, adoption_error = adoptable_desired_leaves(cleaned_hooks, desired_hooks)
            if adoption_error:
                return None, adoption_error, {}
        updated_hooks = merge_hook_values(cleaned_hooks or {}, desired_hooks)
        updated = dict(settings)
        updated["hooks"] = updated_hooks
        description = "merge managed hooks into settings.json"
        history_updates = {history_id: None for history_id in active_histories if history_id != asset_id}
        history_updates[asset_id] = {
            "owner": "agents",
            "asset_id": asset_id,
            "kind": ADAPTER_KIND,
            "platform": "claude",
            "target": "settings.json",
            "script_target": script_target,
            "managed_leaves": adopted_leaves + newly_managed_leaves(cleaned_hooks, updated_hooks),
        }
    after = pretty_json(updated)
    if before == after:
        return None, None, history_updates
    mode = stat.S_IMODE(destination.stat().st_mode) if destination.exists() else creation_mode()
    return AdapterAction(description, destination, "settings.json", before, after, mode), None, history_updates


def display_diff(target: str, before: str, after: str) -> None:
    if not before:
        print(f"NEW  {target}")
    else:
        print(f"CHANGED  {target}")
    lines = difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile=target, tofile=target)
    print("".join(lines), end="")


def atomic_write(path: Path, content: bytes, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_state(path: Path, state: dict[str, Any]) -> None:
    atomic_write(path, pretty_json(state).encode("utf-8"))


def preflight_mutations(home: Path, actions: list[FileAction], adapters: list[AdapterAction]) -> None:
    """Recheck every mutation target immediately before applying the plan."""
    for action in actions:
        validate_home_target(home, action.target, reject_leaf_symlink=True)
    for adapter in adapters:
        validate_home_target(home, adapter.target, reject_leaf_symlink=True)


def remove_empty_parents(home: Path, target: Path) -> None:
    parent = target.parent
    home = home.resolve()
    while parent != home and parent != parent.parent:
        try:
            parent.rmdir()
        except OSError:
            break
        parent = parent.parent


def apply_file_action(home: Path, action: FileAction) -> None:
    destination = validate_home_target(home, action.target, reject_leaf_symlink=True)
    if action.kind == "remove":
        if destination.is_file():
            destination.unlink()
            remove_empty_parents(home, destination)
        return
    if action.desired is None:
        raise RuntimeError(f"missing desired source for {action.target}")
    source = action.desired.source
    atomic_write(destination, source.read_bytes(), action.desired.mode)


def report_file_action(home: Path, action: FileAction, show_diff: bool) -> None:
    destination = home / action.target
    if action.kind == "remove":
        print(f"  {'would remove' if show_diff else 'remove'}: {action.target}")
        return
    if action.desired is None:
        return
    before = destination.read_text(encoding="utf-8", errors="replace") if destination.is_file() else ""
    after = action.desired.source.read_text(encoding="utf-8", errors="replace")
    if show_diff and before != after:
        display_diff(action.target, before, after)
    verb = "would create" if action.kind == "create" else "would update"
    print(f"  {verb}: {action.target}")


def retain_hook_files_on_adapter_error(
    assets: tuple[Asset, ...],
    desired: dict[str, DesiredFile],
    state: dict[str, Any],
    next_state: dict[str, Any],
    actions: list[FileAction],
) -> None:
    """Keep hook scripts available while an unresolved settings adapter blocks cleanup."""
    targets: set[str] = set()
    configured = hook_asset(assets, "claude")
    if configured is not None:
        _asset, script, _fragment = configured
        targets.add(script.target)
    targets.update(
        record["script_target"]
        for record in state.get("adapters", {}).values()
        if isinstance(record, dict) and isinstance(record.get("script_target"), str)
    )
    for target in targets:
        if not any(action.target == target and action.kind == "remove" for action in actions):
            continue
        actions[:] = [action for action in actions if not (action.target == target and action.kind == "remove")]
        if target in state["files"]:
            next_state["files"][target] = state["files"][target]
        elif target in desired:
            next_state["files"][target] = state_record(desired[target])


def apply_adapter_updates(next_state: dict[str, Any], adapter_updates: dict[str, dict[str, Any] | None]) -> None:
    """Retain adapter ownership until its paired historical script is reconciled."""
    for asset_id, record in adapter_updates.items():
        if record is not None:
            next_state["adapters"][asset_id] = record
            continue
        existing = next_state["adapters"].get(asset_id)
        if isinstance(existing, dict) and existing.get("script_target") in next_state["files"]:
            existing["managed_leaves"] = []
            continue
        next_state["adapters"].pop(asset_id, None)


def plan_install(
    repo: Path,
    home: Path,
    platform: str,
    assets: tuple[Asset, ...],
    state: dict[str, Any],
    state_exists: bool,
    prune: bool,
) -> tuple[list[FileAction], list[AdapterAction], dict[str, Any], list[str]]:
    desired = desired_files(repo, assets, platform)
    if not state_exists:
        migrate_legacy_entries(repo, home, state, desired)
    next_state = json.loads(json.dumps(state))
    actions: list[FileAction] = []
    conflicts: list[str] = []
    for target in sorted(desired):
        item = desired[target]
        validate_home_target(home, target)
        destination = home / target
        record = state["files"].get(target)
        if not destination.exists():
            actions.append(FileAction("create", target, item))
            next_state["files"][target] = state_record(item)
            continue
        if destination.is_symlink():
            conflicts.append(f"{target}: symlink destination is unmanaged; preserved")
            continue
        current = file_signature(destination) if destination.is_file() else None
        desired_signature = file_signature(item.source)
        if current is None:
            conflicts.append(f"{target}: destination is not a regular file")
            continue
        if record is not None:
            try:
                recorded = state_signature(record)
            except ValueError as exc:
                conflicts.append(f"{target}: {exc}")
                continue
            if record.get("baseline_known", True) is False:
                if current != desired_signature:
                    conflicts.append(f"{target}: legacy manifest destination differs from source; preserved")
                    continue
                next_state["files"][target] = state_record(item)
                continue
            if current != recorded:
                if current == desired_signature:
                    next_state["files"][target] = state_record(item)
                    continue
                conflicts.append(f"{target}: recorded destination was modified; preserved")
                continue
            if current != desired_signature:
                actions.append(FileAction("update", target, item))
            next_state["files"][target] = state_record(item)
            continue
        if item.asset.kind == "global_instructions" and platform == "codex" and is_codex_managed_global(destination):
            if current != desired_signature:
                actions.append(FileAction("update", target, item))
                next_state["files"][target] = state_record(item)
        elif current == desired_signature:
            next_state["files"][target] = state_record(item)
        elif item.asset.kind == "global_instructions" and platform == "codex":
            conflicts.append(f"{target}: skipped unmanaged global file; preserved")
        else:
            conflicts.append(f"{target}: unmanaged destination differs from source; preserved")

    if prune:
        desired_targets = set(desired)
        for target in sorted(set(state["files"]) - desired_targets):
            validate_home_target(home, target)
            destination = home / target
            record = state["files"][target]
            if destination.is_symlink():
                conflicts.append(f"{target}: stale destination is a symlink; preserved")
                continue
            if not destination.exists():
                next_state["files"].pop(target, None)
                continue
            if not destination.is_file():
                conflicts.append(f"{target}: stale destination is not a regular file; preserved")
                continue
            if record.get("baseline_known", True) is False:
                conflicts.append(f"{target}: legacy destination lacks a trusted baseline; preserved")
                continue
            if file_signature(destination) == state_signature(record):
                actions.append(FileAction("remove", target))
                next_state["files"].pop(target, None)
            else:
                conflicts.append(f"{target}: modified stale destination; preserved")

    adapter_actions: list[AdapterAction] = []
    adapter, adapter_error, adapter_updates = plan_claude_hooks(repo, home, assets, state, prune=prune, uninstall=False) if platform == "claude" else (None, None, {})
    if adapter_error:
        conflicts.append(adapter_error)
        if prune:
            retain_hook_files_on_adapter_error(assets, desired, state, next_state, actions)
    if adapter is not None:
        adapter_actions.append(adapter)
    apply_adapter_updates(next_state, adapter_updates)
    return actions, adapter_actions, next_state, conflicts


def plan_uninstall(
    repo: Path,
    home: Path,
    platform: str,
    assets: tuple[Asset, ...],
    state: dict[str, Any],
    state_exists: bool,
) -> tuple[list[FileAction], list[AdapterAction], dict[str, Any], list[str]]:
    desired = desired_files(repo, assets, platform)
    if not state_exists:
        migrate_legacy_entries(repo, home, state, desired)
    next_state = json.loads(json.dumps(state))
    actions: list[FileAction] = []
    conflicts: list[str] = []
    for target in sorted(next_state["files"]):
        validate_home_target(home, target)
        destination = home / target
        record = next_state["files"][target]
        if destination.is_symlink():
            conflicts.append(f"{target}: recorded destination is a symlink; preserved")
            continue
        if not destination.exists():
            next_state["files"].pop(target, None)
            continue
        if not destination.is_file():
            conflicts.append(f"{target}: recorded destination is not a regular file; preserved")
            continue
        if record.get("baseline_known", True) is False:
            conflicts.append(f"{target}: legacy destination lacks a trusted baseline; preserved")
            continue
        current = file_signature(destination)
        if current == state_signature(record):
            actions.append(FileAction("remove", target))
            next_state["files"].pop(target, None)
        else:
            conflicts.append(f"{target}: modified recorded destination; preserved")
    adapter_actions: list[AdapterAction] = []
    adapter, adapter_error, adapter_updates = plan_claude_hooks(repo, home, assets, state, prune=True, uninstall=True) if platform == "claude" else (None, None, {})
    if adapter_error:
        conflicts.append(adapter_error)
        retain_hook_files_on_adapter_error(assets, desired, state, next_state, actions)
    if adapter is not None:
        adapter_actions.append(adapter)
    apply_adapter_updates(next_state, adapter_updates)
    return actions, adapter_actions, next_state, conflicts


def run(args: argparse.Namespace) -> int:
    repo = Path(__file__).resolve().parents[1]
    home_var = "CODEX_HOME" if args.platform == "codex" else "CLAUDE_HOME"
    home = Path(os.environ.get(home_var, str(Path.home() / f".{args.platform}"))).expanduser().absolute()
    errors, warnings = validate_catalog(repo)
    if errors:
        for error in errors:
            print(f"FAIL  {error}", file=os.sys.stderr)
        return 1
    for warning in warnings:
        print(f"WARN  {warning}")
    try:
        assets = load_catalog(repo)
        desired = desired_files(repo, assets, args.platform)
        state, state_exists = load_state(home, args.platform, desired)
        if args.uninstall:
            actions, adapters, next_state, conflicts = plan_uninstall(repo, home, args.platform, assets, state, state_exists)
        else:
            actions, adapters, next_state, conflicts = plan_install(repo, home, args.platform, assets, state, state_exists, args.prune)
    except (CatalogError, OSError, ValueError) as exc:
        print(f"FAIL  {exc}", file=os.sys.stderr)
        return 1

    if conflicts:
        for conflict in conflicts:
            print(f"CONFLICT  {conflict}", file=os.sys.stderr)
        if not args.uninstall and not args.prune:
            if not args.dry_run and not state_exists and state["files"]:
                try:
                    validate_home_target(home, STATE_FILE, reject_leaf_symlink=True)
                    write_state(home / STATE_FILE, state)
                except (OSError, CatalogError) as exc:
                    print(f"FAIL  could not retain migration state: {exc}", file=os.sys.stderr)
                    return 1
            print("No changes applied because unmanaged or modified destinations were found.", file=os.sys.stderr)
            return 2

    for action in actions:
        if args.dry_run:
            report_file_action(home, action, args.show_diff)
    for adapter in adapters:
        if args.show_diff:
            display_diff(str(adapter.path), adapter.before, adapter.after)
        print(f"  {'would ' if args.dry_run else ''}{adapter.description}")

    if args.dry_run:
        print(f"Dry run ({args.platform}): {len(actions)} file action(s), {len(adapters)} adapter action(s)")
        return 2 if conflicts else 0

    try:
        preflight_mutations(home, actions, adapters)
        for action in actions:
            apply_file_action(home, action)
            verb = "removed" if action.kind == "remove" else ("added" if action.kind == "create" else "updated")
            print(f"  {verb}: {action.target}")
        for adapter in adapters:
            validate_home_target(home, adapter.target, reject_leaf_symlink=True)
            atomic_write(adapter.path, adapter.after.encode("utf-8"), adapter.mode)
            print(f"  {adapter.description}")
    except (OSError, RuntimeError, CatalogError) as exc:
        print(f"FAIL  apply failed before state commit: {exc}", file=os.sys.stderr)
        return 1

    if args.uninstall:
        if conflicts:
            validate_home_target(home, STATE_FILE, reject_leaf_symlink=True)
            write_state(home / STATE_FILE, next_state)
        else:
            state_path = validate_home_target(home, STATE_FILE, reject_leaf_symlink=True)
            if state_path.exists():
                state_path.unlink()
            legacy = validate_home_target(home, LEGACY_DOC_MANIFEST, reject_leaf_symlink=True)
            if legacy.exists():
                legacy.unlink()
    else:
        validate_home_target(home, STATE_FILE, reject_leaf_symlink=True)
        write_state(home / STATE_FILE, next_state)
        legacy = validate_home_target(home, LEGACY_DOC_MANIFEST, reject_leaf_symlink=True)
        if legacy.exists() and not conflicts:
            legacy.unlink()
    if conflicts:
        print(f"Completed safe actions with {len(conflicts)} unresolved conflict(s).", file=os.sys.stderr)
        return 2
    print(f"Completed ({args.platform}): {len(actions)} file action(s), {len(adapters)} adapter action(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("platform", choices=("codex", "claude"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--diff", dest="show_diff", action="store_true")
    parser.add_argument("--update", action="store_true", help="reconcile current catalog sources (same as install)")
    parser.add_argument("--prune", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    if args.show_diff:
        args.dry_run = True
    if args.prune and args.uninstall:
        parser.error("--prune and --uninstall cannot be combined")
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
