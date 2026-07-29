"""Integrity checks for the surface-unknowns behavioral evaluation packet."""

import hashlib
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
                "implicit-checkpoint",
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

        allowed_modes = {"explicit", "checkpoint", "no-op", "handoff", "return"}
        for case in self.cases:
            self.assertTrue(case["prompt"].strip())
            self.assertIn(case["expected_mode"], allowed_modes)
            self.assertTrue(case["expected_driver"].strip())
            self.assertIn(case["question_budget"], (0, 1))
            self.assertIsInstance(case["separate_artifact"], bool)
            self.assertIsInstance(case["reentry_allowed"], bool)
            self.assertTrue(case["must_observe"])
            self.assertTrue(case["must_avoid"])

    def test_no_op_and_reentry_cases_forbid_extra_work(self) -> None:
        no_ops = [case for case in self.cases if case["family"] == "appropriate-no-op"]
        self.assertTrue(all(case["question_budget"] == 0 for case in no_ops))
        self.assertTrue(all(case["separate_artifact"] is False for case in no_ops))

        reentry = next(case for case in self.cases if case["id"] == "plan-same-evidence-reentry")
        self.assertEqual(reentry["expected_mode"], "return")
        self.assertEqual(reentry["expected_driver"], "current")
        self.assertFalse(reentry["reentry_allowed"])

    def test_recorded_results_preserve_exploratory_claim_boundary(self) -> None:
        results = (REPO_ROOT / "tests" / "surface_unknowns_evaluation.md").read_text(encoding="utf-8")
        self.assertIn("Full revised total: 16/16 in one run per case.", results)
        self.assertIn("not empirical validation", results)
        self.assertIn("not whether the Codex host independently selects it", results)
        self.assertIn("does not establish a general performance gain over the base rules", results)

        evaluated_files = {
            "codex/skills/surface-unknowns/SKILL.md": "c68ec80dfa81a1a33ae102f5106ab13487145062e378e7fae7157a82760ad011",
            "codex/AGENTS.md": "2e4710e8771b02ba4a1d6f0b379ae44eee1fbfc5412002e0759fd50ddcc6a744",
            "tests/fixtures/surface_unknowns_cases.json": "c33b61b3e43fc174171caefea243778301008c631e54bf71c55a0d4554255706",
        }
        for path, expected_sha256 in evaluated_files.items():
            actual_sha256 = hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
            self.assertEqual(actual_sha256, expected_sha256, path)


if __name__ == "__main__":
    unittest.main()
