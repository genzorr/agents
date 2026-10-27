"""Contracts for the consolidated research and documentation review routes."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ResearchDocConsolidationContractsTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_docs_only_audit_has_review_owner_and_chat_default(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/review-change/SKILL.md")
            reference = self.read(f"{platform}/skills/review-change/references/docs-only-audit.md")
            self.assertIn("Documentation-only audit", reference)
            self.assertIn("does not require a code diff", text)
            self.assertIn("references/docs-only-audit.md", text)
            self.assertIn("instead of this code-review workflow", text)
            self.assertIn("For a code or change review", text)
            self.assertNotIn("skip diff resolution and follow", text)
            self.assertIn("inconsistencies, gaps, stale references, or unresolved-question mismatches", reference)
            self.assertIn("reports findings in chat by default", reference)
            self.assertIn("Do not ask where to save a report and do not create a findings file", reference)
            self.assertIn("docs/context-file-authoring.md", reference)
            self.assertIn("docs/skill-authoring-principles.md", reference)
            self.assertIn("docs/claim-discipline.md", reference)
            self.assertIn("docs/experiment-protocol-readout-contract.md", reference)

    def test_integration_compares_evidence_and_respects_authorized_scope(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/integrate-research/SKILL.md")
            self.assertIn("Compare research claims and citations with current documents and source evidence", text)
            self.assertIn("If documentation updates are already authorized", text)
            self.assertIn("Do not create a maintained findings file automatically", text)
            self.assertIn("Leave research source files", text)
            self.assertIn("distill-source", text)
            self.assertIn("preserve provenance, conflicts, and uncertainty", text.lower())
            self.assertIn("evidence update", text)
            self.assertIn("chosen baseline", text)
            self.assertIn("method semantics or essential components", text)
            self.assertIn("A recommendation is advice, not authority", text)
            self.assertIn("resolve them under existing authorization", text)
            self.assertIn("Do not silently promote a recommendation into settled project direction or a worker assignment", text)
            self.assertNotIn("## Optional findings artifact", text)

    def test_retired_source_entries_are_absent(self) -> None:
        for path in (
            "codex/skills/bro/SKILL.md",
            "claude/skills/bro/SKILL.md",
            "codex/skills/research-prompt/SKILL.md",
            "claude/skills/research-prompt/SKILL.md",
            "codex/skills/doc-audit/SKILL.md",
            "claude/skills/doc-audit/SKILL.md",
        ):
            self.assertFalse((REPO_ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
