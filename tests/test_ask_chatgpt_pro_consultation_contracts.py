"""Static and recorded-conformance contracts for mode-aware ChatGPT Pro consultations."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE = REPO_ROOT / "tests" / "ask_chatgpt_pro_conformance.md"


class AskChatGPTProConsultationContractsTest(unittest.TestCase):
    def read(self, platform: str) -> str:
        return (REPO_ROOT / platform / "skills" / "ask-chatgpt-pro" / "SKILL.md").read_text(encoding="utf-8")

    def test_platform_twins_are_identical_and_general_purpose(self) -> None:
        codex = self.read("codex")
        claude = self.read("claude")
        self.assertEqual(codex, claude)
        self.assertIn(
            "repository inspection, verification, synthesis refinement, decision support, or execution planning",
            codex,
        )
        self.assertIn(
            "Task type may be code/change review, debugging, architecture/system review, research/comparison, decision support, execution planning, document/log analysis, or mixed",
            codex,
        )

    def test_modes_have_canonical_semantics_and_bounded_secondary_composition(self) -> None:
        text = self.read("codex")
        for mode in ("Discover", "Verify", "Refine", "Decide", "Execute"):
            self.assertIn(f"**{mode}**", text)
            self.assertIn(f"### {mode}", text)
        self.assertIn("Choose exactly one primary mode", text)
        self.assertIn("Add at most one secondary mode", text)
        self.assertIn("The primary mode owns framing, context authority, stop conditions, and the main Required Output", text)
        self.assertIn("A secondary mode may add a bounded section after the primary result", text)
        self.assertIn("If the two modes conflict, omit the secondary mode", text)
        self.assertIn("- Secondary mode: [optional; omit when none]", text)
        self.assertIn("- Mode ordering:", text)
        self.assertIn("Do not chain more than two modes", text)

    def test_context_authority_separates_decisions_from_preferences(self) -> None:
        text = self.read("codex")
        for category in (
            "Primary evidence",
            "User requirements and constraints",
            "Working synthesis",
            "Hypotheses",
            "Selected decisions",
            "Preferences and decision criteria",
            "Assumptions and unknowns",
        ):
            self.assertIn(category, text)
        self.assertIn("what to preserve as a hard constraint", text)
        self.assertIn("what to use as a softer criterion", text)
        self.assertIn("## Selected Decisions", text)
        self.assertIn("## Preferences And Decision Criteria", text)
        self.assertNotIn("## Selected Decisions And Preferences", text)

    def test_blocking_input_stops_before_document_and_final_rule_is_conditional(self) -> None:
        text = self.read("codex")
        self.assertIn(
            "If an input is blocking, stop before writing the consult, ask one pointed question, and do not apply the Final Output Rule until the user answers",
            text,
        )
        self.assertIn("Stop before writing the consult, ask one pointed question, and do not return a document path", text)
        self.assertIn("Apply this rule only when no blocking input remains and a consult document was produced", text)
        self.assertIn("If an input is blocking, stop before writing the consult, ask one pointed question, and do not return a document path", text)

    def test_discover_remains_analysis_only_unless_recommendations_are_requested(self) -> None:
        text = self.read("codex")
        discover = text.split("### Discover", 1)[1].split("### Verify", 1)[0]
        self.assertIn("Perform a fresh independent assessment", discover)
        self.assertIn(
            "Do not request recommendations, next actions, or an implementation plan unless the user explicitly asks for them",
            discover,
        )

    def test_recommendation_grounding_uses_evidence_and_user_authority(self) -> None:
        text = self.read("codex")
        grounding = (
            "Ground recommendations in primary evidence and the applicable user requirements, selected decisions, preferences, and decision criteria. "
            "Label extrapolations beyond those inputs as inferences with confidence and missing evidence."
        )
        self.assertIn(grounding, text)
        self.assertIn("Preserve hard user requirements separately from soft preferences and decision criteria", text)
        self.assertIn("Treat selected decisions as constraints unless the user explicitly asks to reopen them", text)

    def test_source_manifest_output_depth_and_artifacts_are_proportional(self) -> None:
        text = self.read("codex")
        self.assertIn("Build a proportional source manifest", text)
        self.assertIn("Do not turn a broad task into an exhaustive file checklist", text)
        self.assertIn("Do not require every relevant file to be named in advance", text)
        self.assertIn("focused verification or bounded question: about 500–900 words", text)
        self.assertIn("narrow code, PR, or defect review: about 800–1,200 words", text)
        self.assertIn(
            "multi-repository refinement, decision support, or execution planning: about 1,500–3,000 words",
            text,
        )
        self.assertIn("broad architecture or research synthesis: about 2,500–5,000 words", text)
        self.assertIn("These are planning ranges, not quotas", text)
        self.assertNotIn("Ask ChatGPT Pro for one mid-sized report: target 800–1,200 words", text)

    def test_template_and_self_review_are_adaptive(self) -> None:
        text = self.read("codex")
        self.assertIn("Include only sections that contain useful information", text)
        self.assertIn("[Insert the primary mode block.", text)
        self.assertIn("[Include only the applicable task-pattern fields below.]", text)
        self.assertIn("Is a secondary mode genuinely necessary, bounded, ordered after the primary result, and non-conflicting?", text)
        self.assertIn("Did I distinguish selected decisions from softer preferences and decision criteria?", text)
        for task_pattern in (
            "**Code or change review:**",
            "**Debugging:**",
            "**Architecture or system review:**",
            "**Research or comparison:**",
            "**Decision support:**",
            "**Execution planning:**",
            "**Document or log analysis:**",
        ):
            self.assertIn(task_pattern, text)

    def test_recorded_conformance_matrix_covers_semantic_routes(self) -> None:
        text = CONFORMANCE.read_text(encoding="utf-8")
        for case_id in (
            "discover-fresh-audit",
            "verify-hypothesis",
            "refine-existing-synthesis",
            "decide-hard-soft",
            "execute-selected-direction",
            "blocking-input",
            "material-nonblocking",
            "broad-architecture",
            "pdf-opt-in",
            "secondary-mode-composition",
        ):
            self.assertIn(f"`{case_id}`", text)
        self.assertIn("Single same-agent manual conformance pass", text)
        self.assertIn("10/10 PASS", text)
        self.assertIn("does not establish general model performance", text)


if __name__ == "__main__":
    unittest.main()
