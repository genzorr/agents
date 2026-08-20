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

    def test_orchestration_family_is_canonical_explicit_and_codex_only(self) -> None:
        catalog = json.loads(self.read("catalog.json"))
        entries = {item["id"]: item for item in catalog["skills"]}
        expected = {
            "orchestrate-feature": ("codex/skills/orchestrate-feature", "skills/orchestrate-feature", "role:helper"),
            "orchestrate-workers": ("codex/skills/orchestrate-workers", "skills/orchestrate-workers", "role:lens"),
            "sol-luna-orchestration": ("codex/skills/sol-luna-orchestration", "skills/sol-luna-orchestration", "role:lens"),
        }
        self.assertNotIn("orchestrate-sol-feature", entries)
        self.assertFalse((REPO_ROOT / "codex/skills/orchestrate-sol-feature").exists())
        for skill_id, (source, target, role) in expected.items():
            entry = entries[skill_id]
            self.assertEqual(entry["platforms"], ["codex"])
            self.assertEqual(entry["source"], {"codex": source})
            self.assertEqual(entry["install_target"], {"codex": target})
            self.assertEqual(entry["tags"], [role, "domain:orchestration"])
            self.assertFalse((REPO_ROOT / f"claude/skills/{skill_id}").exists())
            self.assertIn("allow_implicit_invocation: false", self.read(f"{source}/agents/openai.yaml"))

    def test_orchestrate_feature_metadata_and_role_defaults_are_truthful(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        metadata = self.read("codex/skills/orchestrate-feature/agents/openai.yaml")
        frontmatter = text.split("---\n", 2)[1]
        profiles = text.split("## Resolve Role Profiles\n", 1)[1].split("## Select New Or Reused Ownership", 1)[0]
        for anchor in (
            "Use only after the operator explicitly invokes orchestrate-feature",
            "Defaults are Sol/high owner, Sol/medium workers, and Sol/high reviewer",
            "never mutates the current orchestrator",
        ):
            self.assertIn(anchor, frontmatter)
        for anchor in (
            "Feature owner | `gpt-5.6-sol` / `high`",
            "Implementation worker | Native `gpt-5.6-sol` / `medium`",
            "Independent reviewer | Native `gpt-5.6-sol` / `high`",
            "an owner override changes only owner creation",
            "a worker override changes only the inner worker profile",
            "a reviewer override changes only the independent reviewer profile",
            "inherits its own role's default, never another role's override",
            "Do not cascade",
            "Stop when a selected value cannot be set or validated; never substitute",
            "profile provenance, not independent post-creation readback",
        ):
            self.assertIn(anchor, profiles)
        self.assertIn('display_name: "Orchestrate Feature"', metadata)
        self.assertIn('short_description: "Dispatch profiled feature owners and workers"', metadata)

    def test_orchestrate_feature_preserves_immutable_orchestrator_and_authority(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        readiness = text.split("## Activate And Resolve Readiness\n", 1)[1].split("## Resolve Role Profiles", 1)[0]
        contract = text.split("## Feature Owner Launch Contract\n", 1)[1].split("## Constrain Inner Delegation", 1)[0]
        for anchor in (
            "Preserve the current model and effort",
            "operator-specified orchestrator profile only as a precondition",
            "mismatch stops",
            "rather than becoming a mutation request or guess",
            "Require callback, practical bounded active waiting, another product-validated mechanism/target, or explicitly accepted manual supervision",
        ):
            self.assertIn(anchor, readiness)
        for field in (
            "**Objective and durable references:**",
            "**Decisions, assumptions, unknowns, and non-goals:**",
            "**Project and starting state:**",
            "**Scope and shared state:**",
            "**Authority:**",
            "**Driver and lens:**",
            "**Resolved role map and inner route:**",
            "**Success, artifacts, verification, and evidence:**",
            "**Stop/ask and reporting gates:**",
            "**Notification and return contract:**",
            "**Final handoff:**",
        ):
            self.assertIn(field, contract)
        for anchor in (
            "never broaden worktree, Git, live-install, or external-write authority",
            "native leaf workers only",
            "forbid the optional ordinary implementation-task route",
            "owns integration, primary review, and feature acceptance",
            "cannot delegate authority or create an ordinary task",
        ):
            self.assertIn(anchor, contract)
        self.assertIn("must not spawn or duplicate the feature owner's implementation workers or reviewer directly", text)
        self.assertIn("All feature-lane child dispatch, correction, reuse, and aggregation stays with the feature owner", text)
        self.assertIn("both requested for the same unresolved feature", readiness)
        self.assertIn("stop and ask the operator to choose one owner topology", readiness)

    def test_orchestrate_feature_preserves_fresh_context_writer_and_profile_safe_reuse(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        reuse = text.split("## Select New Or Reused Ownership\n", 1)[1].split("## Launch A New Feature Owner", 1)[0]
        launch = text.split("## Launch A New Feature Owner\n", 1)[1].split("## Feature Owner Launch Contract", 1)[0]
        delegation = text.split("## Constrain Inner Delegation\n", 1)[1].split("## Supervise And Complete", 1)[0]
        for anchor in (
            "one active durable writer per checkout",
            "Concurrent writers require disjoint paths and one named owner for Git state",
            "owner model/effort",
            "A different owner profile requires a new task",
            "revalidate the complete role map and delivery contract",
            "Old origin identity, callback action, wait cursor, event set, or profiles never carry implicitly",
            "Never replace a running, stalled, failed, or blocked identity silently",
            "exact known idle feature identity",
            "Never send a reset or concurrent assignment to a running owner",
            "Send an idle compatible owner a reset",
        ):
            self.assertIn(anchor, reuse)
        for anchor in (
            "native `create_thread` with fresh context",
            "never a native subagent spawn or `fork_thread`",
            "never inherit or paste parent history",
            "Conversation history is context, not authority",
            "request validation from readback",
            "`launched, awaiting handoff`",
        ):
            self.assertIn(anchor, launch)
        for anchor in (
            "then the native default when no stricter rule exists",
            "governs an additional worktree created after launch",
            "not a task environment already assigned under this compliant outer policy",
        ):
            self.assertIn(anchor, launch)
        for anchor in (
            "no parent turns by default",
            "inherited-turn fork is exceptional",
            "one named load-bearing fact with no durable source",
            "fact, reason, and exact slice",
            "Independent reviewers receive fresh context with no exception",
            "Full parent-history inheritance is prohibited",
            "Keep every worker and reviewer a leaf",
        ):
            self.assertIn(anchor, delegation)

    def test_orchestrate_feature_preserves_route_scoped_sparse_delivery(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        launch = text.split("## Launch A New Feature Owner\n", 1)[1].split("## Feature Owner Launch Contract", 1)[0]
        contract = text.split("## Feature Owner Launch Contract\n", 1)[1].split("## Constrain Inner Delegation", 1)[0]
        supervision = text.split("## Supervise And Complete\n", 1)[1]
        self.assertIn("Resolve callback identity/action only under callback", launch)
        for anchor in (
            "Under callback include exact originating `threadId`/`hostId` when required plus native `send_message_to_thread`",
            "Under active waiting use native attention for gates/blockers and terminal result",
            "A replacement names its validated mechanism/target",
            "Manual supervision remains unobserved until later inspection",
        ):
            self.assertIn(anchor, contract)
        for anchor in (
            "**Callback, default:**",
            "Accepted terminal send establishes delivery",
            "**Practical bounded active waiting:**",
            "Observation establishes delivery; timeout does not",
            "**Product-validated replacement:**",
            "same actionable-blocker, required-gate, and terminal floor",
            "**Explicit manual supervision:**",
            "delivery remains unobserved until inspection",
            "Routine progress, recoverable friction, unchanged status, and repeated messages are not events",
            "never a watcher/subscription",
            "Do not poll repeatedly",
            "cannot remove blocker/terminal delivery",
        ):
            self.assertIn(anchor, supervision)
        callback_lines = [line for line in text.splitlines() if "send_message_to_thread" in line]
        self.assertTrue(callback_lines)
        self.assertTrue(all("callback" in line.lower() for line in callback_lines))

    def test_orchestrate_workers_is_generic_explicit_and_profiled(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        metadata = self.read("codex/skills/orchestrate-workers/agents/openai.yaml")
        frontmatter = text.split("---\n", 2)[1]
        profiles = text.split("## Terms And Profiles\n", 1)[1].split("## Operating Model", 1)[0]
        for anchor in (
            "Use only after explicit invocation of orchestrate-workers",
            "operator-authorized feature launch",
            "explicit sol-luna-orchestration preset",
            "without changing the coordinator profile or lifecycle driver",
        ):
            self.assertIn(anchor, frontmatter)
        for anchor in (
            "Coordinator:",
            "any product-exposed profile",
            "Implementation worker | Native subagent | `gpt-5.6-sol` | `medium`",
            "Independent reviewer | Native subagent | `gpt-5.6-sol` | `high`",
            "one override never changes the coordinator or another role",
            "Stop if an exact selected route/model/effort/context control cannot be set or validated",
        ):
            self.assertIn(anchor, profiles)
        for anchor in (
            "worker/reviewer profile only on explicit operator instruction, an operator-authorized launch contract, or the explicit `sol-luna-orchestration` preset",
            "ordinary implementation-task route always requires a separate explicit operator request",
            "neither a launch contract nor the preset authorizes that route by itself",
        ):
            self.assertIn(anchor, profiles)
        self.assertNotIn("Require the current coordinator to run Sol", text)
        self.assertIn('display_name: "Orchestrate Workers"', metadata)

    def test_orchestrate_workers_owns_generic_lifecycle_and_evidence(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        for heading in (
            "## Decompose And Route",
            "## Dispatch Preamble",
            "## Worker Lifecycle And Continuity",
            "## Compact Worker Contract",
            "## Worker Rules",
            "## Escalated Independent Review",
            "## Operator-Requested Ordinary Implementation Route",
        ):
            self.assertIn(heading, text)
        for anchor in (
            "Parallelism never authorizes a worktree",
            "Launch new workers with no parent turns by default",
            "inherited-turn fork as exceptional",
            "Keep every worker and reviewer a leaf",
            "root work it substitutes for",
            "non-duplicative",
            "Classify every worker",
            "assignment-reset overlay",
            "Profile change is incompatibility",
            "Keep implementation and reviewer identities separate",
            "decision-bearing artifact",
            "plausible wrong implementations",
            "implementation-derived oracles",
            "failure/recovery paths",
            "reports are evidence, not acceptance",
        ):
            self.assertIn(anchor, text)

    def test_orchestrate_workers_preserves_nonduplicative_dispatch_trace(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        preamble = text.split("## Dispatch Preamble\n", 1)[1].split("## Worker Lifecycle And Continuity", 1)[0]
        for anchor in (
            "Before every dispatch, state lane",
            "root work it substitutes for",
            "unique output",
            "downstream decision affected",
            "why the lane is non-duplicative",
            "three-part escalation rationale",
        ):
            self.assertIn(anchor, preamble)

    def test_orchestrate_workers_preserves_complete_handoffs_and_recovery(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        contract = text.split("## Compact Worker Contract\n", 1)[1].split("## Worker Rules", 1)[0]
        for field in (
            "**Objective and durable references:**",
            "**Scope and interfaces:**",
            "**Authority:**",
            "**Context and continuity:**",
            "**Dependencies and handoffs:**",
            "**Success and verification:**",
            "**Stop/ask gates:**",
            "**Return route:**",
            "**Return format:**",
        ):
            self.assertIn(field, contract)
        return_route = next(line for line in contract.splitlines() if line.startswith("- **Return route:**"))
        for anchor in (
            "exact originating coordinator `threadId` and `hostId` when required",
            "explicit native `send_message_to_thread` action",
            "accepted blocker/terminal sends establish delivery",
            "rejection or unavailability remains local delivery failure",
        ):
            self.assertIn(anchor, return_route)
        lifecycle = text.split("## Worker Lifecycle And Continuity\n", 1)[1].split("## Compact Worker Contract", 1)[0]
        for anchor in (
            "Route dependencies through the coordinator",
            "Classify every worker",
            "Reuse a compatible idle worker",
            "assignment-reset overlay",
            "Compaction does not justify recycling",
            "Report lost continuity",
            "Keep implementation and reviewer identities separate",
        ):
            self.assertIn(anchor, lifecycle)

    def test_orchestrate_workers_preserves_auditable_verification(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        operating = text.split("## Operating Model\n", 1)[1].split("## Decompose And Route", 1)[0]
        for anchor in (
            "reports are evidence, not acceptance",
            "missing, stale, contradicted, or decision-critical checks",
            "governing contracts",
            "plausible wrong implementations",
            "failure/recovery paths",
        ):
            self.assertIn(anchor, operating)
        worker_rules = text.split("## Worker Rules\n", 1)[1].split("## Escalated Independent Review", 1)[0]
        for anchor in (
            "decision-bearing artifact",
            "not producer signals",
            "consequence tests",
            "implementation-derived oracles",
            "claim success with missing evidence",
        ):
            self.assertIn(anchor, worker_rules)

    def test_orchestrate_workers_preserves_reviewer_escalation_gates(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        review = text.split("## Escalated Independent Review\n", 1)[1].split("## Operator-Requested Ordinary Implementation Route", 1)[0]
        for anchor in (
            "coordinator is the default reviewer",
            "named acceptance-critical target",
            "material expected value",
            "Generic confidence",
            "If any is missing, do not dispatch",
            "Reuse one compatible idle reviewer",
            "Create a fresh reviewer only when escalation is required",
            "The ordinary implementation route never changes reviewer routing",
        ):
            self.assertIn(anchor, review)

    def test_orchestrate_workers_preserves_ordinary_route_delivery(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        route = text.split("## Operator-Requested Ordinary Implementation Route\n", 1)[1].split("## Coordinator Depth Budget", 1)[0]
        for anchor in (
            "separate explicit operator request",
            "exact originating coordinator `threadId` and `hostId` when required",
            "explicit native `send_message_to_thread` action",
            "return the launch response immediately",
            "do not wait or poll",
            "genuine blocker or final handoff",
            "accepted blocker/terminal send establishes delivery",
            "rejection or unavailability remains local delivery failure",
            "fresh lens invocation",
        ):
            self.assertIn(anchor, route)

    def test_orchestrate_feature_bounds_supervision_and_fails_safe(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        readiness = text.split("## Activate And Resolve Readiness\n", 1)[1].split("## Resolve Role Profiles", 1)[0]
        launch = text.split("## Launch A New Feature Owner\n", 1)[1].split("## Feature Owner Launch Contract", 1)[0]
        supervision = text.split("## Supervise And Complete\n", 1)[1]
        for anchor in (
            "callback, practical bounded active waiting, another product-validated mechanism/target, or explicitly accepted manual supervision",
            "unavailable exact route/model/effort/context/delivery capability",
        ):
            self.assertIn(anchor, readiness)
        for anchor in (
            "one bounded `wait_threads` wait/snapshot",
            "latest wait cursor",
            "supports no later-notification claim",
        ):
            self.assertIn(anchor, launch)
        for anchor in (
            "never a watcher/subscription",
            "Do not poll repeatedly",
            "require explicit manual-supervision acceptance",
        ):
            self.assertIn(anchor, supervision)

    def test_orchestrate_feature_reuse_identity_and_reporting_are_truthful(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        reuse = text.split("## Select New Or Reused Ownership\n", 1)[1].split("## Launch A New Feature Owner", 1)[0]
        for anchor in (
            "one active durable writer per checkout",
            "If writer state is unresolved, serialize or ask",
            "exact known idle feature identity",
            "A title or recollection is insufficient",
            "revalidate the complete role map and delivery contract",
            "Never send a reset or concurrent assignment to a running owner",
            "Send an idle compatible owner a reset with prior disposition",
            "Old origin identity, callback action, wait cursor, event set, or profiles never carry implicitly",
            "Never replace a running, stalled, failed, or blocked identity silently",
        ):
            self.assertIn(anchor, reuse)

    def test_orchestrate_feature_preserves_delivery_floor_and_acceptance_boundary(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        supervision = text.split("## Supervise And Complete\n", 1)[1]
        for anchor in (
            "same actionable-blocker, required-gate, and terminal floor",
            "cannot remove blocker/terminal delivery",
            "Do not routinely rerun accepted scope-complete child checks",
            "terminal classification",
        ):
            self.assertIn(anchor, supervision)
        self.assertIn("owns integration, primary review, and feature acceptance", text)

    def test_orchestrate_workers_preserves_independent_review_protocol(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        review = text.split("## Escalated Independent Review\n", 1)[1].split("## Operator-Requested Ordinary Implementation Route", 1)[0]
        for anchor in (
            "named acceptance-critical target",
            "fresh judgment has material expected value",
            "conflicting plausible interpretations",
            "named reliable deterministic oracle",
            "concrete anchoring concern",
            "cross-worker boundary",
            "If any is missing, do not dispatch",
            "Create a fresh reviewer only when escalation is required",
            "fresh context with no history exception",
            "Independence comes from separate identity",
            "references/independent-reviewer-protocol.md",
        ):
            self.assertIn(anchor, review)
        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        for anchor in (
            "checkout is quiescent",
            "read-only, no-mutation, no-delegation",
            "ship",
            "fix-first",
            "rethink",
            "blocked",
            "failed",
            "voided",
            "coordinator remains acceptance authority",
            "exact reviewer profile",
        ):
            self.assertIn(anchor, protocol)
        self.assertIn("isolated scratch state outside the reviewed checkout", protocol)
        self.assertFalse((REPO_ROOT / "codex/skills/sol-luna-orchestration/references/sol-reviewer-protocol.md").exists())

    def test_sol_luna_is_a_thin_explicit_compatibility_preset(self) -> None:
        text = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        metadata = self.read("codex/skills/sol-luna-orchestration/agents/openai.yaml")
        for anchor in (
            "Composition role: explicit preset lens",
            "Require the current coordinator to run Sol",
            "never change it",
            "Invoke `orchestrate-workers` explicitly",
            "Native Luna subagent | `gpt-5.6-luna` | `xhigh`",
            "Native Sol subagent | `gpt-5.6-sol` | `high`",
            "Luna/xhigh remains the direct-invocation implementation default",
            "only when the operator separately requests it",
            "apply that lens's exact callback identity, action, acceptance, and delivery-failure contract",
            "return the launch response immediately",
            "do not wait or poll",
            "Launched Luna task/thread <thread-id>",
            "no second copy of that protocol",
        ):
            self.assertIn(anchor, text)
        for forbidden in ("## Compact Worker Contract", "## Worker Rules", "## Escalated Independent Review", "## Worker Lifecycle And Continuity"):
            self.assertNotIn(forbidden, text)
        self.assertIn('display_name: "Sol-Luna Orchestration"', metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_orchestration_family_uses_progressive_disclosure_without_protocol_duplication(self) -> None:
        outer = self.read("codex/skills/orchestrate-feature/SKILL.md")
        generic = self.read("codex/skills/orchestrate-workers/SKILL.md")
        preset = self.read("codex/skills/sol-luna-orchestration/SKILL.md")
        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        self.assertLess(len(outer.split()), 2150)
        self.assertLess(len(generic.split()), 2100)
        self.assertLess(len(preset.split()), 575)
        self.assertLess(len(protocol.split()), 625)
        for text in (outer, preset):
            self.assertNotIn("## Compact Worker Contract", text)
            self.assertNotIn("## Worker Rules", text)
            for generic_protocol_phrase in (
                "provisional results satisfy no dependency",
                "Inspect artifacts, not producer signals",
                "three-part escalation rationale",
                "Do not recycle for granularity, assignment count",
            ):
                self.assertNotIn(generic_protocol_phrase, text)
        for generic_protocol_phrase in (
            "provisional results satisfy no dependency",
            "Inspect artifacts, not producer signals",
            "three-part escalation rationale",
            "Do not recycle for granularity, assignment count",
        ):
            self.assertIn(generic_protocol_phrase, generic)
        for forbidden in ("spawn_agent", "codex-reply", "thread/start", "turn/start", "claude-headless"):
            self.assertNotIn(forbidden, outer + generic + preset)

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
