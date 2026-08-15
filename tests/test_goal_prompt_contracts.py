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
        self.assertIn("active protocol or driver decides whether work may be delegated", text)
        self.assertIn("## Configure Only", text)
        self.assertIn("return without launching Luna", text)
        self.assertIn("does not carry to a later task", text)
        self.assertIn("a provisional configuration requires a fresh invocation after the task is resolved", text)
        self.assertIn('display_name: "Sol-Luna Orchestration"', metadata)
        self.assertIn("default_prompt: \"Use $sol-luna-orchestration", metadata)
        self.assertIn("Luna/xhigh subagents by default", metadata)
        self.assertIn("conditional reusable Sol/high review", metadata)
        self.assertIn("ordinary Luna task/thread only when I request one", metadata)
        self.assertIn("policy:\n  allow_implicit_invocation: false\n", metadata)
        self.assertNotIn("allow_implicit_invocation: true", metadata)

    def test_sol_luna_defaults_to_subagents_and_preserves_operator_requested_threads(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for phrase in (
            "Sol remains planner, decision-maker, coordinator, integrator, reviewer, and acceptance authority",
            "Use native Luna subagents by default",
            "only when the operator explicitly asks for a task or thread instead of a subagent",
            "never switch routes silently",
            "Do not change that session's model or reasoning effort",
            "stop and ask the operator to continue from a Sol session or abandon this lens",
            "Use several Luna workers only when every additional worker has a coherent, non-overlapping ownership lane",
            "any writer must have distinct durable write ownership",
            "a sequential dependency chain over one ownership lane stays with one reused worker",
            "workstream map",
            "Launch only the dependency-free frontier concurrently",
            "stay within the running product's concurrency limit",
            "Keep lanes deferred by dependencies or the concurrency limit in the map",
            "dispatch them as prerequisites complete and slots free",
            "Restate the compact current map",
            "this visible state is the recovery point across compaction, not a side-channel file or ledger",
            "Parallel workers share one checkout",
            "Sol schedules one owner for Git state, generated artifacts, build outputs, test databases, ports, formatters, code generation, and other shared mutable state",
            "defers contending steps out of the concurrent frontier",
            "Parallelism does not authorize a Git worktree",
            "each worker verifies only its owned surface",
            "the designated state owner may execute serialized shared-state commands and return their outputs",
            "Sol inspects the integrated full diff, adjudicates all verification evidence, and owns the integration gate",
            "If no compatible worker exists, create a Luna subagent using the model identifier exposed by the running product",
            "currently `gpt-5.6-luna`",
            "Use xhigh effort for Luna subagents",
            "Do not lower or raise Luna effort based on task size, scouting, ambiguity, or cost",
            "use another value only when the operator explicitly requests it",
            "Before each assignment dispatch, reused or new, state the worker identity, reuse status, route, and Luna model and effort in force",
            "improve the contract and context rather than silently changing effort",
            "State the model and effort the running product actually applies",
            "cannot set or confirm the setting in force",
            "stop, and ask the operator before dispatch",
            "Do not fork the parent Sol conversation into a new Luna worker by default",
            "Use the native no-parent-history launch option",
            "confirm that the launched worker inherited no parent turns",
            "Compact Luna Worker Contract plus durable references as the context boundary",
            "If the product cannot set or confirm no-parent-history launch",
            "stop, and ask the operator before dispatch; never degrade silently to inherited history",
            "Fork only the smallest bounded slice of recent parent turns",
            "a load-bearing fact cannot be located in a durable source or summarized without material loss",
            "before dispatch, state that fact, why a summary is unsafe, and the exact bounded history being inherited",
            "Never fork the full parent conversation",
            "Forked history is context, not authority",
            "Every Luna worker remains a leaf",
            "never spawns agents; Sol owns all worker creation and aggregation",
            "Keep the driver's task open after dispatch",
            "Do not claim completion or send repeated no-op updates",
            "Sol mediates every worker-to-worker dependency",
            "only after the upstream worker's assignment is classified complete and Sol validates the final handoff",
            "provisional or mid-run handoffs never satisfy a dependency",
            "Sol records the upstream disposition and dispatches the validated handoff",
            "halt dispatch of its dependents",
            "send a correction or stop only when the running product supports that capability",
            "let the worker finish, classify its output as invalid for integration, and discard or redo the affected work",
            "Send bounded corrections and compatible successive assignments back to the same Luna worker",
            "Never replace a stalled, failed, or context-heavy worker silently",
            "if Sol's contract was incomplete or wrong but the worker remains a fit, correct the same worker",
            "if the work was misclassified or the required judgment or risk handling no longer fits Luna/xhigh, stop and ask the operator",
            "Do not require a failed retry before proper routing",
            "Classify every launched worker as complete, blocked, partial, or failed",
            "No planned lane, dispatched worker, or required handoff may disappear from aggregation",
            "Luna's report is evidence, not acceptance",
            "Dispatch is not completion",
            "Operator-Requested Thread Route",
            "originating Sol session ID",
            "operator requested an ordinary Luna task/thread",
            "Use the Luna model identifier exposed by the running product",
            "at xhigh unless the operator explicitly requests another value",
            "Apply Decompose And Route 1–3 to this route as well",
            "one concise launch response line for each Luna task/thread actually launched",
            "Dispatch a dependent lane only when its upstream assignment is classified complete in the originating Sol session",
            "including the exact originating Sol ID as its return route",
            "do not create a checkpoint solely for this lens",
            "Do not wait, poll, or emit no-op progress messages",
            "operator asks for status or resumes after an expected report did not arrive",
            "never duplicate delivery or launch a replacement silently",
            "Never upgrade Luna work to Sol automatically",
            "report the exact missing capability",
            "Do not silently substitute a subagent for an operator-requested task/thread",
            "substitute a task/thread for the default subagent route",
        ):
            self.assertIn(phrase, text)
        for forbidden in ("spawn_agent", "codex-reply", "thread/start", "turn/start"):
            self.assertNotIn(forbidden, text)

    def test_sol_luna_defines_task_granularity_without_using_it_as_worker_lifecycle(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for phrase in (
            "## Terms",
            "**Task:** the general unit of work currently owned by the driver",
            "**Sol session:** the current Codex task/thread running Sol",
            "**Worker:** a Luna subagent, or the ordinary Luna task/thread on the operator-requested route",
            "**Reviewer:** the independent Sol subagent lane defined below",
            "**Workstream:** a coherent ownership lane within a task",
            "**Assignment:** one bounded contract sent to a worker",
            "**Recycle:** stop reusing a worker or reviewer and create a fresh one",
            "Task, workstream, assignment, and review boundaries are not recycle triggers by themselves",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("Harness", text)

    def test_luna_worker_contract_is_complete(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for field in (
            "**Objective:**",
            "**Durable references:**",
            "**Scope and ownership:**",
            "**Interfaces:**",
            "**Authority:**",
            "**Context and continuity:**",
            "**Dependencies and handoffs, when applicable:**",
            "**Success criteria:**",
            "**Verification:**",
            "**Reviewed behavior-spine proof, only when the driver says it applies:**",
            "**Stop/ask gates:**",
            "**Return route:**",
            "**Return format:**",
        ):
            self.assertIn(field, text)
        for item in (
            "status (`complete`, `blocked`, `partial`, or `failed`)",
            "dependency handoffs",
            "material judgment calls or `none`",
            "the worker's continuity state (`resumable`, `ended`, or `unable to continue`) as evidence for Sol",
            "Sol alone decides whether to reuse or recycle",
            "load-bearing observations that support or weaken acceptance",
            "limitations (including uninspected items and reasons)",
            "divergence from the expected evidence set",
        ):
            self.assertIn(item, text)
        self.assertIn("Report using the return format above; keep any decision-bearing inspection summary concise", text)
        self.assertIn("expected decision-bearing evidence", text)
        self.assertIn("plausible wrong implementations the tests must distinguish", text)
        self.assertIn("ambiguous or conflicting evidence, dependency failure, or other material ambiguity", text)
        self.assertIn("point to files instead of pasting their contents", text)
        self.assertIn("Do not include builder reasoning", text)
        self.assertIn("the parent Sol session for a subagent, or the exact originating Sol session ID", text)
        self.assertIn("delegation permission is always none because every Luna worker remains a leaf", text)
        self.assertIn("the worker remains a leaf", text)
        self.assertIn("Make the applicable Luna Worker Rules part of the contract", text)
        self.assertIn("point to this skill and section when the worker can read it", text)
        self.assertIn("Include conditional fields only when they apply", text)

    def test_sol_luna_reuses_workers_and_recycles_only_on_concrete_triggers(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for phrase in (
            "## Worker Continuity And Recycling",
            "Drive worker lifetime by affinity and context health, not task granularity",
            "Reuse is the default for sequential bounded assignments",
            "A fresh invocation for a later task may reuse such a worker in the same Sol session",
            "invocation does not carry across tasks, but worker identity may",
            "Compaction is expected and is not by itself a reason to recycle",
            "assignment-reset contract",
            "complete Compact Luna Worker Contract with an assignment-reset overlay",
            "Restate every applicable contract field for the new assignment, including interfaces, success criteria, and return format",
            "Old scope, permissions, decisions, and completion claims do not carry forward unless restated",
            "surface any stale or conflicting inherited assumption before acting",
            "A bounded correction within the current assignment needs only the changed constraint, not a full reset",
            "one owner per workstream, not disposable workers per operation",
            "repository, checkout, trust boundary, authority, or permission envelope materially changes",
            "its model or effort conflicts with the Luna setting in force for this lens",
            "continues to act on a superseded contract after a reset restated the current one",
            "decision-critical constraint lost during compaction cannot be restored reliably through a reset",
            "repeats an acceptance-critical miss, stale assumption, or over-engineered direction after correction",
            "Do not create or recycle a worker merely because a task, workstream, or assignment boundary was crossed",
            "or on a fixed count, token budget, or elapsed-time schedule",
            "Small adjacent assignments should not create disposable workers",
            "a large ongoing workstream does not protect an unhealthy or incompatible worker from recycling",
            "Needing an additional independent owner adds a worker; it does not recycle a healthy compatible owner",
            "report the lost continuity and prior disposition before creating a fresh worker",
            "Do not duplicate a handoff or replace a worker merely because delivery is delayed",
            "For independent acceptance review, keep the implementation worker available for fixes and use the Sol reviewer lane below",
            "Keep implementation and review identities separate",
            "use the persistent Sol reviewer lane below",
            "Continuity is a context optimization, not authority or acceptance",
            "Reuse the same Luna task/thread for compatible successive assignments",
            "requests the ordinary task/thread route again",
        ):
            self.assertIn(phrase, text)

    def test_sol_luna_reuses_independent_sol_review_only_when_acceptance_changing(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for phrase in (
            "## Conditional Independent Sol Review",
            "The primary Sol's narrow independent gate is always required",
            "An explicit operator or governing-driver request always requires the independent Sol reviewer",
            "independent judgment plausibly acceptance-changing",
            "cross-worker handoff or contended shared mutable state beyond the common checkout",
            "conflicting or materially incomplete evidence",
            "substantial primary-Sol judgment that creates anchoring risk",
            "For these risk-triggered reviews only, skip the reviewer for a routine, reversible, bounded change",
            "Reuse one compatible, idle Sol reviewer",
            "If none exists, create it as a Sol subagent lane with fresh context and no inherited parent Sol conversation or implementation conversation using the Sol model identifier exposed by the running product",
            "Apply the no-parent-history launch and confirmation rule from Decompose And Route 6 with no bounded-history exception for a new reviewer",
            "ordinary Luna task/thread route does not change the reviewer route",
            "currently `gpt-5.6-sol`",
            "at high effort",
            "Before each review dispatch, state whether the reviewer is reused or new",
            "Dispatch no review packet until implementation is integrated, the checkout is quiescent",
            "Keep the checkout quiescent for the entire review",
            "any primary-Sol or worker mutation during that window invalidates the review",
            "Send a review packet",
            "evidence locations and permitted non-mutating inspection commands",
            "explicit read-only, no-mutation, no-delegation instructions that keep the reviewer a leaf",
            "State-writing test, build, or generation commands must be completed by Sol before dispatch",
            "run in isolated scratch state outside the reviewed checkout",
            "prior review ID, disposition (`ship`, `fix-first`, `rethink`, `blocked`, `failed`, or `voided`), and reviewed state",
            "Explicitly invalidate any prior verdict",
            "carry forward only confirmed project invariants and still-relevant findings",
            "exact accumulated change set or revisions",
            "Separate raw evidence from any primary-Sol interpretation",
            "complete current diff before reading that interpretation",
            "not only changed fixes, summaries, or worker reports",
            "require `ship`, `fix-first`, or `rethink`",
            "require `blocked` with the reason, missing inputs, and current review state",
            "`blocked` is not a verdict",
            "`Failed` means the review dispatch terminated without a verdict or `blocked` report",
            "re-dispatch to the same compatible reviewer when reachable or recycle an unreachable reviewer",
            "Treat read-only isolation as enforced only when the running product reports it",
            "capture exact before/after state",
            "Non-mutating inspection is allowed",
            "reviewer changes to the reviewed checkout or other durable state void the review result",
            "if the mutation cannot be fully reverted, stop and escalate to the operator",
            "Re-establish and reverify the integrated diff baseline before any new review packet or acceptance",
            "A voided review is not a finding against the implementation",
            "Classify every review dispatch as verdict delivered, blocked, failed, or voided",
            "withhold acceptance until Sol resolves the disposition and receives a valid verdict or the operator explicitly waives the review",
            "a failed dispatch must be re-dispatched or explicitly waived",
            "The reviewer's verdict is evidence, not acceptance",
            "Any changed implementation state invalidates the prior verdict, but not the reviewer identity",
            "persistent independent lane, not a disposable worker",
            "After each review dispatch or classification change, restate the reviewer identity, reuse status, last review ID, last disposition, and reviewed state in the visible Sol session state",
            "this is the recovery point across compaction and the source for the next review-reset packet",
            "Reuse the reviewer across fixes and later tasks",
            "never assign concurrent reviews",
            "Compaction, task boundaries, elapsed time, prior `fix-first`, and prior `ship` verdicts are not recycle triggers",
            "it mutates state or assumes implementation ownership",
            "a review reset cannot correct stale or anchored conclusions",
            "operator requests a fresh reviewer or genuinely independent second opinion",
            "One healthy reviewer may persist for the lifetime of the compatible Sol session",
        ):
            self.assertIn(phrase, text)
        review_section = text.split("## Conditional Independent Sol Review\n", 1)[1].split("## Operator-Requested Thread Route", 1)[0]
        self.assertIn("Use another value or reviewer route only when the operator explicitly requests it", review_section)

    def test_sol_luna_assigns_deep_verification_to_luna_and_narrow_gate_to_sol(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        for phrase in (
            "Luna owns one coherent bounded workstream and its implementation-depth verification",
            "recover authoritative contracts",
            "inspect the full final diff within its ownership and the decision-bearing evidence",
            "Inspect the entire final diff for owned paths and the decision-bearing artifacts",
            "report foreign changes to Sol instead of treating them as part of the worker's verification",
            "Sol owns the integrated full-diff and whole-suite gate",
            "Cover each non-interchangeable decision-bearing artifact in the first pass",
            "Do not treat a producer's success signal, metadata, or contract checks as inspection of the decision-bearing artifact",
            "test plausible wrong implementations",
            "trace failure and recovery paths",
            "Sol performs a narrow independent gate",
            "Send no routine progress or acknowledgement messages",
            "without redoing Luna's implementation work",
            "carry a reusable lesson into later Luna worker contracts",
            "propose a durable update to this skill or the governing project checklist",
            "Do not silently modify durable assets without authority",
            "implementation-derived oracle",
            "semantics-preserving implementation refactor remains green",
            "plausible production defect turns the spine red",
            "detector ledger",
            "isolated scratch state",
            "Do not infer oracle independence from a green suite",
        ):
            self.assertIn(phrase, text)
        for heading in ("## Operating Model\n", "## Decompose And Route\n", "## Worker Lifecycle\n", "## Operator-Requested Thread Route\n", "## Sol Token-Efficiency Rules\n"):
            self.assertIn(heading, text)
        operating_model = text.split("## Operating Model\n", 1)[1].split("## Decompose And Route", 1)[0]
        sol_rules = text.split("## Sol Token-Efficiency Rules\n", 1)[1].split("## Operator-Requested Thread Launch Response", 1)[0]
        self.assertIn("decision-critical subset", operating_model)
        self.assertIn("evidence whose observation could change acceptance", operating_model)
        self.assertIn("directly at proportionate depth", operating_model)
        self.assertIn("expand only for conflicts, unexplained gaps, or acceptance-critical uncertainty", operating_model)
        self.assertIn("Dispatch is not completion on either route", operating_model)
        self.assertIn("apply the decision-critical gate defined in the Operating Model at proportionate depth", sol_rules)
        self.assertIn("expanding only for conflicts, unexplained gaps, or acceptance-critical uncertainty", sol_rules)

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
