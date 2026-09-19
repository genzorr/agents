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
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from agent_catalog import (
    ADAPTER_POSIX_SCRIPT_ROLE,
    ADAPTER_WINDOWS_SCRIPT_ROLE,
    NOTIFIER_SUFFIXES,
    Asset,
    CatalogError,
    DesiredFile,
    SourceLayer,
    devin_config_layer,
    desired_files,
    load_catalog,
    notifier_twin,
    settings_hook_layers,
    validate_asset_identity,
    validate_asset_target,
    validate_catalog,
)

STATE_FILE = ".agents-install-state.json"
LEGACY_DOC_MANIFEST = ".agents-doc-manifest"
STATE_SCHEMA_VERSION = 2
ADAPTER_KIND = "claude_settings_hooks"
DEVIN_CONFIG_ADAPTER_KIND = "devin_config"
DEVIN_CONFIG_ALLOWED_PATHS = {
    ("read_config_from", provider)
    for provider in ("agents_standard", "cursor", "windsurf", "claude", "copilot", "opencode", "zed")
}
HOST_IS_WINDOWS = os.name == "nt"
WINDOWS_SCRIPT_SUFFIX = NOTIFIER_SUFFIXES[ADAPTER_WINDOWS_SCRIPT_ROLE]
# The one fragment token: hook commands need the host-selected notifier invocation,
# and nothing in a fragment needs the bare home.
NOTIFIER_TOKEN = "__CLAUDE_NOTIFY__"
# Hook commands are executed by whatever shell Claude Code uses for the platform, so the
# script path is double-quoted: cmd.exe and POSIX shells both pass a double-quoted Windows
# path through unchanged, while a single-quoted or bare one survives only in one of them.
POWERSHELL_PREFIX = "powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File"
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


def migrate_notifier_record_identity(home: Path, target: str, record: dict[str, Any], desired: dict[str, DesiredFile]) -> None:
    """Adopt the current catalog identity for a notifier recorded under an older asset id.

    Moving a notifier script between catalog entries leaves an otherwise valid record
    whose asset id no longer matches the entry that now owns the target, and the
    identity check rejects it before install, prune, or uninstall can reconcile the
    file. Only the settings-hooks adapter's own notifier targets migrate, and only
    when ownership is provable: the recorded baseline must equal the installed file or
    the current source byte for byte, so forged and unrelated records still fail closed.
    """
    item = desired.get(target)
    if item is None or record.get("kind") != "hook" or item.asset.kind != "hook":
        return
    if item.asset.handling.get("claude") != ADAPTER_KIND or record.get("owner") != "agents":
        return
    recorded_id = record.get("asset_id")
    if recorded_id == item.asset.id or record.get("baseline_known") is not True:
        return
    try:
        validate_asset_identity(recorded_id, f"state record {target}")
        scripts, _fragment = settings_hook_layers(item.asset)
        recorded = state_signature(record)
    except ValueError:
        return
    if target not in scripts.values():
        return
    destination = home / PurePosixPath(target)
    installed_baseline = not destination.is_symlink() and destination.is_file() and file_signature(destination) == recorded
    if not installed_baseline and file_signature(item.source) != recorded:
        return
    record["asset_id"] = item.asset.id


def is_supported_hook_command(command: str, invocation: str) -> bool:
    """Accept only the documented direct hook invocation form."""
    if command == invocation:
        return True
    prefix = invocation + ' "'
    if not command.startswith(prefix) or not command.endswith('"'):
        return False
    argument = command[len(prefix) : -1]
    return bool(argument) and '"' not in argument and SHELL_CONTROL_RE.search(argument) is None


def notifier_invocation(home: Path, script_target: str) -> str:
    """Return the command prefix that runs one installed notifier script.

    The form follows the recorded script target, not the current host, so a home
    installed on one platform stays reconcilable from the other.
    """
    validate_home_target(home, script_target, reject_leaf_symlink=True)
    if not script_target.endswith(WINDOWS_SCRIPT_SUFFIX):
        return f"{shlex.quote(str(home))}/{script_target}"
    script = str(PureWindowsPath(home, *PurePosixPath(script_target).parts))
    if '"' in script:
        raise CatalogError(f"selected home cannot be quoted for a PowerShell hook: {home}")
    return f'{POWERSHELL_PREFIX} "{script}"'


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


