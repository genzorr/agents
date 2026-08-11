"""Static contracts for goal quality, Sol–Luna orchestration, and research sufficiency."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class GoalSolLunaResearchContractsTest(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPO_ROOT / relative).read_text(encoding="utf-8")

    def test_goal_prompt_twins_share_one_goal_quality_contract(self) -> None:
        codex = self.read("codex/skills/goal-prompt/SKILL.md")
        claude = self.read("claude/skills/goal-prompt/SKILL.md")
        for text in (codex, claude):
            self.assertIn("## Goal Quality And Completion Contract", text)
            self.assertIn("Every durable goal spec must contain one integrated `Completion Contract`", text)
            self.assertIn("one integrated `Completion Contract`", text)
            for field in (
                "**Outcome:**",
                "**Evidence:**",
                "**Success threshold:**",
                "**Boundaries:**",
                "**Stop/ask gates:**",
                "**Continue conditions:**",
                "**Blocked exit:**",
                "**Evaluator integrity:**",
            ):
                self.assertIn(field, text)
            self.assertIn("Repair activity-only goals", text)
            self.assertIn("Do not score goals numerically", text)
            self.assertIn("<YYYYMMDD-HHMMSS>-<task-slug>-<short-id>-goal.md", text)
            self.assertIn("never overwrite or reuse an earlier goal spec", text)
            self.assertIn("Add the Completion Contract to every spec", text)
            self.assertIn("task or slice the target must activate and read", text)
            self.assertIn("immediate handoff to a target already anchored to the verified same checkout", text)
            self.assertIn("authoring machine's inaccessible `/tmp`", text)
            self.assertIn("Expected Starting Ref", text)
            self.assertIn("Material Drift Check", text)
            self.assertIn("## Frozen Experiment Protocol", text)
            self.assertIn("`protocol_sha256`", text)
            self.assertIn("Route completed runs through `review-experiment`", text)
            self.assertIn("same `<YYYYMMDD-HHMMSS>-<task-slug>-<short-id>` stem", text)
            self.assertIn("with a `-prd.md` suffix", text)
            self.assertIn("durable source of truth", text)
            self.assertNotIn("name: define-goal", text)

    def test_goal_prompt_uses_task_triggered_clauses_without_modes(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/goal-prompt/SKILL.md")
            self.assertIn("## Task-Triggered Clauses", text, platform)
            self.assertIn("Do not classify the task into a mode", text, platform)
            self.assertNotIn("## Conditional Modes", text, platform)
            for clause in (
                "**Deadline or timebox:**",
                "**Evidence-directed exploration:**",
                "**Multiple checkpoints:**",
            ):
                self.assertIn(clause, text, platform)
            self.assertIn("add only clauses required by explicit task facts", text, platform)
            self.assertIn("Do not add a P0/P1/P2 board", text, platform)
            self.assertIn("Duration alone does not require a PRD", text, platform)
            self.assertIn("project or benchmark defaults", text, platform)
            self.assertIn("calibrated evidence bar before rejecting an approach family", text, platform)
            self.assertIn("require measurement for performance claims", text, platform)
            self.assertIn("default to repeated runs for remote or noisy benchmarks", text, platform)
            self.assertIn("label timing evidence inconclusive until that requirement is met", text, platform)
            self.assertIn("Update only the spec already created for this same handoff", text, platform)

    def test_goal_prompt_preserves_lineage_and_non_git_drift_guards(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/goal-prompt/SKILL.md")
            self.assertIn("current Git `HEAD` that is neither the expected ref nor its descendant", text, platform)
            self.assertIn("For non-Git targets, capture a stable version or digest", text, platform)
            self.assertIn("stop if none can be established", text, platform)

    def test_goal_prompt_preserves_platform_specific_bootstrap(self) -> None:
        codex = self.read("codex/skills/goal-prompt/SKILL.md")
        claude = self.read("claude/skills/goal-prompt/SKILL.md")
        self.assertIn("For Codex `/goal`", codex)
        self.assertIn("Set a compact Codex goal", codex)
        self.assertIn("preserves any deadline and stop gates from it", codex)
        self.assertIn("For Claude Code", codex)
        self.assertIn("This skill targets Claude Code directly", claude)
        self.assertIn("Do not tell Claude to set a goal", claude)
        self.assertIn("including any deadline and stop gates it defines", claude)
        self.assertNotIn("Set a compact Codex goal", claude)

    def test_sol_luna_is_operator_controlled_codex_only_lens(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        metadata = self.read("codex/skills/sol-luna-orchestration/agents/openai.yaml")
        catalog = json.loads(self.read("catalog.json"))
        entries = {entry["id"]: entry for entry in catalog["skills"]}
        self.assertIn("sol-luna-orchestration", entries)
        entry = entries["sol-luna-orchestration"]
        self.assertEqual(entry["platforms"], ["codex"])
        self.assertEqual(entry["source"], {"codex": "codex/skills/sol-luna-orchestration"})
        self.assertEqual(entry["install_target"], {"codex": "skills/sol-luna-orchestration"})
        self.assertIn("role:lens", entry.get("tags", []))
        self.assertFalse((REPO_ROOT / "claude/skills/sol-luna-orchestration").exists())
        self.assertIn("Use only when the operator explicitly invokes", text)
        self.assertIn("Composition role: lens", text)
        self.assertIn("does not itself launch work", text)
        self.assertIn("does not own task lifecycle", text)
        self.assertIn("active protocol or driver decides whether an implementation step may be delegated", text)
        self.assertIn("## Configure Only", text)
        self.assertIn("return without launching Luna", text)
        self.assertIn("does not carry to a later task", text)
        self.assertIn("a provisional configuration requires a fresh invocation after the task is resolved", text)
        self.assertIn('display_name: "Sol-Luna Orchestration"', metadata)
        self.assertIn("default_prompt: \"Use $sol-luna-orchestration", metadata)
        self.assertIn("policy:\n  allow_implicit_invocation: false\n", metadata)
        self.assertNotIn("allow_implicit_invocation: true", metadata)

    def test_sol_luna_contract_preserves_thread_authority_and_no_wait(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for phrase in (
            "Sol remains planner, decision-maker, orchestrator, reviewer, and acceptance authority",
            "Use ordinary Codex threads, not subagents",
            "Do not change the current thread's model",
            "originating Sol thread ID",
            "operator's explicit lens invocation requests a Luna worker",
            "name the Luna model choice plus any intentional effort override",
            "Create a new ordinary Codex thread using Luna",
            "current driver already requires a durable checkpoint",
            "immediately return a concise normal response",
            "Do not wait, poll, repeatedly check status",
            "Luna's report is evidence, not acceptance",
            "same Luna thread",
            "Dispatch is not completion",
            "operator asks for status or resumes after an expected report did not arrive",
            "only when the check shows the thread idle or ended with no report delivered",
            "If the check shows work in progress, report that status and do not re-send",
            "never launch a replacement thread silently",
            "Never upgrade Luna work to Sol automatically",
            "Parallelism does not authorize Git worktrees",
            "report the exact missing capability",
        ):
            self.assertIn(phrase, text)
        for forbidden in ("spawn_agent", "codex-reply", "thread/start", "turn/start"):
            self.assertNotIn(forbidden, text)

    def test_luna_worker_contract_is_compact_and_complete(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for field in (
            "**Objective:**",
            "**Durable references:**",
            "**Scope and ownership:**",
            "**Authority:**",
            "**Success criteria:**",
            "**Verification:**",
            "**Stop/ask gates:**",
            "**Return route:**",
            "**Return format:**",
        ):
            self.assertIn(field, text)
        self.assertIn("outcome, changed files or commit, verification, blockers, and material uncertainty", text)
        self.assertIn("point to files instead of pasting their contents", text)
        self.assertIn("Do not include builder reasoning", text)

    def test_research_prompt_twins_share_sufficiency_contract(self) -> None:
        codex = self.read("codex/skills/research-prompt/SKILL.md")
        claude = self.read("claude/skills/research-prompt/SKILL.md")
        for text in (codex, claude):
            self.assertIn("## Research Quality Contract", text)
            for field in (
                "**Decision or downstream action:**",
                "**Evidence standard:**",
                "**Scope boundaries:**",
                "**Sufficiency bar:**",
                "**Unresolved/stop condition:**",
            ):
                self.assertIn(field, text)
            self.assertIn("Do not score research numerically", text)
            self.assertIn("final gap review", text)
            self.assertIn("preserve the gap explicitly", text)
        self.assertIn("open `reference.md`", claude)
        reference = self.read("claude/skills/research-prompt/reference.md")
        self.assertIn("## Research Quality Contract", reference)
        self.assertIn("**Sufficiency bar:**", reference)
        self.assertIn("explicit no-decision result", reference)

    def test_research_skill_family_is_retained_without_define_goal(self) -> None:
        catalog = json.loads(self.read("catalog.json"))
        entries = {entry["id"]: entry for entry in catalog["skills"]}
        self.assertIn("research-prompt", entries)
        self.assertIn("integrate-research", entries)
        self.assertNotIn("define-goal", entries)


if __name__ == "__main__":
    unittest.main()
