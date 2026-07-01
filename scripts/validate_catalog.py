#!/usr/bin/env python3
"""Validate catalog.json against the physical assets in this repo.

Mechanizes the identity/boundary invariants from `docs/harness/work/tasks/T-66.md`
and the S-17 asset-move manifest: the catalog must cover every agents-owned asset
physically present in this repo, preserve platform-specific skill identity, and
never list a Harness-owned, session-harvester-owned, or foreign asset as an
installable entry. Stdlib-only and JSON-based — no YAML dependency, matching
`harness-core`'s durable-frontmatter convention.

Hard failures (exit 1):
    - a catalog source path does not exist under the repo;
    - a skill's `SKILL.md` frontmatter `name:` does not equal its catalog id
      (which must also equal the skill directory name);
    - an `install_target` path does not match its platform's `~/.codex/...` or
      `~/.claude/...` shape;
    - a duplicate id within the same kind + platform;
    - a boundary/foreign id (`harness-*`, `harvest-sessions`,
      `codex-primary-runtime`) appears as an installable catalog entry;
    - a physically-present agents-owned asset (a `codex/skills/*` or
      `claude/skills/*` dir, a `claude/{commands,agents,rules}/*.md` file,
      `codex/AGENTS.md`, or `claude/hooks/notifications.sh` + `claude/hooks.json`)
      has no corresponding catalog entry — this is the disk-to-catalog reverse of
      the source-path check above, and is what makes it impossible to silently
      omit a moved asset from the catalog.

Soft checks (warn, do not fail):
    - if `scripts/install-codex.sh` / `scripts/install-claude.sh` exist, warn if
      their `is_repo_managed_skill` allowlist does not match this catalog's
      per-platform skill id set. These installer scripts do not exist yet (a
      later task adds them); their absence is not a failure.

Usage:
    python3 scripts/validate_catalog.py            # validate this repo
    python3 scripts/validate_catalog.py <repo-dir>  # validate another checkout
"""

# Deferred evaluation of PEP 604 `X | None` unions — required for this script to
# run on the plain system `python3` (3.9+) the repo docs tell users to invoke,
# with no venv/uv dependency.
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ids that are never allowed as installable catalog entries — they are owned by
# repos/harness, repos/session-harvester, or a foreign/unknown provider. Exact
# names plus the harness-* prefix (see the S-17 asset-move manifest).
BOUNDARY_EXACT_IDS = {"harvest-sessions", "codex-primary-runtime"}
BOUNDARY_PREFIX = "harness-"

# install_target shape per platform: "~/.codex/..." or "~/.claude/...".
INSTALL_TARGET_RE = {
    "codex": re.compile(r"^~/\.codex(/|$)"),
    "claude": re.compile(r"^~/\.claude(/|$)"),
}

# Sections of catalog.json that hold installable entries (everything except
# boundary_notes, which is documentation-only by design).
INSTALLABLE_SECTIONS = ("skills", "commands", "subagents", "rules", "hooks", "global_instructions")


def load_catalog(repo: Path) -> dict:
    catalog_path = repo / "catalog.json"
    if not catalog_path.is_file():
        print(f"error: no catalog.json under {repo}", file=sys.stderr)
        sys.exit(2)
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def is_boundary_id(entry_id: str) -> bool:
    return entry_id in BOUNDARY_EXACT_IDS or entry_id.startswith(BOUNDARY_PREFIX)


def check_boundary(catalog: dict) -> list[str]:
    """Return hard-failure messages for boundary/foreign ids listed as installable."""
    errors: list[str] = []
    for section in INSTALLABLE_SECTIONS:
        for entry in catalog.get(section, []):
            if is_boundary_id(entry["id"]):
                errors.append(
                    f"{section}/{entry['id']}: boundary/foreign id must not appear as an "
                    "installable catalog entry"
                )
    return errors


def check_source_paths(catalog: dict, repo: Path) -> list[str]:
    """Return hard-failure messages for catalog source paths missing on disk."""
    errors: list[str] = []
    for section in INSTALLABLE_SECTIONS:
        for entry in catalog.get(section, []):
            source = entry.get("source", {})
            for platform, paths in source.items():
                for path in paths if isinstance(paths, list) else [paths]:
                    if not (repo / path).exists():
                        errors.append(
                            f"{section}/{entry['id']} ({platform}): source path not found: {path}"
                        )
    return errors


def check_skill_identity(catalog: dict, repo: Path) -> list[str]:
    """Return hard-failure messages for skill id / SKILL.md `name:` mismatches."""
    errors: list[str] = []
    for entry in catalog.get("skills", []):
        entry_id = entry["id"]
        for platform, path in entry.get("source", {}).items():
            skill_file = repo / path
            if not skill_file.is_file():
                continue  # already reported by check_source_paths
            dir_name = skill_file.parent.name
            if dir_name != entry_id:
                errors.append(
                    f"skills/{entry_id} ({platform}): directory `{dir_name}` does not match "
                    f"catalog id `{entry_id}`"
                )
            declared = parse_frontmatter_name(skill_file.read_text(encoding="utf-8"))
            if declared != entry_id:
                errors.append(
                    f"skills/{entry_id} ({platform}): frontmatter `name: {declared}` does not "
                    f"match catalog id `{entry_id}`"
                )
    return errors


