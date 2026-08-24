"""Behavior and packaging contracts for text pruning and lifecycle evidence intake."""

import json
import unittest
from pathlib import Path

from scripts.agent_catalog import desired_files, load_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "shared" / "skills" / "text-prune" / "SKILL.md"
CASES = REPO_ROOT / "tests" / "fixtures" / "text_prune_cases.json"
CONFORMANCE = REPO_ROOT / "tests" / "text_prune_conformance.md"


class TextPruneContractsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = SKILL.read_text(encoding="utf-8")
        self.packet = json.loads(CASES.read_text(encoding="utf-8"))

    def test_shared_skill_packages_all_modes_and_role_boundaries(self) -> None:
        references = {
            "Plain prose": "references/plain-prose.md",
            "Evidence-bearing report": "references/evidence-bearing-report.md",
            "Durable documentation": "references/durable-documentation.md",
            "Instructions and prompts": "references/instructions-and-prompts.md",
            "Code comments and docstrings": "references/code-comments-and-docstrings.md",
        }
        for mode, reference in references.items():
            self.assertIn(mode, self.skill)
            self.assertIn(f"]({reference})", self.skill)
            self.assertTrue((SKILL.parent / reference).is_file())
        for phrase in (
            "Use this skill as the driver when pruning text is the whole request",
            "act as a helper",
            "without taking authorization, verification, lifecycle, or completion ownership",
            "A no-op is successful",
            "information-preserving under the stated checks",
            "never as unconditionally lossless",
            "Leave `FLAG` content unchanged",
        ):
            self.assertIn(phrase, self.skill)

    def test_routing_keeps_distinct_owners(self) -> None:
        for phrase in (
            "Route decisions to add, change, slim, merge, deprecate, remove, or keep an instruction asset to `skill-lifecycle`",
            "Route pruning or uninstalling materialized assets to the owning installer contract",
            "Keep `doc-audit` audit-only",
            "Installed `~/.codex` (runtime-home)",
            "`~/.claude` (runtime-home)",
            "redirect to the repository that physically owns the source",
        ):
            self.assertIn(phrase, self.skill)

    def test_mode_references_preserve_high_risk_content_and_consumers(self) -> None:
        report = (SKILL.parent / "references" / "evidence-bearing-report.md").read_text(encoding="utf-8")
        durable = (SKILL.parent / "references" / "durable-documentation.md").read_text(encoding="utf-8")
        instructions = (SKILL.parent / "references" / "instructions-and-prompts.md").read_text(encoding="utf-8")
        comments = (SKILL.parent / "references" / "code-comments-and-docstrings.md").read_text(encoding="utf-8")
        for phrase in ("observations", "counterevidence", "uncertainty", "non-claims", "observation, conclusion, and decision distinct"):
            self.assertIn(phrase, report)
        for phrase in ("exact-phrase", "source-shape", "heading or anchor", "catalog and traveling-reference", "Do not re-wrap or unwrap untouched prose", "paired consumer update"):
            self.assertTrue(phrase in durable or phrase in instructions, phrase)
        for phrase in ("licenses", "generated markers", "suppression directives", "doctest", "Edit no executable behavior"):
            self.assertIn(phrase, comments)

    def test_fixture_covers_required_consequences(self) -> None:
        cases = self.packet["cases"]
        required_ids = {
            "plain-prose-no-op",
            "plain-prose-ambiguous-repetition",
            "report-deceptive-repetition",
            "report-preserved-caveat",
            "report-evidence-separation",
            "durable-stale-unproven",
            "durable-exact-links-and-anchors",
            "durable-exact-phrase-consumer",
            "durable-authorized-paired-consumer",
            "durable-untouched-prose-no-reflow",
            "instruction-installed-home-refusal",
            "instruction-boundary-preservation",
            "instruction-catalog-and-traveling-reference",
            "comment-license",
            "comment-doctest-example",
            "comment-tool-directive",
            "helper-beneath-driver",
            "route-prune-skills",
            "route-prune-installed-assets",
            "discovery-natural-language-positive",
            "discovery-unrelated-writing-negative",
        }
        self.assertEqual({case["id"] for case in cases}, required_ids)
        self.assertEqual({case["mode"] for case in cases}, {"plain-prose", "evidence-bearing-report", "durable-documentation", "instructions-and-prompts", "code-comments-and-docstrings", "routing"})
        for case in cases:
            self.assertTrue(case["request"].strip(), case["id"])
            self.assertTrue(case["expected"].strip(), case["id"])
            self.assertTrue(case["must_preserve"], case["id"])
            self.assertTrue(case["must_avoid"], case["id"])

    def test_recorded_conformance_covers_every_fixture_without_overclaiming(self) -> None:
        conformance = CONFORMANCE.read_text(encoding="utf-8")
        for case in self.packet["cases"]:
            self.assertIn(f"`{case['id']}`", conformance)
        self.assertIn("21/21 PASS", conformance)
        self.assertIn("does not establish host-level trigger precision", conformance)
        self.assertIn("losslessness guarantee", conformance)

    def test_catalog_materializes_shared_skill_references_and_codex_metadata(self) -> None:
        assets = load_catalog(REPO_ROOT)
        for platform in ("codex", "claude"):
            installed = desired_files(REPO_ROOT, assets, platform)
            skill_path = "skills/text-prune/SKILL.md"
            self.assertIn(skill_path, installed)
            self.assertEqual(installed[skill_path].source.resolve(), SKILL.resolve())
            for document in ("skill-authoring-principles.md", "context-file-authoring.md", "claim-discipline.md", "experiment-protocol-readout-contract.md"):
                target = f"skills/text-prune/docs/{document}"
                self.assertIn(target, installed)
                self.assertEqual(installed[target].asset.id, "text-prune")
        codex_installed = desired_files(REPO_ROOT, assets, "codex")
        self.assertIn("skills/text-prune/agents/openai.yaml", codex_installed)
        metadata = codex_installed["skills/text-prune/agents/openai.yaml"].source.read_text(encoding="utf-8")
        self.assertIn('default_prompt: "Use $text-prune', metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)

    def test_lifecycle_intake_is_version_bound_and_fail_closed(self) -> None:
        skill_lifecycle = (REPO_ROOT / "shared" / "skills" / "skill-lifecycle" / "SKILL.md").read_text(encoding="utf-8")
        policy = (REPO_ROOT / "docs" / "skill-lifecycle-policy.md").read_text(encoding="utf-8")
        for phrase in ("version-bound evidence route", "candidate as evidence, not a verdict", "session-harvester-owned materializer", "`insufficient_evidence`"):
            self.assertIn(phrase, skill_lifecycle)
        for phrase in (
            "proposal-only evidence source, not a lifecycle decision",
            "This intake route accepts `session-analysis-4`",
            "must map exactly to `add`, `change`, `slim`, `merge`, `deprecate`, `remove`, or `keep + watch`",
            "Only `actionable` may proceed to the normal lifecycle threshold assessment",
            "`asset_inventory.py materialize`",
            "fresh external-scratch output",
            "never hard-code a checkout path, reimplement the digest algorithm",
            "A current digest mismatch invalidates the proposal instead of silently rebasing it",
            "Use categorical findings plus `insufficient_evidence`; never compute an aggregate grade",
            "The session-analysis path has no per-skill invocation telemetry",
            "separate aggregate `usage_evidence.py` path",
            "Neither silence, absent exact events, nor zero aggregate observations establishes disuse",
        ):
            self.assertIn(phrase, policy)
        for dimension in ("discovery or invocation quality", "instruction adherence", "execution efficiency and rework", "observed outcome quality", "evidence coverage and attribution confidence"):
            self.assertIn(dimension, policy)

    def test_scalable_mechanism_tie_break_has_matching_constraints(self) -> None:
        for path in ("codex/AGENTS.md", "claude/rules/think-before-coding.md"):
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            ladder = text.index("reuse-before-build ladder")
            tie_break = text.index("when candidate designs otherwise satisfy", ladder)
            self.assertGreater(tie_break, ladder, path)
            for phrase in (
                "correctness, safety, authority, proportional-proof, cost, latency, and maintainability constraints",
                "stronger models, search, learning, evaluation, or compute",
                "task-specific heuristics",
                "does not override domain invariants, deterministic checks, or bounded task-specific logic",
                "does not license a new evaluator, judge, corpus, runner, dependency, or abstraction",
            ):
                self.assertIn(phrase, text, path)


if __name__ == "__main__":
    unittest.main()
