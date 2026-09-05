"""Static instruction contracts for session handoffs."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class SessionHandoffContractsTest(unittest.TestCase):
    def read(self, platform: str) -> str:
        return (REPO_ROOT / platform / "skills" / "session-handoff" / "SKILL.md").read_text(encoding="utf-8")

    def test_twins_preserve_context_without_inventing_authorization(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(platform)
            self.assertIn("prompts for after compaction", text)
            self.assertIn("shared working model", text)
            self.assertIn("prior context, not new user authorization", text)
            self.assertIn("it does not by itself define what the user wants next", text)
            self.assertIn("**Agreed:**", text)
            self.assertIn("**Candidate:**", text)
            self.assertIn("**Undecided:**", text)
            self.assertIn("Never impersonate the user", text)
            self.assertIn("**Brief source:**", text)
            self.assertIn("**Authority:**", text)
            self.assertLess(text.index("**Authority:**"), text.index("**Recommended candidate:**"))
            self.assertIn("re-read it after any later compaction", text)
            self.assertIn("repeat that path in the first response", text)

    def test_twins_require_descriptive_recovery_and_loss_audit(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(platform)
            for heading in (
                "## Session narrative",
                "## Important context to preserve",
                "## Current work state",
                "## Decisions and rationale",
                "## Findings and dead ends",
                "## Unresolved and user-owned choices",
                "## Continuation landscape",
                "## Resumption posture",
                "## Relevant artifacts",
            ):
                self.assertIn(heading, text)
            self.assertIn("Keep the brief dense, not terse", text)
            self.assertIn("A discussion-only session can warrant a handoff even when no files changed", text)
            self.assertIn("assume the transcript will disappear", text)
            self.assertIn("Apply a cold-start test", text)
            self.assertIn("Never return only a path when the user asked for a copyable compaction prompt", text)
            self.assertIn("repository or worktree path, branch, HEAD SHA", text)
            self.assertIn('"Not repository work"', text)
            self.assertIn("avoid writing a low-value brief", text)
            self.assertIn("git rev-parse --show-toplevel", text)
            self.assertIn("git status --short --branch", text)
            self.assertIn("date '+%Y-%m-%d %H:%M %Z'", text)

    def test_twins_keep_execution_and_harness_lifecycle_separate(self) -> None:
        codex = self.read("codex")
        claude = self.read("claude")
        self.assertIn("use `goal-prompt`", codex)
        self.assertIn("use `/goal-prompt`", claude)
        self.assertIn("use `harness-record` with `harness checkpoint`", codex)
        self.assertNotIn("harness-task-checkpoint", codex)
        self.assertIn("use `/harness-task-checkpoint`", claude)
        for text in (codex, claude):
            self.assertNotIn("`harness close", text)
            self.assertIn("Do not write a competing Harness checkpoint shape or close the task from this skill", text)


if __name__ == "__main__":
    unittest.main()