def parse_frontmatter_name(text: str) -> str | None:
    """Return the `name:` value from a leading `---` frontmatter block, or None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    for line in text[3:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        if key.strip() == "name":
            return value.strip()
    return None


def check_install_targets(catalog: dict) -> list[str]:
    """Return hard-failure messages for install_target paths with the wrong platform shape."""
    errors: list[str] = []
    for section in INSTALLABLE_SECTIONS:
        for entry in catalog.get(section, []):
            for platform, target in entry.get("install_target", {}).items():
                pattern = INSTALL_TARGET_RE.get(platform)
                if pattern is None:
                    errors.append(f"{section}/{entry['id']}: unknown platform `{platform}`")
                    continue
                if not pattern.match(target):
                    errors.append(
                        f"{section}/{entry['id']} ({platform}): install_target `{target}` does "
                        f"not match the ~/.{platform}/... shape"
                    )
    return errors


def cataloged_source_paths(catalog: dict) -> set[str]:
    """Return every repo-relative path listed in any entry's `source` field."""
    paths: set[str] = set()
    for section in INSTALLABLE_SECTIONS:
        for entry in catalog.get(section, []):
            for _platform, value in entry.get("source", {}).items():
                paths.update(value if isinstance(value, list) else [value])
    return paths


def check_disk_coverage(catalog: dict, repo: Path) -> list[str]:
    """Return hard-failure messages for physically-present assets missing from the catalog.

    Reverse of `check_source_paths`: walks the known agents-owned asset locations
    on disk and requires each one to appear as a catalog `source` path. This is
    what makes it impossible to move an asset into the repo and silently forget
    to catalog it.
    """
    cataloged = cataloged_source_paths(catalog)
    errors: list[str] = []

    for platform in ("codex", "claude"):
        skills_dir = repo / platform / "skills"
        if not skills_dir.is_dir():
            continue
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                continue  # not a skill asset; identity check elsewhere would flag it
            rel = str(skill_file.relative_to(repo))
            if rel not in cataloged:
                errors.append(f"disk: {rel} has no catalog entry")

    for subdir in ("commands", "agents", "rules"):
        tree = repo / "claude" / subdir
        if not tree.is_dir():
            continue
        for path in sorted(tree.iterdir()):
            if path.is_file() and path.suffix == ".md":
                rel = str(path.relative_to(repo))
                if rel not in cataloged:
                    errors.append(f"disk: {rel} has no catalog entry")

    for fixed_path in ("codex/AGENTS.md", "claude/hooks/notifications.sh", "claude/hooks.json"):
        if (repo / fixed_path).is_file() and fixed_path not in cataloged:
            errors.append(f"disk: {fixed_path} has no catalog entry")

    return errors


def check_duplicate_ids(catalog: dict) -> list[str]:
    """Return hard-failure messages for duplicate ids within the same kind + platform."""
    errors: list[str] = []
    for section in INSTALLABLE_SECTIONS:
        seen: dict[str, set[str]] = {}
        for entry in catalog.get(section, []):
            entry_id = entry["id"]
            platforms = set(entry.get("platforms", []))
            prior = seen.setdefault(entry_id, set())
            overlap = prior & platforms
            if overlap:
                errors.append(
                    f"{section}/{entry_id}: duplicate id for platform(s) {sorted(overlap)}"
                )
            prior |= platforms
    return errors


# `is_repo_managed_skill` in install-{codex,claude}.sh is expected to look like a
# bash case/list of skill names. This regex is intentionally loose: it only pulls
# out bare identifier-looking tokens, since the installer scripts don't exist yet
# and their eventual shape is a later task's contract.
SKILL_NAME_TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def catalog_skill_ids(catalog: dict, platform: str) -> set[str]:
    return {
        entry["id"]
        for entry in catalog.get("skills", [])
        if platform in entry.get("platforms", [])
    }


def check_installer_allowlist_parity(catalog: dict, repo: Path) -> list[str]:
    """Return warnings if an installer script's allowlist diverges from the catalog.

    Soft check only: `scripts/install-codex.sh` / `scripts/install-claude.sh` do not
    exist yet (a later task adds them per the S-17 board), so their absence is not
    a failure — this only warns when the file IS present and its
    `is_repo_managed_skill` allowlist looks out of sync with the catalog.
    """
    warnings: list[str] = []
    for platform, script_name in (("codex", "install-codex.sh"), ("claude", "install-claude.sh")):
        script_path = repo / "scripts" / script_name
        if not script_path.is_file():
            continue
        text = script_path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"is_repo_managed_skill\(\)\s*\{(.*?)\n\}", text, re.DOTALL)
        if not match:
            warnings.append(
                f"{script_name}: could not locate `is_repo_managed_skill` body to check parity"
            )
            continue
        body = match.group(1)
        allowlist = {tok for tok in SKILL_NAME_TOKEN_RE.findall(body) if "-" in tok or "_" in tok}
        catalog_ids = catalog_skill_ids(catalog, platform)
        missing_from_allowlist = catalog_ids - allowlist
        extra_in_allowlist = allowlist - catalog_ids
        for skill_id in sorted(missing_from_allowlist):
            warnings.append(
                f"{script_name}: catalog skill `{skill_id}` not found in is_repo_managed_skill allowlist"
            )
        for skill_id in sorted(extra_in_allowlist):
            warnings.append(
                f"{script_name}: allowlist token `{skill_id}` has no matching catalog skill"
            )
    return warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "repo",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repo root (default: this checkout)",
    )
    args = ap.parse_args()
    repo = args.repo

    catalog = load_catalog(repo)

    errors: list[str] = []
    errors.extend(check_boundary(catalog))
    errors.extend(check_source_paths(catalog, repo))
    errors.extend(check_skill_identity(catalog, repo))
    errors.extend(check_install_targets(catalog))
    errors.extend(check_duplicate_ids(catalog))
    errors.extend(check_disk_coverage(catalog, repo))

    warnings = check_installer_allowlist_parity(catalog, repo)

    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"FAIL  {error}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} catalog error(s).", file=sys.stderr)
        return 1
    print(f"OK — catalog valid ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
