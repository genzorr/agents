#!/usr/bin/env python3
"""Check asset ownership consistency across agents, Harness, Claude Headless, and session-harvester.

This is a read-only S-17 guard. It verifies the repo split at the level that
matters for install safety: physical skill/command/subagent source ownership and
installer scope. It does not inspect installed global homes.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from agent_catalog import CatalogError, catalog_named_ids, catalog_skill_ids, load_catalog
except ModuleNotFoundError:  # Imported as a module from repository tests.
    from scripts.agent_catalog import CatalogError, catalog_named_ids, catalog_skill_ids, load_catalog

HARNESS_COMMANDS = {"execute.md"}
HARNESS_AGENTS = {"harness-task-bootstrap.md", "task-verifier.md"}
SESSION_SKILL = "harvest-sessions"
FOREIGN_SKILLS = {"codex-primary-runtime"}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def skill_dirs(repo: Path, platform: str) -> set[str]:
    roots = (repo / platform / "skills", repo / "shared" / "skills")
    return {
        path.name
        for root in roots
        if root.is_dir()
        for path in root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def md_names(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {path.name for path in root.iterdir() if path.is_file() and path.suffix == ".md"}


def bash_return_zero_patterns(script: Path, function_name: str) -> tuple[set[str], list[str]]:
    if not script.is_file():
        return set(), [f"missing required installer script: {script}"]
    text = script.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"{re.escape(function_name)}\(\)\s*\{{(.*?)\n\}}", text, re.DOTALL)
    if not match:
        return set(), [f"{script.name}: could not locate `{function_name}` body"]
    patterns: set[str] = set()
    for line in match.group(1).splitlines():
        if "return 0" not in line:
            continue
        token = line.strip().split(")", 1)[0].strip()
        if token and token != "*":
            patterns.update(token.split("|"))
    if not patterns:
        return set(), [f"{script.name}: `{function_name}` has no managed return-0 patterns"]
    return patterns, []


def check_agents(agents: Path) -> list[str]:
    errors: list[str] = []
    try:
        assets = load_catalog(agents)
    except CatalogError as exc:
        return [f"agents: invalid catalog: {exc}"]
    physical_by_platform = {platform: skill_dirs(agents, platform) for platform in ("codex", "claude")}
    catalog_by_platform = {platform: catalog_skill_ids(assets, platform) for platform in ("codex", "claude")}
    physical = physical_by_platform["codex"] | physical_by_platform["claude"]
    catalog = catalog_by_platform["codex"] | catalog_by_platform["claude"]
    boundary = {name for name in physical | catalog if name.startswith("harness-")}
    boundary |= (physical | catalog) & ({SESSION_SKILL} | FOREIGN_SKILLS)
    for name in sorted(boundary):
        errors.append(f"agents: boundary/foreign skill must not be owned here: {name}")
    for platform in ("codex", "claude"):
        if physical_by_platform[platform] != catalog_by_platform[platform]:
            errors.append(
                f"agents: {platform} physical skill dirs and catalog ids differ "
                f"(physical-only={sorted(physical_by_platform[platform] - catalog_by_platform[platform])}, "
                f"catalog-only={sorted(catalog_by_platform[platform] - physical_by_platform[platform])})"
            )

    commands = md_names(agents / "claude" / "commands")
    expected_commands = {f"{name}.md" for name in catalog_named_ids(assets, "command", "claude")}
    if commands != expected_commands:
        errors.append(f"agents: physical Claude commands and catalog ids differ (physical={sorted(commands)}, catalog={sorted(expected_commands)})")

    agents_files = md_names(agents / "claude" / "agents")
    expected_agents = {f"{name}.md" for name in catalog_named_ids(assets, "subagent", "claude")}
    if agents_files != expected_agents:
        errors.append(f"agents: physical Claude subagents and catalog ids differ (physical={sorted(agents_files)}, catalog={sorted(expected_agents)})")
    return errors


def check_harness(harness: Path) -> list[str]:
    errors: list[str] = []
    skills = skill_dirs(harness, "codex") | skill_dirs(harness, "claude")
    for name in sorted(skills):
        if not name.startswith("harness-"):
            errors.append(f"harness: non-harness skill present: {name}")

    commands = md_names(harness / "claude" / "commands")
    extra_commands = commands - HARNESS_COMMANDS
    if extra_commands:
        errors.append(f"harness: non-Harness Claude commands present: {sorted(extra_commands)}")

    agents = md_names(harness / "claude" / "agents")
    extra_agents = agents - HARNESS_AGENTS
    if extra_agents:
        errors.append(f"harness: non-Harness Claude agents present: {sorted(extra_agents)}")

    if (harness / "claude" / "rules").exists():
        errors.append("harness: Claude rules directory should stay owned by agents")
    if (harness / "codex" / "AGENTS.md").exists():
        errors.append("harness: Codex global AGENTS.md should stay owned by agents")

    for script_name in ("install-codex.sh", "install-claude.sh"):
        patterns, pattern_errors = bash_return_zero_patterns(
            harness / "scripts" / script_name,
            "is_repo_managed_skill",
        )
        errors.extend(f"harness: {error}" for error in pattern_errors)
        invalid = {pattern for pattern in patterns if pattern != "harness-*"}
        if invalid:
            errors.append(f"harness: {script_name} skill allowlist has non-harness entries: {sorted(invalid)}")
    return errors


def check_session_harvester(harvester: Path) -> list[str]:
    errors: list[str] = []
    legacy_skill = harvester / "harvest-sessions-skill.md"
    canonical_dir = harvester / "skills" / SESSION_SKILL
    canonical_skill = canonical_dir / "SKILL.md"
    canonical_dir_is_symlink = canonical_dir.is_symlink()
    canonical_skill_is_symlink = canonical_skill.is_symlink()
    has_canonical = (
        canonical_skill.is_file()
        and not canonical_dir_is_symlink
        and not canonical_skill_is_symlink
    )
    if legacy_skill.exists() or legacy_skill.is_symlink():
        errors.append("session-harvester: legacy harvest-sessions-skill.md is no longer supported")
    if canonical_dir_is_symlink:
        errors.append("session-harvester: canonical skills/harvest-sessions directory must not be a symlink")
    elif canonical_skill_is_symlink:
        errors.append("session-harvester: canonical skills/harvest-sessions/SKILL.md must not be a symlink")
    elif not has_canonical:
        errors.append("session-harvester: canonical skills/harvest-sessions must contain SKILL.md")
    fields = parse_frontmatter(canonical_skill.read_text(encoding="utf-8")) if has_canonical else {}
    if has_canonical and fields.get("name") != SESSION_SKILL:
        errors.append("session-harvester: canonical skill frontmatter name must be harvest-sessions")
    if skill_dirs(harvester, "codex") or skill_dirs(harvester, "claude"):
        errors.append("session-harvester: unexpected codex/ or claude/ skill tree present")

    skill_root = harvester / "skills"
    if skill_root.is_dir():
        foreign_dirs = {
            path.name for path in skill_root.iterdir() if path.is_dir() and path.name != SESSION_SKILL
        }
        if foreign_dirs:
            errors.append(f"session-harvester: foreign skill directories present: {sorted(foreign_dirs)}")
        unexpected_entries = {
            path.name for path in skill_root.iterdir() if not path.is_dir() and path.name != ".gitkeep"
        }
        if unexpected_entries:
            errors.append(f"session-harvester: unexpected files in skills root: {sorted(unexpected_entries)}")

    script = harvester / "scripts" / "install-claude-skill.sh"
    if not script.is_file():
        errors.append("session-harvester: missing scripts/install-claude-skill.sh")
    else:
        text = script.read_text(encoding="utf-8", errors="ignore")
        if "skills/harvest-sessions" not in text:
            errors.append("session-harvester: installer does not target harvest-sessions")
        if "CODEX_HOME" in text:
            errors.append("session-harvester: installer should not manage Codex assets")
    return errors


def check_disjoint_ownership(agents: Path, harness: Path, claude_headless: Path) -> list[str]:
    """Reject duplicate physical ownership without prescribing sibling asset sets."""
    errors: list[str] = []
    skill_owned = {
        "agents": skill_dirs(agents, "codex") | skill_dirs(agents, "claude"),
        "harness": skill_dirs(harness, "codex") | skill_dirs(harness, "claude"),
        "claude-headless": skill_dirs(claude_headless, "codex") | skill_dirs(claude_headless, "claude"),
        "session-harvester": {SESSION_SKILL},
    }
    labels = sorted(skill_owned)
    for i, left in enumerate(labels):
        for right in labels[i + 1 :]:
            overlap = skill_owned[left] & skill_owned[right]
            if overlap:
                errors.append(f"duplicate skill ownership between {left} and {right}: {sorted(overlap)}")

    command_overlap = md_names(agents / "claude" / "commands") & md_names(
        harness / "claude" / "commands"
    )
    if command_overlap:
        errors.append(
            "duplicate Claude command ownership between agents and harness: "
            f"{sorted(command_overlap)}"
        )

    agent_overlap = md_names(agents / "claude" / "agents") & md_names(
        harness / "claude" / "agents"
    )
    if agent_overlap:
        errors.append(
            "duplicate Claude subagent ownership between agents and harness: "
            f"{sorted(agent_overlap)}"
        )
    return errors


def main() -> int:
    default_agents = Path(__file__).resolve().parents[1]
    default_repos = default_agents.parent

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=Path, default=default_agents)
    parser.add_argument("--harness", type=Path, default=default_repos / "harness")
    parser.add_argument("--claude-headless", type=Path, default=default_repos / "claude-headless")
    parser.add_argument("--session-harvester", type=Path, default=default_repos / "session-harvester")
    args = parser.parse_args()

    errors: list[str] = []
    for label, repo in (
        ("agents", args.agents),
        ("harness", args.harness),
        ("claude-headless", args.claude_headless),
        ("session-harvester", args.session_harvester),
    ):
        if not repo.is_dir():
            errors.append(f"{label}: repo not found: {repo}")

    if not errors:
        errors.extend(check_agents(args.agents))
        errors.extend(check_harness(args.harness))
        errors.extend(check_session_harvester(args.session_harvester))
        errors.extend(check_disjoint_ownership(args.agents, args.harness, args.claude_headless))

    for error in errors:
        print(f"FAIL  {error}", file=sys.stderr)
    if errors:
        print(f"\n{len(errors)} cross-repo consistency error(s).", file=sys.stderr)
        return 1

    print("OK — cross-repo asset ownership is consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
