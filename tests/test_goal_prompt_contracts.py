"""Static contracts for goal-prompt drift and near-miss guards."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class GoalPromptContractsTest(unittest.TestCase):
    def read(self, platform: str) -> str:
        return (REPO_ROOT / platform / "skills" / "goal-prompt" / "SKILL.md").read_text(encoding="utf-8")

    def test_twins_require_delayed_handoff_and_research_near_miss_guards(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(platform)
            for phrase in (
                "Expected Starting Ref",
                "Material Drift Check",
                "Does Not Count",
                "Adversarial Failure Modes",
            ):
                self.assertIn(phrase, text, platform)
            self.assertIn("handoff intended to resume after the current session", text, platform)
            self.assertIn("git rev-parse --show-toplevel", text, platform)
            self.assertIn("commits produced by this goal", text, platform)
            self.assertIn("source/config changes that invalidate", text, platform)
            self.assertIn("ask the operator", text, platform)
            self.assertIn("explicit operator decision", text, platform)
            self.assertIn("task-specific `Does Not Count` section", text, platform)
            self.assertIn("record the failure as not counting", text, platform)
            self.assertIn("candidate rejection still follows the existing research-rejection rule", text, platform)
            self.assertIn("reference the drift gate from the Completion Contract", text, platform)
            self.assertIn("do not add generic boilerplate to Standard goals", text, platform)


if __name__ == "__main__":
    unittest.main()
