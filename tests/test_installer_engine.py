"""Behavior contracts for the catalog-driven installer engine."""

from __future__ import annotations

import copy
import json
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from scripts.agent_catalog import CatalogError, validate_asset_target, validate_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]


def write_fixture(repo: Path, platform: str = "codex", *, travel: bool = False, global_file: bool = False, hooks: bool = False) -> None:
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    for name in ("agent_catalog.py", "install-assets.py"):
        shutil.copy2(REPO_ROOT / "scripts" / name, scripts / name)
    wrapper = "install-codex.sh" if platform == "codex" else "install-claude.sh"
    shutil.copy2(REPO_ROOT / "scripts" / wrapper, scripts / wrapper)
    (scripts / wrapper).chmod(0o755)

    assets: dict[str, list[dict]] = {"skills": [], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
    skill_root = repo / platform / "skills" / "sample"
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text("---\nname: sample\ndescription: Fixture skill.\n---\n\nfixture\n", encoding="utf-8")
    tool = skill_root / "tool.sh"
    tool.write_text("#!/bin/sh\necho fixture\n", encoding="utf-8")
    tool.chmod(0o755)
    assets["skills"].append({"id": "sample", "kind": "skill", "platforms": [platform], "owner": "agents", "source": {platform: f"{platform}/skills/sample"}, "install_target": {platform: "skills/sample"}})

    if global_file:
        (repo / "codex").mkdir(exist_ok=True)
        (repo / "codex" / "AGENTS.md").write_text("# Global Codex Instructions\nfixture\n", encoding="utf-8")
        assets["global_instructions"].append({"id": "codex-agents-md", "kind": "global_instructions", "platforms": ["codex"], "owner": "agents", "source": {"codex": "codex/AGENTS.md"}, "install_target": {"codex": "AGENTS.md"}})

    if travel:
        rule_root = repo / "claude" / "rules"
        rule_root.mkdir(parents=True)
        (rule_root / "fixture.md").write_text("Read docs/fixture.md before continuing.\n", encoding="utf-8")
        docs = repo / "docs"
        docs.mkdir()
        (docs / "fixture.md").write_text("fixture reference\n", encoding="utf-8")
        assets["rules"].append({"id": "fixture", "kind": "rule", "platforms": ["claude"], "owner": "agents", "source": {"claude": "claude/rules/fixture.md"}, "install_target": {"claude": "rules/fixture.md"}})
        assets["traveling_documents"].append({"id": "fixture-doc", "kind": "traveling_document", "platforms": ["claude"], "owner": "agents", "source": {"claude": "docs/fixture.md"}, "install_target": {"claude": "docs/fixture.md"}})

    if hooks:
        hook_root = repo / "claude" / "hooks"
        hook_root.mkdir(parents=True)
        (hook_root / "notifications.sh").write_text("#!/bin/sh\necho notify\n", encoding="utf-8")
        (hook_root / "notifications.sh").chmod(0o755)
        (repo / "claude" / "hooks.json").write_text(json.dumps({"hooks": {"Notification": [{"hooks": [{"type": "command", "command": "__CLAUDE_HOME__/hooks/notifications.sh"}]}]}}), encoding="utf-8")
        assets["hooks"].append({"id": "claude-notifications", "kind": "hook", "platforms": ["claude"], "owner": "agents", "source": {"claude": [{"path": "claude/hooks/notifications.sh", "target": "hooks/notifications.sh"}, {"path": "claude/hooks.json", "target": None, "role": "settings-hooks"}]}, "install_target": {"claude": "hooks/notifications.sh"}, "handling": {"claude": "claude_settings_hooks"}})

    (repo / "catalog.json").write_text(json.dumps({"assets_comment": "fixture", **assets}, indent=2) + "\n", encoding="utf-8")


def replace_fixture_hook_asset(repo: Path) -> None:
    """Replace the fixture hook with a new catalog identity and script target."""
    old_script = repo / "claude/hooks/notifications.sh"
    new_script = repo / "claude/hooks/replacement.sh"
    old_script.rename(new_script)
    fragment_path = repo / "claude/hooks.json"
    fragment = json.loads(fragment_path.read_text())
    fragment["hooks"]["Notification"][0]["hooks"][0]["command"] = "__CLAUDE_HOME__/hooks/replacement.sh"
    fragment_path.write_text(json.dumps(fragment), encoding="utf-8")
    catalog_path = repo / "catalog.json"
    catalog = json.loads(catalog_path.read_text())
    hook = catalog["hooks"][0]
    hook["id"] = "claude-replacement"
    hook["source"]["claude"][0] = {"path": "claude/hooks/replacement.sh", "target": "hooks/replacement.sh"}
    hook["install_target"]["claude"] = "hooks/replacement.sh"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")


class InstallerEngineTest(unittest.TestCase):
    def run_installer(self, repo: Path, platform: str, home: Path, *args: str) -> subprocess.CompletedProcess[str]:
        wrapper = repo / "scripts" / ("install-codex.sh" if platform == "codex" else "install-claude.sh")
        env = os.environ.copy()
        env["CODEX_HOME" if platform == "codex" else "CLAUDE_HOME"] = str(home)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(["bash", str(wrapper), *args], text=True, capture_output=True, env=env, check=False)

    def test_dry_run_and_diff_do_not_create_fresh_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            for option in (("--dry-run",), ("--diff",), ("--dry-run", "--prune")):
                result = self.run_installer(repo, "codex", home, *option)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(home.exists())

    def test_install_update_idempotence_and_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            first = self.run_installer(repo, "codex", home)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual((home / "skills/sample/tool.sh").stat().st_mode & 0o777, 0o755)
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(state["platform"], "codex")
            second = self.run_installer(repo, "codex", home, "--update")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("0 file action(s)", second.stdout)
            (repo / "codex/skills/sample/SKILL.md").write_text("---\nname: sample\ndescription: Fixture skill.\n---\n\nupdated\n", encoding="utf-8")
            updated = self.run_installer(repo, "codex", home)
            self.assertEqual(updated.returncode, 0, updated.stderr)
            self.assertIn("updated", (home / "skills/sample/SKILL.md").read_text())

    def test_populated_prune_and_uninstall_dry_runs_are_observational(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
            before = json.dumps({str(path.relative_to(home)): path.read_bytes().hex() for path in home.rglob("*") if path.is_file()}, sort_keys=True)
            for args in (("--prune", "--dry-run"), ("--uninstall", "--diff")):
                result = self.run_installer(repo, "codex", home, *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                after = json.dumps({str(path.relative_to(home)): path.read_bytes().hex() for path in home.rglob("*") if path.is_file()}, sort_keys=True)
                self.assertEqual(after, before)

    def test_exact_adoption_and_unmanaged_conflict_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_fixture(repo)
            adopted_home = Path(tmp) / "adopted"
            adopted_path = adopted_home / "skills/sample/SKILL.md"
            adopted_path.parent.mkdir(parents=True)
            adopted_path.write_bytes((repo / "codex/skills/sample/SKILL.md").read_bytes())
            adopted = self.run_installer(repo, "codex", adopted_home)
            self.assertEqual(adopted.returncode, 0, adopted.stderr)
            self.assertIn("skills/sample/SKILL.md", json.loads((adopted_home / ".agents-install-state.json").read_text())["files"])

            conflict_home = Path(tmp) / "conflict"
            conflict_path = conflict_home / "skills/sample/SKILL.md"
            conflict_path.parent.mkdir(parents=True)
            conflict_path.write_text("user content\n", encoding="utf-8")
            conflict = self.run_installer(repo, "codex", conflict_home)
            self.assertEqual(conflict.returncode, 2)
            self.assertIn("unmanaged destination differs", conflict.stderr)
            self.assertEqual(conflict_path.read_text(), "user content\n")
            self.assertFalse((conflict_home / ".agents-install-state.json").exists())

    def test_catalog_deleted_asset_prunes_and_uninstall_uses_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["skills"] = []
            shutil.rmtree(repo / "codex/skills/sample")
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            pruned = self.run_installer(repo, "codex", home, "--prune")
            self.assertEqual(pruned.returncode, 0, pruned.stderr)
            self.assertFalse((home / "skills/sample").exists())
            self.assertTrue((home / ".agents-install-state.json").exists())

            repo2, home2 = Path(tmp) / "repo2", Path(tmp) / "home2"
            write_fixture(repo2)
            self.assertEqual(self.run_installer(repo2, "codex", home2).returncode, 0)
            catalog2 = json.loads((repo2 / "catalog.json").read_text())
            catalog2["skills"] = []
            shutil.rmtree(repo2 / "codex/skills/sample")
            (repo2 / "catalog.json").write_text(json.dumps(catalog2), encoding="utf-8")
            uninstalled = self.run_installer(repo2, "codex", home2, "--uninstall")
            self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
            self.assertFalse((home2 / "skills/sample").exists())
            self.assertFalse((home2 / ".agents-install-state.json").exists())

    def test_uninstall_preserves_unrecorded_exact_desired_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            destination = home / "skills/sample/SKILL.md"
            destination.parent.mkdir(parents=True)
            destination.write_bytes((repo / "codex/skills/sample/SKILL.md").read_bytes())

            result = self.run_installer(repo, "codex", home, "--uninstall")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(destination.exists())
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_uninstall_preserves_recorded_file_when_it_matches_only_current_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
            source = repo / "codex/skills/sample/SKILL.md"
            source.write_text("---\nname: sample\ndescription: Current fixture skill.\n---\n\ncurrent\n", encoding="utf-8")
            destination = home / "skills/sample/SKILL.md"
            destination.write_bytes(source.read_bytes())

            result = self.run_installer(repo, "codex", home, "--uninstall")

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("modified recorded destination", result.stderr)
            self.assertTrue(destination.exists())
            self.assertTrue((home / ".agents-install-state.json").exists())

    def test_directory_source_file_retirement_prunes_only_unchanged_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for modified in (False, True):
                repo, home = Path(tmp) / f"repo-{modified}", Path(tmp) / f"home-{modified}"
                write_fixture(repo)
                self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
                source = repo / "codex/skills/sample/tool.sh"
                retired = home / "skills/sample/tool.sh"
                source.unlink()

                updated = self.run_installer(repo, "codex", home)
                self.assertEqual(updated.returncode, 0, updated.stderr)
                state = json.loads((home / ".agents-install-state.json").read_text())
                self.assertIn("skills/sample/tool.sh", state["files"])
                self.assertTrue(retired.exists())
                if modified:
                    retired.write_text("operator edit\n", encoding="utf-8")

                pruned = self.run_installer(repo, "codex", home, "--prune")
                if modified:
                    self.assertEqual(pruned.returncode, 2, pruned.stderr)
                    self.assertIn("modified stale destination", pruned.stderr)
                    self.assertEqual(retired.read_text(), "operator edit\n")
                else:
                    self.assertEqual(pruned.returncode, 0, pruned.stderr)
                    self.assertFalse(retired.exists())

    def test_modified_stale_asset_is_preserved_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
            destination = home / "skills/sample/SKILL.md"
            destination.write_text("operator edit\n", encoding="utf-8")
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["skills"] = []
            shutil.rmtree(repo / "codex/skills/sample")
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            result = self.run_installer(repo, "codex", home, "--prune")
            self.assertEqual(result.returncode, 2)
            self.assertIn("modified stale destination", result.stderr)
            self.assertEqual(destination.read_text(), "operator edit\n")

    def test_stale_foreign_record_cannot_authorize_reserved_target_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
            state_path = home / ".agents-install-state.json"
            state = json.loads(state_path.read_text())
            record = state["files"].pop("skills/sample/SKILL.md")
            foreign = home / "skills/harness-foreign/SKILL.md"
            foreign.parent.mkdir(parents=True)
            foreign.write_bytes((repo / "codex/skills/sample/SKILL.md").read_bytes())
            foreign.chmod(int(record["mode"], 8))
            record["asset_id"] = "retired-skill"
            state["files"]["skills/harness-foreign/SKILL.md"] = record
            state_path.write_text(json.dumps(state), encoding="utf-8")

            result = self.run_installer(repo, "codex", home, "--prune")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("reserved or foreign target", result.stderr)
            self.assertTrue(foreign.exists())

    def test_stale_record_identity_cannot_authorize_a_different_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
            state_path = home / ".agents-install-state.json"
            state = json.loads(state_path.read_text())
            record = state["files"].pop("skills/sample/SKILL.md")
            forged = home / "skills/other/SKILL.md"
            forged.parent.mkdir(parents=True)
            forged.write_bytes((repo / "codex/skills/sample/SKILL.md").read_bytes())
            forged.chmod(int(record["mode"], 8))
            state["files"]["skills/other/SKILL.md"] = record
            state_path.write_text(json.dumps(state), encoding="utf-8")

            result = self.run_installer(repo, "codex", home, "--prune")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("asset identity does not match target", result.stderr)
            self.assertTrue(forged.exists())

    def test_removed_hook_record_cannot_authorize_a_different_same_namespace_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for operation in ("--prune", "--uninstall"):
                repo, home = Path(tmp) / f"repo-{operation}", Path(tmp) / f"home-{operation}"
                write_fixture(repo, "claude", hooks=True)
                self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
                state_path = home / ".agents-install-state.json"
                state = json.loads(state_path.read_text())
                record = state["files"].pop("hooks/notifications.sh")
                original = home / "hooks/notifications.sh"
                forged = home / "hooks/forged.sh"
                forged.write_bytes(original.read_bytes())
                forged.chmod(int(record["mode"], 8))
                original.unlink()
                state["files"]["hooks/forged.sh"] = record
                state_path.write_text(json.dumps(state), encoding="utf-8")
                settings = home / "settings.json"
                before = settings.read_bytes()

                catalog = json.loads((repo / "catalog.json").read_text())
                catalog["hooks"] = []
                shutil.rmtree(repo / "claude/hooks")
                (repo / "claude/hooks.json").unlink()
                (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

                result = self.run_installer(repo, "claude", home, operation)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("hook target is not bound", result.stderr)
                self.assertTrue(forged.exists())
                self.assertEqual(settings.read_bytes(), before)

    def test_legacy_manifest_migrates_to_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", travel=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            (home / ".agents-install-state.json").unlink()
            (home / ".agents-doc-manifest").write_text("docs/fixture.md\n", encoding="utf-8")
            migrated = self.run_installer(repo, "claude", home)
            self.assertEqual(migrated.returncode, 0, migrated.stderr)
            self.assertTrue((home / ".agents-install-state.json").exists())
            self.assertFalse((home / ".agents-doc-manifest").exists())

    def test_codex_unmanaged_global_file_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, global_file=True)
            destination = home / "AGENTS.md"
            destination.parent.mkdir(parents=True)
            destination.write_text("operator instructions\n", encoding="utf-8")
            result = self.run_installer(repo, "codex", home)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(destination.read_text(), "operator instructions\n")
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_ancestor_symlinks_fail_closed_for_install_prune_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            write_fixture(repo)
            outside = root / "outside"
            outside.mkdir()
            home = root / "home"
            home.mkdir()
            (home / "skills").symlink_to(outside, target_is_directory=True)
            result = self.run_installer(repo, "codex", home)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse((outside / "sample/SKILL.md").exists())

            populated = root / "populated"
            shutil.rmtree(repo)
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", populated).returncode, 0)
            shutil.rmtree(populated / "skills")
            (populated / "skills").symlink_to(outside, target_is_directory=True)
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["skills"] = []
            shutil.rmtree(repo / "codex/skills/sample")
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            pruned = self.run_installer(repo, "codex", populated, "--prune")
            self.assertEqual(pruned.returncode, 1, pruned.stderr)

            uninstall_home = root / "uninstall"
            shutil.rmtree(repo)
            write_fixture(repo)
            self.assertEqual(self.run_installer(repo, "codex", uninstall_home).returncode, 0)
            shutil.rmtree(uninstall_home / "skills")
            (uninstall_home / "skills").symlink_to(outside, target_is_directory=True)
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["skills"] = []
            shutil.rmtree(repo / "codex/skills/sample")
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            uninstalled = self.run_installer(repo, "codex", uninstall_home, "--uninstall")
            self.assertEqual(uninstalled.returncode, 1, uninstalled.stderr)

    def test_modified_legacy_document_is_preserved_until_exact_retry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", travel=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            (home / ".agents-install-state.json").unlink()
            destination = home / "docs/fixture.md"
            destination.write_text("operator edit\n", encoding="utf-8")
            (home / ".agents-doc-manifest").write_text("docs/fixture.md\n", encoding="utf-8")
            conflicted = self.run_installer(repo, "claude", home)
            self.assertEqual(conflicted.returncode, 2, conflicted.stderr)
            self.assertIn("legacy manifest destination differs", conflicted.stderr)
            self.assertEqual(destination.read_text(), "operator edit\n")
            migrated = json.loads((home / ".agents-install-state.json").read_text())
            self.assertFalse(migrated["files"]["docs/fixture.md"]["baseline_known"])
            self.assertTrue((home / ".agents-doc-manifest").exists())
            destination.write_bytes((repo / "docs/fixture.md").read_bytes())
            retried = self.run_installer(repo, "claude", home)
            self.assertEqual(retried.returncode, 0, retried.stderr)
            self.assertFalse((home / ".agents-doc-manifest").exists())
            self.assertTrue(json.loads((home / ".agents-install-state.json").read_text())["files"]["docs/fixture.md"]["baseline_known"])

    def test_claude_adapter_history_preserves_unrelated_hooks_after_catalog_removal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({"hooks": {"UserEvent": [{"hooks": [{"type": "command", "command": "/usr/local/bin/other"}]}]}}), encoding="utf-8")
            installed = self.run_installer(repo, "claude", home)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            merged = json.loads(settings.read_text())
            self.assertEqual(merged["hooks"]["UserEvent"][0]["hooks"][0]["command"], "/usr/local/bin/other")
            self.assertIn("Notification", merged["hooks"])
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertIn("claude-notifications", state["adapters"])

            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["hooks"] = []
            shutil.rmtree(repo / "claude/hooks")
            (repo / "claude/hooks.json").unlink()
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            uninstalled = self.run_installer(repo, "claude", home, "--uninstall")
            self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
            remaining = json.loads(settings.read_text())
            self.assertEqual(list(remaining["hooks"]), ["UserEvent"])
            self.assertFalse((home / "hooks/notifications.sh").exists())
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_modified_historical_claude_hook_is_preserved_for_retry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            installed = self.run_installer(repo, "claude", home)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            settings = home / "settings.json"
            modified = json.loads(settings.read_text())
            modified["hooks"]["Notification"][0]["hooks"][0]["command"] += " --operator-edit"
            settings.write_text(json.dumps(modified), encoding="utf-8")

            removed = self.run_installer(repo, "claude", home, "--uninstall")
            self.assertEqual(removed.returncode, 2, removed.stderr)
            self.assertIn("recorded hook leaves were modified or moved", removed.stderr)
            self.assertEqual(json.loads(settings.read_text()), modified)
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertIn("claude-notifications", state["adapters"])
            self.assertTrue((home / "hooks/notifications.sh").exists())

    def test_uninstall_preserves_current_only_hook_script_and_retains_retry_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            source = repo / "claude/hooks/notifications.sh"
            source.write_text("#!/bin/sh\necho current\n", encoding="utf-8")
            script = home / "hooks/notifications.sh"
            script.write_bytes(source.read_bytes())

            result = self.run_installer(repo, "claude", home, "--uninstall")

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertTrue(script.exists())
            self.assertNotIn(str(script), (home / "settings.json").read_text())
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(state["adapters"]["claude-notifications"]["managed_leaves"], [])

    def test_uninstall_preserves_unrecorded_claude_hook_script_and_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            (home / ".agents-install-state.json").unlink()
            script = home / "hooks/notifications.sh"
            settings = home / "settings.json"
            script_before = script.read_bytes()
            settings_before = settings.read_bytes()

            result = self.run_installer(repo, "claude", home, "--uninstall")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(script.read_bytes(), script_before)
            self.assertEqual(settings.read_bytes(), settings_before)
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_no_history_install_adopts_exact_hook_leaf_before_script_and_uninstalls_both(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            script = home / "hooks/notifications.sh"
            script.parent.mkdir(parents=True)
            script.write_bytes((repo / "claude/hooks/notifications.sh").read_bytes())
            script.chmod(0o755)
            settings = home / "settings.json"
            settings.write_text(json.dumps({"hooks": {"Notification": [{"hooks": [{"type": "command", "command": f"{home}/hooks/notifications.sh"}]}]}}), encoding="utf-8")

            installed = self.run_installer(repo, "claude", home)

            self.assertEqual(installed.returncode, 0, installed.stderr)
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(len(state["adapters"]["claude-notifications"]["managed_leaves"]), 1)
            self.assertIn("hooks/notifications.sh", state["files"])
            removed = self.run_installer(repo, "claude", home, "--uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertFalse(script.exists())
            self.assertNotIn(str(script), settings.read_text())
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_no_history_install_rejects_ambiguous_preexisting_hook_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            script = home / "hooks/notifications.sh"
            script.parent.mkdir(parents=True)
            script.write_bytes((repo / "claude/hooks/notifications.sh").read_bytes())
            script.chmod(0o755)
            leaf = {"hooks": [{"type": "command", "command": f"{home}/hooks/notifications.sh"}]}
            settings = home / "settings.json"
            settings.write_text(json.dumps({"hooks": {"Notification": [leaf, copy.deepcopy(leaf)]}}), encoding="utf-8")
            before = settings.read_bytes()

            result = self.run_installer(repo, "claude", home)

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("desired hook leaf is ambiguous", result.stderr)
            self.assertEqual(settings.read_bytes(), before)
            self.assertTrue(script.exists())
            self.assertFalse((home / ".agents-install-state.json").exists())

    def test_forged_adapter_history_cannot_authorize_an_unrelated_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            settings = home / "settings.json"
            before = settings.read_bytes()
            state_path = home / ".agents-install-state.json"
            state = json.loads(state_path.read_text())
            state["adapters"]["claude-notifications"]["managed_leaves"][0]["leaf"]["command"] = "/usr/local/bin/unrelated"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            result = self.run_installer(repo, "claude", home, "--uninstall")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("managed_leaves", result.stderr)
            self.assertEqual(settings.read_bytes(), before)
            self.assertTrue((home / "hooks/notifications.sh").exists())

    def test_hook_fragment_command_update_reconciles_from_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            settings = home / "settings.json"
            old_command = json.loads(settings.read_text())["hooks"]["Notification"][0]["hooks"][0]["command"]
            fragment_path = repo / "claude/hooks.json"
            fragment = json.loads(fragment_path.read_text())
            new_command = f'{home}/hooks/notifications.sh "updated message"'
            fragment["hooks"]["Notification"][0]["hooks"][0]["command"] = '__CLAUDE_HOME__/hooks/notifications.sh "updated message"'
            fragment_path.write_text(json.dumps(fragment), encoding="utf-8")

            result = self.run_installer(repo, "claude", home)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = json.loads(settings.read_text())
            installed_command = updated["hooks"]["Notification"][0]["hooks"][0]["command"]
            self.assertNotEqual(installed_command, old_command)
            self.assertEqual(installed_command, new_command)
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(state["adapters"]["claude-notifications"]["managed_leaves"][0]["leaf"]["command"], new_command)
            self.assertTrue((home / "hooks/notifications.sh").exists())

    def test_replacement_hook_reconciles_prune_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for operation in ("--prune", "--uninstall"):
                repo, home = Path(tmp) / f"repo-{operation}", Path(tmp) / f"home-{operation}"
                write_fixture(repo, "claude", hooks=True)
                self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
                old_command = f"{home}/hooks/notifications.sh"
                replace_fixture_hook_asset(repo)

                result = self.run_installer(repo, "claude", home, operation)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(old_command, (home / "settings.json").read_text())
                self.assertFalse((home / "hooks/notifications.sh").exists())
                if operation == "--prune":
                    self.assertTrue((home / "hooks/replacement.sh").exists())
                    state = json.loads((home / ".agents-install-state.json").read_text())
                    self.assertEqual(set(state["adapters"]), {"claude-replacement"})
                    self.assertEqual(self.run_installer(repo, "claude", home, "--prune").returncode, 0)
                else:
                    self.assertFalse((home / ".agents-install-state.json").exists())

    def test_removed_hook_prunes_and_retries_without_a_configured_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            old_command = f"{home}/hooks/notifications.sh"
            catalog_path = repo / "catalog.json"
            catalog = json.loads(catalog_path.read_text())
            catalog["hooks"] = []
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            shutil.rmtree(repo / "claude/hooks")
            (repo / "claude/hooks.json").unlink()

            pruned = self.run_installer(repo, "claude", home, "--prune")
            self.assertEqual(pruned.returncode, 0, pruned.stderr)
            self.assertNotIn(old_command, (home / "settings.json").read_text())
            self.assertFalse((home / "hooks/notifications.sh").exists())
            state = json.loads((home / ".agents-install-state.json").read_text())
            self.assertEqual(state["adapters"], {})
            self.assertNotIn("hooks/notifications.sh", state["files"])
            retried = self.run_installer(repo, "claude", home, "--prune")
            self.assertEqual(retried.returncode, 0, retried.stderr)

    def test_modified_removed_hook_retains_history_until_prune_or_uninstall_retry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for operation in ("--prune", "--uninstall"):
                repo, home = Path(tmp) / f"repo-{operation}", Path(tmp) / f"home-{operation}"
                write_fixture(repo, "claude", hooks=True)
                self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
                script = home / "hooks/notifications.sh"
                original = script.read_bytes()
                script.write_text("operator edit\n", encoding="utf-8")
                catalog = json.loads((repo / "catalog.json").read_text())
                catalog["hooks"] = []
                (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
                shutil.rmtree(repo / "claude/hooks")
                (repo / "claude/hooks.json").unlink()

                conflicted = self.run_installer(repo, "claude", home, operation)
                self.assertEqual(conflicted.returncode, 2, conflicted.stderr)
                state_path = home / ".agents-install-state.json"
                state = json.loads(state_path.read_text())
                self.assertIn("claude-notifications", state["adapters"])
                self.assertIn("hooks/notifications.sh", state["files"])
                self.assertNotIn(f"{home}/hooks/notifications.sh", (home / "settings.json").read_text())

                script.write_bytes(original)
                retried = self.run_installer(repo, "claude", home, operation)
                self.assertEqual(retried.returncode, 0, retried.stderr)
                self.assertFalse(script.exists())
                if operation == "--prune":
                    state = json.loads(state_path.read_text())
                    self.assertNotIn("claude-notifications", state["adapters"])
                else:
                    self.assertFalse(state_path.exists())

    def test_modified_replacement_hook_retains_history_until_prune_or_uninstall_retry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for operation in ("--prune", "--uninstall"):
                repo, home = Path(tmp) / f"repo-{operation}", Path(tmp) / f"home-{operation}"
                write_fixture(repo, "claude", hooks=True)
                self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
                script = home / "hooks/notifications.sh"
                original = script.read_bytes()
                script.write_text("operator edit\n", encoding="utf-8")
                replace_fixture_hook_asset(repo)

                conflicted = self.run_installer(repo, "claude", home, operation)
                self.assertEqual(conflicted.returncode, 2, conflicted.stderr)
                state_path = home / ".agents-install-state.json"
                state = json.loads(state_path.read_text())
                self.assertIn("claude-notifications", state["adapters"])
                self.assertIn("hooks/notifications.sh", state["files"])
                self.assertNotIn(f"{home}/hooks/notifications.sh", (home / "settings.json").read_text())

                script.write_bytes(original)
                retried = self.run_installer(repo, "claude", home, operation)
                self.assertEqual(retried.returncode, 0, retried.stderr)
                self.assertFalse(script.exists())
                if operation == "--prune":
                    self.assertTrue((home / "hooks/replacement.sh").exists())
                    state = json.loads(state_path.read_text())
                    self.assertEqual(set(state["adapters"]), {"claude-replacement"})
                else:
                    self.assertFalse(state_path.exists())

    def test_no_state_path_reference_is_not_inferred_as_managed_hook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({"hooks": {"Notification": [{"hooks": [{"type": "command", "command": f"/usr/bin/printf {home}/hooks/notifications.sh"}]}]}}), encoding="utf-8")
            before = settings.read_bytes()

            result = self.run_installer(repo, "claude", home)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = json.loads(settings.read_text())
            self.assertEqual(updated["hooks"]["Notification"][0]["hooks"][0]["command"], f"/usr/bin/printf {home}/hooks/notifications.sh")
            self.assertTrue((home / "hooks/notifications.sh").exists())

    def test_hook_uninstall_removes_only_recorded_structural_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            settings = home / "settings.json"
            value = json.loads(settings.read_text())
            value["hooks"]["Notification"].append(copy.deepcopy(value["hooks"]["Notification"][0]))
            value["hooks"]["Notification"].append({"metadata": "keep"})
            settings.write_text(json.dumps(value), encoding="utf-8")

            result = self.run_installer(repo, "claude", home, "--uninstall")

            self.assertEqual(result.returncode, 0, result.stderr)
            remaining = json.loads(settings.read_text())
            self.assertEqual(len(remaining["hooks"]["Notification"]), 2)
            self.assertEqual(remaining["hooks"]["Notification"][1], {"metadata": "keep"})

    def test_moved_hook_leaf_conflicts_without_deleting_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            settings = home / "settings.json"
            value = json.loads(settings.read_text())
            leaf = value["hooks"]["Notification"].pop(0)
            value["hooks"]["Notification"].append({"metadata": "keep"})
            value["hooks"]["Notification"].append(leaf)
            before = settings.read_bytes()
            settings.write_text(json.dumps(value), encoding="utf-8")

            result = self.run_installer(repo, "claude", home, "--uninstall")

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("recorded hook leaves were modified or moved", result.stderr)
            self.assertEqual(settings.read_bytes(), json.dumps(value).encode("utf-8"))
            self.assertTrue((home / "hooks/notifications.sh").exists())

    def test_dangling_symlink_retains_state_for_prune_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for operation in ("--prune", "--uninstall"):
                repo, home = Path(tmp) / f"repo-{operation}", Path(tmp) / f"home-{operation}"
                write_fixture(repo)
                self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
                target = home / "skills/sample/SKILL.md"
                target.unlink()
                target.symlink_to(home / "missing")
                if operation == "--prune":
                    catalog = json.loads((repo / "catalog.json").read_text())
                    catalog["skills"] = []
                    shutil.rmtree(repo / "codex/skills/sample")
                    (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

                result = self.run_installer(repo, "codex", home, operation)

                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("is a symlink", result.stderr)
                self.assertTrue(target.is_symlink())
                self.assertIn("skills/sample/SKILL.md", json.loads((home / ".agents-install-state.json").read_text())["files"])

    def test_harness_owned_targets_are_rejected_for_catalog_and_state(self) -> None:
        for platform, asset_id, kind, target in (
            ("claude", "execute", "command", "commands/execute.md"),
            ("claude", "task-verifier", "subagent", "agents/task-verifier.md"),
            ("claude", "task-bootstrap", "subagent", "agents/harness-task-bootstrap.md"),
            ("codex", "stop", "hook", "hooks/stop.sh"),
        ):
            with self.subTest(target=target):
                with self.assertRaisesRegex(CatalogError, "reserved or foreign target"):
                    validate_asset_target(platform, asset_id, kind, target, "fixture")

        with tempfile.TemporaryDirectory() as tmp:
            for target, asset_id, kind in (("commands/execute.md", "execute", "command"), ("agents/task-verifier.md", "task-verifier", "subagent")):
                repo, home = Path(tmp) / f"repo-{asset_id}", Path(tmp) / f"home-{asset_id}"
                write_fixture(repo, "claude")
                self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
                state_path = home / ".agents-install-state.json"
                state = json.loads(state_path.read_text())
                record = state["files"].pop("skills/sample/SKILL.md")
                record.update({"asset_id": asset_id, "kind": kind})
                forged = home / target
                forged.parent.mkdir(parents=True)
                forged.write_bytes((repo / "claude/skills/sample/SKILL.md").read_bytes())
                forged.chmod(int(record["mode"], 8))
                state["files"][target] = record
                state_path.write_text(json.dumps(state), encoding="utf-8")

                result = self.run_installer(repo, "claude", home, "--uninstall")

                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("reserved or foreign target", result.stderr)
                self.assertTrue(forged.exists())

    def test_claude_home_path_is_shell_quoted_in_hook_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home with space"
            write_fixture(repo, "claude", hooks=True)

            result = self.run_installer(repo, "claude", home)

            self.assertEqual(result.returncode, 0, result.stderr)
            command = json.loads((home / "settings.json").read_text())["hooks"]["Notification"][0]["hooks"][0]["command"]
            self.assertEqual(command, f"'{home}'/hooks/notifications.sh")
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)

    def test_history_only_shell_chain_is_not_a_managed_hook_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            state_path = home / ".agents-install-state.json"
            state = json.loads(state_path.read_text())
            state["adapters"]["claude-notifications"]["managed_leaves"][0]["leaf"]["command"] += " && /usr/bin/foreign"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            settings = home / "settings.json"
            before = settings.read_bytes()

            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["hooks"] = []
            shutil.rmtree(repo / "claude/hooks")
            (repo / "claude/hooks.json").unlink()
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            result = self.run_installer(repo, "claude", home, "--uninstall")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("managed_leaves", result.stderr)
            self.assertEqual(settings.read_bytes(), before)
            self.assertTrue((home / "hooks/notifications.sh").exists())

    def test_partial_apply_is_retryable_without_permanent_recorded_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo)
            scripts_path = str(repo / "scripts")
            sys.path.insert(0, scripts_path)
            try:
                spec = importlib.util.spec_from_file_location("install_assets_fault_fixture", repo / "scripts/install-assets.py")
                self.assertIsNotNone(spec)
                self.assertIsNotNone(spec.loader)
                module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
                original_atomic_write = module.atomic_write
                calls = 0

                def fail_on_second(path: Path, content: bytes, mode: int | None = None) -> None:
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        raise OSError("simulated mid-apply failure")
                    original_atomic_write(path, content, mode)

                args = type("Args", (), {"platform": "codex", "dry_run": False, "show_diff": False, "update": False, "prune": False, "uninstall": False})()
                with mock.patch.object(module, "atomic_write", side_effect=fail_on_second):
                    os.environ["CODEX_HOME"] = str(home)
                    try:
                        self.assertEqual(module.run(args), 1)
                    finally:
                        os.environ.pop("CODEX_HOME", None)
                self.assertFalse((home / ".agents-install-state.json").exists())
            finally:
                sys.modules.pop("install_assets_fault_fixture", None)
                sys.path.remove(scripts_path)
            retried = self.run_installer(repo, "codex", home)
            self.assertEqual(retried.returncode, 0, retried.stderr)
            self.assertTrue((home / "skills/sample/tool.sh").exists())

    def test_forged_foreign_or_inconsistent_state_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for mutation in (
                lambda record: record.update({"owner": "harness"}),
                lambda record: record.update({"asset_id": "harness-forged"}),
                lambda record: record.update({"asset_id": "other"}),
            ):
                repo, home = Path(tmp) / "repo", Path(tmp) / f"home-{id(mutation)}"
                if repo.exists():
                    shutil.rmtree(repo)
                write_fixture(repo)
                self.assertEqual(self.run_installer(repo, "codex", home).returncode, 0)
                state_path = home / ".agents-install-state.json"
                state = json.loads(state_path.read_text())
                mutation(next(iter(state["files"].values())))
                state_path.write_text(json.dumps(state), encoding="utf-8")
                result = self.run_installer(repo, "codex", home, "--update")
                self.assertEqual(result.returncode, 1, result.stderr)

    def test_unlisted_nested_hook_file_is_reported_by_catalog_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_fixture(repo, "claude", hooks=True)
            extra = repo / "claude/hooks/extra.sh"
            extra.write_text("#!/bin/sh\n", encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertTrue(any("claude/hooks/extra.sh" in error for error in errors))

    def test_settings_mode_is_preserved_and_new_settings_match_creation_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text("{}\n", encoding="utf-8")
            settings.chmod(0o640)
            self.assertEqual(self.run_installer(repo, "claude", home).returncode, 0)
            self.assertEqual(settings.stat().st_mode & 0o777, 0o640)

            new_home = Path(tmp) / "new-home"
            self.assertEqual(self.run_installer(repo, "claude", new_home).returncode, 0)
            self.assertEqual((new_home / "settings.json").stat().st_mode & 0o777, 0o644)

    def test_claude_hook_top_level_type_collision_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({"hooks": [{"foreign": "kept"}]}), encoding="utf-8")
            before = settings.read_bytes()

            result = self.run_installer(repo, "claude", home)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("incompatible nonempty hook types", result.stderr)
            self.assertEqual(settings.read_bytes(), before)
            self.assertFalse((home / "hooks/notifications.sh").exists())

    def test_claude_hook_nested_type_collision_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({"hooks": {"Notification": {"foreign": "kept"}}}), encoding="utf-8")
            before = settings.read_bytes()

            result = self.run_installer(repo, "claude", home)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("incompatible nonempty hook types", result.stderr)
            self.assertEqual(settings.read_bytes(), before)
            self.assertFalse((home / "hooks/notifications.sh").exists())

    def test_required_adapter_skip_is_a_non_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text("not json\n", encoding="utf-8")
            result = self.run_installer(repo, "claude", home)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("unresolved settings.json hook adapter", result.stderr)

    def test_skill_frontmatter_validates_expanded_target_not_each_source_layer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_fixture(repo)
            support = repo / "codex/support"
            support.mkdir(parents=True)
            (support / "helper.txt").write_text("support\n", encoding="utf-8")
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["skills"][0]["source"]["codex"] = [
                {"path": "codex/skills/sample", "target": "skills/sample"},
                {"path": "codex/support", "target": "skills/sample/support"},
            ]
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertEqual(errors, [])

    def test_claude_settings_and_managed_hook_reconcile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, home = Path(tmp) / "repo", Path(tmp) / "home"
            write_fixture(repo, "claude", hooks=True)
            settings = home / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({"env": {"fixture": "kept"}}), encoding="utf-8")
            installed = self.run_installer(repo, "claude", home)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            merged = json.loads(settings.read_text())
            self.assertEqual(merged["env"], {"fixture": "kept"})
            self.assertIn("hooks", merged)
            removed = self.run_installer(repo, "claude", home, "--uninstall")
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertEqual(json.loads(settings.read_text()), {"env": {"fixture": "kept"}})
            self.assertFalse((home / "hooks/notifications.sh").exists())

    def test_rule_only_travel_reference_is_declared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_fixture(repo, "claude", travel=True)
            errors, _warnings = validate_catalog(repo)
            self.assertEqual(errors, [])
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["traveling_documents"] = []
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertTrue(any("not cataloged for travel" in error for error in errors))

    def test_catalog_rejects_traversal_and_layer_collision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_fixture(repo, "claude", hooks=True)
            catalog = json.loads((repo / "catalog.json").read_text())
            catalog["skills"][0]["install_target"]["claude"] = "../escape"
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertTrue(any("unsafe relative path" in error for error in errors))

            catalog["skills"][0]["install_target"]["claude"] = "skills/sample"
            catalog["hooks"][0]["source"]["claude"][1]["target"] = "hooks/notifications.sh"
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            errors, _warnings = validate_catalog(repo)
            self.assertTrue(any("settings hook adapter needs exactly one script and one settings-hooks fragment" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
