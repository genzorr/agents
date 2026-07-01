#!/usr/bin/env python3
"""Check skill ownership consistency across agents, harness, and session-harvester.

This is a read-only S-17 guard. It verifies the repo split at the level that
matters for install safety: physical skill source ownership and installer scope.
It does not inspect installed global homes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

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
    root = repo / platform / "skills"
    if not root.is_dir():
        return set()
    return {path.name for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()}


def md_names(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {path.name for path in root.iterdir() if path.is_file() and path.suffix == ".md"}


def catalog_skill_ids(agents: Path) -> set[str]:
    catalog = json.loads((agents / "catalog.json").read_text(encoding="utf-8"))
    return {entry["id"] for entry in catalog.get("skills", [])}


def bash_return_zero_patterns(script: Path, function_name: str) -> set[str]:
    text = script.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"{re.escape(function_name)}\(\)\s*\{{(.*?)\n\}}", text, re.DOTALL)
    if not match:
        return set()
    patterns: set[str] = set()
    for line in match.group(1).splitlines():
        if "return 0" not in line:
            continue
        token = line.strip().split(")", 1)[0].strip()
        if token and token != "*":
            patterns.update(token.split("|"))
    return patterns


def check_agents(agents: Path) -> list[str]:
    errors: list[str] = []
    physical = skill_dirs(agents, "codex") | skill_dirs(agents, "claude")
    catalog = catalog_skill_ids(agents)
    boundary = {name for name in physical | catalog if name.startswith("harness-")}
    boundary |= (physical | catalog) & ({SESSION_SKILL} | FOREIGN_SKILLS)
    for name in sorted(boundary):
        errors.append(f"agents: boundary/foreign skill must not be owned here: {name}")
    if physical != catalog:
        errors.append(
            "agents: physical skill dirs and catalog skill ids differ "
            f"(physical-only={sorted(physical - catalog)}, catalog-only={sorted(catalog - physical)})"
        )
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
        patterns = bash_return_zero_patterns(harness / "scripts" / script_name, "is_repo_managed_skill")
        invalid = {pattern for pattern in patterns if pattern != "harness-*"}
        if invalid:
            errors.append(f"harness: {script_name} skill allowlist has non-harness entries: {sorted(invalid)}")
    return errors


def check_session_harvester(harvester: Path) -> list[str]:
    errors: list[str] = []
    skill_file = harvester / "harvest-sessions-skill.md"
    if not skill_file.is_file():
        return ["session-harvester: missing harvest-sessions-skill.md"]
    fields = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    if fields.get("name") != SESSION_SKILL:
        errors.append("session-harvester: skill frontmatter name must be harvest-sessions")
    if skill_dirs(harvester, "codex") or skill_dirs(harvester, "claude"):
        errors.append("session-harvester: unexpected codex/ or claude/ skill tree present")

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


def check_disjoint_ownership(agents: Path, harness: Path) -> list[str]:
    errors: list[str] = []
    owned = {
        "agents": skill_dirs(agents, "codex") | skill_dirs(agents, "claude"),
        "harness": skill_dirs(harness, "codex") | skill_dirs(harness, "claude"),
        "session-harvester": {SESSION_SKILL},
    }
    labels = sorted(owned)
    for i, left in enumerate(labels):
        for right in labels[i + 1 :]:
            overlap = owned[left] & owned[right]
            if overlap:
                errors.append(f"duplicate skill ownership between {left} and {right}: {sorted(overlap)}")
    return errors


def main() -> int:
    default_agents = Path(__file__).resolve().parents[1]
    default_repos = default_agents.parent

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=Path, default=default_agents)
    parser.add_argument("--harness", type=Path, default=default_repos / "harness")
    parser.add_argument("--session-harvester", type=Path, default=default_repos / "session-harvester")
    args = parser.parse_args()

    errors: list[str] = []
    for label, repo in (
        ("agents", args.agents),
        ("harness", args.harness),
        ("session-harvester", args.session_harvester),
    ):
        if not repo.is_dir():
            errors.append(f"{label}: repo not found: {repo}")

    if not errors:
        errors.extend(check_agents(args.agents))
        errors.extend(check_harness(args.harness))
        errors.extend(check_session_harvester(args.session_harvester))
        errors.extend(check_disjoint_ownership(args.agents, args.harness))

    for error in errors:
        print(f"FAIL  {error}", file=sys.stderr)
    if errors:
        print(f"\n{len(errors)} cross-repo consistency error(s).", file=sys.stderr)
        return 1

    print("OK — cross-repo skill ownership is consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
