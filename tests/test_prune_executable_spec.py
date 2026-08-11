"""Executable specification for ownership-safe plain-file Codex prune."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def file_inventory(root: Path) -> dict[str, tuple[str, int]]:
    """Return public file signatures without using installer implementation helpers."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            stat.S_IMODE(path.stat().st_mode),
        )
        for path in root.rglob("*")
        if path.is_file()
    }


class OwnershipSafePruneExecutableSpecTest(unittest.TestCase):
    def test_ownership_safe_stale_directory_prune_is_selective_and_retryable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, home, outside = root / "repo", root / "codex-home", root / "outside"
            slug = f"pilot-{secrets.token_hex(6)}"
            foreign_slug = f"foreign-{secrets.token_hex(6)}"
            skill_bytes = f"---\nname: {slug}\ndescription: Randomized pilot fixture.\n---\n\n{secrets.token_hex(24)}\n".encode()
            tool_bytes = f"#!/bin/sh\nprintf '%s\\n' '{secrets.token_hex(24)}'\n".encode()
            foreign_bytes = secrets.token_bytes(47)
            outside_bytes = secrets.token_bytes(31)

            shutil.copytree(
                REPO_ROOT / "scripts",
                repo / "scripts",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )

            source_dir = repo / "codex" / "skills" / slug
            source_dir.mkdir(parents=True)
            (source_dir / "SKILL.md").write_bytes(skill_bytes)
            tool_source = source_dir / "tool.sh"
            tool_source.write_bytes(tool_bytes)
            tool_source.chmod(0o755)
            catalog = {
                "assets_comment": "randomized ownership-safe prune fixture",
                "skills": [{
                    "id": slug,
                    "kind": "skill",
                    "platforms": ["codex"],
                    "owner": "agents",
                    "source": {"codex": f"codex/skills/{slug}"},
                    "install_target": {"codex": f"skills/{slug}"},
                }],
                "commands": [],
                "subagents": [],
                "rules": [],
                "hooks": [],
                "global_instructions": [],
                "traveling_documents": [],
            }
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            outside.mkdir()
            outside_sentinel = outside / "sentinel.bin"
            outside_sentinel.write_bytes(outside_bytes)
            outside_before = file_inventory(outside)
            env = {**os.environ, "CODEX_HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1"}
            wrapper = repo / "scripts" / "install-codex.sh"

            installed = subprocess.run(["bash", str(wrapper)], cwd=repo, env=env, text=True, capture_output=True, check=False)
            self.assertEqual(installed.returncode, 0, installed.stderr)

            installed_skill = home / "skills" / slug / "SKILL.md"
            installed_tool = home / "skills" / slug / "tool.sh"
            state_path = home / ".agents-install-state.json"
            original_state = json.loads(state_path.read_text(encoding="utf-8"))
            skill_target = f"skills/{slug}/SKILL.md"
            tool_target = f"skills/{slug}/tool.sh"
            self.assertEqual(set(original_state["files"]), {skill_target, tool_target})
            self.assertEqual(installed_skill.read_bytes(), skill_bytes)
            self.assertEqual(installed_tool.read_bytes(), tool_bytes)
            original_tool_mode = stat.S_IMODE(installed_tool.stat().st_mode)
            self.assertEqual(original_tool_mode, 0o755)

            foreign = home / "skills" / foreign_slug / "sentinel.bin"
            foreign.parent.mkdir(parents=True)
            foreign.write_bytes(foreign_bytes)
            catalog["skills"] = []
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            shutil.rmtree(source_dir)
            installed_tool.chmod(0o700)

            first = subprocess.run(["bash", str(wrapper), "--prune"], cwd=repo, env=env, text=True, capture_output=True, check=False)
            self.assertEqual(first.returncode, 2, "chmod-only conflict must return exit 2")
            self.assertIn("CONFLICT", first.stderr, "exit 2 must identify a semantic conflict category")
            self.assertIn(tool_target, first.stderr, "the conflict must identify the unresolved public target")
            self.assertFalse(installed_skill.exists(), "unchanged retired sibling must be removed")
            self.assertTrue(installed_tool.exists(), "chmod-only retired file must be preserved")
            self.assertEqual(installed_tool.read_bytes(), tool_bytes, "preserved retired bytes must not be rewritten")
            self.assertEqual(stat.S_IMODE(installed_tool.stat().st_mode), 0o700, "preserved retired mode must not be rewritten")
            self.assertTrue(foreign.exists(), "foreign sentinel must survive prune")
            self.assertEqual(foreign.read_bytes(), foreign_bytes, "foreign sentinel bytes must remain unchanged")
            self.assertEqual(file_inventory(outside), outside_before, "wrapper must not write outside fixture repo and scratch home")

            retained = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(set(retained["files"]), {tool_target}, "unresolved historical state must be retained exactly")
            self.assertEqual(retained["files"][tool_target], original_state["files"][tool_target], "retained retry authority must equal the installed public record")
            self.assertNotIn(f"skills/{foreign_slug}/sentinel.bin", retained["files"], "foreign sentinel must remain unrecorded")

            installed_tool.chmod(original_tool_mode)
            retry = subprocess.run(["bash", str(wrapper), "--prune"], cwd=repo, env=env, text=True, capture_output=True, check=False)
            self.assertEqual(retry.returncode, 0, retry.stderr)
            self.assertFalse(installed_tool.exists(), "exact retry must remove the restored retired file")
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["files"], {}, "exact retry must clear resolved file history")
            self.assertTrue(foreign.exists(), "foreign sentinel must survive exact retry")
            self.assertEqual(foreign.read_bytes(), foreign_bytes)
            self.assertEqual(file_inventory(outside), outside_before)


if __name__ == "__main__":
    unittest.main()
