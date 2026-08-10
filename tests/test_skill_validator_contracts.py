"""Focused behavior contracts for skill portability and ownership guards."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from scripts.agent_catalog import desired_files, load_catalog, validate_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = REPO_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATE_SKILLS = load_script("validate_skills")
CROSS_REPO = load_script("check_cross_repo_consistency")


def write_skill(repo: Path, platform: str, name: str, body: str = "") -> None:
    path = repo / platform / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nname: {name}\ndescription: Test skill.\n---\n\n{body}", encoding="utf-8")


class SkillValidatorContractsTest(unittest.TestCase):
    def test_file_valued_skill_source_user_home_dependency_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source = repo / "shared" / "portable.md"
            source.parent.mkdir(parents=True)
            source.write_text("Read /Users/alice/private-policy.md.\n", encoding="utf-8")
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex", "claude"], "owner": "agents", "source": {"codex": "shared/portable.md", "claude": "shared/portable.md"}, "install_target": {"codex": "skills/portable/SKILL.md", "claude": "skills/portable/SKILL.md"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            errors, _warnings = VALIDATE_SKILLS.validate_catalog_skill_sources(repo)

        self.assertEqual(len(errors), 2)
        self.assertTrue(all("operative user-home dependency" in error for error in errors))

    def test_shared_skill_source_user_home_dependency_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill = repo / "shared" / "skills" / "portable" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: portable\ndescription: Fixture skill.\n---\n\nRead /Users/alice/private-policy.md.\n", encoding="utf-8")
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex", "claude"], "owner": "agents", "source": {"codex": "shared/skills/portable", "claude": "shared/skills/portable"}, "install_target": {"codex": "skills/portable", "claude": "skills/portable"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            errors, _warnings = VALIDATE_SKILLS.validate_catalog_skill_sources(repo)

        self.assertEqual(len(errors), 2)
        self.assertTrue(all("operative user-home dependency" in error for error in errors))

    def test_platform_extra_file_requires_catalog_source_layer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill = repo / "shared" / "skills" / "portable" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: portable\ndescription: Fixture skill.\n---\n", encoding="utf-8")
            extra = repo / "codex" / "skills" / "portable" / "agents" / "openai.yaml"
            extra.parent.mkdir(parents=True)
            extra.write_text("interface:\n  display_name: Portable\n", encoding="utf-8")
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex", "claude"], "owner": "agents", "source": {"codex": "shared/skills/portable", "claude": "shared/skills/portable"}, "install_target": {"codex": "skills/portable", "claude": "skills/portable"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            errors, _warnings = validate_catalog(repo)

        self.assertEqual(errors, ["disk: codex/skills/portable/agents/openai.yaml has no catalog entry"])

    def test_shared_skill_sources_expand_identically_for_both_platforms(self) -> None:
        assets = load_catalog(REPO_ROOT)
        codex_files = desired_files(REPO_ROOT, assets, "codex")
        claude_files = desired_files(REPO_ROOT, assets, "claude")
        shared_root = REPO_ROOT / "shared" / "skills"
        shared_targets = {
            target: desired
            for target, desired in codex_files.items()
            if desired.asset.kind == "skill" and desired.source.is_relative_to(shared_root)
        }
        self.assertTrue(shared_targets)
        for target, codex_desired in shared_targets.items():
            self.assertIn(target, claude_files)
            self.assertEqual(codex_desired.source, claude_files[target].source)

    def test_user_home_dependency_requires_path_local_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = repo / "codex" / "skills" / "portable"
            write_skill(repo, "codex", "portable", "Open /Users/alice/private-policy.md before continuing.")
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(warnings, [])
            self.assertEqual(len(errors), 1)
            self.assertIn("operative user-home dependency", errors[0])

            write_skill(repo, "codex", "portable", "Example-only: /Users/alice/private-policy.md is illustrative.")
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 1)
            self.assertIn("classified example-only", warnings[0])

            write_skill(
                repo,
                "codex",
                "portable",
                "Read /Users/alice/private-policy.md; example-only: /Users/alice/illustration.md.",
            )
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(len(errors), 1)
            self.assertIn("/Users/alice/private-policy.md", errors[0])
            self.assertEqual(len(warnings), 1)
            self.assertIn("/Users/alice/illustration.md", warnings[0])

    def test_hard_coded_posix_and_windows_homes_need_example_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = repo / "codex" / "skills" / "portable"
            write_skill(
                repo,
                "codex",
                "portable",
                'Read "/home/alice/private.md", C:\\Users\\Alice\\private.md, and /Users/alice/private.md.',
            )
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(warnings, [])
            self.assertEqual(len(errors), 3)
            self.assertTrue(all("operative user-home dependency" in error for error in errors))

            write_skill(
                repo,
                "codex",
                "portable",
                "example-only: /home/alice/private.md; example-only: C:\\Users\\Alice\\private.md; example-only: /Users/alice/private.md.",
            )
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 3)
            self.assertTrue(all("classified example-only" in warning for warning in warnings))
            self.assertTrue(all(not warning.endswith(".") for warning in warnings))

            write_skill(repo, "codex", "portable", "runtime-home: /Users/alice/private.md")
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(warnings, [])
            self.assertEqual(len(errors), 1)
            self.assertIn("/Users/alice/private.md", errors[0])

    def test_home_relative_paths_need_example_or_runtime_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = repo / "codex" / "skills" / "portable"
            write_skill(repo, "codex", "portable", 'Read "~", "~/.cache/a.md", $HOME/.cache/b.md, and ${HOME}/.cache/c.md.')
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(warnings, [])
            self.assertEqual(len(errors), 4)

            write_skill(
                repo,
                "codex",
                "portable",
                "runtime-home: ~; runtime-home: ~/.cache/a.md; $HOME/.cache/b.md (runtime-home); example-only: ${HOME}/.cache/c.md.",
            )
            dependencies, examples, runtime_homes = VALIDATE_SKILLS.user_home_references(
                VALIDATE_SKILLS.skill_directory_text(skill_dir)
            )
            self.assertEqual(dependencies, [])
            self.assertEqual(examples, ["${HOME}/.cache/c.md"])
            self.assertEqual(runtime_homes, ["$HOME/.cache/b.md", "~", "~/.cache/a.md"])
            errors, warnings = VALIDATE_SKILLS.check_doc_references(skill_dir, repo)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 1)
            self.assertIn("example-only", warnings[0])

    def test_skill_lifecycle_twins_use_the_traveling_agents_policy(self) -> None:
        policy = (REPO_ROOT / "docs/skill-lifecycle-policy.md").read_text(encoding="utf-8")
        self.assertIn("Generic Skill Lifecycle Policy and Audit Method", policy)
        self.assertIn("Harness's lifecycle policy is the stricter project-specific overlay", policy)
        self.assertIn("hard-coded user-home dependency", policy)
        for platform in ("codex", "claude"):
            text = (REPO_ROOT / "shared" / "skills" / "skill-lifecycle" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("docs/skill-lifecycle-policy.md", text)
            self.assertIn("Harness lifecycle policy as the project-specific overlay", text)
            self.assertNotIn("/Users/", text)

    def test_claude_headless_physical_ownership_is_checked_for_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claude_headless = root / "claude-headless"
            write_skill(claude_headless, "codex", "claude-headless")
            write_skill(claude_headless, "codex", "delegate-to-claude")
            write_skill(claude_headless, "claude", "claude-headless")

            agents = root / "agents"
            harness = root / "harness"
            write_skill(agents, "codex", "claude-headless")
            errors = CROSS_REPO.check_disjoint_ownership(agents, harness, claude_headless)
            self.assertEqual(len(errors), 1)
            self.assertIn("agents and claude-headless", errors[0])

    def test_session_harvester_requires_canonical_owned_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            harvester = Path(tmp)
            script = harvester / "scripts" / "install-claude-skill.sh"
            script.parent.mkdir(parents=True)
            script.write_text("SRC=skills/harvest-sessions\n", encoding="utf-8")

            legacy = harvester / "harvest-sessions-skill.md"
            legacy.write_text("---\nname: harvest-sessions\n---\n", encoding="utf-8")
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("legacy harvest-sessions-skill.md is no longer supported" in error for error in errors))
            self.assertTrue(any("canonical skills/harvest-sessions must contain SKILL.md" in error for error in errors))

            canonical = harvester / "skills" / "harvest-sessions" / "SKILL.md"
            canonical.parent.mkdir(parents=True)
            canonical.write_text("---\nname: harvest-sessions\n---\n", encoding="utf-8")
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("legacy harvest-sessions-skill.md is no longer supported" in error for error in errors))

            legacy.unlink()
            self.assertEqual(CROSS_REPO.check_session_harvester(harvester), [])

            canonical.unlink()
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("must contain SKILL.md" in error for error in errors))

            canonical.write_text("---\nname: wrong-name\n---\n", encoding="utf-8")
            foreign = harvester / "skills" / "foreign-skill"
            foreign.mkdir()
            write_skill(harvester, "codex", "unexpected-skill")
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("frontmatter name" in error for error in errors))
            self.assertTrue(any("foreign skill directories" in error for error in errors))
            self.assertTrue(any("unexpected codex/ or claude/ skill tree" in error for error in errors))

    def test_session_harvester_canonical_layout_rejects_symlinked_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            harvester = Path(tmp) / "session-harvester"
            script = harvester / "scripts" / "install-claude-skill.sh"
            script.parent.mkdir(parents=True)
            script.write_text("SRC=skills/harvest-sessions\n", encoding="utf-8")
            unreadable_as_utf8 = Path(tmp) / "invalid-skill.md"
            unreadable_as_utf8.write_bytes(b"\xff")

            legacy = harvester / "harvest-sessions-skill.md"
            legacy.symlink_to(unreadable_as_utf8)
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("legacy harvest-sessions-skill.md is no longer supported" in error for error in errors))

            legacy.unlink()
            external_skill = Path(tmp) / "external-skill.md"
            external_skill.write_text("---\nname: harvest-sessions\n---\n", encoding="utf-8")
            external_dir = Path(tmp) / "external-skill"
            external_dir.mkdir()
            (external_dir / "SKILL.md").write_text("---\nname: harvest-sessions\n---\n", encoding="utf-8")
            canonical_dir = harvester / "skills" / "harvest-sessions"
            canonical_dir.parent.mkdir()
            canonical_dir.symlink_to(external_dir, target_is_directory=True)
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("canonical skills/harvest-sessions directory must not be a symlink" in error for error in errors))

            canonical_dir.unlink()
            canonical_dir.mkdir()
            (canonical_dir / "SKILL.md").symlink_to(external_skill)
            errors = CROSS_REPO.check_session_harvester(harvester)
            self.assertTrue(any("canonical skills/harvest-sessions/SKILL.md must not be a symlink" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
