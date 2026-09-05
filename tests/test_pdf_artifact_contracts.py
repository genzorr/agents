"""Behavior contracts for explicit PDF opt-in in external-model handoffs."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class PdfArtifactContractsTest(unittest.TestCase):
    def read(self, platform: str, skill: str) -> str:
        filename = "references/pro-consult.md" if skill == "ask-chatgpt-pro" else "SKILL.md"
        return (REPO_ROOT / "shared" / "skills" / skill / filename).read_text(encoding="utf-8")

    def test_external_handoff_skills_keep_pdf_opt_in(self) -> None:
        for platform in ("codex", "claude"):
            for skill in ("ask-chatgpt-pro", "ask-oracle"):
                text = self.read(platform, skill)
                self.assertIn("invoking this skill does not request a pdf", text.lower(), (platform, skill))
                self.assertIn('"do provide pdf along with other output"', text.lower(), (platform, skill))
                self.assertIn("from the finalized Markdown", text, (platform, skill))
                self.assertIn("one export", text, (platform, skill))
                self.assertIn("keep the layout simple", text, (platform, skill))
                self.assertIn("skip page-by-page visual/CV verification", text, (platform, skill))
                self.assertIn("file exists and is readable", text, (platform, skill))
                self.assertIn("If the user does not explicitly request a PDF, do not create one", text, (platform, skill))
                self.assertNotIn("Also create a PDF if file generation is available", text, (platform, skill))

    def test_external_handoff_skills_require_markdown_by_default(self) -> None:
        for platform in ("codex", "claude"):
            chatgpt = self.read(platform, "ask-chatgpt-pro")
            oracle = self.read(platform, "ask-oracle")
            self.assertIn("Always request a downloadable Markdown report", chatgpt, platform)
            self.assertIn("Always instruct GPT Pro to create a downloadable `.md` file", oracle, platform)


if __name__ == "__main__":
    unittest.main()
