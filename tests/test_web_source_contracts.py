"""Behavior contracts for Devin web-source verification guidance."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class WebSourceContractsTest(unittest.TestCase):
    def test_devin_requires_opened_primary_sources(self) -> None:
        text = (REPO_ROOT / "devin/AGENTS.md").read_text(encoding="utf-8")
        for phrase in (
            "leads, not evidence",
            "open the primary source",
            "at least two primary sources for each question or problem",
            "rest on search results only",
            "separate verification pass",
            "not against intermediate notes or earlier drafts",
            "Explore subagent can search but cannot fetch URLs",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
