"""Static contracts for goal quality, Sol–Luna orchestration, and research sufficiency."""

import json
import re
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
        }
        self.assertNotIn("orchestrate-sol-feature", entries)
        self.assertFalse((REPO_ROOT / "codex/skills/orchestrate-sol-feature").exists())
        self.assertNotIn("sol-luna-orchestration", entries)
        self.assertFalse((REPO_ROOT / "codex/skills/sol-luna-orchestration").exists())
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
            "Use only after the operator invokes orchestrate-feature",
            "Defaults are Sol/medium owner, Luna/xhigh workers, feature-owner self-review",
            "requested reviewer Sol/high",
            "never mutates the orchestrator",
        ):
            self.assertIn(anchor, frontmatter)
        for anchor in (
            "Feature owner | `gpt-5.6-sol` / `medium`",
            "Implementation worker | Native `gpt-5.6-luna` / `xhigh`",
            "Independent reviewer | Disabled; when explicitly requested, native `gpt-5.6-sol` / `high`",
            "owner and worker overrides change only their profiles",
            "reviewer profile wording in an explicitly operator-authorized activation source activates review and changes only that profile",
            "only the current operator invocation or an authoritative operator decision explicitly scoped to this resolved feature can activate it",
            "standing or global reviewer preferences never activate review",
            "inherits its enabled role's default, never another override",
            "Never infer reviewer activation",
            "driver requirement without operator authorization stops",
            "Do not cascade",
            "never substitute or validate reviewer controls while disabled",
            "profile provenance, not independent readback",
        ):
            self.assertIn(anchor, profiles)
        self.assertIn('display_name: "Orchestrate Feature"', metadata)
        self.assertIn('short_description: "Launch feature owners with opt-in review"', metadata)

    def test_orchestration_resolves_named_workstream_profiles_per_field(self) -> None:
        feature = self.read("codex/skills/orchestrate-feature/SKILL.md")
        workers = self.read("codex/skills/orchestrate-workers/SKILL.md")
        prd = self.read("docs/orchestrate-feature-prd.md")
        feature_profiles = feature.split("## Resolve Role Profiles\n", 1)[1].split("## Select New Or Reused Ownership", 1)[0]
        worker_profiles = workers.split("## Terms And Profiles\n", 1)[1].split("## Operating Model", 1)[0]
        for text, terms in (
            (feature_profiles, ("role defaults", "general worker override", "named workstream")),
            (worker_profiles, ("role default", "general worker override", "named-workstream override")),
        ):
            positions = [text.index(term) for term in terms]
            self.assertEqual(positions, sorted(positions))
            self.assertNotIn("named-workstream override, then an explicit general worker override", text)
        self.assertIn("labels are routing inputs rather than a required decomposition", feature_profiles)
        self.assertIn("Labels alone never require decomposition or dispatch", worker_profiles)
        self.assertIn("never changes the coordinator, another workstream, or any other role", worker_profiles)
        self.assertIn("main workstream: Sol/medium; additional workstreams: Luna/xhigh", prd)
        self.assertIn("Require an Astra/medium reviewer", prd)

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
            "**Resolved role map, reviewer request, and inner route:**",
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
            "reviewer activation recorded as `disabled` or `operator-requested`",
            "exact operator-request provenance, acceptance target",
            "owns integration, default self-review, and feature acceptance",
            "cannot delegate authority or create an ordinary task",
        ):
            self.assertIn(anchor, contract)
        self.assertIn("must not spawn or duplicate the feature owner's implementation workers or reviewer directly", text)
        self.assertIn("All feature-lane child dispatch, correction, reuse, and aggregation stays with the feature owner", text)
        self.assertIn("both requested for the same unresolved feature", readiness)
        self.assertIn("stop and ask the operator to choose one owner topology", readiness)

    def test_orchestrate_feature_binds_owner_depth_budget_and_boundaries(self) -> None:
        text = self.read("codex/skills/orchestrate-feature/SKILL.md")
        contract = text.split("## Feature Owner Launch Contract\n", 1)[1].split("## Constrain Inner Delegation", 1)[0]
        delegation = text.split("## Constrain Inner Delegation\n", 1)[1].split("## Supervise And Complete", 1)[0]
        for anchor in (
            "cannot delegate authority or create an ordinary task",
            "delegate coherent execution-depth work—broad investigation, implementation, implementation-depth diagnostics, builds, focused tests, and owned-diff inspection—to configurable native workers when a safe delegation boundary exists",
            "Workers may perform substantial implementation, build, test, diagnostic, and inspection work; they are not limited to code-writing.",
            "It retains architecture/risk decisions, assignment contracts, feature-lane Git/shared-state writer assignment",
            "synthesis and integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo",
            "reporting; external-landing authority stays exactly as granted",
            "It names exactly one writer—owner or worker—per shared mutable resource within granted authority",
            "it serializes all others, including itself, and evaluates evidence",
            "It records substantial direct work and its no-boundary reason in its in-task plan or worker-dispatch context",
            "existing final handoff `decisions/divergence`",
            "it creates no new file, ledger, side channel, or notification event",
            "It may perform trivial glue, narrow corrections, decision-critical inspection, or work without a coherent delegation boundary.",
        ):
            self.assertIn(anchor, contract)
        for anchor in (
            "Owner must primarily orchestrate through synthesis, integration, integrated-diff inspection, evidence judgment, and retain-or-redo/acceptance.",
            "It cannot create another feature task, use the ordinary task route, delegate authority, or treat profile names as proof; it must delegate execution-depth work at safe boundaries.",
            "Sequential compatible-worker assignments remain valid; parallel workers require non-overlapping lanes.",
        ):
            self.assertIn(anchor, delegation)

    def test_orchestrate_feature_docs_bind_delegation_contract_in_named_sections(self) -> None:
        prd = self.read("docs/orchestrate-feature-prd.md")
        goals = prd.split("## Goals\n", 1)[1].split("## Non-Goals", 1)[0]
        owner = prd.split("### Feature owner\n", 1)[1].split("### Implementation workers", 1)[0]
        workers = prd.split("### Implementation workers\n", 1)[1].split("### Independent reviewer", 1)[0]
        for anchor in (
            "primarily an active orchestrator",
            "exactly one named writer at a time",
        ):
            self.assertIn(anchor, goals)
        for anchor in (
            "delegate coherent execution-depth work whenever a safe delegation boundary exists",
            "no-boundary reason",
        ):
            self.assertIn(anchor, owner)
        self.assertIn(
            "may perform substantial implementation, build, test, diagnostic, and inspection work",
            workers,
        )
        self.assertIn("cannot delegate, and return only blockers", workers)
        self.assertNotIn("cannot delegate authority", workers)

        spec = self.read("docs/orchestrate-feature-spec.md")
        authority = spec.split("## Authority And Scope\n", 1)[1].split("## Source Ownership", 1)[0]
        contract = spec.split("## Feature Owner Launch Contract\n", 1)[1].split("## Feature-Task And Subagent Continuity", 1)[0]
        static = spec.split("## Static And Behavioral Contracts\n", 1)[1].split("## Validation", 1)[0]
        acceptance = spec.split("## Acceptance\n", 1)[1]
        self.assertIn("T-42 owns feature-owner delegation", authority)
        for anchor in (
            "delegate coherent execution-depth work",
            "one writer at a time",
            "no-boundary reason",
        ):
            self.assertIn(anchor, contract)
        for anchor in (
            "worker model/effort remains resolved from the role map",
            "tests do not require a worker count",
        ):
            self.assertIn(anchor, static)
        for anchor in (
            "sequentially on one compatible worker",
            "without creating another feature-owner task",
        ):
            self.assertIn(anchor, acceptance)

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
            "The feature owner alone owns this callback",
            "native children return only to it through native collaboration/results",
            "existing-task messages omit both `model` and `thinking` fields",
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
            "Preserve coordinator profile and driver",
        ):
            self.assertIn(anchor, frontmatter)
        for anchor in (
            "Coordinator:",
            "any product-exposed profile",
            "Implementation worker | When delegated | Native subagent | `gpt-5.6-luna` | `xhigh`",
            "Independent reviewer | Disabled unless explicitly operator-requested | Native subagent | `gpt-5.6-sol` | `high`",
            "one override never changes another role or the coordinator",
            "Reviewer activation and profile are separate",
            "Only an explicit operator request activates review",
            "launch contract must carry the request",
            "do not resolve or validate reviewer controls, identity, or protocol",
            "stop if an exact control cannot be validated",
            "Creation profile:",
            "Existing-task message:",
            "preserves the recipient's settings and omits both `model` and `thinking` fields entirely",
            "including null or presumed-current values",
            "a sender profile belongs in text metadata only when relevant",
        ):
            self.assertIn(anchor, profiles)
        for anchor in (
            "Use another enabled-role profile only on explicit operator instruction",
            "ordinary task route always requires a separate explicit request",
            "the launch contract does not authorize it",
        ):
            self.assertIn(anchor, profiles)
        self.assertNotIn("Require the current coordinator to run Sol", text)
        self.assertIn('display_name: "Orchestrate Workers"', metadata)

    def test_orchestrate_workers_owns_generic_lifecycle_and_evidence(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        for heading in (
            "## Decompose And Route",
            "## Dispatch Readiness",
            "## Worker Lifecycle And Continuity",
            "## Compact Worker Contract",
            "## Worker Rules",
            "## Operator-Requested Independent Review",
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
        preamble = text.split("## Dispatch Readiness\n", 1)[1].split("## Worker Lifecycle And Continuity", 1)[0]
        for anchor in (
            "Before every dispatch, internally resolve and validate the lane",
            "root work it substitutes for",
            "unique output",
            "downstream decision affected",
            "non-duplicative rationale",
            "explicit operator request and exact acceptance target",
            "consequential profile override",
            "inherited-context exception",
            "unresolved or unobservable control",
            "degraded supervision or delivery",
            "changed topology/authority/shared-state ownership or conflict",
        ):
            self.assertIn(anchor, preamble)
        self.assertNotIn("Before every dispatch, state lane", preamble)

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
        self.assertIn("delegation is always none", contract)
        route_lines = [line for line in contract.splitlines() if line.startswith("- **") and "route:**" in line]
        self.assertEqual(len(route_lines), 3)
        native_route = next(line for line in route_lines if line.startswith("- **Native subagent route:**"))
        ordinary_route = next(line for line in route_lines if line.startswith("- **Separately authorized ordinary-task route:**"))
        self.assertIn("**Return route:** include exactly one applicable route below; never copy fields from the other route.", contract)
        for callback_handle in ("threadId", "hostId", "send_message_to_thread"):
            self.assertNotIn(callback_handle, native_route)
        for anchor in (
            "worker or reviewer returns only to its immediate parent through native collaboration/results",
            "only after a separate explicit operator request",
            "Verify the exact recipient and authorized callback purpose",
            "exact originating coordinator `threadId` and `hostId` when required",
            "explicit native `send_message_to_thread` action",
            "Accepted blocker/terminal sends establish delivery",
            "rejection or unavailability remains local delivery failure",
        ):
            self.assertIn(anchor, native_route if anchor.startswith("worker") else ordinary_route)
        self.assertNotIn("sender, recipient, and purpose", ordinary_route)
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

    def test_orchestrate_workers_compacts_final_handoffs_without_losing_decisive_evidence(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        contract = text.split("## Compact Worker Contract\n", 1)[1].split("## Worker Rules", 1)[0]
        for anchor in (
            "status and outcome; changed scope; exact tested repository/artifact state",
            "verification commands and results",
            "material gaps, decisions, or constraints",
            "only when they affect a decision, reuse, integration, or the next action",
            "Reference existing accessible evidence for long output or inventories",
            "Do not create an artifact solely to shorten the message",
            "impose an arbitrary size cap",
            "Preserve a failure with its condition and evidence",
        ):
            self.assertIn(anchor, contract)
        self.assertIn("Before reuse, resend the full contract with an assignment-reset overlay", text)
        self.assertIn("A bounded current-assignment correction needs only changed constraints", text)

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
        worker_rules = text.split("## Worker Rules\n", 1)[1].split("## Operator-Requested Independent Review", 1)[0]
        for anchor in (
            "decision-bearing artifact",
            "not producer signals",
            "consequence tests",
            "implementation-derived oracles",
            "claim success with missing evidence",
        ):
            self.assertIn(anchor, worker_rules)

    def test_orchestrate_workers_requires_operator_requested_review(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        review = text.split("## Operator-Requested Independent Review\n", 1)[1].split("## Operator-Requested Ordinary Implementation Route", 1)[0]
        for anchor in (
            "coordinator reviews and accepts by default",
            "Only an explicit operator request for this task activates a reviewer",
            "No other signal—including task characteristics, evidence gaps, driver preference, or agent judgment—authorizes review",
            "unauthorized driver requirement is a stop-and-ask condition only when the next action requires independent review",
            "Complete already-authorized implementation and verification first",
            "do not claim independent acceptance or waive the driver’s review requirement",
            "Do not resolve or validate reviewer route/model/effort, read the reviewer protocol, or create/reuse a reviewer while disabled",
            "record the operator request and exact acceptance target",
            "Reuse one compatible idle reviewer",
            "Create a fresh reviewer only when operator-requested review is active",
            "ordinary implementation route never changes reviewer activation or routing",
        ):
            self.assertIn(anchor, review)
        for forbidden in (
            "otherwise escalate",
            "fresh judgment has material expected value",
            "conflicting plausible interpretations",
            "concrete anchoring concern",
            "If any is missing, do not dispatch",
        ):
            self.assertNotIn(forbidden, review)

    def test_orchestration_family_rejects_implicit_reviewer_activation_language(self) -> None:
        paths = (
            "codex/skills/orchestrate-feature/SKILL.md",
            "codex/skills/orchestrate-workers/SKILL.md",
        )
        review_target = re.compile(r"\b(review|reviewer|reviewers|independent review)\b")
        allowed_review_fragments = {
            "a driver requirement without operator authorization stops at required review.",
            "An unauthorized driver requirement is a stop-and-ask condition only when the next action requires independent review.",
            "Complete already-authorized implementation and verification first, then leave a concrete review handoff;",
            "do not claim independent acceptance or waive the driver’s review requirement.",
            "description: Dispatch or reuse one profiled feature-owner task from a long-lived project orchestrator, with reusable native workers and an independent reviewer only when explicitly operator-requested.",
            "Defaults are Sol/medium owner, Luna/xhigh workers, feature-owner self-review, and requested reviewer Sol/high.",
            "- **Role map:** immutable current-orchestrator observation plus independently resolved owner and worker profiles, reviewer activation, and the reviewer profile only when operator-requested.",
            "| Independent reviewer | Disabled;",
            "Reviewer activation is operator-only: only the current operator invocation or an authoritative operator decision explicitly scoped to this resolved feature can activate it;",
            "standing or global reviewer preferences never activate review.",
            "reviewer profile wording in an explicitly operator-authorized activation source activates review and changes only that profile.",
            "For owner and enabled reviewer profiles, an omitted field inherits its enabled role's default, never another override;",
            "Never infer reviewer activation;",
            "never substitute or validate reviewer controls while disabled.",
            "- **Resolved role map, reviewer request, and inner route:** complete role map;",
            "reviewer activation recorded as `disabled` or `operator-requested`;",
            "when requested, exact operator-request provenance, acceptance target, and separate reviewer profile/provenance;",
            "State that the owner owns integration, default self-review, and feature acceptance;",
            "may create only native leaf workers and an operator-requested reviewer;",
            "Pass the worker profile and reviewer activation as `disabled` or `operator-requested`;",
            "only when requested, also pass the exact operator-request provenance, acceptance target, and reviewer profile/provenance.",
            "The lens owns decomposition, contracts, context, continuity, evidence, review routing, and acceptance;",
            "The project orchestrator must not spawn or duplicate the feature owner's implementation workers or reviewer directly.",
            "Independent reviewers receive fresh context with no exception.",
            "Keep every worker and reviewer a leaf and keep their identities separate.",
            "- **Creation profile:** model and effort selected while creating a new worker or reviewer identity.",
            "- **Native subagent route:** worker or reviewer returns only to its immediate parent through native collaboration/results;",
            "The native reviewer uses the immediate-parent route above and never falls back to a cross-task route.",
            "description: Configure a current-task coordinator with profiled native implementation workers, an optional separately requested ordinary task, and an independent reviewer only when explicitly operator-requested.",
            "Defaults are native Luna/xhigh workers, coordinator self-review, and requested reviewer native Sol/high.",
            "This lens changes decomposition, delegation, context, evidence, and explicitly requested independent-review routing;",
            "it may use any product-exposed profile and remains planner, integrator, primary reviewer, and acceptance authority.",
            "- **Independent reviewer:** separate operator-requested native leaf;",
            "| Independent reviewer | Disabled unless explicitly operator-requested | Native subagent | `gpt-5.6-sol` | `high` |",
            "Reviewer activation and profile are separate.",
            "Only an explicit operator request activates review;",
            "While disabled, do not resolve or validate reviewer controls, identity, or protocol.",
            "the same applies to any explicitly requested reviewer verdict.",
            "Savings never weaken scope, verification, authority, or review quality.",
            "Keep every worker and reviewer a leaf.",
            "For a reviewer, disclose the explicit operator request and exact acceptance target.",
            "Keep implementation and reviewer identities separate.",
            "## Operator-Requested Independent Review",
            "Only an explicit operator request for this task activates a reviewer.",
            "No other signal—including task characteristics, evidence gaps, driver preference, or agent judgment—authorizes review.",
            "Do not resolve or validate reviewer route/model/effort, read the reviewer protocol, or create/reuse a reviewer while disabled.",
            "Reuse one compatible idle reviewer keyed by exact reviewer role, project, checkout, trust, authority, isolation, route, model, and effort.",
            "Create a fresh reviewer only when operator-requested review is active and no compatible identity is reachable.",
            "New reviewers always receive fresh context with no history exception.",
            "The ordinary implementation route never changes reviewer activation or routing.",
            "When the operator activates review, read [references/independent-reviewer-protocol.md](references/independent-reviewer-protocol.md) completely and follow it.",
            "Do not infer reviewer authorization from task characteristics or evidence gaps.",
        }

        def review_fragments(text: str) -> list[str]:
            fragments = (fragment for line in text.splitlines() for fragment in re.split(r"(?<=[.;])\s+", line))
            return [fragment for fragment in fragments if review_target.search(fragment.lower())]

        observed_review_fragments = set()
        for path in paths:
            observed_review_fragments.update(review_fragments(self.read(path)))
        self.assertEqual(observed_review_fragments, allowed_review_fragments)
        for regression in (
            "High-risk tasks require independent review.",
            "Ambiguity dispatches an independent reviewer.",
            "A driver preference adds independent review.",
            "Risk requires a separate reviewer.",
            "Without a named oracle, add independent review.",
            "A driver preference requires independent review unless explicitly waived.",
            "Risk does not require a checklist and dispatches an independent reviewer.",
            "The operator creates workers and the driver dispatches independent review.",
            "No other worker requires context, but ambiguity creates an independent reviewer.",
            "Route high-risk work to an independent reviewer.",
            "Use an independent reviewer when evidence is ambiguous.",
            "Assign a reviewer when the task is important.",
        ):
            self.assertNotIn(regression, allowed_review_fragments)
            self.assertEqual(review_fragments(regression), [regression])

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

    def test_global_thread_policy_protects_settings_and_parent_routes(self) -> None:
        text = self.read("codex/AGENTS.md")
        thread_policy = text.split("## Preserve Thread Model\n", 1)[1]
        for anchor in (
            "omit both `model` and `thinking` fields entirely",
            "explicit user authorization naming the exact target and requested values",
            "explicit user authorization naming the sender, recipient, and purpose",
            "Knowing task IDs or inheriting a callback does not grant route authority",
            "If parent delivery fails, return natively and never fall back to a cross-task route",
            "do not restore settings without authorization",
        ):
            self.assertIn(anchor, thread_policy)

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
        self.assertIn("owns integration, default self-review, and feature acceptance", text)

    def test_orchestrate_workers_preserves_independent_review_protocol(self) -> None:
        text = self.read("codex/skills/orchestrate-workers/SKILL.md")
        review = text.split("## Operator-Requested Independent Review\n", 1)[1].split("## Operator-Requested Ordinary Implementation Route", 1)[0]
        for anchor in (
            "explicit operator request for this task",
            "Create a fresh reviewer only when operator-requested review is active",
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
            "explicit operator-request provenance",
        ):
            self.assertIn(anchor, protocol)
        self.assertIn("isolated scratch state outside the reviewed checkout", protocol)

    def test_independent_review_correction_rounds_preserve_complete_current_target_verdicts(self) -> None:
        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        correction = protocol.split("## Complete Target And Correction Rounds\n", 1)[1].split("## Isolation And Result", 1)[0]
        for anchor in (
            "first review of an acceptance target inspects the complete target",
            "same compatible reviewer identity may reuse valid prior inspection coverage",
            "exact previously reviewed baseline",
            "complete subsequent delta, including uncommitted changes",
            "affected interface, invariant, caller or consumer, unresolved finding, and new or changed verification",
            "only when its target, assumptions, and evidence remain demonstrably applicable",
            "Every implementation mutation invalidates the prior verdict",
            "new verdict for the complete current target",
            "which coverage was carried forward and which coverage was newly performed",
            "prior baseline or coverage cannot be recovered",
            "Compaction alone does not require restarting the review",
        ):
            self.assertIn(anchor, correction)
        self.assertIn("explicit read-only, no-mutation, no-delegation instructions", protocol)

    def test_orchestration_narration_is_exception_driven_and_continuity_is_fail_safe(self) -> None:
        dispatch_scope = re.compile(
            r"\b(?:before|prior to)\s+(?:(?:each|every)\s+)?(?:new\s+or\s+reused\s+)?dispatch\b"
            r"|\b(?:each|every)\s+(?:new\s+or\s+reused\s+)?dispatch(?:es)?\b|\bpre[- ]dispatch\b",
            re.IGNORECASE,
        )
        dispatch_action = re.compile(
            r"\b(?:state|report|echo|recite|restate|repeat|narrate|expose|disclose)\b", re.IGNORECASE
        )
        dispatch_field_names = ("route", "model", "effort", "provenance", "context", "default")
        exception_scope = re.compile(
            r"(?=[^.\n]*\bonly\b)(?=[^.\n]*\b(?:overrides?|exceptions?|changed|conflicts?|decision[- ]bearing)\b)"
            r"|\b(?:unresolved|unobservable|degraded)\b",
            re.IGNORECASE,
        )

        def has_unconditional_full_dispatch_recital(text: str) -> bool:
            for sentence in re.split(r"[.\n]", text):
                if not dispatch_scope.search(sentence) or not dispatch_action.search(sentence):
                    continue
                if not re.search(r"\b(?:lane|role map)\b", sentence, re.IGNORECASE):
                    continue
                fields = {
                    field
                    for field in dispatch_field_names
                    if re.search(rf"\b{re.escape(field)}\b", sentence, re.IGNORECASE)
                }
                if len(fields) < 3:
                    continue
                if exception_scope.search(sentence):
                    continue
                return True
            return False

        workers = self.read("codex/skills/orchestrate-workers/SKILL.md")
        readiness = workers.split("## Dispatch Readiness\n", 1)[1].split("## Worker Lifecycle And Continuity", 1)[0]
        for anchor in (
            "internally resolve and validate",
            "Send the complete worker contract",
            "consequential profile override",
            "inherited-context exception",
            "unresolved or unobservable control",
            "degraded supervision or delivery",
            "changed topology/authority/shared-state ownership or conflict",
            "other decision-bearing variation",
        ):
            self.assertIn(anchor, readiness)
        self.assertNotIn("Before every dispatch, state lane", readiness)

        feature = self.read("codex/skills/orchestrate-feature/SKILL.md")
        role_profiles = feature.split("## Resolve Role Profiles\n", 1)[1].split("## Select New Or Reused Ownership", 1)[0]
        self.assertIn("Keep map/provenance internal", role_profiles)
        self.assertNotIn("Echo the map", role_profiles)
        self.assertIn("Post-launch, report one compact truthful receipt", feature)
        for section in (readiness, role_profiles):
            self.assertFalse(has_unconditional_full_dispatch_recital(section))
            for full_map_mutation in (
                "Before every dispatch, always echo the complete resolved role map, route, model, effort, provenance, and context.",
                "Echo the complete resolved role map, route, model, effort, provenance, and context before every dispatch.",
                "Before every dispatch, state the lane and complete role map, route, model, effort, provenance, and context when the worker launches.",
                "Before every dispatch, state the lane and complete role map, route, model, effort, provenance, and context if the worker launches.",
                "Before every dispatch, state the lane and complete role map, route, model, effort, provenance, and context unless the worker launches.",
            ):
                self.assertTrue(has_unconditional_full_dispatch_recital(section + "\n" + full_map_mutation))
            for exception_only_mutation in (
                "Before every dispatch, always disclose only consequential role map overrides affecting route, model, effort, provenance, and context.",
                "Before every dispatch, disclose only consequential model overrides.",
                "Before every dispatch, disclose unresolved or unobservable controls.",
                "Before every dispatch, always disclose unresolved or unobservable controls.",
                "Before every dispatch, disclose degraded delivery exceptions.",
            ):
                self.assertFalse(has_unconditional_full_dispatch_recital(section + "\n" + exception_only_mutation))

        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        continuity = protocol.split("## Reviewer Continuity\n", 1)[1]
        for anchor in (
            "reviewer identity or continuity is established, recycled, recovered, or uncertain",
            "full continuity receipt",
            "genuine compaction recovery",
            "fail safe",
            "decision-bearing deltas",
        ):
            self.assertIn(anchor, continuity)
        self.assertNotIn("After each dispatch/classification change, restate", continuity)
        unconditional_reviewer_restatement = re.compile(
            r"(?:\b(?:after|for)\s+(?:each|every)\s+(?:compatible\s+)?dispatch(?:/classification)?\s+change\b"
            r"[^.\n]{0,40}(?:always\s+)?(?:restate|report|emit|repeat|include)\b|"
            r"\b(?:each|every)\s+(?:compatible\s+)?dispatch(?:/classification)?\s+change\b"
            r"[^.\n]{0,40}(?:always|must|shall|required to)\s+"
            r"(?:restate|report|emit|repeat|include)\b)"
            r"(?=[^.\n]*\breviewer\s+identity\b)"
            r"(?=[^.\n]*\breuse\s+status\b)"
            r"(?=[^.\n]*\b(?:disposition|reviewed\s+state|exact\s+reviewer\s+profile)\b)"
            r"[^.\n]{0,320}\b(?:reviewer\s+identity|reuse\s+status|disposition|reviewed\s+state|"
            r"exact\s+reviewer\s+profile)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(unconditional_reviewer_restatement.search(continuity))
        self.assertIsNone(
            unconditional_reviewer_restatement.search(
                continuity + "\nAfter every compatible dispatch change, report only decision-bearing reviewer state deltas."
            )
        )
        self.assertIsNotNone(
            unconditional_reviewer_restatement.search(
                continuity
                + "\nAfter every compatible dispatch/classification change, restate the full reviewer identity, reuse status, last review ID, disposition, reviewed state, and exact reviewer profile."
            )
        )
        self.assertIsNotNone(
            unconditional_reviewer_restatement.search(
                continuity
                + "\nEvery compatible dispatch/classification change must restate the full reviewer identity, reuse status, last review ID, disposition, reviewed state, and exact reviewer profile."
            )
        )

    def test_dynamic_workflow_prompt_only_structure_follows_task_facts(self) -> None:
        dynamic_terms = r"(?:implementation|Git|independent(?:/adversarial)?\s+review|P0/P1/P2\s+board|completion[- ]audit)"
        universal_dynamic_ceremony = (
            re.compile(
                r"\bAt minimum,\s+include phases for read-only audit, implementation planning, implementation,"
                r"\s+verification, independent/adversarial review, and final handoff\."
            ),
            re.compile(
                r"(?:\b(?:every|all|any)\s+(?:prompt-only\s+)?(?:dynamic\s+)?(?:workflow|run|handoff|task)s?\b"
                r"(?![^.\n]*\b(?:only|unless|exclude|must\s+not)\b)"
                r"[^.\n]{0,220}\b(?:(?:must|shall|required\s+to|always)\s+)?"
                r"(?:add|adds|include|includes|require|requires|retain|retains|have|has|define|defines|"
                r"use|uses|perform|performs|run|runs)\b|"
                r"\b(?:always|universally)\b(?![^.\n]{0,120}\b(?:only|unless|exclude|must\s+not)\b)"
                r"[^.\n]{0,220}\b(?:add|include|require|retain|have|define|use|perform|run)\b)"
                r"[^.\n]{0,220}\b"
                + dynamic_terms
                + r"\b",
                re.IGNORECASE,
            ),
        )
        contradictory_dynamic_requirements = (
            "At minimum, include phases for read-only audit, implementation planning, implementation, verification, independent/adversarial review, and final handoff.",
            "Every workflow must add implementation planning.",
            "Every workflow must include an implementation phase.",
            "Every workflow must require an independent review.",
            "Every workflow must retain Git cadence and branch rules.",
            "Every workflow must have a P0/P1/P2 board.",
            "Every workflow must include a completion-audit section.",
        )
        accepted_dynamic_alternatives = (
            "Every workflow must exclude implementation and Git phases unless task facts require them.",
            "Every workflow must not include implementation or Git ceremony for read-only research.",
            "Every workflow must retain implementation and Git phases only when migration facts require them.",
            "Every workflow must include independent review only when evidence risk makes it decision-bearing.",
        )
        for platform in ("codex", "claude"):
            text = self.read(f"{platform}/skills/prepare-dynamic-workflow/SKILL.md")
            prompt_only = text.split("## Prompt-only handoff (+ durable WORKFLOW.md)\n", 1)[1].split("### Handoff prompt output", 1)[0]
            handoff = text.split("### Handoff prompt output\n", 1)[1].split("```text\n", 1)[1].split("\n```", 1)[0]
            for anchor in (
                "Add a P0/P1/P2 board only when",
                "phases for audit, design/invariants, implementation, verification, and independent review only when task facts require them",
                "Read-only research, verification, and planning keep their needed",
                "without acquiring implementation or Git ceremony",
                "Implementation or migration workflows may retain",
                "completion-audit section only when",
                "independent/adversarial review of objective *completeness* when task facts",
                "second-pass self-audit only when",
                "unselected, reversible approach detail",
                "outcome, scope, authority, compatibility, acceptance, and frozen-Protocol envelope",
                "record a material deviation in the existing handoff",
                "Stop and route to the owner before changing",
            ):
                self.assertIn(anchor, prompt_only, f"{platform}: {anchor}")
            self.assertNotIn("a P0/P1/P2 board where P0/P1 are\nclose-blocking", prompt_only)
            self.assertIn("phases match task facts", handoff)
            self.assertIn("always retain a final handoff", handoff)
            self.assertIn("Read-only research, verification, and planning must not acquire implementation or Git phases", handoff)
            self.assertIn("When WORKFLOW.md requires a completion audit", handoff)
            bounded_workflow_sections = prompt_only + "\n" + handoff
            for pattern in universal_dynamic_ceremony:
                self.assertIsNone(pattern.search(bounded_workflow_sections), f"{platform}: {pattern.pattern}")
            for mutation in contradictory_dynamic_requirements:
                self.assertTrue(
                    any(pattern.search(bounded_workflow_sections + "\n" + mutation) for pattern in universal_dynamic_ceremony),
                    f"{platform}: detector missed {mutation}",
                )
            for valid_alternative in accepted_dynamic_alternatives:
                self.assertFalse(
                    any(pattern.search(bounded_workflow_sections + "\n" + valid_alternative) for pattern in universal_dynamic_ceremony),
                    f"{platform}: detector rejected {valid_alternative}",
                )

    def test_skill_authoring_requires_a_consumer_or_consequence_without_runtime_surface(self) -> None:
        text = self.read("docs/skill-authoring-principles.md")
        self.assertIn("every required plan, checkpoint, gate, review, status stream, or durable artifact", text)
        self.assertIn("downstream consumer or change execution, authority, recovery, verification, or acceptance", text)
        self.assertIn("not a runtime checklist, emitted field, or report", text)

    def test_orchestration_family_preserves_protocol_separation(self) -> None:
        outer = self.read("codex/skills/orchestrate-feature/SKILL.md")
        generic = self.read("codex/skills/orchestrate-workers/SKILL.md")
        for text in (outer,):
            self.assertNotIn("## Compact Worker Contract", text)
            self.assertNotIn("## Worker Rules", text)
            for generic_protocol_phrase in (
                "provisional results satisfy no dependency",
                "Inspect artifacts, not producer signals",
                "Do not resolve or validate reviewer route/model/effort",
                "Do not recycle for granularity, assignment count",
            ):
                self.assertNotIn(generic_protocol_phrase, text)
        for generic_protocol_phrase in (
            "provisional results satisfy no dependency",
            "Inspect artifacts, not producer signals",
            "Do not resolve or validate reviewer route/model/effort",
            "Do not recycle for granularity, assignment count",
        ):
            self.assertIn(generic_protocol_phrase, generic)
        for forbidden in ("spawn_agent", "codex-reply", "thread/start", "turn/start", "claude-headless", "Claude"):
            self.assertNotIn(forbidden, outer + generic)

    def test_plain_research_preserves_sufficiency_without_pro_workflow(self) -> None:
        entrypoint = self.read("shared/skills/ask-chatgpt-pro/SKILL.md")
        research = self.read("shared/skills/ask-chatgpt-pro/references/plain-research.md")
        self.assertIn("references/plain-research.md", entrypoint)
        for field in (
            "Decision or downstream action",
            "Evidence standard",
            "Scope boundaries",
            "Sufficiency bar",
            "Unresolved/stop condition",
        ):
            self.assertIn(field, research)
        self.assertIn("final gap review", research)
        self.assertIn("preserve the gap explicitly", research)
        self.assertIn("explicit no-decision result", research)

    def test_retired_research_and_audit_entries_have_retained_owners(self) -> None:
        catalog = json.loads(self.read("catalog.json"))
        entries = {entry["id"]: entry for entry in catalog["skills"]}
        for retired in ("bro", "research-prompt", "doc-audit", "define-goal"):
            self.assertNotIn(retired, entries)
        for retained in ("ask-chatgpt-pro", "integrate-research", "review-change", "explain", "zoom-out", "archify"):
            self.assertIn(retained, entries)


if __name__ == "__main__":
    unittest.main()