def validate_managed_leaves(asset_id: str, leaves: object, invocation: str) -> list[dict[str, Any]]:
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
        if not isinstance(command, str) or not is_supported_hook_command(command, invocation):
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


_MISSING = object()


def config_value_at(value: Any, path: list[str]) -> Any:
    current = value
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return _MISSING
        current = current[part]
    return current


def config_value_leaves(value: Any, path: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    """Flatten a JSON object into independently owned leaf values."""
    if isinstance(value, dict):
        result: list[dict[str, Any]] = []
        for key, child in value.items():
            if not isinstance(key, str) or not key:
                raise CatalogError("Devin config fragment keys must be non-empty strings")
            result.extend(config_value_leaves(child, (*path, key)))
        return result
    if not path:
        raise CatalogError("Devin config fragment root must be an object")
    return [{"path": list(path), "value": copy.deepcopy(value)}]


def json_values_equal(left: Any, right: Any) -> bool:
    try:
        return json.dumps(left, sort_keys=True, separators=(",", ":"), allow_nan=False) == json.dumps(right, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError):
        return False


def validate_managed_values(asset_id: str, values: object) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        raise CatalogError(f"invalid adapter state for {asset_id}: managed_values must be a list")
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for identity in values:
        if not isinstance(identity, dict) or set(identity) != {"path", "value"} or not isinstance(identity["path"], list):
            raise CatalogError(f"invalid adapter state for {asset_id}: managed_values must contain path/value identities")
        path = identity["path"]
        if not path or any(not isinstance(part, str) or not part for part in path):
            raise CatalogError(f"invalid adapter state for {asset_id}: managed_values path is invalid")
        key = tuple(path)
        if key in seen:
            raise CatalogError(f"invalid adapter state for {asset_id}: duplicate managed value path")
        if key not in DEVIN_CONFIG_ALLOWED_PATHS:
            raise CatalogError(f"invalid adapter state for {asset_id}: unmanaged config path {'.'.join(path)}")
        try:
            json.dumps(identity["value"], allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise CatalogError(f"invalid adapter state for {asset_id}: managed value is not JSON") from exc
        if key[0] == "read_config_from" and not isinstance(identity["value"], bool):
            raise CatalogError(f"invalid adapter state for {asset_id}: {'.'.join(path)} must be boolean")
        seen.add(key)
        normalized.append({"path": list(path), "value": copy.deepcopy(identity["value"])})
    paths = list(seen)
    if any(left != right and (left[: len(right)] == right or right[: len(left)] == left) for left in paths for right in paths):
        raise CatalogError(f"invalid adapter state for {asset_id}: overlapping managed value paths")
    return normalized


def remove_managed_values(value: dict[str, Any], values: list[dict[str, Any]]) -> tuple[dict[str, Any], bool]:
    """Remove exact recorded values and their now-empty object parents."""
    for identity in values:
        if not json_values_equal(config_value_at(value, identity["path"]), identity["value"]):
            return value, False
    result = copy.deepcopy(value)
    for identity in sorted(values, key=lambda item: len(item["path"]), reverse=True):
        parents: list[tuple[dict[str, Any], str]] = []
        current: dict[str, Any] = result
        for part in identity["path"][:-1]:
            child = current[part]
            if not isinstance(child, dict):
                return value, False
            parents.append((current, part))
            current = child
        del current[identity["path"][-1]]
        for parent, key in reversed(parents):
            child = parent.get(key)
            if isinstance(child, dict) and not child:
                del parent[key]
            else:
                break
    return result, True


def merge_config_values(existing: dict[str, Any], desired: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Merge desired leaves without overwriting an unowned differing value."""
    leaves = config_value_leaves(desired)
    if not leaves:
        raise CatalogError("Devin config fragment must contain at least one leaf value")
    leaves = validate_managed_values("Devin config fragment", leaves)
    result = copy.deepcopy(existing)
    for identity in leaves:
        path = identity["path"]
        current_value = config_value_at(result, path)
        if current_value is not _MISSING and not json_values_equal(current_value, identity["value"]):
            rendered = ".".join(path)
            raise CatalogError(f"unresolved config.json adapter: unmanaged value differs at {rendered}; preserved")
        current: dict[str, Any] = result
        for part in path[:-1]:
            if part not in current:
                child = {}
                current[part] = child
            else:
                child = current[part]
            if not isinstance(child, dict):
                rendered = ".".join(path)
                raise CatalogError(f"unresolved config.json adapter: incompatible value at {rendered}; preserved")
            current = child
        current[path[-1]] = copy.deepcopy(identity["value"])
    return result, leaves


def adapter_script_targets(record: dict[str, Any]) -> list[str]:
    """Return the notifier scripts one adapter record may own, wired one first.

    Authority is the recorded wired target plus the twin derived from its name, never
    a list the state file supplies: installed state must not be able to nominate an
    extra file for removal. Both notifiers stay reconcilable after the adapter is
    replaced, and a home installed on one host stays reconcilable from the other.
    """
    wired = record["script_target"]
    twin = notifier_twin(wired) if isinstance(wired, str) else None
    return [wired] if twin is None else [wired, twin]


def _validate_adapter_record(home: Path, asset_id: str, record: object) -> None:
    if not isinstance(record, dict):
        raise CatalogError(f"invalid adapter state for {asset_id}")
    common = {"owner", "asset_id", "kind", "platform", "target"}
    if not common.issubset(record) or record["owner"] != "agents" or record["asset_id"] != asset_id:
        raise CatalogError(f"invalid adapter state for {asset_id}: foreign or inconsistent identity")
    if record["kind"] == ADAPTER_KIND:
        required = {"script_target", "managed_leaves"}
        if not required.issubset(record) or record["platform"] != "claude" or record["target"] != "settings.json":
            raise CatalogError(f"invalid adapter state for {asset_id}: foreign or inconsistent identity")
        for script_target in adapter_script_targets(record):
            validate_asset_target("claude", asset_id, "hook", script_target, f"adapter state {asset_id}")
        validate_managed_leaves(asset_id, record["managed_leaves"], notifier_invocation(home, record["script_target"]))
        return
    if record["kind"] == DEVIN_CONFIG_ADAPTER_KIND:
        if "managed_values" not in record or record["platform"] != "devin" or record["target"] != "config.json":
            raise CatalogError(f"invalid adapter state for {asset_id}: foreign or inconsistent identity")
        validate_asset_target("devin", asset_id, "config", "config.json", f"adapter state {asset_id}")
        validate_managed_values(asset_id, record["managed_values"])
        return
    raise CatalogError(f"invalid adapter state for {asset_id}: unknown adapter kind")


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
        if desired is not None:
            migrate_notifier_record_identity(home, target, record, desired)
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
            history_match = isinstance(adapter, dict) and target in adapter_script_targets(adapter)
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


GLOBAL_MANAGED_MARKERS = {
    "codex": "<!-- managed-by: genzorr/agents; asset: codex-agents-md -->",
    "claude": "<!-- managed-by: genzorr/agents; asset: claude-claude-md -->",
    "devin": "<!-- managed-by: genzorr/agents; asset: devin-agents-md -->",
}


def is_managed_global(path: Path, header: str, marker: str) -> bool:
    if not path.exists() or path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
        return True
    first_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:2]
    return first_lines == [header, marker]


def is_codex_managed_global(path: Path) -> bool:
    return is_managed_global(path, "# Global Codex Instructions", GLOBAL_MANAGED_MARKERS["codex"])


def is_claude_managed_global(path: Path) -> bool:
    return is_managed_global(path, "# Global Claude Instructions", GLOBAL_MANAGED_MARKERS["claude"])


def is_devin_managed_global(path: Path) -> bool:
    return is_managed_global(path, "# Global Devin Instructions", GLOBAL_MANAGED_MARKERS["devin"])


def source_text(layer: SourceLayer, repo: Path) -> str:
    return (repo / layer.path).read_text(encoding="utf-8")


def hook_asset(assets: tuple[Asset, ...], platform: str) -> tuple[Asset, dict[str, str], SourceLayer] | None:
    for asset in assets:
        if asset.handling.get(platform) != ADAPTER_KIND:
            continue
        scripts, fragment = settings_hook_layers(asset)
        return asset, scripts, fragment
    return None


def devin_config_asset(assets: tuple[Asset, ...]) -> tuple[Asset, SourceLayer] | None:
    for asset in assets:
        if asset.handling.get("devin") == DEVIN_CONFIG_ADAPTER_KIND:
            return asset, devin_config_layer(asset)
    return None


def host_script_target(scripts: dict[str, str]) -> str:
    """Return the notifier target this host can actually execute."""
    return scripts[ADAPTER_WINDOWS_SCRIPT_ROLE if HOST_IS_WINDOWS else ADAPTER_POSIX_SCRIPT_ROLE]


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


def json_string_body(value: str) -> str:
    """Escape a rendered value for substitution inside a JSON string literal.

    The token is substituted before parsing, so the value must survive as JSON text and
    not merely as a shell word. A Windows path is backslash-separated and would
    otherwise inject invalid \\escape sequences; the same hazard exists on POSIX for
    any home containing a backslash or a double quote.
    """
    return json.dumps(value)[1:-1]


def rendered_hook_fragment(repo: Path, layer: SourceLayer, home: Path, invocation: str) -> dict[str, Any]:
    text = source_text(layer, repo).replace(NOTIFIER_TOKEN, json_string_body(invocation))
    value = json.loads(text)
    if not isinstance(value, dict) or not isinstance(value.get("hooks"), (dict, list)):
        raise CatalogError("Claude hook fragment must contain a hooks object or array")
    return value


def supported_fragment_hooks(repo: Path, layer: SourceLayer, home: Path, invocation: str, script_target: str) -> Any:
    """Return the fragment's desired hooks, refusing commands state cannot re-validate.

    Every recorded leaf has to re-validate against the notifier invocation on the next
    run, so a fragment whose commands the loader would later reject is refused before
    it is merged rather than after it is written.
    """
    desired = rendered_hook_fragment(repo, layer, home, invocation)["hooks"]
    for identity in hook_leaves(desired):
        command = identity["leaf"]["command"]
        if not is_supported_hook_command(command, invocation):
            raise CatalogError(f"fragment command does not invoke {script_target}: {command}")
    return desired


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
    if configured is None and not histories:
        return None, None, {}
    if uninstall and not histories:
        return None, None, {}
    if configured is None and not (prune or uninstall):
        return None, None, {}

    asset_id: str | None = None
    script_target: str | None = None
    desired_hooks: Any = None
    fragment_error: str | None = None
    if configured is not None:
        asset, scripts, fragment = configured
        asset_id = asset.id
        if not uninstall:
            # Only the host-executable notifier is wired into settings.json; the other
            # script is still materialized, so switching platforms needs no reinstall.
            # Uninstall needs neither: it reconciles from the recorded target.
            script_target = host_script_target(scripts)
            invocation = notifier_invocation(home, script_target)
            try:
                desired_hooks = supported_fragment_hooks(repo, fragment, home, invocation, script_target)
            except (ValueError, OSError) as exc:
                # The fragment gates only the merge. Uninstall never reads it, and prune
                # still retires recorded history that no current fragment can claim.
                fragment_error = f"unresolved settings.json hook adapter: {exc}"
                if not prune:
                    return None, fragment_error, {}

    merge = configured is not None and not uninstall and fragment_error is None
    active_histories = histories if (prune or uninstall) else ({asset_id: histories[asset_id]} if asset_id in histories else {})
    if fragment_error is not None:
        active_histories = {history_id: record for history_id, record in active_histories.items() if history_id != asset_id}
        if not active_histories:
            return None, fragment_error, {}

    destination = validate_home_target(home, "settings.json", reject_leaf_symlink=True)
    if not destination.exists():
        if uninstall:
            return None, fragment_error, {history_id: None for history_id in active_histories}
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
    if not merge:
        if "hooks" not in settings:
            return None, fragment_error, {history_id: None for history_id in active_histories}
        updated_hooks = cleaned_hooks
        updated = dict(settings)
        if updated_hooks is None:
            del updated["hooks"]
        else:
            updated["hooks"] = updated_hooks
        description = "remove Agents hooks from settings.json"
        history_updates = {history_id: None for history_id in active_histories}
    else:
        # merge implies a configured adapter: every other combination returned above.
        adopted_leaves: list[dict[str, Any]] = []
        if asset_id not in histories:
            adopted_leaves, adoption_error = adoptable_desired_leaves(cleaned_hooks, desired_hooks)
            if adoption_error:
                return None, adoption_error, {}
            if adopted_leaves:
                cleaned_hooks, _matched = remove_managed_leaves(cleaned_hooks, adopted_leaves)
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
            "managed_leaves": newly_managed_leaves(cleaned_hooks, updated_hooks),
        }
    after = pretty_json(updated)
    if before == after:
        return None, fragment_error, history_updates
    mode = stat.S_IMODE(destination.stat().st_mode) if destination.exists() else creation_mode()
    return AdapterAction(description, destination, "settings.json", before, after, mode), fragment_error, history_updates


def plan_devin_config(
    repo: Path,
    home: Path,
    assets: tuple[Asset, ...],
    state: dict[str, Any],
    *,
    prune: bool,
    uninstall: bool,
) -> tuple[AdapterAction | None, str | None, dict[str, dict[str, Any] | None]]:
    configured = devin_config_asset(assets)
    histories = {
        asset_id: record
        for asset_id, record in state.get("adapters", {}).items()
        if isinstance(record, dict) and record.get("kind") == DEVIN_CONFIG_ADAPTER_KIND and record.get("target") == "config.json"
    }
    if configured is None and not histories:
        return None, None, {}
    if uninstall and not histories:
        return None, None, {}
    if configured is None and not (prune or uninstall):
        return None, None, {}

    asset_id: str | None = None
    desired_config: dict[str, Any] | None = None
    if configured is not None and not uninstall:
        asset, fragment = configured
        asset_id = asset.id
        try:
            desired_config = json.loads(source_text(fragment, repo))
        except (OSError, json.JSONDecodeError) as exc:
            return None, f"unresolved config.json adapter: invalid managed fragment ({exc})", {}
        if not isinstance(desired_config, dict):
            return None, "unresolved config.json adapter: managed fragment root is not an object", {}

    active_histories = histories if (prune or uninstall) else ({asset_id: histories[asset_id]} if asset_id in histories else {})
    destination = validate_home_target(home, "config.json", reject_leaf_symlink=True)
    destination_exists = destination.exists()
    if not destination_exists:
        if uninstall:
            return None, None, {history_id: None for history_id in active_histories}
        settings: dict[str, Any] = {}
        before = ""
    else:
        try:
            before = destination.read_text(encoding="utf-8")
            settings = json.loads(before)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            return None, f"unresolved config.json adapter: existing config is not strict JSON ({exc}); preserved", {}
        if not isinstance(settings, dict):
            return None, "unresolved config.json adapter: config root is not an object; preserved", {}

    cleaned = settings
    if destination_exists:
        historical_by_path: dict[tuple[str, ...], dict[str, Any]] = {}
        for history in active_histories.values():
            for value in history["managed_values"]:
                key = tuple(value["path"])
                prior = historical_by_path.get(key)
                if prior is not None and not json_values_equal(prior["value"], value["value"]):
                    return None, f"unresolved config.json adapter: overlapping history differs at {'.'.join(key)}; preserved", {}
                historical_by_path[key] = value
        historical_values = list(historical_by_path.values())
        cleaned, matched = remove_managed_values(settings, historical_values)
        if not matched:
            return None, "unresolved config.json adapter: recorded values were modified or moved; preserved", {}

    merge = configured is not None and not uninstall
    if not merge:
        updated = cleaned
        description = "remove managed values from config.json"
        history_updates = {history_id: None for history_id in active_histories}
    else:
        try:
            updated, managed_values = merge_config_values(cleaned, desired_config or {})
        except CatalogError as exc:
            return None, str(exc), {}
        description = "merge managed values into config.json"
        history_updates = {history_id: None for history_id in active_histories if history_id != asset_id}
        history_updates[asset_id] = {
            "owner": "agents",
            "asset_id": asset_id,
            "kind": DEVIN_CONFIG_ADAPTER_KIND,
            "platform": "devin",
            "target": "config.json",
            "managed_values": managed_values,
        }
    after = pretty_json(updated)
    if before == after:
        return None, None, history_updates
    mode = stat.S_IMODE(destination.stat().st_mode) if destination.exists() else creation_mode()
    return AdapterAction(description, destination, "config.json", before, after, mode), None, history_updates


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
        _asset, scripts, _fragment = configured
        targets.update(scripts.values())
    for record in state.get("adapters", {}).values():
        if isinstance(record, dict) and isinstance(record.get("script_target"), str):
            targets.update(adapter_script_targets(record))
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
        if isinstance(existing, dict) and existing.get("kind") == ADAPTER_KIND and any(target in next_state["files"] for target in adapter_script_targets(existing)):
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
        if current == desired_signature:
            next_state["files"][target] = state_record(item)
            continue
        managed_global = item.asset.kind == "global_instructions" and (
            (platform == "codex" and is_codex_managed_global(destination))
            or (platform == "claude" and is_claude_managed_global(destination))
            or (platform == "devin" and is_devin_managed_global(destination))
        )
        if managed_global:
            if current != desired_signature:
                actions.append(FileAction("update", target, item))
                next_state["files"][target] = state_record(item)
        elif item.asset.kind == "global_instructions":
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
    if platform == "claude":
        adapter, adapter_error, adapter_updates = plan_claude_hooks(repo, home, assets, state, prune=prune, uninstall=False)
    elif platform == "devin":
        adapter, adapter_error, adapter_updates = plan_devin_config(repo, home, assets, state, prune=prune, uninstall=False)
    else:
        adapter, adapter_error, adapter_updates = None, None, {}
    if adapter_error:
        conflicts.append(adapter_error)
        if prune and platform == "claude":
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
    if platform == "claude":
        adapter, adapter_error, adapter_updates = plan_claude_hooks(repo, home, assets, state, prune=True, uninstall=True)
    elif platform == "devin":
        adapter, adapter_error, adapter_updates = plan_devin_config(repo, home, assets, state, prune=True, uninstall=True)
    else:
        adapter, adapter_error, adapter_updates = None, None, {}
    if adapter_error:
        conflicts.append(adapter_error)
        if platform == "claude":
            retain_hook_files_on_adapter_error(assets, desired, state, next_state, actions)
    if adapter is not None:
        adapter_actions.append(adapter)
    apply_adapter_updates(next_state, adapter_updates)
    return actions, adapter_actions, next_state, conflicts


def run(args: argparse.Namespace) -> int:
    repo = Path(__file__).resolve().parents[1]
    home_vars = {"agents": "AGENTS_HOME", "codex": "CODEX_HOME", "claude": "CLAUDE_HOME", "devin": "DEVIN_HOME"}
    if args.platform == "devin":
        default_home = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming")) / "devin" if os.name == "nt" else Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "devin"
    else:
        default_home = Path.home() / f".{args.platform}"
    home = Path(os.environ.get(home_vars[args.platform], str(default_home))).expanduser().absolute()
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
    parser.add_argument("platform", choices=("agents", "codex", "claude", "devin"))
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
