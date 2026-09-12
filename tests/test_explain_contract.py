from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARED_SKILL = ROOT / "shared" / "skills" / "explain"
CODEX_METADATA = ROOT / "codex" / "skills" / "explain" / "agents" / "openai.yaml"


class ExplainContractTest(unittest.TestCase):
    def test_shared_skill_keeps_the_explanation_in_chat_and_evidence_grounded(self) -> None:
        skill = (SHARED_SKILL / "SKILL.md").read_text(encoding="utf-8")

        for phrase in (
            "coherent explanation in the conversation",
            "small realistic example or execution path",
            "source anchors",
            "passive evidence",
            "do not require a fixed opening contract",
            "do not append a closing question by default",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

        self.assertNotIn("render_static.py", skill)
        self.assertNotIn("Default to static HTML", skill)

    def test_visuals_are_preferred_when_useful_with_a_complete_host_fallback(self) -> None:
        skill = (SHARED_SKILL / "SKILL.md").read_text(encoding="utf-8")

        for phrase in (
            "Prefer interactive visualizations when interaction improves understanding",
            "the bundled `visualize` skill is the primary route",
            "If the host does not provide that capability",
            "do not claim that the host can render an inline HTML or interactive visual",
            "do not force interactivity for a trivial fact",
            "standard plotting tools",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_visualizer_is_bounded_helper_and_explain_owns_the_narrative_contract(self) -> None:
        skill = (SHARED_SKILL / "SKILL.md").read_text(encoding="utf-8")

        for phrase in (
            "use it as a bounded helper for the visual surface",
            "rendering, embedding, accessibility",
            "Explain governs the surrounding causal narrative",
            "source anchors, limitations, and textual equivalent",
            "do not suppress Explain's complete explanation or evidence handoff",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_visualizer_and_export_boundaries_preserve_security_and_fidelity(self) -> None:
        skill = (SHARED_SKILL / "SKILL.md").read_text(encoding="utf-8")

        for phrase in (
            "Keep source-derived strings passive",
            "Encode labels as data",
            "Preserve direction, ownership, state transitions, failure paths",
            "Standalone diagram artifacts made through `archify` default to static editorial HTML",
            "interactive theme/export controls are opt-in",
            "Use Archify for explicit diagram-artifact requests",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

        self.assertFalse((SHARED_SKILL / "scripts" / "render_static.py").exists())

    def test_codex_metadata_routes_optional_interactive_visuals_without_changing_the_narrative_owner(self) -> None:
        metadata = CODEX_METADATA.read_text(encoding="utf-8")

        self.assertIn("$explain", metadata)
        self.assertIn("$visualize", metadata)
        self.assertIn("when interaction improves understanding", metadata)
        self.assertIn("keep prose plus evidence as the narrative", metadata)
        self.assertNotIn("default HTML", metadata)

    def test_archify_remains_the_exportable_diagram_route(self) -> None:
        for relative, invocation in (
            ("codex/skills/archify/SKILL.md", "`explain`"),
            ("claude/skills/archify/SKILL.md", "`/explain`"),
        ):
            with self.subTest(relative=relative):
                archify = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(f"When understanding is the goal, use {invocation}", archify)
                self.assertIn("exportable technical diagram artifact", archify)
                self.assertIn("examples/*.json", archify)
                self.assertIn("node bin/archify.mjs render", archify)
                self.assertIn("self-contained `.html`", archify)


if __name__ == "__main__":
    unittest.main()
