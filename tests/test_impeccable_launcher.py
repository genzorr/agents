"""Managed Impeccable launches keep provider execution in the current session."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(os.name == "nt", "POSIX launcher behavior; native CMD requires Windows")
class ImpeccableLauncherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(prefix="impeccable-launch-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.engine = self.root / "fake engine"
        self.engine.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "if sys.argv[1:] == ['engine-probe']: print('impeccable-engine 0.1.14'); sys.exit(0)\n"
            "print(json.dumps({'args': sys.argv[1:], 'provider': os.environ.get('IMPECCABLE_LIVE_COPY_AGENT'), "
            "'updates': os.environ.get('IMPECCABLE_NO_UPDATE_CHECK'), 'skill': os.environ.get('IMPECCABLE_SKILL_DIR')}))\n"
            "sys.exit(19)\n"
        )
        self.engine.chmod(0o755)
        self.env = {
            **os.environ,
            "IMPECCABLE_BIN": str(self.engine),
            "IMPECCABLE_LIVE_COPY_AGENT": "codex",
            "IMPECCABLE_NO_UPDATE_CHECK": "0",
        }
        self.env.pop("IMPECCABLE_SKILL_DIR", None)
        self.env.pop("IMPECCABLE_SELF", None)

    def launcher(self, provider: str) -> Path:
        skill = self.root / provider / "skill with spaces"
        shutil.copytree(ROOT / provider / "skills/impeccable", skill)
        return skill / "scripts/impeccable"

    def test_commands_inherit_no_provider_mode_and_preserve_arguments_and_failure(self) -> None:
        for provider in ("codex", "claude"):
            with self.subTest(provider=provider):
                launcher = self.launcher(provider)
                result = subprocess.run(
                    [str(launcher), "context", "--target", "a file; $(not a command).tsx"],
                    env=self.env, text=True, capture_output=True, check=False,
                )
                self.assertEqual(result.returncode, 19)
                output = json.loads(result.stdout)
                self.assertEqual(output["args"], ["context", "--target", "a file; $(not a command).tsx"])
                self.assertEqual(output["provider"], "off")
                self.assertEqual(output["updates"], "1")
                self.assertEqual(Path(output["skill"]), launcher.parent.parent)

    def test_unreviewed_engine_is_refused_before_command_execution(self) -> None:
        self.engine.write_text("#!/bin/sh\necho impeccable-engine 99.0.0\n")
        for provider in ("codex", "claude"):
            with self.subTest(provider=provider):
                result = subprocess.run(
                    [str(self.launcher(provider)), "context"], env=self.env,
                    text=True, capture_output=True, check=False,
                )
                self.assertEqual(result.returncode, 127)
                self.assertEqual(result.stdout, "")
                self.assertIn("unreviewed engine", result.stderr)

    def test_failed_handshake_is_refused_even_with_matching_version_text(self) -> None:
        self.engine.write_text("#!/bin/sh\necho impeccable-engine 0.1.14\nexit 7\n")
        result = subprocess.run(
            [str(self.launcher("codex")), "context"], env=self.env,
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 127)
        self.assertEqual(result.stdout, "")

    def test_direct_runner_aliases_cannot_override_disabled_provider(self) -> None:
        for provider in ("codex", "claude"):
            launcher = self.launcher(provider)
            for verb in ("live-commit-manual-edits", "commit-manual-edits"):
                for option in ("--provider=codex", "--provider=claude", "--provider=auto"):
                    with self.subTest(provider=provider, verb=verb, option=option):
                        result = subprocess.run(
                            [str(launcher), verb, option], env=self.env,
                            text=True, capture_output=True, check=False,
                        )
                        self.assertEqual(result.returncode, 2)
                        self.assertEqual(result.stdout, "")
                        self.assertIn("current agent session", result.stderr)


if __name__ == "__main__":
    unittest.main()
