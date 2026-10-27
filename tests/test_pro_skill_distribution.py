"""Installation structure checks; behavioral conformance is recorded separately."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProSkillDistributionTest(unittest.TestCase):
    def test_pro_skills_are_discoverable_in_supported_runtimes(self) -> None:
        skills = {entry["id"]: entry for entry in json.loads((ROOT / "catalog.json").read_text())["skills"]}
        for name in ("ask-pro", "answer-pro"):
            with self.subTest(name=name):
                self.assertEqual(set(skills[name]["platforms"]), {"codex", "claude", "pi"})
                self.assertTrue((ROOT / "shared/skills" / name / "SKILL.md").is_file())
                metadata = (ROOT / "codex/skills" / name / "agents/openai.yaml").read_text()
                self.assertNotIn("allow_implicit_invocation: false", metadata)
        for retired in ("ask-chatgpt-pro", "ask-oracle"):
            self.assertNotIn(retired, skills)
            self.assertFalse((ROOT / "shared/skills" / retired).exists())
            self.assertFalse((ROOT / "codex/skills" / retired).exists())


if __name__ == "__main__":
    unittest.main()
