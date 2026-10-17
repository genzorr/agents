"""Observable scratch-home install, conflict, and recovery guarantees."""

import builtins
import copy
import io
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pi_setup", ROOT / "scripts/install-pi.py")
setup = None
if sys.platform == "linux":
    setup = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(setup)


class PiSetupPlatformTests(unittest.TestCase):
    def test_unsupported_platform_import_and_cli_diagnostic(self):
        original_import = builtins.__import__

        def without_fcntl(name, *args, **kwargs):
            if name == "fcntl":
                raise ImportError("fcntl is unavailable on Windows")
            return original_import(name, *args, **kwargs)

        spec = importlib.util.spec_from_file_location("pi_setup_windows_probe", ROOT / "scripts/install-pi.py")
        module = importlib.util.module_from_spec(spec)
        stderr = io.StringIO()
        with patch.object(sys, "platform", "win32"), patch("builtins.__import__", side_effect=without_fcntl), patch.object(sys, "argv", ["install-pi.py", "--dry-run"]), patch.object(sys, "stderr", stderr):
            spec.loader.exec_module(module)
            with self.assertRaises(SystemExit) as exit_result:
                module.main()
        self.assertEqual(exit_result.exception.code, 2)
        self.assertIn("supports Linux only", stderr.getvalue())

    def test_windows_discovery_skips_linux_suite_before_installer_import(self):
        spec = importlib.util.spec_from_file_location("pi_setup_tests_windows_probe", Path(__file__))
        module = importlib.util.module_from_spec(spec)
        with patch.object(sys, "platform", "win32"):
            spec.loader.exec_module(module)
        self.assertIsNone(module.setup)
        self.assertTrue(module.PiSetupTests.__unittest_skip__)


