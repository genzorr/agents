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

    def test_goal_prompt_conditionally_preserves_semantics_and_rejects_shortcuts(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/goal-prompt/SKILL.md")
            for phrase in (
                "implements a source or paper, claims a behavior-preserving refactor, or transforms data whose meaning must survive",
                "require discriminating proof that would fail for that shortcut",
                "when exact semantic preservation is immaterial",
            ):
                self.assertIn(phrase, text, f"{platform}: {phrase}")

    def test_goal_prompt_carries_reviewed_behavior_spines_into_completion_contracts(self) -> None:
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/goal-prompt/SKILL.md")
            for phrase in (
                "**Reviewed behavior spine:**",
                "approved behavior authority",
                "supported public seam",
                "prohibited shortcuts",
                "independent oracle",
                "semantics-preserving implementation refactor to remain green",
                "detector ledger for deleted or weakened tests",
                "small local changes or unstable behavior",
            ):
                self.assertIn(phrase, text, f"{platform}: {phrase}")

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
        entry = {item["id"]: item for item in catalog["skills"]}["sol-luna-orchestration"]

        self.assertEqual(entry["platforms"], ["codex"])
        self.assertEqual(entry["source"], {"codex": "codex/skills/sol-luna-orchestration"})
        self.assertFalse((REPO_ROOT / "claude/skills/sol-luna-orchestration").exists())
        for anchor in (
            "Use only when the operator explicitly invokes",
            "Composition role: lens",
            "## Configure Only",
            "return without launching a worker",
            "requires a fresh explicit invocation",
        ):
            self.assertIn(anchor, text)
        self.assertIn('display_name: "Sol-Luna Orchestration"', metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_sol_luna_preserves_default_routes_models_and_context_boundaries(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        defaults = text.split("## Preconditions And Defaults\n", 1)[1].split("## Operating Model", 1)[0]
        for anchor in (
            "Native Luna subagent",
            "Ordinary Codex task/thread",
            "Escalated independent review",
            "xhigh",
            "high",
            "only when the operator explicitly requests it",
            "never substitute silently",
        ):
            self.assertIn(anchor, defaults)
        for anchor in (
            "without parent-chat history by default",
            "Never inherit the full parent conversation",
            "Inherited history is context, not authority",
            "Keep every worker and reviewer a leaf",
            "Parallelism never authorizes a worktree",
        ):
            self.assertIn(anchor, text)
        for forbidden in ("spawn_agent", "codex-reply", "thread/start", "turn/start"):
            self.assertNotIn(forbidden, text)

    def test_sol_luna_dispatch_preamble_requires_nonduplicative_decision_trace(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        preamble = text.split("## Dispatch Preamble\n", 1)[1].split("## Worker Lifecycle And Continuity", 1)[0]
        for anchor in (
            "Before every dispatch, state the lane identity",
            "For a worker dispatch, also name",
            "root work this lane substitutes for",
            "unique output it owns",
            "named downstream decision it will affect or accelerate",
            "non-duplicative substitution rather than parallel coverage of an existing lane",
            "reviewer escalation adds independent judgment and is not a worker substitution",
        ):
            self.assertIn(anchor, preamble)

    def test_sol_luna_worker_contract_supports_handoffs_reuse_and_recovery(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for field in (
            "**Objective:**",
            "**Durable references:**",
            "**Scope and ownership:**",
            "**Interfaces:**",
            "**Authority:**",
            "**Context and continuity:**",
            "**Dependencies and handoffs:**",
            "**Success criteria:**",
            "**Verification:**",
            "**Stop/ask gates:**",
            "**Return route:**",
            "**Return format:**",
        ):
            self.assertIn(field, text)
        for anchor in (
            "Route every dependency through Sol",
            "Classify every worker as complete, blocked, partial, or failed",
            "Reuse a compatible idle worker",
            "assignment-reset overlay",
            "Compaction is expected",
            "Do not recycle for task granularity",
            "Report lost continuity",
            "Keep implementation and reviewer identities separate",
        ):
            self.assertIn(anchor, text)

    def test_sol_luna_reuses_luna_checks_and_requires_auditable_verification(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        operating = text.split("## Operating Model\n", 1)[1].split("## Decompose And Route", 1)[0]
        for anchor in (
            "do not rerun them routinely",
            "missing, stale after integration, contradicted",
            "decision-critical question",
            "A worker report is evidence, not acceptance",
        ):
            self.assertIn(anchor, operating)
        worker_contract = text.split("## Compact Worker Contract\n", 1)[1].split("## Worker Rules", 1)[0]
        for anchor in ("commands run", "exact checkout state tested", "paths and criteria covered"):
            self.assertIn(anchor, worker_contract)
        worker_rules = text.split("## Worker Rules\n", 1)[1].split("## Escalated Independent Sol Review", 1)[0]
        for anchor in (
            "governing contracts",
            "decision-bearing artifact",
            "producer success signals",
            "consequence tests",
            "implementation-derived oracles",
            "failure surface",
        ):
            self.assertIn(anchor, worker_rules)

    def test_sol_luna_escalates_review_only_when_independence_has_material_value(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        review = text.split("## Escalated Independent Sol Review\n", 1)[1].split("## Operator-Requested Thread Route", 1)[0]
        for anchor in (
            "Main Sol is the default reviewer",
            "named acceptance-critical target",
            "material expected value",
            "conflicting plausible interpretations",
            "named reliable deterministic oracle",
            "concrete anchoring concern",
            "cross-worker boundary",
            "Generic confidence",
            "If any part is missing, do not dispatch",
            "Reuse one compatible idle Sol reviewer",
            "Create a fresh Sol/high reviewer only when escalation is required",
            "references/sol-reviewer-protocol.md",
        ):
            self.assertIn(anchor, review)
        self.assertNotIn("claude-headless", text)
        self.assertNotIn("Opus", text)

        protocol = self.read("codex/skills/sol-luna-orchestration/references/sol-reviewer-protocol.md")
        for anchor in (
            "checkout is quiescent",
            "read-only, no-mutation, no-delegation",
            "ship",
            "fix-first",
            "rethink",
            "blocked",
            "failed",
            "voided",
            "main Sol remains acceptance authority",
            "Reuse the reviewer across fixes and later tasks",
        ):
            self.assertIn(anchor, protocol)

    def test_sol_luna_preserves_operator_requested_thread_delivery(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        route = text.split("## Operator-Requested Thread Route\n", 1)[1].split("## Sol Depth Budget", 1)[0]
        for anchor in (
            "originating Sol session ID",
            "operator requested the ordinary Luna task/thread route",
            "return the launch response immediately",
            "do not wait or poll",
            "fresh lens invocation",
            "Launched Luna task/thread <thread-id>",
        ):
            self.assertIn(anchor, route)

    def test_sol_luna_uses_progressive_disclosure(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        protocol = self.read("codex/skills/sol-luna-orchestration/references/sol-reviewer-protocol.md")
        self.assertLess(len(text.split()), 3600)
        self.assertLess(len(protocol.split()), 1500)
        self.assertIn("read [references/sol-reviewer-protocol.md]", text)
        self.assertNotIn("voided", text)
        self.assertIn("voided", protocol)

    def test_sol_luna_supports_explicit_alternate_worker_profiles_without_changing_defaults(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        metadata = self.read("codex/skills/sol-luna-orchestration/agents/openai.yaml")
        frontmatter = text.split("---\n", 2)[1]
        defaults = text.split("## Preconditions And Defaults\n", 1)[1].split("## Operating Model", 1)[0]
        for anchor in (
            "Luna/xhigh remains the default profile",
            "selected native implementation subagent",
            "only when the operator explicitly requests it",
            "never raise its model or effort without an explicit operator request",
            "operator-authorized ordinary-task launch contract satisfies this requirement",
            "an agent-relayed request without such an operator-authorized contract does not",
        ):
            self.assertIn(anchor, text)
        self.assertIn("gpt-5.6-luna", defaults)
        self.assertIn("xhigh", defaults)
        self.assertIn("reusable Luna/xhigh subagents by default", frontmatter)
        self.assertIn("Luna/xhigh", metadata)
        self.assertNotIn("Compact Luna Worker Contract", text)
        self.assertNotIn("Luna Worker Rules", text)

    def test_orchestrate_sol_feature_is_explicit_codex_only_helper(self) -> None:
        text = self.read("codex/skills/orchestrate-sol-feature/SKILL.md")
        metadata = self.read("codex/skills/orchestrate-sol-feature/agents/openai.yaml")
        catalog = json.loads(self.read("catalog.json"))
        entry = {item["id"]: item for item in catalog["skills"]}["orchestrate-sol-feature"]

        self.assertEqual(entry["platforms"], ["codex"])
        self.assertEqual(entry["source"], {"codex": "codex/skills/orchestrate-sol-feature"})
        self.assertEqual(entry["install_target"], {"codex": "skills/orchestrate-sol-feature"})
        self.assertEqual(entry["tags"], ["role:helper", "domain:orchestration"])
        self.assertFalse((REPO_ROOT / "claude/skills/orchestrate-sol-feature").exists())
        skill_files = {
            path.relative_to(REPO_ROOT / "codex/skills/orchestrate-sol-feature").as_posix()
            for path in (REPO_ROOT / "codex/skills/orchestrate-sol-feature").rglob("*")
            if path.is_file()
        }
        self.assertEqual(skill_files, {"SKILL.md", "agents/openai.yaml"})
        frontmatter = text.split("---\n", 2)[1]
        self.assertIn("Use only after the operator explicitly invokes orchestrate-sol-feature", frontmatter)
        self.assertIn("does not authorize unrelated work or broaden", frontmatter)
        self.assertIn("Composition role: helper", text)
        self.assertIn('display_name: "Orchestrate Sol Feature"', metadata)
        self.assertIn('short_description: "Dispatch Sol/high features with Sol/medium workers"', metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_orchestrate_sol_feature_enforces_the_three_level_owner_topology(self) -> None:
        text = self.read("codex/skills/orchestrate-sol-feature/SKILL.md")
        for anchor in (
            "ordinary `gpt-5.6-sol` / `high` task",
            "native `gpt-5.6-sol` / `medium` leaf subagent",
            "independent `gpt-5.6-sol` / `high` subagent",
            "Use the native ordinary-task creation surface, never a native subagent spawn",
            "The inner lens's no-worktree-without-operator-approval rule governs an additional worktree created after launch, not a task environment already assigned under this compliant outer policy",
            "title that distinguishes it from the project orchestrator and sibling feature owners",
            "project orchestrator must not spawn or duplicate the feature's implementation workers directly",
            "forbid workers from delegating",
            "forbid the feature owner from creating another ordinary task",
            "Forbid the inner ordinary Luna task/thread route",
            "owns integration, review, and feature-level acceptance",
        ):
            self.assertIn(anchor, text)

    def test_orchestrate_sol_feature_launch_contract_preserves_context_and_authority(self) -> None:
        text = self.read("codex/skills/orchestrate-sol-feature/SKILL.md")
        contract = text.split("## Feature Owner Launch Contract\n", 1)[1].split("## Constrain Feature-Owner Delegation", 1)[0]
        for field in (
            "**Objective:**",
            "**Durable references:**",
            "**Decisions, assumptions, unknowns, and non-goals:**",
            "**Project and starting state:**",
            "**Scope and shared state:**",
            "**Authority:**",
            "**Driver and lens:**",
            "**Worker profile and topology:**",
            "**Success criteria and artifacts:**",
            "**Verification and decision-bearing evidence:**",
            "**Stop/ask and reporting gates:**",
            "**Return route:**",
            "**Final handoff format:**",
        ):
            self.assertIn(field, contract)
        for anchor in (
            "never inherit or paste the full parent conversation",
            "Conversation history is context, not authority",
            "never broaden worktree, branch, push, PR, merge, live-install, or external-write authority",
            "one active durable writer per checkout",
            "do not fabricate one",
        ):
            self.assertIn(anchor, text)

    def test_orchestrate_sol_feature_reuse_identity_and_reporting_are_truthful(self) -> None:
        text = self.read("codex/skills/orchestrate-sol-feature/SKILL.md")
        reuse = text.split("## Select New Or Reused Ownership\n", 1)[1].split("## Launch A New Feature Owner", 1)[0]
        for anchor in (
            "Before every new or reused dispatch, require one active durable writer per checkout by default",
            "counting the project orchestrator and all feature owners",
            "If active-writer state cannot be recovered from recorded launches and native inspection, treat it as unresolved and serialize or ask",
            "Concurrent writers otherwise require disjoint ownership or explicit worktree authority",
            "exact known task identity",
            "A title, summary, or unsupported recollection is never sufficient",
            "send a complete reset",
            "Preserve a compatible task's configured model and effort",
            "Never replace a stalled, failed, or blocked owner silently",
        ):
            self.assertIn(anchor, reuse)
        for anchor in (
            "profile provenance, not independent metadata readback",
            "Never use a pending client identity where a ready task identity is required",
            "`launched, awaiting handoff`",
            "Do not poll repeatedly",
            "`complete`, `blocked`, `partial`, or `failed`",
        ):
            self.assertIn(anchor, text)

    def test_orchestrate_sol_feature_uses_progressive_disclosure(self) -> None:
        text = self.read("codex/skills/orchestrate-sol-feature/SKILL.md")
        inner = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        self.assertLess(len(text.split()), 3000)
        self.assertLess(len(inner.split()), 3600)

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
