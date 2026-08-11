"""Load, validate, and expand the Agents asset catalog.

The catalog is the desired-state authority. This module deliberately contains
no install-home mutation; the installer engine and validators share its model.
"""

from __future__ import annotations

import json
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

CATALOG_SECTIONS = (
    "skills",
    "commands",
    "subagents",
    "rules",
    "hooks",
    "global_instructions",
    "traveling_documents",
)
SECTION_KINDS = {
    "skills": "skill",
    "commands": "command",
    "subagents": "subagent",
    "rules": "rule",
    "hooks": "hook",
    "global_instructions": "global_instructions",
    "traveling_documents": "traveling_document",
}
PLATFORMS = ("codex", "claude")
BOUNDARY_EXACT_IDS = {"harvest-sessions", "codex-primary-runtime"}
BOUNDARY_PREFIX = "harness-"
KNOWN_HANDLING = {"codex_global_instructions", "claude_settings_hooks"}
ASSET_KEYS = {"$comment", "id", "kind", "platforms", "owner", "source", "install_target", "handling", "tags"}
SOURCE_LAYER_KEYS = {"path", "target", "role"}
ADAPTER_FRAGMENT_ROLE = "settings-hooks"
ADAPTER_POSIX_SCRIPT_ROLE = "posix-script"
ADAPTER_WINDOWS_SCRIPT_ROLE = "windows-script"
ADAPTER_SCRIPT_ROLES = (ADAPTER_POSIX_SCRIPT_ROLE, ADAPTER_WINDOWS_SCRIPT_ROLE)
ADAPTER_ROLES = (*ADAPTER_SCRIPT_ROLES, ADAPTER_FRAGMENT_ROLE)
NOTIFIER_SUFFIXES = {ADAPTER_POSIX_SCRIPT_ROLE: ".sh", ADAPTER_WINDOWS_SCRIPT_ROLE: ".ps1"}
VALID_KINDS = set(SECTION_KINDS.values())
RESERVED_ASSET_IDS = {"harvest-sessions", "codex-primary-runtime"}
RESERVED_TARGET_ROOTS = {"skills/codex-primary-runtime", "skills/harvest-sessions"}
RESERVED_TARGET_PREFIXES = ("skills/harness-",)
RESERVED_TARGETS = {
    "codex": {"hooks.json", "hooks/stop.sh", "hooks/notifications.sh"},
    "claude": {"commands/execute.md", "agents/task-verifier.md", "agents/harness-task-bootstrap.md"},
}
DOC_REF_RE = re.compile(r"(?<!/)docs/[A-Za-z0-9/_.-]+\.md")
TEMPLATED_DOC_MARKERS = ("RUN_ID", "YYYYMMDD")
EXAMPLE_DOC_REFS = {"docs/architecture.md", "docs/loop-closure.md"}


class CatalogError(ValueError):
    """Raised when catalog structure or source coverage is invalid."""


@dataclass(frozen=True)
class SourceLayer:
    path: str
    target: str | None
    role: str | None = None


@dataclass(frozen=True)
class Asset:
    id: str
    kind: str
    platforms: tuple[str, ...]
    owner: str
    sources: dict[str, tuple[SourceLayer, ...]]
    install_targets: dict[str, str]
    handling: dict[str, str]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class DesiredFile:
    target: str
    source: Path
    asset: Asset
    mode: int