@unittest.skipUnless(sys.platform == "linux", "Pi setup requires Linux")
class PiSetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pi setup ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "task home"
        self.agent = self.home / ".pi/agent"
        self.repo = self.root / "source"
        for relative, data in {"pi/permissions/index.ts": "export default function() {}\n", "pi/permissions/policy.mjs": "export const policy = {};\n", "pi/permissions/profile.json": "{}\n", "pi/permissions/child-inheritance.mjs": "export const qualified = true;\n", "pi/permissions/child-inheritance.mjs": "export const inherited = true;\n"}.items():
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        self.repo_patch = patch.object(setup, "REPO", self.repo)
        self.repo_patch.start()
        self.addCleanup(self.repo_patch.stop)
        self.install = setup.Setup(self.home, self.agent)

    def write(self, relative, value):
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        return path

    def tree(self):
        return {str(path.relative_to(self.home)): (path.read_bytes(), path.stat().st_mode) for path in self.home.rglob("*") if path.is_file()}

    def test_native_path_spellings_share_store_and_normalized_launch_paths(self):
        process_home = self.root / "process home"
        expected = process_home / "agent store"
        spellings = ["~/agent store", str(expected), expected.as_uri(), "file://localhost" + expected.as_uri()[7:]]
        with patch.object(Path, "home", return_value=process_home), patch.dict(os.environ, {}, clear=True), patch.object(sys, "stdout", io.StringIO()):
            for index, spelling in enumerate(spellings):
                options = ["--agent-dir", spelling] if index % 2 else []
                with patch.dict(os.environ, {"PI_CODING_AGENT_DIR": spelling}), patch.object(sys, "argv", ["install-pi.py", "--home", self.home.as_uri(), *options]):
                    self.assertEqual(setup.main(), 0)
                self.assertTrue((expected / ".agents-pi-setup.json").exists())
                self.assertTrue((expected / "settings.json").is_file())
                self.assertFalse((self.home / ".local/bin/pi-accounts").exists())
                if index == 0:
                    installed = self.tree()
                else:
                    self.assertEqual(self.tree(), installed)
            self.assertEqual(setup.resolve_install_path("~"), process_home)
            self.assertEqual(setup.resolve_install_path("./agent/../target"), Path.cwd() / "target")
            self.assertEqual(setup.resolve_install_path(" spaced "), Path.cwd() / " spaced ")
        self.assertFalse((self.home / "~").exists())
        self.assertFalse((self.home / "file:").exists())

    def test_unsupported_file_uri_fails_before_any_install_writes(self):
        for uri in ("file://remote-host/tmp/pi", "file:///tmp/encoded%2fslash", "file:///tmp/bad%ZZ", "file:///tmp/percent%", "file:///tmp/null%00byte"):
            with patch.object(sys, "argv", ["install-pi.py", "--home", str(self.home), "--agent-dir", uri]), patch.object(sys, "stderr", io.StringIO()):
                with self.assertRaises(SystemExit) as result:
                    setup.main()
            self.assertEqual(result.exception.code, 2)
            self.assertFalse(self.home.exists())

    def test_fresh_dry_run_creates_nothing(self):
        self.install.recover(True)
        self.assertTrue(self.install.plan())
        self.assertFalse(self.home.exists())

    def test_install_twice_preserves_other_settings_and_accounts_then_uninstalls(self):
        settings = {"extensions": ["foreign-extension"], "packages": ["npm:pi-subagents"], "defaultModel": "chosen", "defaultThinkingLevel": "high", "provider": {"enabled": True}}
        self.write(".pi/agent/settings.json", json.dumps(settings))
        auth = self.write(".pi/agent/auth.json", '{"foreign-provider":{"synthetic":true}}')
        pool = self.write(".pi/agent/accounts/pool.json", '{"synthetic":true}')
        expected_auth, expected_pool = auth.read_bytes(), pool.read_bytes()
        self.install.apply(self.install.plan())
        installed = self.tree()
        self.assertEqual(self.install.plan(), {})
        self.assertEqual(self.tree(), installed)
        actual = json.loads((self.agent / "settings.json").read_text())
        self.assertEqual(actual.pop("extensions"), ["foreign-extension", self.install.extension])
        self.assertEqual(actual, {k: v for k, v in settings.items() if k != "extensions"})
        self.install.apply(self.install.plan(True))
        self.assertEqual(json.loads((self.agent / "settings.json").read_text()), settings)
        self.assertEqual(auth.read_bytes(), expected_auth)
        self.assertEqual(pool.read_bytes(), expected_pool)
        self.assertFalse(self.install.state.exists())
        self.assertFalse(self.install.target("wrapper").exists())
        self.assertEqual(self.install.plan(True), {})

    def test_unmanaged_and_modified_owned_files_fail_before_writes(self):
        foreign = self.write(".local/lib/pi-agentic-local/permissions/index.ts", "foreign\n")
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            self.install.plan()
        self.assertEqual(self.tree(), before)
        foreign.unlink()
        self.install.apply(self.install.plan())
        foreign.write_text("operator modification\n")
        before = self.tree()
        for uninstall in (False, True):
            with self.assertRaisesRegex(ValueError, "modified"):
                self.install.plan(uninstall)
            self.assertEqual(self.tree(), before)

    def test_invalid_settings_and_existing_extension_are_preserved(self):
        for text in ("// invalid JSON", "[]", '{"extensions":{}}', json.dumps({"extensions": [self.install.extension]})):
            self.write(".pi/agent/settings.json", text)
            before = self.tree()
            with self.assertRaises(ValueError):
                self.install.plan()
            self.assertEqual(self.tree(), before)

    def test_owned_update_replaces_only_unmodified_output(self):
        self.install.apply(self.install.plan())
        (self.repo / "pi/permissions/index.ts").write_text("export default function updated() {}\n")
        self.install.apply(self.install.plan())
        self.assertEqual(self.install.target("permissions/index.ts").read_text(), "export default function updated() {}\n")

    def test_failed_partial_write_rolls_back_original_bytes_and_modes(self):
        self.write(".pi/agent/settings.json", '{ "extensions": ["foreign"] }\n')
        before = self.tree()
        original = setup.atomic_write
        count = 0

        def fail_once(path, value):
            nonlocal count
            count += 1
            if count == 4:
                raise OSError("synthetic disk failure")
            original(path, value)

        with patch.object(setup, "atomic_write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "disk failure"):
                self.install.apply(self.install.plan())
        self.assertEqual(self.tree(), before)
        self.assertFalse(self.install.journal.exists())

    def test_interrupted_transaction_recovers_and_rejects_external_changes(self):
        changes = self.install.plan()
        setup.atomic_write(self.install.journal, setup.content(setup.encoded({"owner": setup.OWNER, "home": str(self.home), "changes": changes}), 0o600))
        first = next(iter(changes))
        setup.atomic_write(self.install.target(first), changes[first][1])
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "interrupted"):
            self.install.recover(True)
        self.assertEqual(self.tree(), before)
        self.install.target(first).write_text("external edit")
        with self.assertRaisesRegex(ValueError, "recovery conflict"):
            self.install.recover(False)
        self.assertTrue(self.install.journal.exists())
        setup.atomic_write(self.install.target(first), changes[first][1])
        self.install.recover(False)
        self.assertEqual(self.tree(), {})

    def test_state_cannot_nominate_credentials_or_arbitrary_paths(self):
        self.install.apply(self.install.plan())
        state = json.loads(self.install.state.read_text())
        for key in ("../../foreign", "auth/pool.json", "settings", "state"):
            bad = copy.deepcopy(state)
            bad["files"][key] = {"sha256": "a" * 64, "mode": 0o600}
            self.install.state.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                self.install.plan(True)

    def test_uninstall_preserves_settings_edits_made_after_install(self):
        self.install.apply(self.install.plan())
        path = self.agent / "settings.json"
        settings = json.loads(path.read_text())
        settings["extensions"].append({"path": "foreign", "enabled": True})
        settings["defaultModel"] = "changed after install"
        path.write_text(json.dumps(settings))
        self.install.apply(self.install.plan(True))
        self.assertEqual(json.loads(path.read_text()), {"extensions": [{"path": "foreign", "enabled": True}], "defaultModel": "changed after install"})

    def test_state_is_bound_to_task_home(self):
        self.install.apply(self.install.plan())
        other = setup.Setup(self.root / "different home", self.agent)
        with self.assertRaisesRegex(ValueError, "invalid Pi setup state"):
            other.plan(True)

    def test_symlink_destination_and_parent_are_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.home.mkdir()
        (self.home / ".local").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.install.plan()
        self.assertEqual(list(outside.iterdir()), [])

    def legacy_install(self):
        self.install.apply(self.install.plan())
        state = json.loads(self.install.state.read_text())
        for key in ("auth/accounts.mjs", "auth/cli.mjs", "auth/pi-sdk.mjs", "wrapper", "service", "timer"):
            value = setup.content(("synthetic historical " + key + "\n").encode(), 0o755 if key == "wrapper" else 0o644)
            setup.atomic_write(self.install.target(key), value)
            state["files"][key] = setup.signature(value)
        setup.atomic_write(self.install.state, setup.content(setup.encoded(state), 0o600))
        return state

    def test_default_update_and_uninstall_preserve_legacy_account_outputs(self):
        state = self.legacy_install()
        legacy = {key: self.install.target(key).read_bytes() for key in state["files"] if key.startswith("auth/") or key in {"wrapper", "service", "timer"}}
        self.install.target("wrapper").write_text("operator modified legacy wrapper\n")
        legacy["wrapper"] = self.install.target("wrapper").read_bytes()
        self.install.apply(self.install.plan())
        self.install.apply(self.install.plan(uninstall=True))
        for key, data in legacy.items():
            self.assertEqual(self.install.target(key).read_bytes(), data)
        self.assertFalse(json.loads(self.install.state.read_text())["extension"])

    def test_default_permission_changes_preserve_external_wrapper_symlink_until_retirement(self):
        self.legacy_install()
        wrapper = self.install.target("wrapper")
        wrapper.unlink()
        external = self.root / "external-npm-cli.mjs"
        external.write_text("external npm source\n")
        wrapper.symlink_to(external)
        (self.repo / "pi/permissions/index.ts").write_text("export default function updated() {}\n")
        self.install.apply(self.install.plan())
        self.assertIn("updated", self.install.target("permissions/index.ts").read_text())
        self.install.apply(self.install.plan(uninstall=True))
        self.assertTrue(wrapper.is_symlink())
        self.assertEqual(external.read_text(), "external npm source\n")
        self.assertIn("wrapper", json.loads(self.install.state.read_text())["files"])
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.install.plan(retire_accounts=True)
        self.assertEqual(self.tree(), before)
        self.assertEqual(external.read_text(), "external npm source\n")

    def test_default_permission_changes_do_not_follow_legacy_module_directory_symlink(self):
        self.legacy_install()
        directory = self.home / ".local/lib/pi-accounts"
        external = self.root / "external-module-directory"
        directory.rename(external)
        directory.symlink_to(external, target_is_directory=True)
        expected = {path.name: path.read_bytes() for path in external.iterdir()}
        self.install.apply(self.install.plan())
        self.install.apply(self.install.plan(uninstall=True))
        self.assertTrue(directory.is_symlink())
        self.assertEqual({path.name: path.read_bytes() for path in external.iterdir()}, expected)
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.install.plan(retire_accounts=True)
        self.assertEqual(self.tree(), before)
        self.assertEqual({path.name: path.read_bytes() for path in external.iterdir()}, expected)

    def test_explicit_retirement_preserves_credentials_settings_and_future_npm_wrapper(self):
        self.legacy_install()
        auth = self.write(".pi/agent/auth.json", '{"synthetic":"unchanged"}')
        pool = self.write(".pi/agent/accounts/pool.json", '{"synthetic":"selected"}')
        before = (auth.read_bytes(), pool.read_bytes(), (self.agent / "settings.json").read_bytes())
        plan = self.install.plan(retire_accounts=True)
        self.assertIn("wrapper", plan)
        self.assertTrue(self.install.target("wrapper").exists())
        self.install.apply(plan)
        self.assertFalse(self.install.target("wrapper").exists())
        self.assertEqual((auth.read_bytes(), pool.read_bytes(), (self.agent / "settings.json").read_bytes()), before)
        npm = self.write("npm-prefix/bin/pi-accounts", "external npm tool\n")
        self.install.target("wrapper").symlink_to(npm)
        self.install.apply(self.install.plan(uninstall=True))
        self.assertTrue((self.home / ".local/bin/pi-accounts").is_symlink())
        self.assertEqual(npm.read_text(), "external npm tool\n")

    def test_retirement_modified_or_unowned_files_fail_closed(self):
        self.legacy_install()
        self.install.target("service").write_text("operator modified unit\n")
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "modified"):
            self.install.plan(retire_accounts=True)
        self.assertEqual(self.tree(), before)



if __name__ == "__main__":
    unittest.main()
