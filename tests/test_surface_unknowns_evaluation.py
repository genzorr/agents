"""Integrity checks for the surface-unknowns behavioral evaluation packet."""

import json
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = REPO_ROOT / "tests" / "fixtures" / "surface_unknowns_cases.json"


class SurfaceUnknownsEvaluationPacketTest(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        self.cases = self.packet["cases"]

    def test_packet_has_balanced_required_families(self) -> None:
        counts = Counter(case["family"] for case in self.cases)
        self.assertEqual(
            set(counts),
            {
                "explicit-discovery",
                "ordinary-uncertainty",
                "appropriate-no-op",
                "overlap-routing",
                "plan-invalidation",
            },
        )
        self.assertTrue(all(count >= 3 for count in counts.values()))

    def test_cases_have_unique_ids_and_complete_scoring_contracts(self) -> None:
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 15)

        allowed_modes = {"explicit", "ordinary", "no-op", "handoff", "return"}
        for case in self.cases:
            self.assertTrue(case["prompt"].strip())
            self.assertIn(case["expected_mode"], allowed_modes)
            self.assertTrue(case["expected_driver"].strip())
            self.assertIn(case["question_budget"], (0, 1))
            self.assertIsInstance(case["separate_artifact"], bool)
            self.assertIsInstance(case["reentry_allowed"], bool)
            self.assertTrue(case["must_observe"])
            self.assertTrue(case["must_avoid"])

    def test_no_op_and_ordinary_cases_forbid_extra_surface_pass(self) -> None:
        no_ops = [case for case in self.cases if case["family"] == "appropriate-no-op"]
        self.assertTrue(all(case["question_budget"] == 0 for case in no_ops))
        self.assertTrue(all(case["separate_artifact"] is False for case in no_ops))

        ordinary = [case for case in self.cases if case["family"] == "ordinary-uncertainty"]
        self.assertTrue(all(case["expected_mode"] == "ordinary" for case in ordinary))
        self.assertTrue(all(case["expected_driver"] == "current" for case in ordinary))
        self.assertTrue(all(case["separate_artifact"] is False for case in ordinary))
        self.assertTrue(all(case["reentry_allowed"] is False for case in ordinary))

    def test_recorded_results_preserve_exploratory_claim_boundary(self) -> None:
        results = (REPO_ROOT / "tests" / "surface_unknowns_evaluation.md").read_text(encoding="utf-8")
        self.assertIn("not empirical validation", results)
        self.assertIn("explicitly requested", results)
        self.assertIn("ordinary uncertainty handling", results)
        self.assertIn("no separate surface-unknowns pass", results)
        self.assertIn("does not establish host-level invocation precision", results)
        self.assertIn("Historical Evaluation Of The Prior Contract", results)
        self.assertIn("c33b61b3e43fc174171caefea243778301008c631e54bf71c55a0d4554255706", results)
        self.assertIn("Historical full revised total: 16/16", results)
        self.assertIn("not a validation claim for the current explicit-only behavior", results)


if __name__ == "__main__":
    unittest.main()
