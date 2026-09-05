"""Contracts for the consolidated research and documentation review routes."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ResearchDocConsolidationContractsTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def test_plain_research_route_is_standalone_and_unbounded(self) -> None:
        entrypoint = self.read("shared/skills/ask-chatgpt-pro/SKILL.md")
        reference = self.read("shared/skills/ask-chatgpt-pro/references/plain-research.md")
        self.assertIn("Plain external research", entrypoint)
        self.assertIn("references/plain-research.md", entrypoint)
        self.assertIn("Do not load Pro-only", entrypoint)
        self.assertIn("no fixed word or line range", reference)
        self.assertIn("mandatory findings file", reference)
        self.assertIn("downstream researcher for the research result", reference)
        self.assertIn("must not ask that researcher to generate another research prompt", reference)
        for field in (
            "Decision or downstream action",
            "Evidence standard",
            "Scope boundaries",
            "Sufficiency bar",
            "Unresolved/stop condition",
        ):
            self.assertIn(field, reference)

    def test_pro_route_retains_github_authority_and_artifact_contract(self) -> None:
        entrypoint = self.read("shared/skills/ask-chatgpt-pro/SKILL.md")
        artifact = self.read("shared/skills/ask-chatgpt-pro/references/pro-consult.md")
        self.assertIn("references/pro-consult.md", entrypoint)
        self.assertIn("Pro repository consultation", entrypoint)
        self.assertIn("exact commit SHA", artifact)
        self.assertIn("Check GitHub visibility", artifact)
        self.assertIn("keep the consult read-only", artifact.lower())
        self.assertIn("Always request a downloadable Markdown report", artifact)
        self.assertIn("If a required push was not allowed or failed", artifact)

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
