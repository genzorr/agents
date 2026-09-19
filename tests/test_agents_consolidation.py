"""Integration contracts for the shared Agents home and Devin configuration."""

from __future__ import annotations

import json
import hashlib
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.agent_catalog import load_catalog, validate_catalog


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME_VARIABLES = {
    "agents": "AGENTS_HOME",
    "codex": "CODEX_HOME",
    "claude": "CLAUDE_HOME",
    "devin": "DEVIN_HOME",
}


def run_installer(platform: str, home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, HOME_VARIABLES[platform]: str(home), "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / f"install-{platform}.sh"), *args],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


class AgentsConsolidationTest(unittest.TestCase):
    def test_every_installer_dry_run_leaves_a_fresh_home_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for platform in HOME_VARIABLES:
                with self.subTest(platform=platform):
                    home = root / platform
                    result = run_installer(platform, home, "--dry-run", "--diff")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertFalse(home.exists())

    def test_project_claude_surface_cannot_hide_the_common_agents_baseline(self) -> None:
        claude = REPO_ROOT / "CLAUDE.md"
        if not claude.exists():
            return
        imports_baseline = "@AGENTS.md" in claude.read_text(encoding="utf-8")
        aliases_baseline = claude.is_symlink() and os.readlink(claude) == "AGENTS.md"
        self.assertTrue(imports_baseline or aliases_baseline)

    def test_portable_skills_have_one_runtime_location(self) -> None:
        assets = load_catalog(REPO_ROOT)
        by_id = {asset.id: asset for asset in assets if asset.kind == "skill"}
        portable = {
            "babysit-pr",
            "design-experiment",
            "docker-optimize",
            "logging-optimize",
            "review-experiment",
            "skill-lifecycle",
            "thermo-nuclear-code-quality-review",
        }
        for asset_id in portable:
            with self.subTest(asset_id=asset_id):
                self.assertEqual(set(by_id[asset_id].platforms), {"agents", "claude"})
                self.assertNotIn("codex", by_id[asset_id].platforms)
                self.assertNotIn("devin", by_id[asset_id].platforms)

        for asset_id in {"ask-oracle", "ask-chatgpt-pro", "explain", "surface-unknowns", "systemic-diagnosis", "text-prune"}:
            with self.subTest(provider_specific=asset_id):
                self.assertIn("codex", by_id[asset_id].platforms)
                self.assertNotIn("agents", by_id[asset_id].platforms)

    def test_shared_state_is_order_independent_and_provider_installs_do_not_touch_it(self) -> None:
        for order in (("codex", "devin"), ("devin", "codex")):
            with self.subTest(order=order), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                agents_home = root / "agents"
                installed = run_installer("agents", agents_home)
                self.assertEqual(installed.returncode, 0, installed.stderr)
                shared_state = agents_home / ".agents-install-state.json"
                before = shared_state.read_bytes()

                for platform in order:
                    result = run_installer(platform, root / platform)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(shared_state.read_bytes(), before)

                repeated = run_installer("agents", agents_home)
                self.assertEqual(repeated.returncode, 0, repeated.stderr)
                self.assertEqual(shared_state.read_bytes(), before)

                wrong_home = run_installer("codex", agents_home)
                self.assertEqual(wrong_home.returncode, 1, wrong_home.stderr)
                self.assertIn("expected schema 2 for codex", wrong_home.stderr)
                self.assertEqual(shared_state.read_bytes(), before)

                codex_state = root / "codex/.agents-install-state.json"
                codex_before = codex_state.read_bytes()
                wrong_shared = run_installer("agents", root / "codex")
                self.assertEqual(wrong_shared.returncode, 1, wrong_shared.stderr)
                self.assertIn("expected schema 2 for agents", wrong_shared.stderr)
                self.assertEqual(codex_state.read_bytes(), codex_before)

                wrong_devin = run_installer("devin", agents_home)
                self.assertEqual(wrong_devin.returncode, 1, wrong_devin.stderr)
                self.assertIn("expected schema 2 for devin", wrong_devin.stderr)
                self.assertEqual(shared_state.read_bytes(), before)

                devin_state = root / "devin/.agents-install-state.json"
                devin_before = devin_state.read_bytes()
                wrong_shared = run_installer("agents", root / "devin")
                self.assertEqual(wrong_shared.returncode, 1, wrong_shared.stderr)
                self.assertIn("expected schema 2 for agents", wrong_shared.stderr)
                self.assertEqual(devin_state.read_bytes(), devin_before)
                self.assertTrue((agents_home / "skills/babysit-pr/SKILL.md").is_file())
                self.assertFalse((root / "codex/skills/babysit-pr").exists())
                self.assertFalse((root / "devin/skills/babysit-pr").exists())
                self.assertTrue((root / "codex/skills/ask-oracle/SKILL.md").is_file())

                foreign = agents_home / "skills/foreign/SKILL.md"
                foreign.parent.mkdir(parents=True)
                foreign.write_text("foreign\n", encoding="utf-8")
                pruned = run_installer("agents", agents_home, "--prune")
                self.assertEqual(pruned.returncode, 0, pruned.stderr)
                self.assertTrue(foreign.is_file())
                removed = run_installer("agents", agents_home, "--uninstall")
                self.assertEqual(removed.returncode, 0, removed.stderr)
                self.assertTrue(foreign.is_file())
                self.assertFalse((agents_home / "skills/babysit-pr").exists())

    def test_claude_keeps_managed_copies_of_portable_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            claude_home = Path(tmp) / "claude"
            result = run_installer("claude", claude_home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((claude_home / "skills/babysit-pr/SKILL.md").is_file())
            self.assertTrue((claude_home / "skills/ask-oracle/SKILL.md").is_file())

    def test_codex_prune_retires_only_the_recorded_legacy_shared_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agents_home = root / "agents"
            codex_home = root / "codex"
            shared = run_installer("agents", agents_home)
            self.assertEqual(shared.returncode, 0, shared.stderr)

            source = REPO_ROOT / "shared/skills/babysit-pr/SKILL.md"
            legacy = codex_home / "skills/babysit-pr/SKILL.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_bytes(source.read_bytes())
            mode = stat.S_IMODE(legacy.stat().st_mode)
            state = {
                "schema_version": 2,
                "owner": "agents",
                "platform": "codex",
                "files": {
                    "skills/babysit-pr/SKILL.md": {
                        "owner": "agents",
                        "asset_id": "babysit-pr",
                        "kind": "skill",
                        "sha256": hashlib.sha256(legacy.read_bytes()).hexdigest(),
                        "mode": format(mode, "04o"),
                        "baseline_known": True,
                    }
                },
                "adapters": {},
            }
            (codex_home / ".agents-install-state.json").write_text(json.dumps(state), encoding="utf-8")
            foreign = codex_home / "skills/foreign/SKILL.md"
            foreign.parent.mkdir(parents=True)
            foreign.write_text("foreign\n", encoding="utf-8")

            pruned = run_installer("codex", codex_home, "--prune")
            self.assertEqual(pruned.returncode, 0, pruned.stderr)
            self.assertFalse(legacy.exists())
            self.assertTrue(foreign.is_file())
            self.assertTrue((agents_home / "skills/babysit-pr/SKILL.md").is_file())

    def test_devin_config_merge_conflict_and_uninstall_are_leaf_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "devin"
            home.mkdir()
            config = home / "config.json"
            config.write_text(
                json.dumps({"theme_mode": "dark", "agent": {"model": "operator-model"}, "read_config_from": {"private_provider": True}}, indent=2) + "\n",
                encoding="utf-8",
            )

            installed = run_installer("devin", home)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            instructions = home / "AGENTS.md"
            self.assertEqual(instructions.read_bytes(), (REPO_ROOT / "devin/AGENTS.md").read_bytes())
            merged = json.loads(config.read_text())
            self.assertEqual(merged["theme_mode"], "dark")
            self.assertEqual(merged["agent"]["model"], "operator-model")
            self.assertTrue(merged["read_config_from"]["private_provider"])
            self.assertTrue(merged["read_config_from"]["agents_standard"])
            self.assertFalse(merged["read_config_from"]["claude"])

            repeated = run_installer("devin", home)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            before_conflict = json.loads(config.read_text())
            before_conflict["read_config_from"]["claude"] = 0
            config.write_text(json.dumps(before_conflict, indent=2) + "\n", encoding="utf-8")
            conflicted = run_installer("devin", home)
            self.assertEqual(conflicted.returncode, 2, conflicted.stderr)
            self.assertIn("recorded values were modified", conflicted.stderr)
            self.assertEqual(json.loads(config.read_text()), before_conflict)

            before_conflict["read_config_from"]["claude"] = False
            config.write_text(json.dumps(before_conflict, indent=2) + "\n", encoding="utf-8")
            removed = run_installer("devin", home, "--uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertEqual(
                json.loads(config.read_text()),
                {"theme_mode": "dark", "agent": {"model": "operator-model"}, "read_config_from": {"private_provider": True}},
            )
            self.assertFalse(instructions.exists())
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_devin_global_instructions_are_distinct_and_unmanaged_files_are_preserved(self) -> None:
        source = REPO_ROOT / "devin/AGENTS.md"
        text = source.read_text(encoding="utf-8")
        self.assertNotEqual(source.read_bytes(), (REPO_ROOT / "codex/AGENTS.md").read_bytes())
        self.assertIn("<!-- managed-by: genzorr/agents; asset: devin-agents-md -->", text)
        self.assertIn("## Devin Runtime Boundaries", text)
        self.assertNotIn("## Sandbox Escalation", text)
        self.assertNotIn("## Preserve Thread Model", text)

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "devin"
            home.mkdir()
            destination = home / "AGENTS.md"
            destination.write_text("operator instructions\n", encoding="utf-8")

            installed = run_installer("devin", home)

            self.assertEqual(installed.returncode, 2, installed.stderr)
            self.assertIn("skipped unmanaged global file", installed.stderr)
            self.assertEqual(destination.read_text(encoding="utf-8"), "operator instructions\n")
            self.assertFalse((home / "config.json").exists())
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_devin_managed_global_marker_can_be_reconciled_without_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "devin"
            home.mkdir()
            destination = home / "AGENTS.md"
            destination.write_text(
                "# Global Devin Instructions\n<!-- managed-by: genzorr/agents; asset: devin-agents-md -->\nold managed content\n",
                encoding="utf-8",
            )

            installed = run_installer("devin", home)

            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertEqual(destination.read_bytes(), (REPO_ROOT / "devin/AGENTS.md").read_bytes())
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(state["files"]["AGENTS.md"]["asset_id"], "devin-agents-md")

            destination.write_text(destination.read_text(encoding="utf-8") + "\noperator addition\n", encoding="utf-8")
            modified = destination.read_text(encoding="utf-8")
            uninstalled = run_installer("devin", home, "--uninstall")
            self.assertEqual(uninstalled.returncode, 2, uninstalled.stderr)
            self.assertIn("modified recorded destination", uninstalled.stderr)
            self.assertEqual(destination.read_text(encoding="utf-8"), modified)
            retained_state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(set(retained_state["files"]), {"AGENTS.md"})
            self.assertEqual(retained_state["adapters"], {})

    def test_devin_preserves_unmanaged_conflicts_and_json_with_comments(self) -> None:
        cases = (
            '{\n  "read_config_from": {"agents_standard": false}\n}\n',
            '{\n  // operator comment\n  "theme_mode": "dark"\n}\n',
        )
        for content in cases:
            with self.subTest(content=content), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "devin"
                home.mkdir()
                config = home / "config.json"
                config.write_text(content, encoding="utf-8")
                result = run_installer("devin", home)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(config.read_text(encoding="utf-8"), content)
                self.assertFalse((home / "AGENTS.md").exists())
                self.assertFalse((home / ".agents-install-state.json").exists())

    def test_devin_state_cannot_nominate_an_unmanaged_config_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "devin"
            installed = run_installer("devin", home)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            config = home / "config.json"
            current = json.loads(config.read_text())
            current["theme_mode"] = "dark"
            config.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
            state_path = home / ".agents-install-state.json"
            state = json.loads(state_path.read_text())
            state["adapters"]["devin-defaults"]["managed_values"].append({"path": ["theme_mode"], "value": "dark"})
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

            result = run_installer("devin", home, "--uninstall")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("unmanaged config path theme_mode", result.stderr)
            self.assertEqual(json.loads(config.read_text()), current)

    def test_catalog_rejects_shared_runtime_duplicates_and_divergent_claude_copies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for root, body in (("shared", "portable"), ("claude", "different")):
                skill = repo / root / "skills/sample"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(f"---\nname: sample\ndescription: Fixture.\n---\n\n{body}\n", encoding="utf-8")
            sections = {name: [] for name in ("skills", "commands", "subagents", "rules", "hooks", "configs", "global_instructions", "traveling_documents")}
            entry = {
                "id": "sample",
                "kind": "skill",
                "platforms": ["agents", "codex"],
                "owner": "agents",
                "source": {"agents": "shared/skills/sample", "codex": "shared/skills/sample"},
                "install_target": {"agents": "skills/sample", "codex": "skills/sample"},
            }
            sections["skills"] = [entry]
            catalog = repo / "catalog.json"
            catalog.write_text(json.dumps(sections), encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertTrue(any("duplicate codex discovery" in error for error in errors))

            entry["platforms"] = ["agents", "claude"]
            entry["source"] = {"agents": "shared/skills/sample", "claude": "claude/skills/sample"}
            entry["install_target"] = {"agents": "skills/sample", "claude": "skills/sample"}
            catalog.write_text(json.dumps(sections), encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertTrue(any("must use the same complete source layers" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
