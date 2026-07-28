"""Contracts for the no-hard-wrap rule on always-on instruction surfaces.

Hard-wrapping prose splits phrases across a newline plus indentation, which breaks
exact-string matching: grep, patch context lines, and the substring assertions in
test_bounded_cognition_contracts.py. No formatter in this repo wraps Markdown, so
any wrap is an authoring choice and is reachable by a rule.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Surfaces the rule itself must be stated on.
RULE_SURFACES = ("claude/rules/conciseness.md", "codex/AGENTS.md")

# Files the rule is enforced against. Kept to the always-on layer, where a broken
# phrase match is most costly; the wider doc tree is not yet reflowed.
ENFORCED = ("claude/rules", "codex/AGENTS.md")

SPECIAL_PREFIXES = ("#", "|", ">", "-", "*", "+", "---", "===")


def is_prose(line: str) -> bool:
    """A plain paragraph line: not blank, not a heading/table/quote/list/rule."""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(SPECIAL_PREFIXES):
        return False
    return not re.match(r"^\d+\.\s", stripped)


def wrapped_pairs(text: str) -> list[tuple[int, str]]:
    """Consecutive prose lines outside code fences — the signature of a hard wrap.

    With one paragraph per line, two adjacent plain-prose lines cannot occur:
    paragraphs are blank-line separated and list items carry their own marker.
    """
    findings = []
    in_fence = False
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if index + 1 < len(lines) and is_prose(line) and is_prose(lines[index + 1]):
            findings.append((index + 1, line.strip()[:60]))
    return findings


class LineBreakContractsTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_rule_is_stated_on_both_global_surfaces(self) -> None:
        for path in RULE_SURFACES:
            text = self.read(path)
            self.assertIn("Line Breaks In Files", text, f"{path} lost the rule heading")
            self.assertIn("Never hard-wrap prose to a column width", text, path)
            self.assertIn("One paragraph, bullet, or table row is one line", text, path)

    def test_always_on_surfaces_are_not_hard_wrapped(self) -> None:
        targets = []
        for entry in ENFORCED:
            path = REPO_ROOT / entry
            targets.extend(sorted(path.glob("*.md")) if path.is_dir() else [path])

        self.assertTrue(targets, "no enforcement targets resolved")
        for path in targets:
            rel = path.relative_to(REPO_ROOT)
            findings = wrapped_pairs(path.read_text(encoding="utf-8"))
            self.assertEqual(
                findings,
                [],
                f"{rel} appears hard-wrapped at line(s) "
                f"{[line for line, _ in findings]}; join each paragraph onto one line",
            )


if __name__ == "__main__":
    unittest.main()