def _safe_relative(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CatalogError(f"{label}: expected a non-empty relative path")
    if "\\" in value:
        raise CatalogError(f"{label}: backslash is not allowed in relative paths")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise CatalogError(f"{label}: unsafe relative path `{value}`")
    return path.as_posix()


def _boundary_id(asset_id: str) -> bool:
    return asset_id in BOUNDARY_EXACT_IDS or asset_id.startswith(BOUNDARY_PREFIX)


def validate_asset_identity(asset_id: object, label: str, *, allow_legacy_document: bool = False) -> str:
    legacy_document = allow_legacy_document and isinstance(asset_id, str) and asset_id.startswith("legacy-document:")
    if (
        not isinstance(asset_id, str)
        or not asset_id
        or asset_id in RESERVED_ASSET_IDS
        or asset_id.startswith(BOUNDARY_PREFIX)
        or (not legacy_document and ("/" in asset_id or "\\" in asset_id))
    ):
        raise CatalogError(f"{label}: invalid or foreign asset identity")
    return asset_id


def validate_asset_target(
    platform: str,
    asset_id: object,
    kind: object,
    target: object,
    label: str,
    *,
    allow_legacy_document: bool = False,
) -> str:
    if platform not in PLATFORMS:
        raise CatalogError(f"{label}: unknown platform")
    asset_id = validate_asset_identity(asset_id, label, allow_legacy_document=allow_legacy_document)
    if kind not in VALID_KINDS:
        raise CatalogError(f"{label}: unknown asset kind")
    target = _safe_relative(target, f"{label} target")
    if target in RESERVED_TARGETS[platform] or any(target == root or target.startswith(root + "/") for root in RESERVED_TARGET_ROOTS) or any(target.startswith(prefix) for prefix in RESERVED_TARGET_PREFIXES):
        raise CatalogError(f"{label}: reserved or foreign target")
    if asset_id.startswith("legacy-document:"):
        if kind != "traveling_document" or asset_id.removeprefix("legacy-document:") != target:
            raise CatalogError(f"{label}: legacy identity does not match target")
        return target
    if kind == "skill":
        valid = target == f"skills/{asset_id}" or target.startswith(f"skills/{asset_id}/")
    elif kind == "command":
        valid = target == f"commands/{asset_id}.md" or target.startswith(f"commands/{asset_id}/")
    elif kind == "subagent":
        valid = target == f"agents/{asset_id}.md" or target.startswith(f"agents/{asset_id}/")
    elif kind == "rule":
        valid = target == f"rules/{asset_id}.md" or target.startswith(f"rules/{asset_id}/")
    elif kind == "hook":
        valid = target.startswith("hooks/")
    elif kind == "global_instructions":
        valid = target == "AGENTS.md"
    else:
        valid = target.startswith("docs/")
    if not valid:
        raise CatalogError(f"{label}: asset identity does not match target")
    return target


def _source_layers(entry: dict, platform: str) -> tuple[SourceLayer, ...]:
    raw = entry.get("source", {}).get(platform)
    if isinstance(raw, str):
        return (SourceLayer(raw, entry["install_target"][platform]),)
    if not isinstance(raw, list) or not raw:
        raise CatalogError(f"{entry.get('id', '<unknown>')} ({platform}): source must be a path or layer list")
    layers: list[SourceLayer] = []
    for index, layer in enumerate(raw):
        if isinstance(layer, str):
            layers.append(SourceLayer(layer, entry["install_target"][platform]))
            continue
        if not isinstance(layer, dict):
            raise CatalogError(f"{entry.get('id', '<unknown>')} ({platform}) source layer {index}: expected object")
        unknown = sorted(set(layer) - SOURCE_LAYER_KEYS)
        if unknown:
            raise CatalogError(f"{entry.get('id', '<unknown>')} ({platform}) source layer {index}: unsupported key(s) {', '.join(unknown)}")
        path = layer.get("path")
        target = layer.get("target", entry["install_target"][platform])
        role = layer.get("role")
        if role is not None and not isinstance(role, str):
            raise CatalogError(f"{entry.get('id', '<unknown>')} ({platform}) source layer {index}: role must be a string")
        if target is not None and not isinstance(target, str):
            raise CatalogError(f"{entry.get('id', '<unknown>')} ({platform}) source layer {index}: target must be string or null")
        if target is None and not isinstance(role, str):
            raise CatalogError(f"{entry.get('id', '<unknown>')} ({platform}) adapter-only source needs a role")
        layers.append(SourceLayer(path, target, role))
    return tuple(layers)


def _parse_asset(section: str, entry: object) -> Asset:
    if not isinstance(entry, dict):
        raise CatalogError(f"{section}: every entry must be an object")
    # Unsupported keys are rejected rather than ignored: silently tolerated metadata
    # reads as a behavior contract the loader never honors. Prose belongs in `$comment`.
    unknown = sorted(set(entry) - ASSET_KEYS)
    if unknown:
        raise CatalogError(f"{section}/{entry.get('id', '<unknown>')}: unsupported key(s) {', '.join(unknown)}")
    asset_id = entry.get("id")
    kind = entry.get("kind")
    if not isinstance(asset_id, str) or not asset_id:
        raise CatalogError(f"{section}: entry id must be a non-empty string")
    if not isinstance(kind, str) or kind != SECTION_KINDS[section]:
        raise CatalogError(f"{section}/{asset_id}: kind must match its catalog section")
    platforms_raw = entry.get("platforms")
    if not isinstance(platforms_raw, list) or not platforms_raw or any(platform not in PLATFORMS for platform in platforms_raw):
        raise CatalogError(f"{section}/{asset_id}: platforms must be a non-empty list of codex/claude")
    platforms = tuple(platforms_raw)
    if len(set(platforms)) != len(platforms):
        raise CatalogError(f"{section}/{asset_id}: duplicate platform declaration")
    owner = entry.get("owner")
    if owner != "agents":
        raise CatalogError(f"{section}/{asset_id}: owner must be `agents`")
    validate_asset_identity(asset_id, f"{section}/{asset_id}")
    targets = entry.get("install_target")
    if not isinstance(targets, dict) or set(targets) != set(platforms):
        raise CatalogError(f"{section}/{asset_id}: install_target must cover exactly its platforms")
    install_targets = {platform: validate_asset_target(platform, asset_id, kind, targets[platform], f"{section}/{asset_id} {platform} install_target") for platform in platforms}
    source_map = entry.get("source")
    if not isinstance(source_map, dict) or set(source_map) != set(platforms):
        raise CatalogError(f"{section}/{asset_id}: source must cover exactly its platforms")
    sources = {platform: _source_layers(entry, platform) for platform in platforms}
    handling_raw = entry.get("handling", {})
    if not isinstance(handling_raw, dict) or not set(handling_raw).issubset(platforms):
        raise CatalogError(f"{section}/{asset_id}: handling must name declared platforms")
    handling: dict[str, str] = {}
    for platform, mode in handling_raw.items():
        if mode not in KNOWN_HANDLING:
            raise CatalogError(f"{section}/{asset_id} ({platform}): unknown handling mode `{mode}`")
        handling[platform] = mode
    tags = entry.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        raise CatalogError(f"{section}/{asset_id}: tags must be strings")
    for platform in platforms:
        for index, layer in enumerate(sources[platform]):
            if layer.target is not None:
                validate_asset_target(platform, asset_id, kind, layer.target, f"{section}/{asset_id} {platform} layer {index}")
            elif not (kind == "hook" and platform == "claude" and handling.get(platform) == "claude_settings_hooks" and layer.role == ADAPTER_FRAGMENT_ROLE):
                raise CatalogError(f"{section}/{asset_id} {platform} layer {index}: unconsumed target-null layer")
    return Asset(asset_id, kind, platforms, owner, sources, install_targets, handling, tuple(tags))


def _source_resolved(repo: Path, source: str, label: str) -> Path:
    relative = _safe_relative(source, f"{label} source")
    path = repo / relative
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(repo.resolve())
    except (FileNotFoundError, ValueError) as exc:
        raise CatalogError(f"{label}: source path not found or escapes repository: {source}") from exc
    if path.is_symlink():
        raise CatalogError(f"{label}: source path must not be a symlink: {source}")
    return path


def _iter_source_files(repo: Path, layer: SourceLayer, label: str) -> list[tuple[str, Path, int]]:
    source = _source_resolved(repo, layer.path, label)
    if layer.target is None:
        return []
    target = _safe_relative(layer.target, f"{label} target")
    if source.is_file():
        return [(target, source, stat.S_IMODE(source.stat().st_mode))]
    if not source.is_dir():
        raise CatalogError(f"{label}: source is neither a file nor directory: {layer.path}")
    result: list[tuple[str, Path, int]] = []
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise CatalogError(f"{label}: source tree contains symlink: {path.relative_to(repo)}")
        if not path.is_file():
            continue
        relative = PurePosixPath(path.relative_to(source).as_posix())
        result.append(((PurePosixPath(target) / relative).as_posix(), path, stat.S_IMODE(path.stat().st_mode)))
    if not result:
        raise CatalogError(f"{label}: directory source is empty: {layer.path}")
    return result


def _entry_source_paths(asset: Asset) -> set[str]:
    return {layer.path for layers in asset.sources.values() for layer in layers}


def _catalog_assets(raw: dict) -> list[Asset]:
    assets: list[Asset] = []
    seen: set[str] = set()
    for section in CATALOG_SECTIONS:
        entries = raw.get(section, [])
        if not isinstance(entries, list):
            raise CatalogError(f"{section}: expected a list")
        for entry in entries:
            asset = _parse_asset(section, entry)
            if asset.id in seen:
                raise CatalogError(f"duplicate catalog identity: {asset.id}")
            if _boundary_id(asset.id):
                raise CatalogError(f"{asset.id}: boundary/foreign id must not be installable")
            seen.add(asset.id)
            assets.append(asset)
    return assets


def notifier_twin(script_target: str) -> str | None:
    """Return the other host's notifier for one notifier target, or None.

    The pair is derived from the target name rather than read from installed state,
    so a home cannot nominate an extra file as adapter-owned. `settings_hook_layers`
    enforces the naming this derivation relies on.
    """
    for suffix in NOTIFIER_SUFFIXES.values():
        if script_target.endswith(suffix):
            other = next(value for value in NOTIFIER_SUFFIXES.values() if value != suffix)
            return script_target[: -len(suffix)] + other
    return None


def settings_hook_layers(asset: Asset) -> tuple[dict[str, str], SourceLayer]:
    """Return the adapter's role-keyed notifier targets and its settings fragment."""
    layers = asset.sources["claude"]
    scripts = {
        layer.role: layer.target
        for layer in layers
        if layer.role in ADAPTER_SCRIPT_ROLES and isinstance(layer.target, str)
    }
    fragments = [layer for layer in layers if layer.role == ADAPTER_FRAGMENT_ROLE and layer.target is None]
    if len(layers) != len(ADAPTER_ROLES) or len(scripts) != len(ADAPTER_SCRIPT_ROLES) or len(fragments) != 1:
        raise CatalogError(
            f"{asset.id}: Claude settings hook adapter needs exactly one script and one settings-hooks fragment "
            f"per host platform (roles: {', '.join(ADAPTER_ROLES)})"
        )
    posix_target = scripts[ADAPTER_POSIX_SCRIPT_ROLE]
    if not posix_target.endswith(NOTIFIER_SUFFIXES[ADAPTER_POSIX_SCRIPT_ROLE]) or notifier_twin(posix_target) != scripts[ADAPTER_WINDOWS_SCRIPT_ROLE]:
        # The installer derives a replaced adapter's historical ownership from this
        # naming, so unpaired notifier targets would strand a home's hook files.
        raise CatalogError(
            f"{asset.id}: Claude settings hook adapter notifiers must be `<name>{NOTIFIER_SUFFIXES[ADAPTER_POSIX_SCRIPT_ROLE]}`"
            f" and `<name>{NOTIFIER_SUFFIXES[ADAPTER_WINDOWS_SCRIPT_ROLE]}` twins"
        )
    return scripts, fragments[0]


def _validate_adapter_cardinality(assets: list[Asset]) -> None:
    adapters = [asset for asset in assets if asset.handling.get("claude") == "claude_settings_hooks"]
    if len(adapters) > 1:
        raise CatalogError("catalog: multiple Claude settings hook adapters")
    if not adapters:
        return
    adapter = adapters[0]
    if adapter.kind != "hook" or adapter.platforms != ("claude",):
        raise CatalogError(f"{adapter.id}: Claude settings hook adapter must be a Claude hook")
    settings_hook_layers(adapter)


def _validate_source_collisions(repo: Path, assets: list[Asset]) -> None:
    targets: dict[str, dict[str, str]] = {platform: {} for platform in PLATFORMS}
    for asset in assets:
        for platform in asset.platforms:
            for index, layer in enumerate(asset.sources[platform]):
                label = f"{asset.kind}/{asset.id} ({platform}) layer {index}"
                for target, _source, _mode in _iter_source_files(repo, layer, label):
                    validate_asset_target(platform, asset.id, asset.kind, target, label)
                    prior_target = next(
                        (prior_path for prior_path in targets[platform] if target == prior_path or target.startswith(prior_path + "/") or prior_path.startswith(target + "/")),
                        None,
                    )
                    if prior_target is not None:
                        raise CatalogError(f"{asset.id} ({platform}): target collision at `{target}` with {targets[platform][prior_target]}")
                    targets[platform][target] = f"{asset.kind}/{asset.id}"


def _covered_by_source(path: str, source_paths: set[str]) -> bool:
    return any(path == source or path.startswith(source + "/") for source in source_paths)


def _physical_asset_paths(repo: Path) -> set[str]:
    # as_posix(), not str(): these are compared against catalog source paths, which are
    # always forward-slashed. A native separator would miss every entry on Windows and
    # report the whole tree as uncatalogued.
    paths: set[str] = set()
    for platform in (*PLATFORMS, "shared"):
        skills = repo / platform / "skills"
        if skills.is_dir():
            paths.update(path.relative_to(repo).as_posix() for path in skills.rglob("*") if path.is_file())
    for category in ("commands", "agents", "rules"):
        root = repo / "claude" / category
        if root.is_dir():
            paths.update(path.relative_to(repo).as_posix() for path in root.iterdir() if path.is_file() and path.suffix == ".md")
    for path in (repo / "codex" / "AGENTS.md", repo / "claude" / "hooks.json"):
        if path.is_file():
            paths.add(path.relative_to(repo).as_posix())
    hook_root = repo / "claude" / "hooks"
    if hook_root.is_dir():
        paths.update(path.relative_to(repo).as_posix() for path in sorted(hook_root.rglob("*")) if path.is_file())
    return paths


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def _managed_text_sources(repo: Path, assets: list[Asset]) -> list[tuple[str, str, str]]:
    surfaces: list[tuple[str, str, str]] = []
    for asset in assets:
        if asset.kind in {"traveling_document", "hook"}:
            continue
        for platform in asset.platforms:
            for index, layer in enumerate(asset.sources[platform]):
                source = _source_resolved(repo, layer.path, f"{asset.id} ({platform}) layer {index}")
                files = [source] if source.is_file() else [path for path in sorted(source.rglob("*")) if path.is_file()]
                for path in files:
                    try:
                        text = path.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        continue
                    surfaces.append((platform, asset.id, text))
    return surfaces


def validate_catalog(repo: Path) -> tuple[list[str], list[str]]:
    """Return (hard errors, warnings) for the catalog and source tree."""
    errors: list[str] = []
    warnings: list[str] = []
    try:
        raw = json.loads((repo / "catalog.json").read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise CatalogError("catalog root must be an object")
        assets = _catalog_assets(raw)
        _validate_adapter_cardinality(assets)
        source_paths = {path for asset in assets for path in _entry_source_paths(asset)}
        for asset in assets:
            for platform in asset.platforms:
                for index, layer in enumerate(asset.sources[platform]):
                    _source_resolved(repo, layer.path, f"{asset.id} ({platform}) layer {index}")
                    if layer.target is not None:
                        _safe_relative(layer.target, f"{asset.id} ({platform}) layer {index} target")
        _validate_source_collisions(repo, assets)
        for physical in sorted(_physical_asset_paths(repo)):
            if not _covered_by_source(physical, source_paths):
                errors.append(f"disk: {physical} has no catalog entry")
        for asset in assets:
            if asset.kind != "skill":
                continue
            for platform in asset.platforms:
                skill_target = f"skills/{asset.id}/SKILL.md"
                expanded_skill_files: list[Path] = []
                for index, layer in enumerate(asset.sources[platform]):
                    label = f"{asset.id} ({platform}) layer {index}"
                    expanded_skill_files.extend(
                        source for target, source, _mode in _iter_source_files(repo, layer, label) if target == skill_target
                    )
                if len(expanded_skill_files) != 1:
                    errors.append(f"{asset.id} ({platform}): expanded target must contain exactly one {skill_target}")
                    continue
                fields = _frontmatter(expanded_skill_files[0].read_text(encoding="utf-8"))
                if fields.get("name") != asset.id:
                    errors.append(f"{asset.id} ({platform}): frontmatter name does not match id")
                if not fields.get("description", "").strip():
                    errors.append(f"{asset.id} ({platform}): description is missing or empty")
        traveling_by_platform = {
            platform: {
                target
                for asset in assets
                if asset.kind == "traveling_document" and platform in asset.platforms
                for target in (asset.install_targets[platform],)
            }
            for platform in PLATFORMS
        }
        for platform, asset_id, text in _managed_text_sources(repo, assets):
            for ref in sorted(set(DOC_REF_RE.findall(text))):
                if any(marker in ref for marker in TEMPLATED_DOC_MARKERS):
                    continue
                if ref in EXAMPLE_DOC_REFS and not (repo / ref).is_file():
                    warnings.append(f"{asset_id} ({platform}): example-only doc reference {ref}")
                    continue
                if not (repo / ref).is_file():
                    errors.append(f"{asset_id} ({platform}): doc reference not found: {ref}")
                elif ref not in traveling_by_platform[platform]:
                    errors.append(f"{asset_id} ({platform}): doc reference is not cataloged for travel: {ref}")
    except (OSError, json.JSONDecodeError, CatalogError) as exc:
        errors.append(str(exc))
    return errors, warnings


def load_catalog(repo: Path) -> tuple[Asset, ...]:
    """Load and structurally validate the catalog for installer use."""
    try:
        raw = json.loads((repo / "catalog.json").read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise CatalogError("catalog root must be an object")
        assets = _catalog_assets(raw)
        _validate_adapter_cardinality(assets)
        _validate_source_collisions(repo, assets)
        return tuple(assets)
    except (OSError, json.JSONDecodeError, CatalogError) as exc:
        raise CatalogError(str(exc)) from exc


def desired_files(repo: Path, assets: tuple[Asset, ...], platform: str) -> dict[str, DesiredFile]:
    """Expand all materialized files for one platform into relative targets."""
    result: dict[str, DesiredFile] = {}
    for asset in assets:
        if platform not in asset.platforms:
            continue
        for index, layer in enumerate(asset.sources[platform]):
            label = f"{asset.kind}/{asset.id} ({platform}) layer {index}"
            for target, source, mode in _iter_source_files(repo, layer, label):
                validate_asset_target(platform, asset.id, asset.kind, target, label)
                if target in result:
                    raise CatalogError(f"{asset.id} ({platform}): target collision at `{target}`")
                result[target] = DesiredFile(target, source, asset, mode)
    return result


def asset_for_target(assets: tuple[Asset, ...], platform: str, target: str) -> Asset | None:
    """Return the catalog owner for a target path when it is materialized."""
    for asset in assets:
        if platform not in asset.platforms:
            continue
        for layer in asset.sources[platform]:
            if layer.target == target:
                return asset
    return None


def catalog_skill_ids(assets: tuple[Asset, ...], platform: str) -> set[str]:
    return {asset.id for asset in assets if asset.kind == "skill" and platform in asset.platforms}


def catalog_named_ids(assets: tuple[Asset, ...], kind: str, platform: str) -> set[str]:
    return {asset.id for asset in assets if asset.kind == kind and platform in asset.platforms}
