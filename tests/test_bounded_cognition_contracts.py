"""Behavior contracts for bounded-cognition and source-distillation guidance."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class BoundedCognitionContractsTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (REPO_ROOT / path).read_text(encoding="utf-8")

    def read_skill(self, platform: str, skill: str) -> str:
        source = "shared" if skill in {"surface-unknowns", "systemic-diagnosis"} else platform
        return self.read(f"{source}/skills/{skill}/SKILL.md")

    def test_global_surfaces_encode_local_reasoning_and_bounded_failure(self) -> None:
        codex = self.read("codex/AGENTS.md")
        think = self.read("claude/rules/think-before-coding.md")
        surgical = self.read("claude/rules/surgical-changes.md")

        for text in (codex, think):
            self.assertIn("local reasoning", text)
            self.assertIn("bounded failure", text)
            self.assertIn("blast radius", text)
            self.assertIn("local component correctness is not sufficient", text)
            self.assertIn("first find and reuse the existing path for its durable behavior", text)
            self.assertIn("do not implement a parallel copy in the nearest adapter", text)

        for text in (codex, surgical):
            self.assertIn("small diff", text.lower())
            self.assertIn("hidden operational knowledge", text)
            self.assertIn("proportionate safeguards", text)

    def test_global_surfaces_require_consequence_level_test_design(self) -> None:
        for path in ("codex/AGENTS.md", "claude/rules/think-before-coding.md"):
            text = self.read(path)
            for phrase in (
                "Test consequences, not decisions.",
                "production defect it would catch",
                "synthetic valid and invalid inputs",
                "test that enforcement through observable behavior",
                "artifact or contract under test",
                "what the remaining production code still guarantees",
            ):
                self.assertIn(phrase, text, path)

    def test_global_authorization_preserves_mixed_requests_and_existing_consent(self) -> None:
        for path in ("codex/AGENTS.md", "claude/rules/think-before-coding.md"):
            text = self.read(path)
            self.assertIn("unless the current session already authorizes that action and scope", text)
        claude = self.read("claude/rules/think-before-coding.md")
        self.assertIn("Do not implement unless the request also authorizes changes", claude)
        self.assertIn("Ask only for user-owned or difficult-to-reverse choices", claude)
        self.assertNotIn("If you are not confident in it, ask instead of guessing", claude)

    def test_denials_distinguish_user_refusal_from_runtime_enforcement(self) -> None:
        text = self.read("claude/CLAUDE.md")
        for source in ("explicit user refusal", "automatic approval denial", "sandbox restriction", "application failure"):
            self.assertIn(source, text)
        self.assertIn("Do not retry, broaden, or route around a denied action", text)
        self.assertIn("existing authorization is not permission to bypass a denial", text)
        self.assertIn("runtime’s supported escalation procedure", text)
        self.assertNotIn("A denied tool call means the user declined it", text)

    def test_tdd_and_review_twins_require_reviewed_behavior_spine_semantics(self) -> None:
        for platform in ("codex", "claude"):
            tdd = self.read_skill(platform, "tdd")
            for phrase in (
                "Keep behavior authority separate from implementation",
                "supported public seam",
                "controlled external boundaries",
                "independent oracle",
                "claim ceiling",
                "red-before-green evidence",
                "legitimate implementation change that remains green",
                "plausible production defect that turns the spine red",
                "production defect it would catch",
                "observable consequence it protects",
                "documented public, safety, compatibility, or shipped-artifact contract",
                "production identifiers, generated keys, internal paths, or source shape",
                "implementation-derived rather than independent",
            ):
                self.assertIn(phrase, tdd, f"{platform} tdd: {phrase}")

            review = self.read_skill(platform, "review-change")
            for phrase in (
                "decision-locking assertions",
                "production defect and observable consequence",
                "supported public seam",
                "controlled boundaries",
                "independent oracle",
                "claim ceiling",
                "legitimate implementation change remains green",
                "plausible production defect turns it red",
                "detector ledger",
                "documented public, safety, compatibility, or shipped-artifact contract",
                "Do not infer oracle independence from a green suite",
                "production identifiers, generated keys, internal paths, or source shape",
                "isolated scratch state",
            ):
                self.assertIn(phrase, review, f"{platform} review-change: {phrase}")

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

    def test_review_twins_discriminate_semantic_fidelity_from_plausible_shortcuts(self) -> None:
        for platform in ("codex", "claude"):
            review = self.read_skill(platform, "review-change")
            for phrase in (
                "implements a source or paper, claims a behavior-preserving refactor, or transforms data whose meaning must survive",
                "ordinary happy-path test could accept a plausible semantic shortcut",
                "only when semantic fidelity is material",
            ):
                self.assertIn(phrase, review, f"{platform}: {phrase}")

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
                text = self.read_skill(platform, skill)
                reference_paragraphs = [
                    paragraph
                    for paragraph in text.split("\n\n")
                    if "docs/whole-system-review.md" in paragraph
                ]
                self.assertEqual(len(reference_paragraphs), 1)
                self.assertIn("skip", reference_paragraphs[0].lower())

    def test_surface_unknowns_twins_define_mode_roles_and_bounded_routing(self) -> None:
        codex = self.read_skill("codex", "surface-unknowns")
        claude = self.read_skill("claude", "surface-unknowns")
        self.assertEqual(codex, claude)

        for text in (codex, claude):
            self.assertIn("**Explicit discovery pass:** Driver", text)
            self.assertIn("Use only when the user explicitly invokes this skill or asks to identify unknowns or blind spots", text)
            self.assertIn("ordinary ambiguity, source checking, and assumption handling stay with the active workflow", text)
            self.assertIn("Keep exactly one driver active", text)
            self.assertIn("return the bounded finding to that driver rather than creating a parallel driver", text)
            self.assertNotIn("Autonomous checkpoint", text)
            self.assertNotIn("Re-entry Guard", text)
            self.assertIn("highest expected decision value net of inspection, delay, and interruption cost", text)
            self.assertIn("not empirically validated, exhaustive categories or mandatory stages", text)
            self.assertIn("teach enough structure before asking them to choose", text)
            self.assertIn("why its plausible alternatives differ", text)
            self.assertIn("Never claim exhaustive discovery of unknown unknowns", text)
            self.assertIn("Do not turn ordinary reversible implementation discretion into a user approval gate", text)
            self.assertIn("Tests and review establish implementation evidence", text)
            self.assertIn("explanation and transfer questions probe understanding", text)

    def test_global_surfaces_preserve_selective_uncertainty_behavior_without_named_invocation(self) -> None:
        codex = self.read("codex/AGENTS.md")
        think = self.read("claude/rules/think-before-coding.md")

        for text in (codex, think):
            self.assertNotIn("surface-unknowns", text)
            self.assertIn("multiple plausible", text)
            self.assertIn("materially different actions", text)
            self.assertIn("one interpretation dominates", text)
            self.assertIn("resolution costs more than it can change", text)
            self.assertIn("observed evidence, user decisions, supported inferences, assumptions, and unresolved unknowns", text)
            self.assertIn("remaining verification gaps in the final handoff", text)

    def test_surface_unknowns_codex_metadata_requires_explicit_invocation(self) -> None:
        metadata = self.read("codex/skills/surface-unknowns/agents/openai.yaml")
        self.assertIn('default_prompt: "Use $surface-unknowns', metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)

        catalog = self.read("catalog.json")
        surface_entry = catalog.split('"id": "surface-unknowns"', 1)[1].split('"id": "thermo-nuclear-code-quality-review"', 1)[0]
        self.assertNotIn('"role:router"', surface_entry)

    def test_systemic_diagnosis_is_an_explicit_optional_lens(self) -> None:
        text = self.read("shared/skills/systemic-diagnosis/SKILL.md")
        selector = self.read("docs/systemic-diagnosis-selector.md")
        metadata = self.read("codex/skills/systemic-diagnosis/agents/openai.yaml")
        self.assertIn("Use only when the user explicitly requests systemic diagnosis", text)
        self.assertIn("Do not infer activation from the shape of an ordinary task", text)
        self.assertIn("Normal uncertainty handling, source checking, and bounded software diagnosis remain with the active workflow", text)
        self.assertIn("adds questions and evidence discipline", text)
        self.assertIn("only after the user explicitly requests", selector)
        self.assertIn("An ordinary recurring or cross-boundary symptom does not activate it", selector)
        self.assertIn('default_prompt: "Use $systemic-diagnosis', metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_no_source_branded_umbrella_skill_was_added(self) -> None:
        for platform in ("codex", "claude"):
            self.assertFalse((REPO_ROOT / platform / "skills" / "shape-of-the-system").exists())

    def test_architecture_review_scopes_candidates_and_stops_for_selection(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read_skill(platform, "architecture-review")
            for behavior in (
                "upcoming work",
                "none supplies a scope",
                "history to prioritize repeatedly changed paths",
                "churn as a priority signal",
                "not evidence of an architecture defect",
                "valid to return no candidates",
                "do not fill a quota",
                "Stop for selection",
                "one user-selected candidate",
                "grill-with-docs",
                "do not develop implementation detail for or schedule unselected candidates",
                "When no candidate clears the bar",
                "Candidates: None",
                "Recommended next step: No action",
                "selected candidate's grilling yields concrete work",
                "do not create tasks directly",
                "harness-record",
                "inbox items",
                "without elaborating or scheduling them",
            ):
                self.assertIn(behavior, text, f"{platform}: {behavior}")

    def test_architecture_review_conditionally_applies_multi_entrypoint_capability_lens(self) -> None:
        reference = self.read("docs/multi-entrypoint-capability-review.md")
        for behavior in (
            "two or more entrypoints reach the same durable behavior",
            "Skip it when the change stays behind one existing interface",
            "Map responsibilities onto the project's current names",
            "Map every entrypoint and bypass",
            "transaction or commit boundary and its owner",
            "duplicate intentionally when owners or reasons to change differ",
            "capture it durably in project documentation or through `harness-record` before implementing",
            "keep the seam internal rather than introducing a port for testing alone",
            "no capability-boundary delta",
            "Do not prescribe `app/`, `capabilities/`, `domain/`, `contracts/`, `platform/`, or `shared/` directories",
            "Do not create a new architecture or capability-contract skill",
        ):
            self.assertIn(behavior, reference)

        for platform in ("codex", "claude"):
            text = self.read_skill(platform, "architecture-review")
            reference_paragraphs = [
                paragraph
                for paragraph in text.split("\n\n")
                if "docs/multi-entrypoint-capability-review.md" in paragraph
            ]
            self.assertEqual(len(reference_paragraphs), 1)
            self.assertIn("When the reviewed change adds an entrypoint or touches durable behavior reachable from two or more entrypoints", reference_paragraphs[0])
            self.assertIn("Skip it when work stays behind one existing interface, entrypoints share only a product-free primitive, or the project already has one proven behavior path and the new work does not change it.", reference_paragraphs[0])
            self.assertFalse((REPO_ROOT / platform / "skills" / "capability-core-adapters").exists())
            self.assertFalse((REPO_ROOT / platform / "skills" / "capability-contract").exists())

    def test_architecture_review_conditionally_applies_comprehensive_audit_protocol(self) -> None:
        reference = self.read("docs/comprehensive-codebase-audit.md")
        for behavior in (
            "explicitly asks for a comprehensive, exhaustive, repo-wide, or entire-codebase architecture audit",
            "Inventory every identifiable subsystem",
            "stable ID and name",
            "exact ownership boundary",
            "fresh read-only lane",
            "exact boundary that does not overlap another lane",
            "bounded to the number the coordinator can actively manage",
            "schedule remaining inventory rows in explicit batches",
            "mark the audit `partial`",
            "do not claim independently validated comprehensive completion",
            "fixed maximum of two material findings or `skip` per lane",
            "split it into narrower inventory rows and review each in its own lane",
            "Verdict: recommend | skip",
            "Confidence: high | medium | low",
            "Dependency shape: <in-process | local-substitutable | remote-owned | true-external>",
            "independently verifies every finding",
            "Deduplicate overlapping findings",
            "Overlap and duplication",
            "Materiality and over-abstraction",
            "Schema completeness",
            "Dependency-aware ranking",
            "fresh Luna lanes",
            "do not automatically escalate to a Sol reviewer",
            "Unchanged-repository completion",
            "repository must be unchanged by the audit",
            "each accepted finding as exactly one numbered entry under the normal `Candidates:` heading",
            "Only after the operator selects one candidate",
            "grill-with-docs",
        ):
            self.assertIn(behavior, reference)
        self.assertIn("Candidates:\n1. <short name>", reference)
        self.assertIn("If scratch writes are unavailable, keep the ledger in visible session state", reference)
        self.assertIn("first ledger entry declares the audited boundary", reference)
        self.assertIn("prepare-dynamic-workflow", reference)
        self.assertIn("explicitly invoked Sol–Luna on Codex", reference)

        for platform in ("codex", "claude"):
            text = self.read_skill(platform, "architecture-review")
            reference_paragraphs = [
                paragraph
                for paragraph in text.split("\n\n")
                if "docs/comprehensive-codebase-audit.md" in paragraph
            ]
            self.assertEqual(len(reference_paragraphs), 1)
            self.assertIn("explicitly asks for a comprehensive, exhaustive, repo-wide, or entire-codebase audit", reference_paragraphs[0])
            self.assertIn("ordinary scoped reviews continue with this workflow", reference_paragraphs[0])
            self.assertIn("explicitly requests a comprehensive, exhaustive, repo-wide, or entire-codebase architecture audit", text)

    def test_catalog_keeps_visualize_outside_agents_ownership(self) -> None:
        catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        foreign = catalog["boundary_notes"]["foreign"]
        self.assertFalse(foreign["manage"])
        self.assertIn("codex-primary-runtime", foreign["assets"])
        self.assertIn("Visualize (Codex bundled/plugin capability)", foreign["assets"])
        self.assertIn("Outside Agents ownership and management", foreign["note"])
        self.assertIn("never installed, updated, or pruned", foreign["note"])

    def test_grill_with_docs_routes_unknowns_to_evidence_without_forcing_a_choice(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read_skill(platform, "grill-with-docs")
            for behavior in (
                "**Needs evidence**",
                "If a material branch",
                "cheapest reliable discriminator",
                "Record it as an open question or stop gate",
                "stop pursuing that branch",
                "resume it only after the evidence exists",
                "prototype",
                "ask-chatgpt-pro",
                "design-experiment",
                'Treat "I don\'t know" as valid information',
                "preserve a user-owned choice",
                "Do not keep rephrasing a question",
                "unless they require missing empirical or experiential evidence",
                "unrouted **Needs evidence** item",
                "evidence route",
            ):
                self.assertIn(behavior, text, f"{platform}: {behavior}")


if __name__ == "__main__":
    unittest.main()
