#!/usr/bin/env python3
"""Validate repo-managed skill frontmatter across both config trees.

Adapted from `repos/harness/scripts/validate_skills.py` for the assets that
physically live in this repo (`repos/agents`): `codex/skills/*/SKILL.md` and
`claude/skills/*/SKILL.md`. Stdlib-only and string-based — no YAML dependency.

Hard failures (exit 1):
    - a skill directory is missing its `SKILL.md`
    - `name:` is missing or does not match the directory name
    - `description:` is missing or empty
    - static doc references (`docs/*.md` strings under a skill directory) that
      do not resolve to a repo file, unless explicitly marked as known example
      placeholders.

Warnings (do not fail):
    - cross-tree presence parity — a skill present in one tree but not the
      other. Informational because some skills legitimately live in one tree
      only (e.g. the `codex-project-init` / `custom-init` project-init twins
      are a deliberate cross-name counterpart gap, not a parity bug).
    - explicitly known example-only doc placeholders that are not meant to
      resolve or travel.

Deferred on purpose: cross-tree *frontmatter* parity (`model`/`effort`/
`allowed-tools`/`argument-hint`). Codex skills omit those Claude-runtime fields
by convention, so enforcing parity would emit false positives.

Usage:
    python3 scripts/validate_skills.py            # validate this repo
    python3 scripts/validate_skills.py <repo-dir> # validate another checkout
"""

# Deferred evaluation of PEP 604 `X | None` unions — required for this script to
# run on the plain system `python3` (3.9+) the repo docs tell users to invoke,
# with no venv/uv dependency.
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Claude-runtime frontmatter fields that Codex skills omit by convention.
# Listed here only to document the deliberate cross-tree parity deferral.
CLAUDE_RUNTIME_FIELDS = ("model", "effort", "allowed-tools", "argument-hint")

# Relative static doc references a skill directory may point at. Same shape the
# installers discover (`scripts/install-*.sh`): `docs/<path>.md`. Absolute
# cross-repo references such as `/Users/.../docs/name.md` are intentionally not
# travel candidates for this repo.
DOC_REF_RE = re.compile(r"docs/[A-Za-z0-9/_.-]+\.md")

# Run-local templated / generated doc paths (e.g. `docs/harness/ops/RUN_ID/*`,
# `docs/audits/YYYYMMDD-*`). These are produced inside a run directory at runtime
# and never exist as static repo files; the installers skip them on copy and the
# validator skips them on check.
TEMPLATED_DOC_MARKERS = ("RUN_ID", "YYYYMMDD")
EXAMPLE_DOC_REFS = {"docs/architecture.md", "docs/loop-closure.md"}


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return top-level ``key: value`` pairs from the leading ``---`` block.

    String-based and forgiving (untrusted file input): only simple single-line
    ``key: value`` entries are captured; anything else is ignored.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def is_empty_frontmatter_value(value: str | None) -> bool:
    if value is None:
        return True
    stripped = value.strip()
    if not stripped:
        return True
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return not stripped[1:-1].strip()
    return False


def check_skill(skill_dir: Path) -> list[str]:
    """Return hard-failure messages for a single skill directory (empty = ok)."""
    name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{name}: missing SKILL.md"]

    fields = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    errors: list[str] = []

    declared = fields.get("name")
    if declared is None:
        errors.append(f"{name}: frontmatter has no `name:`")
    elif declared != name:
        errors.append(f"{name}: `name: {declared}` does not match directory `{name}`")

    if is_empty_frontmatter_value(fields.get("description")):
        errors.append(f"{name}: `description:` is missing or empty")

    return errors


def doc_references(text: str) -> list[str]:
    """Return the static ``docs/*.md`` references in skill text, sorted-unique.

    Run-local templated/generated paths (`RUN_ID`, `YYYYMMDD`) are excluded — the
    installers skip them on copy, so the validator skips them on check.
    """
    refs = set()
    for match in DOC_REF_RE.finditer(text):
        if match.start() > 0 and text[match.start() - 1] == "/":
            continue
        ref = match.group(0)
        if any(marker in ref for marker in TEMPLATED_DOC_MARKERS):
            continue
        refs.add(ref)
    return sorted(refs)


def skill_directory_text(skill_dir: Path) -> str:
    """Return UTF-8-ish text from every file in a skill directory."""
    chunks: list[str] = []
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def check_doc_references(skill_dir: Path, repo_root: Path) -> tuple[list[str], list[str]]:
    """Return (hard errors, warnings) for static doc refs.

    Missing refs are packaging failures because they would not travel into the
    install tree. A tiny explicit allowlist covers example-only placeholders in
    reference material.
    """
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [], []
    errors: list[str] = []
    warnings: list[str] = []
    for ref in doc_references(skill_directory_text(skill_dir)):
        if (repo_root / ref).is_file():
            continue
        message = f"{skill_dir.name}: doc reference not found: {ref}"
        if ref in EXAMPLE_DOC_REFS:
            warnings.append(f"{message} (example-only)")
        else:
            errors.append(message)
    return errors, warnings


def _skill_names(tree_dir: Path) -> list[str]:
    if not tree_dir.is_dir():
        return []
    return sorted(d.name for d in tree_dir.iterdir() if d.is_dir())


def cross_tree_parity(codex_names: list[str], claude_names: list[str]) -> list[str]:
    """Return informational warnings for skills present in only one tree."""
    codex, claude = set(codex_names), set(claude_names)
    warnings: list[str] = []
    for missing in sorted(codex - claude):
        warnings.append(f"{missing}: present in codex/ but not claude/ (ok if tree-specific)")
    for missing in sorted(claude - codex):
        warnings.append(f"{missing}: present in claude/ but not codex/ (ok if tree-specific)")
    return warnings


def validate_trees(codex_dir: Path, claude_dir: Path) -> tuple[list[str], list[str]]:
    """Return (hard_errors, warnings) for both skill trees."""
    errors: list[str] = []
    warnings: list[str] = []
    for tree, label in ((codex_dir, "codex"), (claude_dir, "claude")):
        repo_root = tree.parent.parent
        for name in _skill_names(tree):
            errors.extend(f"{label}/{msg}" for msg in check_skill(tree / name))
            doc_errors, doc_warnings = check_doc_references(tree / name, repo_root)
            errors.extend(f"{label}/{msg}" for msg in doc_errors)
            warnings.extend(f"{label}/{msg}" for msg in doc_warnings)
    warnings.extend(cross_tree_parity(_skill_names(codex_dir), _skill_names(claude_dir)))
    return errors, warnings


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

    codex_dir = args.repo / "codex" / "skills"
    claude_dir = args.repo / "claude" / "skills"
    if not codex_dir.is_dir() and not claude_dir.is_dir():
        print(f"error: no codex/skills or claude/skills under {args.repo}", file=sys.stderr)
        return 2

    errors, warnings = validate_trees(codex_dir, claude_dir)

    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"FAIL  {error}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} frontmatter error(s).", file=sys.stderr)
        return 1
    print(f"OK — skill frontmatter valid ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
