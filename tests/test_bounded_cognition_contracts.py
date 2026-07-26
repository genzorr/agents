"""Behavior contracts for bounded-cognition and source-distillation guidance."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class BoundedCognitionContractsTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_global_surfaces_encode_local_reasoning_and_bounded_failure(self) -> None:
        codex = self.read("codex/AGENTS.md")
        think = self.read("claude/rules/think-before-coding.md")
        surgical = self.read("claude/rules/surgical-changes.md")

        for text in (codex, think):
            self.assertIn("local reasoning", text)
            self.assertIn("bounded failure", text)
            self.assertIn("blast radius", text)
            self.assertIn("local component correctness is not sufficient", text)

        for text in (codex, surgical):
            self.assertIn("small diff", text.lower())
            self.assertIn("hidden operational knowledge", text)
            self.assertIn("proportionate safeguards", text)

    def test_distill_source_twins_open_complete_contract_and_keep_promotion_separate(self) -> None:
        for path in (
            "codex/skills/distill-source/SKILL.md",
            "claude/skills/distill-source/SKILL.md",
        ):
            text = self.read(path)
            self.assertIn("docs/distill-source-contract.md", text)
            self.assertIn("coverage ledger", text)
            self.assertIn("keep`, `reject`, `defer`", text)
            self.assertIn("Never auto-promote", text)
            self.assertIn("one large completeness-critical source", text)

        contract = self.read("docs/distill-source-contract.md")
        self.assertIn("Omitted middle section", contract)
        self.assertIn("Already covered", contract)
        self.assertIn("Conflicting principles", contract)
        self.assertIn("Multi-repo mapping", contract)
        self.assertIn("Proposal boundary", contract)
        self.assertIn("Do not call a distillation **complete**", contract)
        self.assertIn("Source mechanism | Existing owner / surface | Coverage | Gap", contract)
        self.assertIn("does not enter scope automatically", contract)

    def test_whole_system_reference_is_conditional_and_progressively_disclosed(self) -> None:
        reference = self.read("docs/whole-system-review.md")
        self.assertIn("Skip it for a contained local refactor", reference)
        self.assertIn("What defeats claimed isolation?", reference)
        self.assertIn("Can a transient disturbance become self-sustaining?", reference)
        self.assertIn("What invariant spans components, and who owns it?", reference)
        self.assertIn("Which control loops interact?", reference)
        self.assertIn("What proves the assembled path?", reference)
        self.assertIn("Anti-Overengineering Guardrails", reference)

        for platform in ("codex", "claude"):
            for skill in ("architecture-review", "systemic-diagnosis", "review-change"):
                text = self.read(f"{platform}/skills/{skill}/SKILL.md")
                reference_paragraphs = [
                    paragraph
                    for paragraph in text.split("\n\n")
                    if "docs/whole-system-review.md" in paragraph
                ]
                self.assertEqual(len(reference_paragraphs), 1)
                self.assertIn("skip", reference_paragraphs[0].lower())

    def test_no_source_branded_umbrella_skill_was_added(self) -> None:
        for platform in ("codex", "claude"):
            self.assertFalse((REPO_ROOT / platform / "skills" / "shape-of-the-system").exists())


if __name__ == "__main__":
    unittest.main()
