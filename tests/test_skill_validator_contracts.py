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
    def test_production_catalog_validates(self) -> None:
        errors, _warnings = validate_catalog(REPO_ROOT)
        self.assertEqual(errors, [])

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

    def test_all_managed_skills_materialize_their_runtime_doc_reference_closure(self) -> None:
        assets = load_catalog(REPO_ROOT)
        for platform in ("codex", "claude"):
            installed = desired_files(REPO_ROOT, assets, platform)
            for asset in assets:
                if asset.kind != "skill" or platform not in asset.platforms:
                    continue
                skill = asset.id
                skill_root = f"skills/{skill}"
                owned = [item for item in installed.values() if item.asset.id == skill]
                self.assertTrue(owned, f"{platform}/{skill}: no desired files")
                for item in owned:
                    text = item.source.read_text(encoding="utf-8", errors="ignore")
                    for reference in VALIDATE_SKILLS.doc_references(text):
                        target = f"{skill_root}/{reference}"
                        self.assertIn(target, installed, f"{platform}/{skill}: installed reference does not resolve: {reference}")
                        self.assertEqual(installed[target].asset.id, skill)
                        self.assertEqual(installed[target].source.resolve(), (REPO_ROOT / reference).resolve())

    def test_architecture_review_materializes_shared_references(self) -> None:
        assets = load_catalog(REPO_ROOT)
        expected_references = (
            (REPO_ROOT / "docs" / "multi-entrypoint-capability-review.md").resolve(),
            (REPO_ROOT / "docs" / "comprehensive-codebase-audit.md").resolve(),
        )
        for platform in ("codex", "claude"):
            installed = desired_files(REPO_ROOT, assets, platform)
            for expected_source in expected_references:
                target = f"skills/architecture-review/docs/{expected_source.name}"
                self.assertIn(target, installed)
                self.assertEqual(installed[target].asset.id, "architecture-review")
                self.assertEqual(installed[target].source.resolve(), expected_source)

    def test_skill_local_doc_layer_satisfies_catalog_travel_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "codex", "portable", "Open `docs/policy.md` before continuing.")
            policy = repo / "docs" / "policy.md"
            policy.parent.mkdir()
            policy.write_text("Open `docs/nested.md` before continuing.\n", encoding="utf-8")
            nested = repo / "docs" / "nested.md"
            nested.write_text("Nested policy.\n", encoding="utf-8")
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex"], "owner": "agents", "source": {"codex": [{"path": "codex/skills/portable", "target": "skills/portable"}, {"path": "docs/policy.md", "target": "skills/portable/docs/policy.md"}, {"path": "docs/nested.md", "target": "skills/portable/docs/nested.md"}]}, "install_target": {"codex": "skills/portable"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            errors, warnings = validate_catalog(repo)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_home_root_travel_does_not_satisfy_a_skill_relative_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "codex", "portable", "Open `docs/policy.md` before continuing.")
            policy = repo / "docs" / "policy.md"
            policy.parent.mkdir()
            policy.write_text("Portable policy.\n", encoding="utf-8")
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex"], "owner": "agents", "source": {"codex": "codex/skills/portable"}, "install_target": {"codex": "skills/portable"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": [{"id": "policy-doc", "kind": "traveling_document", "platforms": ["codex"], "owner": "agents", "source": {"codex": "docs/policy.md"}, "install_target": {"codex": "docs/policy.md"}}]}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            errors, warnings = validate_catalog(repo)

        self.assertEqual(warnings, [])
        self.assertEqual(errors, ["portable (codex): skill-relative doc reference is not materialized by the same asset: docs/policy.md"])

    def test_unlabeled_former_allowlist_name_fails_both_validators(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "codex", "portable", "Open `docs/loop-closure.md` before continuing.")
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex"], "owner": "agents", "source": {"codex": "codex/skills/portable"}, "install_target": {"codex": "skills/portable"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            catalog_errors, catalog_warnings = validate_catalog(repo)
            skill_errors, skill_warnings = VALIDATE_SKILLS.check_doc_references(repo / "codex" / "skills" / "portable", repo)

        self.assertEqual(catalog_warnings, [])
        self.assertEqual(catalog_errors, ["portable (codex): doc reference not found: docs/loop-closure.md"])
        self.assertEqual(skill_warnings, [])
        self.assertEqual(skill_errors, ["portable: doc reference not found: docs/loop-closure.md"])

    def test_catalog_and_skill_validator_share_line_local_example_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            body = "Example-only: `docs/prefix.md`\ndocs/plain-suffix.md (example-only)\n`docs/backtick-suffix.md` (example-only)\n\"docs/quote-suffix.md\" (example-only)\n"
            write_skill(repo, "codex", "portable", body)
            catalog = {"assets_comment": "fixture", "skills": [{"id": "portable", "kind": "skill", "platforms": ["codex"], "owner": "agents", "source": {"codex": "codex/skills/portable"}, "install_target": {"codex": "skills/portable"}}], "commands": [], "subagents": [], "rules": [], "hooks": [], "global_instructions": [], "traveling_documents": []}
            (repo / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            catalog_errors, catalog_warnings = validate_catalog(repo)
            skill_errors, skill_warnings = VALIDATE_SKILLS.check_doc_references(repo / "codex" / "skills" / "portable", repo)

        self.assertEqual(VALIDATE_SKILLS.classified_doc_references(body), ([], ["docs/backtick-suffix.md", "docs/plain-suffix.md", "docs/prefix.md", "docs/quote-suffix.md"]))
        self.assertEqual(catalog_errors, [])
        self.assertEqual(len(catalog_warnings), 4)
        self.assertTrue(all("classified example-only" in warning for warning in catalog_warnings))
        self.assertEqual(skill_errors, [])
        self.assertEqual(len(skill_warnings), 4)
        self.assertTrue(all("classified example-only" in warning for warning in skill_warnings))

    def test_shared_classifier_accepts_opening_delimiters_for_home_labels(self) -> None:
        text = "Example-only: `/Users/alice/example.md`\nruntime-home: \"~/.cache/tool\"\n"
        dependencies, examples, runtime_homes = VALIDATE_SKILLS.user_home_references(text)
        self.assertEqual(dependencies, [])
        self.assertEqual(examples, ["/Users/alice/example.md"])
        self.assertEqual(runtime_homes, ["~/.cache/tool"])

    def test_only_real_home_root_document_consumer_remains(self) -> None:
        catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual([entry["id"] for entry in catalog["traveling_documents"]], ["model-and-effort-doc"])

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
