"""Pi catalog distribution and provisional-link migration behavior in scratch homes."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.agent_catalog import CatalogError, load_catalog, validate_catalog

ROOT = Path(__file__).resolve().parents[1]


def inventory(home):
    if not home.exists():
        return {}
    result = {}
    for path in home.rglob("*"):
        if path.is_symlink():
            result[str(path.relative_to(home))] = ("link", os.readlink(path))
        elif path.is_file():
            result[str(path.relative_to(home))] = (stat.S_IMODE(path.stat().st_mode), path.read_bytes())
    return result


@contextlib.contextmanager
def migration_module(repo):
    scripts = str(repo / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec = importlib.util.spec_from_file_location("pi_migration_test", repo / "scripts/migrate-pi-assets.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        yield module
    finally:
        sys.path.remove(scripts)
        sys.modules.pop("pi_asset_engine", None)
        sys.modules.pop("agent_catalog", None)


class PiMigrationPlatformTest(unittest.TestCase):
    def test_windows_discovery_skips_linux_runtime_and_symlink_cases(self):
        spec = importlib.util.spec_from_file_location("pi_assets_windows_discovery", Path(__file__))
        module = importlib.util.module_from_spec(spec)
        with patch.object(sys, "platform", "win32"):
            spec.loader.exec_module(module)
        self.assertTrue(module.PiAssetsTest.__unittest_skip__)

    def test_unsupported_migration_exits_before_accessing_homes(self):
        with migration_module(ROOT) as module:
            stderr = io.StringIO()
            with patch.object(sys, "platform", "win32"), patch.object(sys, "argv", ["migrate-pi-assets.py", "--pi-home", "/synthetic/pi", "--codex-home", "/synthetic/codex"]), patch.object(sys, "stderr", stderr), patch.object(module, "migrate", side_effect=AssertionError("unsupported host reached mutation planner")):
                with self.assertRaises(SystemExit) as result:
                    module.main()
            self.assertEqual(result.exception.code, 2)
            self.assertIn("Linux only", stderr.getvalue())


@unittest.skipUnless(sys.platform == "linux", "Pi runtime distribution and migration are qualified on Linux")
class PiAssetsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="pi asset distribution ")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.repo = self.root / "repo"
        self.home = self.root / "agent"
        self.codex = self.root / "codex"
        for name in ("agent_catalog.py", "install-assets.py", "migrate-pi-assets.py", "install-pi-assets.sh", "lib/python.sh"):
            path = self.repo / "scripts" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / "scripts" / name, path)
        self.write(self.repo / "pi/AGENTS.md", "# Global Pi Instructions\n\nRead docs/guidance.md.\n")
        self.write(self.repo / "docs/guidance.md", "Synthetic guidance.\n")
        self.write(self.repo / "pi/skills/sample/SKILL.md", "---\nname: sample\ndescription: Synthetic portable skill.\n---\n\nUse this workflow.\n")
        self.catalog = {
            "skills": [{"id": "sample", "kind": "skill", "owner": "agents", "platforms": ["pi"], "source": {"pi": "pi/skills/sample"}, "install_target": {"pi": "skills/sample"}}],
            "global_instructions": [{"id": "pi-agents-md", "kind": "global_instructions", "owner": "agents", "platforms": ["pi"], "source": {"pi": "pi/AGENTS.md"}, "install_target": {"pi": "AGENTS.md"}}],
            "traveling_documents": [{"id": "guidance-doc", "kind": "traveling_document", "owner": "agents", "platforms": ["pi"], "source": {"pi": "docs/guidance.md"}, "install_target": {"pi": "docs/guidance.md"}}],
        }
        self.save_catalog()
        self.env = dict(os.environ, HOME=str(self.root / "process-home"), PI_CODING_AGENT_DIR=str(self.home), PYTHONDONTWRITEBYTECODE="1")

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        return path

    def save_catalog(self):
        self.write(self.repo / "catalog.json", json.dumps(self.catalog))

    def install(self, *args, expected=0, real=False):
        repo = ROOT if real else self.repo
        result = subprocess.run([sys.executable, str(repo / "scripts/install-assets.py"), "pi", *args], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def migrate(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(self.repo / "scripts/migrate-pi-assets.py"), "--pi-home", str(self.home), "--codex-home", str(self.codex), *args], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def provisional(self):
        self.home.mkdir()
        # Deliberately dangling: migration may inspect the link text, never its target.
        (self.home / "AGENTS.md").symlink_to(self.codex / "AGENTS.md")
        (self.home / "docs").symlink_to(os.path.relpath(self.codex / "docs", self.home), target_is_directory=True)
        settings = {"skills": ["foreign-before", str(self.codex / "skills"), {"path": "foreign-after"}], "extensions": ["/synthetic/pi-agentic-local/permissions"], "packages": ["npm:pi-subagents"], "defaultModel": "chosen", "defaultThinkingLevel": "high"}
        self.write(self.home / "settings.json", json.dumps(settings))
        for name in (".agents-pi-setup.json", "auth.json", "accounts/pool.json", "sessions/synthetic.jsonl", "extensions/foreign.ts"):
            self.write(self.home / name, "synthetic foreign fixture\n")
        return settings

    def test_fresh_preview_and_diff_create_nothing(self):
        for args in (("--dry-run",), ("--diff",)):
            self.install(*args)
            self.assertFalse(self.home.exists())
            self.migrate("--dry-run")
            self.assertFalse(self.home.exists())

    def test_install_idempotent_update_uninstall_preserves_optional_and_foreign_assets(self):
        self.home.mkdir()
        for name in (".agents-pi-setup.json", "settings.json", "auth.json", "accounts/pool.json", "extensions/foreign.ts"):
            self.write(self.home / name, "synthetic accepted optional or foreign data\n")
        foreign = inventory(self.home)
        self.install()
        installed = inventory(self.home)
        self.install()
        self.assertEqual(inventory(self.home), installed)
        self.write(self.repo / "pi/AGENTS.md", "# Global Pi Instructions\n\nUpdated. Read docs/guidance.md.\n")
        self.install("--update")
        self.assertIn("Updated.", (self.home / "AGENTS.md").read_text())
        self.install("--uninstall")
        self.assertEqual(inventory(self.home), foreign)

    def test_modified_and_foreign_outputs_fail_closed(self):
        path = self.write(self.home / "AGENTS.md", "foreign instructions\n")
        before = inventory(self.home)
        self.install(expected=2)
        self.assertEqual(inventory(self.home), before)
        path.unlink()
        self.install()
        self.write(path, "operator modification\n")
        before = inventory(self.home)
        self.install(expected=2)
        self.assertEqual(inventory(self.home), before)
        self.install("--uninstall", expected=2)
        self.assertEqual(path.read_text(), "operator modification\n")
        self.assertTrue((self.home / ".agents-install-state.json").exists())

    def test_stale_skill_prune_preserves_modified_and_foreign_content(self):
        self.install()
        self.write(self.home / "skills/sample/operator.md", "foreign\n")
        self.write(self.home / "skills/sample/SKILL.md", "operator modification\n")
        self.catalog["skills"] = []
        self.save_catalog()
        shutil.rmtree(self.repo / "pi/skills/sample")
        self.install("--prune", expected=2)
        self.assertEqual((self.home / "skills/sample/SKILL.md").read_text(), "operator modification\n")
        self.assertEqual((self.home / "skills/sample/operator.md").read_text(), "foreign\n")
        self.write(self.home / "skills/sample/SKILL.md", "---\nname: sample\ndescription: Synthetic portable skill.\n---\n\nUse this workflow.\n")
        self.install("--prune")
        self.assertFalse((self.home / "skills/sample/SKILL.md").exists())
        self.assertTrue((self.home / "skills/sample/operator.md").exists())

    def test_foreign_or_other_platform_ledger_is_preserved(self):
        self.install()
        path = self.home / ".agents-install-state.json"
        good = json.loads(path.read_text())
        for key, value in (("owner", "foreign"), ("platform", "codex")):
            bad = dict(good, **{key: value})
            path.write_text(json.dumps(bad))
            before = inventory(self.home)
            self.install("--uninstall", expected=1)
            self.assertEqual(inventory(self.home), before)

    def test_legacy_document_ledger_cannot_claim_private_or_non_document_data(self):
        for target in ("accounts/pool.json", "private/operator.json"):
            with self.subTest(target=target):
                self.install()
                private = self.write(self.home / target, '{"synthetic_private_data":"preserve"}\n')
                ledger = self.home / ".agents-install-state.json"
                state = json.loads(ledger.read_text())
                state["files"][target] = {
                    "owner": "agents", "asset_id": f"legacy-document:{target}",
                    "kind": "traveling_document", "sha256": hashlib.sha256(private.read_bytes()).hexdigest(),
                    "mode": format(stat.S_IMODE(private.stat().st_mode), "04o"), "baseline_known": True,
                }
                ledger.write_text(json.dumps(state))
                before = inventory(self.home)
                for args in (("--prune",), ("--uninstall",)):
                    self.install(*args, expected=1)
                    self.assertEqual(inventory(self.home), before)
                del state["files"][target]
                ledger.write_text(json.dumps(state))

    def test_broken_provisional_symlink_conflicts_even_in_dry_run(self):
        self.home.mkdir()
        (self.home / "AGENTS.md").symlink_to(self.codex / "AGENTS.md")
        before = inventory(self.home)
        self.install("--dry-run", expected=2)
        self.assertEqual(inventory(self.home), before)

    def test_migration_install_uninstall_and_rollback_preserve_other_settings(self):
        original_settings = self.provisional()
        initial = inventory(self.home)
        self.migrate("--dry-run")
        self.assertEqual(inventory(self.home), initial)
        self.migrate()
        self.assertFalse((self.home / "AGENTS.md").is_symlink())
        migrated = inventory(self.home)
        self.migrate()
        self.assertEqual(inventory(self.home), migrated)
        settings = json.loads((self.home / "settings.json").read_text())
        self.assertEqual(settings["skills"], ["foreign-before", {"path": "foreign-after"}])
        self.install()
        before = inventory(self.home)
        self.migrate("--rollback", expected=1)
        self.assertEqual(inventory(self.home), before)
        self.install("--uninstall")
        settings["defaultModel"] = "changed-after-migration"
        settings["extensions"].append("another-foreign-extension")
        self.write(self.home / "settings.json", json.dumps(settings))
        before = inventory(self.home)
        self.migrate("--rollback", "--dry-run")
        self.assertEqual(inventory(self.home), before)
        self.migrate("--rollback")
        final = inventory(self.home)
        self.assertEqual(final["AGENTS.md"], initial["AGENTS.md"])
        self.assertEqual(final["docs"], initial["docs"])
        restored = json.loads((self.home / "settings.json").read_text())
        self.assertEqual(restored["skills"], original_settings["skills"])
        self.assertEqual(restored["defaultModel"], "changed-after-migration")
        self.assertIn("another-foreign-extension", restored["extensions"])
        for name in ("auth.json", "accounts/pool.json", ".agents-pi-setup.json", "extensions/foreign.ts"):
            self.assertEqual(final[name], initial[name])
        self.assertFalse(self.codex.exists())

    def test_migration_foreign_link_or_malformed_settings_make_no_changes(self):
        self.provisional()
        path = self.home / "docs"
        path.unlink()
        path.symlink_to(self.root / "foreign")
        before = inventory(self.home)
        self.migrate(expected=1)
        self.assertEqual(inventory(self.home), before)
        path.unlink()
        path.symlink_to(self.codex / "docs")
        self.write(self.home / "settings.json", '{"skills":{}}')
        before = inventory(self.home)
        self.migrate(expected=1)
        self.assertEqual(inventory(self.home), before)

    def test_partial_migration_retains_recovery_record_and_rolls_back(self):
        self.provisional()
        initial = inventory(self.home)
        with migration_module(self.repo) as module:
            original = module.ENGINE.atomic_write

            def fail_settings(path, *args):
                if path.name == "settings.json":
                    raise OSError("synthetic partial-write failure")
                return original(path, *args)

            with patch.object(module.ENGINE, "atomic_write", side_effect=fail_settings):
                with self.assertRaisesRegex(ValueError, "interrupted"):
                    module.migrate(self.home, self.codex)
        self.assertFalse((self.home / "AGENTS.md").exists())
        self.assertTrue((self.home / ".agents-pi-migration.json").exists())
        self.migrate(expected=1)
        self.migrate("--rollback")
        self.assertEqual(inventory(self.home), initial)

    def test_rollback_preserves_conflicting_foreign_content_and_record(self):
        self.provisional()
        self.migrate()
        self.write(self.home / "AGENTS.md", "new foreign instructions\n")
        before = inventory(self.home)
        self.migrate("--rollback", expected=1)
        self.assertEqual(inventory(self.home), before)

    def test_forged_migration_record_cannot_restore_foreign_links(self):
        self.home.mkdir()
        record = {"owner": "agents-pi-migration", "schema_version": 1, "pi_home": str(self.home), "codex_home": str(self.codex), "links": {"AGENTS.md": "/foreign/AGENTS.md"}, "skill_index": None, "stage": "complete"}
        self.write(self.home / ".agents-pi-migration.json", json.dumps(record))
        before = inventory(self.home)
        self.migrate("--rollback", expected=1)
        self.assertEqual(inventory(self.home), before)

    def test_shared_home_and_pi_duplicate_skill_is_rejected(self):
        entry = self.catalog["skills"][0]
        entry["platforms"].append("agents")
        entry["source"]["agents"] = entry["source"]["pi"]
        entry["install_target"]["agents"] = "skills/sample"
        self.save_catalog()
        with self.assertRaisesRegex(CatalogError, "duplicate pi discovery"):
            load_catalog(self.repo)

    def test_empty_legacy_home_overrides_keep_cwd_instead_of_real_home_fallback(self):
        for platform, variable in {"agents": "AGENTS_HOME", "codex": "CODEX_HOME", "claude": "CLAUDE_HOME", "devin": "DEVIN_HOME"}.items():
            cwd = self.root / ("empty-override-" + platform)
            cwd.mkdir()
            env = dict(self.env, **{variable: ""}, XDG_CONFIG_HOME=str(self.root / "config"), APPDATA=str(self.root / "appdata"))
            result = subprocess.run([sys.executable, str(self.repo / "scripts/install-assets.py"), platform], env=env, cwd=cwd, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads((cwd / ".agents-install-state.json").read_text())
            self.assertEqual(state["platform"], platform)
        self.assertFalse(Path(self.env["HOME"]).exists())
        self.assertFalse((self.root / "config").exists())
        self.assertFalse((self.root / "appdata").exists())

    def test_pi_home_spellings_and_default_share_native_destination(self):
        process_home = Path(self.env["HOME"])
        intended = process_home / ".pi/agent"
        self.env.pop("PI_CODING_AGENT_DIR")
        self.install()
        self.assertTrue((intended / "AGENTS.md").is_file())
        before = inventory(intended)
        for spelling in ("~/.pi/agent", intended.as_uri()):
            self.env["PI_CODING_AGENT_DIR"] = spelling
            self.install()
            self.assertEqual(inventory(intended), before)
        self.assertFalse(self.home.exists())

    def test_pi_operations_do_not_mutate_native_shared_home(self):
        shared = self.root / "process-home/.agents"
        env = dict(self.env, AGENTS_HOME=str(shared))
        result = subprocess.run([sys.executable, str(ROOT / "scripts/install-assets.py"), "agents"], env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        before = inventory(shared)
        self.install(real=True)
        self.assertEqual(inventory(shared), before)
        self.install("--uninstall", real=True)
        self.assertEqual(inventory(shared), before)

    def test_actual_catalog_installs_complete_pi_assets_without_shared_duplicates(self):
        self.install(real=True)
        assets = load_catalog(ROOT)
        pi_ids = {a.id for a in assets if a.kind == "skill" and "pi" in a.platforms}
        shared_ids = {a.id for a in assets if a.kind == "skill" and "agents" in a.platforms}
        self.assertEqual(pi_ids, {"integrate-research", "review-change", "ask-chatgpt-pro", "distill-source", "diagnose", "explain", "architecture-review", "surface-unknowns", "archify"})
        self.assertFalse(pi_ids & shared_ids)
        self.assertEqual({p.parent.name for p in (self.home / "skills").glob("*/SKILL.md")}, pi_ids)
        self.assertEqual((self.home / "skills/distill-source/SKILL.md").read_bytes(), (ROOT / "codex/skills/distill-source/SKILL.md").read_bytes())
        for identity, source in (("architecture-review", "codex/skills/architecture-review"), ("archify", "codex/skills/archify"), ("surface-unknowns", "shared/skills/surface-unknowns")):
            expected = inventory(ROOT / source)
            if identity == "architecture-review":
                for name in ("multi-entrypoint-capability-review", "whole-system-review", "comprehensive-codebase-audit"):
                    path = ROOT / "docs" / f"{name}.md"
                    expected[f"docs/{name}.md"] = (stat.S_IMODE(path.stat().st_mode), path.read_bytes())
            self.assertEqual(inventory(self.home / "skills" / identity), expected)
        for deferred in ("tdd", "text-prune", "ask-oracle"):
            self.assertFalse((self.home / "skills" / deferred).exists())
        self.assertTrue((self.home / "AGENTS.md").is_file())
        self.assertTrue((self.home / "docs/context-file-authoring.md").is_file())
        before = inventory(self.home)
        self.install(real=True)
        self.assertEqual(inventory(self.home), before)
        self.install("--uninstall", real=True)
        self.assertEqual(inventory(self.home), {})


if __name__ == "__main__":
    unittest.main()
