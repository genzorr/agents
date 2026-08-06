"""Safety and packaging contracts for the storage-cleanup skill twins."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class StorageCleanupContractsTest(unittest.TestCase):
    def read_skill(self, platform: str) -> str:
        return (REPO_ROOT / platform / "skills" / "storage-cleanup" / "SKILL.md").read_text(encoding="utf-8")

    def test_twins_share_the_same_cleanup_contract(self) -> None:
        codex = self.read_skill("codex")
        claude = self.read_skill("claude").replace("disable-model-invocation: true\n", "")
        self.assertEqual(codex, claude)

    def test_cleanup_is_explicit_and_preserves_agent_history(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read_skill(platform)
            for phrase in (
                "Agent session/history data is protected",
                "Never delete or propose deleting Codex, Claude, or other agent session history",
                "Age, completion status, inactivity, or size does not make this data disposable",
                "Inspection is read-only",
                "Present the cleanup plan and stop",
                "explicit approval of the specific candidate(s) or bounded group(s)",
                "No blanket temp-directory cleanup",
                "No autonomous recurring cleanup",
                "Non-agent logs",
                "Agent session/history state and logs",
                "Protected/unknown",
            ):
                self.assertIn(phrase, text, (platform, phrase))

    def test_platforms_disable_implicit_invocation(self) -> None:
        claude = self.read_skill("claude")
        self.assertIn("disable-model-invocation: true", claude)

        metadata = (
            REPO_ROOT / "codex" / "skills" / "storage-cleanup" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_catalog_and_installers_manage_both_twins(self) -> None:
        catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        entry = next(item for item in catalog["skills"] if item["id"] == "storage-cleanup")
        self.assertEqual(set(entry["platforms"]), {"codex", "claude"})
        self.assertEqual(entry["source"]["codex"], "codex/skills/storage-cleanup/SKILL.md")
        self.assertEqual(entry["source"]["claude"], "claude/skills/storage-cleanup/SKILL.md")

        for installer in ("scripts/install-codex.sh", "scripts/install-claude.sh"):
            text = (REPO_ROOT / installer).read_text(encoding="utf-8")
            self.assertIn("|storage-cleanup|", text, installer)


if __name__ == "__main__":
    unittest.main()
