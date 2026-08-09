"""Behavior contracts for the portable claim-discipline reference and integrations."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCE = REPO_ROOT / "docs" / "claim-discipline.md"
CASES = REPO_ROOT / "tests" / "fixtures" / "claim_discipline_cases.json"
CONFORMANCE = REPO_ROOT / "tests" / "claim_discipline_conformance.md"


class ClaimDisciplineContractsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = REFERENCE.read_text(encoding="utf-8")
        self.packet = json.loads(CASES.read_text(encoding="utf-8"))

    def test_reference_defines_evidence_first_claim_selection(self) -> None:
        for phrase in (
            "Evidence-first claim selection",
            "non-vacuous",
            "alternative explanations",
            "counterevidence",
            "supported conditions",
            "incidental conditions",
            "explicit non-claims",
            "downstream decision",
            "strong discriminator, weak conclusion",
            "Safety rules",
            "authorization boundaries",
            "guardrails",
            "acceptance proof",
        ):
            self.assertIn(phrase, self.reference, phrase)
        self.assertNotIn("evidence or decision boundary", self.reference)

    def test_behavior_fixture_covers_required_overgeneralization_consequences(self) -> None:
        cases = self.packet["cases"]
        required_ids = {
            "provider-specific-overgeneralization",
            "several-sessions-one-project",
            "one-failed-implementation",
            "absolute-versus-scoped",
            "vacuous-weakening",
            "inadequate-discriminator",
            "safety-and-authorization-boundary",
        }
        self.assertEqual({case["id"] for case in cases}, required_ids)
        for case in cases:
            for field in (
                "failure_mode",
                "observation",
                "weakest_supported_conclusion",
                "explicit_non_claim",
                "decision_boundary",
            ):
                self.assertTrue(case[field].strip(), (case["id"], field))
            self.assertTrue(case["must_preserve"], case["id"])
            self.assertTrue(case["must_avoid"], case["id"])

        anchors = {
            "provider-specific-overgeneralization": ("Provider-specific evidence", "provider-independent"),
            "several-sessions-one-project": ("Several sessions from one project", "cross-project"),
            "one-failed-implementation": ("One failed implementation", "mechanism family"),
            "absolute-versus-scoped": ("Absolute versus scoped claims", "always"),
            "vacuous-weakening": ("Vacuous weakening", "non-vacuous"),
            "inadequate-discriminator": ("Inadequate discriminator", "unresolved"),
            "safety-and-authorization-boundary": ("strong boundaries", "must not remove"),
        }
        for case_id, required_phrases in anchors.items():
            for phrase in required_phrases:
                self.assertIn(phrase, self.reference, (case_id, phrase))

    def test_existing_claim_bearing_surfaces_load_one_conditional_reference(self) -> None:
        for platform in ("codex", "claude"):
            for skill in ("design-experiment", "review-experiment", "distill-source", "integrate-research", "skill-lifecycle", "systemic-diagnosis"):
                text = (REPO_ROOT / platform / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual(text.count("docs/claim-discipline.md"), 1, (platform, skill))

        for path in (
            "codex/AGENTS.md",
            "claude/rules/think-before-coding.md",
            "claude/rules/conciseness.md",
        ):
            self.assertNotIn("docs/claim-discipline.md", (REPO_ROOT / path).read_text(encoding="utf-8"), path)

    def test_templates_keep_claim_ladder_and_readout_separation_in_existing_fields(self) -> None:
        for path in (
            "codex/skills/design-experiment/templates/protocol.md",
            "claude/skills/design-experiment/templates/protocol.md",
        ):
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            for phrase in ("weakest non-vacuous positive claim", "exact rejection scope", "next discriminator"):
                self.assertIn(phrase, text, path)
        for path in (
            "codex/skills/review-experiment/templates/readout.md",
            "claude/skills/review-experiment/templates/readout.md",
        ):
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            for phrase in ("weakest non-vacuous conclusion", "counterevidence", "explicit non-claims"):
                self.assertIn(phrase, text, path)

    def test_recorded_skill_interface_conformance_covers_required_cases(self) -> None:
        text = CONFORMANCE.read_text(encoding="utf-8")
        for case in self.packet["cases"]:
            self.assertIn(f"`{case['id']}`", text)
        self.assertIn("Single same-agent manual conformance pass", text)
        self.assertIn("14/14 PASS", text)
        self.assertIn("does not establish general model performance", text)
        self.assertEqual(text.count("Design-experiment — PASS"), 7)
        self.assertEqual(text.count("Review-experiment — PASS"), 7)

    def test_authoritative_guidance_keeps_scope_conditional_without_global_loading(self) -> None:
        authoring = (REPO_ROOT / "docs/skill-authoring-principles.md").read_text(encoding="utf-8")
        context = (REPO_ROOT / "docs/context-file-authoring.md").read_text(encoding="utf-8")
        lifecycle = (REPO_ROOT / "docs/skill-lifecycle-policy.md").read_text(encoding="utf-8")
        self.assertIn("least restrictive behavior", authoring)
        self.assertIn("The broader the loading surface, the more evidence is required", context)
        self.assertIn("Thin evidence should produce a narrow rule", lifecycle)
        self.assertIn("Claim weakening must not remove, dilute, or bypass", self.reference)

    def test_existing_authority_and_adoption_boundaries_remain_strong(self) -> None:
        for platform in ("codex", "claude"):
            for skill in ("design-experiment", "review-experiment"):
                text = (REPO_ROOT / platform / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(
                    "Never authorize adoption or a default change" in text
                    or "never authorizes adoption or a default change" in text,
                    (platform, skill),
                )
                self.assertIn("Never mutate an Area Brief", text, (platform, skill))
        boundary_phrases = {
            "AGENTS.md": ("Ask the operator before", "live mutation"),
            "codex/AGENTS.md": ("External writes, destructive actions", "confirmation"),
            "claude/rules/think-before-coding.md": ("External writes, destructive actions", "confirmation"),
        }
        for path, phrases in boundary_phrases.items():
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase.lower(), text.lower(), path)

    def test_no_new_skill_entity_or_numeric_weakness_surface_exists(self) -> None:
        for platform in ("codex", "claude"):
            skill_root = REPO_ROOT / platform / "skills"
            self.assertFalse((skill_root / "claim-discipline").exists())
        catalog = (REPO_ROOT / "catalog.json").read_text(encoding="utf-8")
        self.assertNotIn('"id": "claim-discipline"', catalog)
        self.assertNotIn("weakness_score", self.reference)
        self.assertNotIn("hypothesis_id", self.reference)


if __name__ == "__main__":
    unittest.main()
