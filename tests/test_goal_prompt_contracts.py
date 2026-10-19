"""Static contracts for goal quality, Codex orchestration, and research sufficiency."""

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

    def test_orchestration_family_preserves_codex_and_admits_pi_counterparts(self) -> None:
        catalog = json.loads(self.read("catalog.json"))
        entries = {item["id"]: item for item in catalog["skills"]}
        expected = {
            "orchestrate-feature": ("codex/skills/orchestrate-feature", "skills/orchestrate-feature", "role:helper"),
            "orchestrate-workers": ("codex/skills/orchestrate-workers", "skills/orchestrate-workers", "role:helper"),
        }
        self.assertNotIn("orchestrate-sol-feature", entries)
        self.assertFalse((REPO_ROOT / "codex/skills/orchestrate-sol-feature").exists())
        self.assertNotIn("sol-luna-orchestration", entries)
        self.assertFalse((REPO_ROOT / "codex/skills/sol-luna-orchestration").exists())
        for skill_id, (source, target, role) in expected.items():
            entry = entries[skill_id]
            platforms = ["codex", "pi"]
            self.assertEqual(entry["platforms"], platforms)
            self.assertEqual(entry["source"]["codex"], source)
            self.assertEqual(entry["install_target"]["codex"], target)
            self.assertEqual(set(entry["source"]), set(platforms))
            self.assertEqual(set(entry["install_target"]), set(platforms))
            self.assertEqual(entry["tags"], [role, "domain:orchestration"])
            self.assertFalse((REPO_ROOT / f"claude/skills/{skill_id}").exists())
            self.assertIn("allow_implicit_invocation: false", self.read(f"{source}/agents/openai.yaml"))

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

    def section(self, text: str, heading: str) -> str:
        return text.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]

    def test_feature_invocation_preserves_separate_owner_and_external_acceptance(self) -> None:
        feature = self.read("codex/skills/orchestrate-feature/SKILL.md")
        prepare = self.section(feature, "Prepare and launch")
        contract = self.section(feature, "Owner contract")
        self.assertIn("exactly one ordinary owner", prepare)
        self.assertIn("refuse nested ordinary feature-owner creation", prepare)
        self.assertIn("never a native leaf or inherited fork", prepare)
        self.assertIn("regardless of task size/duration", feature)
        self.assertIn("the owner cannot accept its feature or close its task", contract)
        self.assertIn("no ordinary-task-creation authority and may create only authorized native leaves", contract)
        self.assertIn("Scope → Plan → Execute → Review → Close", contract)
        self.assertIn("reuses approved behavior", contract)
        self.assertIn("not parent history or this outer skill", contract)

    def test_submitted_ui_requests_authorize_on_demand_help_advice_and_review(self) -> None:
        for name in ("orchestrate-feature", "orchestrate-workers"):
            ui = self.read(f"codex/skills/{name}/agents/openai.yaml")
            prompt = ui.split('default_prompt: "', 1)[1].split('"', 1)[0]
            self.assertIn(f"${name}", prompt)
            self.assertIn("I authorize as many bounded Luna helpers as useful and advisor consultation as needed", prompt)
            self.assertIn("independent review", prompt)
            self.assertIn("allow_implicit_invocation: false", ui)
        workers = self.read("codex/skills/orchestrate-workers/SKILL.md")
        roles = self.section(workers, "Authorized roles")
        self.assertIn("actual explicit user delegation request", roles)
        self.assertIn("Missing optional assistance leaves direct execution continuing", roles)
        self.assertIn("never silently substitute or waive it", roles)

    def test_dispatch_uses_separable_results_and_preserves_owner_execution(self) -> None:
        workers = self.read("codex/skills/orchestrate-workers/SKILL.md")
        roles = self.section(workers, "Authorized roles")
        self.assertIn("loop with the owner by default", roles)
        self.assertIn("expected avoided work or delivery benefit exceeds briefing, supervision and integration cost", roles)
        self.assertIn("Bounded helper owns the result and its verification/repair", roles)
        self.assertIn("Insufficient reason alone for another worker", roles)
        self.assertIn("without a fixed helper-count cap or per-dispatch permission", roles)
        self.assertIn("parallel when resource ownership permits", roles)
        self.assertIn("Never manufacture assignments", roles)
        self.assertIn("planning agent requires explicit instruction", roles)
        self.assertIn("No automatic main/planning layer or justification for ordinary direct implementation", roles)

    def test_creation_profiles_resolve_only_used_roles_without_cascading(self) -> None:
        workers = self.read("codex/skills/orchestrate-workers/SKILL.md")
        profiles = self.section(workers, "Authorized roles")
        # These identifiers are the selected public creation contract, not runtime availability claims.
        self.assertIn("Bounded helper | `gpt-6-luna` / `xhigh`", profiles)
        self.assertIn("independent reviewer | `gpt-6.1-sol` / `high`", profiles)
        self.assertIn("unresolved question | `gpt-6.1-sol` / `xhigh`", profiles)
        self.assertIn("main execution worker | `gpt-6.1-sol` / `medium`", profiles)
        precedence = ("role default", "explicit general worker override", "matching named-assignment override")
        positions = [profiles.index(term) for term in precedence]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Resolve only used roles", profiles)
        self.assertIn("one override never changes another role or the coordinator", profiles)
        self.assertIn("An omitted named field retains the resolved general field", profiles)
        self.assertIn("never silently upgrade or substitute", profiles)
        self.assertIn("not independent readback", profiles)
        feature = self.section(self.read("codex/skills/orchestrate-feature/SKILL.md"), "Prepare and launch")
        self.assertIn("`gpt-6.1-sol` / `medium`", feature)
        self.assertIn("Preserve the orchestrator's exact settings", feature)
        self.assertIn("stop on mismatch or an unobservable explicit requirement", feature)

    def test_advisor_is_available_before_consequential_commitment(self) -> None:
        advisor = self.section(self.read("codex/skills/orchestrate-workers/SKILL.md"), "Advisor on demand")
        self.assertIn("Create the advisor on first use and reuse it", advisor)
        self.assertIn("Consult before committing to a consequential technical direction", advisor)
        self.assertIn("focused investigation", advisor)
        self.assertIn("Do not wait for repeated failed implementations or consult on routine settled choices", advisor)
        self.assertIn("decisive facts/references, constraints and credible alternatives", advisor)
        self.assertIn("cannot replace a user-owned product/scope decision", advisor)
        self.assertIn("cannot be its independent reviewer", advisor)

    def test_native_context_routes_and_continuity_preserve_boundaries(self) -> None:
        workers = self.read("codex/skills/orchestrate-workers/SKILL.md")
        assignment = self.section(workers, "Assignment and continuity")
        self.assertIn("receive no parent turns", assignment)
        self.assertIn("Agents remain leaves and return only to their immediate parent", assignment)
        self.assertIn("No sibling, ordinary-task or higher-orchestrator fallback", assignment)
        self.assertIn("The coordinator alone steers children", assignment)
        self.assertIn("provisional results satisfy no dependency", assignment)
        self.assertIn("Do not reset active work", assignment)
        self.assertIn("Same-assignment messages carry deltas", assignment)
        self.assertIn("new assignments/uncertain continuity need prior disposition", assignment)
        self.assertIn("not elapsed time/compaction/ordinary repair", assignment)
        self.assertIn("Never silently replace failure", assignment)
        self.assertIn("including `model` and `thinking`, even when null", workers)
        self.assertIn("without unauthorized restoration", workers)

    def test_shared_resources_and_scientific_evidence_fail_closed(self) -> None:
        assignment = self.section(self.read("codex/skills/orchestrate-workers/SKILL.md"), "Assignment and continuity")
        self.assertIn("Serialize conflicts including the parent", assignment)
        self.assertIn("Git/index, generated/build state, databases, ports/devices and shared execution", assignment)
        self.assertIn("protect foreign work", assignment)
        self.assertIn("verify explicit predecessor dependencies", assignment)
        self.assertIn("Unknown ownership/cleanup blocks affected work", assignment)
        self.assertIn("Preserve scientific freezes, launch/run limits and valid negatives", assignment)
        self.assertIn("complete owned-change inspection", assignment)
        self.assertIn("consequence tests with independent expectations", assignment)
        self.assertIn("reject implementation-derived oracles unless exact shape is the contract", assignment)
        self.assertIn("sample only interchangeable items with basis/limits", assignment)

    def test_review_is_conditional_but_required_feature_review_cannot_be_waived_locally(self) -> None:
        workers = self.section(self.read("codex/skills/orchestrate-workers/SKILL.md"), "Assess returns and obtain review")
        self.assertIn("independent review of the final delivered target before reporting readiness for validation", workers)
        self.assertIn("actual task-scoped user request", workers)
        self.assertIn("If absent/unavailable, preserve the required review as pending", workers)
        self.assertIn("only when review is active", workers)
        self.assertIn("references/independent-reviewer-protocol.md", workers)
        self.assertIn("an implementer/advisor who shaped the candidate cannot fill it", workers)
        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        self.assertIn("only an authorized task-scoped waiver removes it", protocol)
        self.assertIn("read-only/no-delegation instructions", protocol)
        self.assertIn("Serialize overlapping writers or use an authorized snapshot", protocol)
        self.assertIn("only when established by the product", protocol)
        self.assertIn("void the verdict and recycle the reviewer", protocol)

    def test_review_corrections_bind_complete_target_and_acceptance_blocking_closure(self) -> None:
        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        coverage = self.section(protocol, "Coverage, correction and result")
        self.assertIn("complete target diff with decision-critical dependencies", coverage)
        self.assertIn("recover the exact baseline, findings and applicable coverage", coverage)
        self.assertIn("complete subsequent delta, affected interfaces/invariants/consumers and new verification", coverage)
        self.assertIn("Findings that block acceptance need independent confirmation of closure regardless of severity label", coverage)
        self.assertIn("owner checks cannot independently clear", coverage)
        self.assertIn("exact target and carried/new coverage", coverage)
        self.assertIn("Missing necessary evidence prevents a supported verdict", coverage)
        self.assertIn("intended-use validation", coverage)

    def test_feature_review_covers_final_delivery_without_expanding_manual_mandates(self) -> None:
        feature = self.section(self.read("codex/skills/orchestrate-feature/SKILL.md"), "Owner contract")
        workers = self.section(self.read("codex/skills/orchestrate-workers/SKILL.md"), "Assess returns and obtain review")
        protocol = self.read("codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md")
        for text in (feature, workers, protocol):
            self.assertIn("final delivered target", text)
            self.assertIn("unless the user explicitly waives review", text)
            self.assertIn("complete intervening delta and affected surfaces", text)
            self.assertIn("not after every edit", text)
        for text in (workers, protocol):
            self.assertIn("actual checkpoint mandate", text)
            self.assertIn("unrequested final-state review", text)

    def test_origin_receives_assesses_and_continues_without_asking_to_finish(self) -> None:
        feature = self.read("codex/skills/orchestrate-feature/SKILL.md")
        prepare = self.section(feature, "Prepare and launch")
        receive = self.section(feature, "Orchestrator receives and acts")
        self.assertIn("pending orchestrator assessment", prepare)
        self.assertIn("check the expected identity, assignment and applicable target", receive)
        self.assertIn("Read the linked handoff and decision-bearing evidence", receive)
        self.assertIn("perform already-authorized missing validation", receive)
        self.assertIn("same compatible owner when authorized", receive)
        self.assertIn("contain affected consumers, preserve original/invalidating evidence", receive)
        self.assertIn("never ask whether to finish work already requested", receive)
        self.assertIn("remaining outcome, allowed work, applicable state/evidence, affected verification/review and return condition", receive)
        self.assertIn("unresolved reserved choice", receive)
        self.assertIn("relay labeled unassessed, with the pending responsibility retained", receive)
        self.assertIn("assessment, validation state and next action", receive)
        self.assertIn("Passing checks, a `ship` verdict and a finished owner chat cannot close the feature", receive)
        self.assertIn("Cancellation/supersession remain distinct", receive)

    def test_transport_acceptance_and_manual_ordinary_exception_remain_truthful(self) -> None:
        feature = self.read("codex/skills/orchestrate-feature/SKILL.md")
        prepare = self.section(feature, "Prepare and launch")
        delivery = self.section(feature, "Owner messages and delivery")
        self.assertIn("exact origin `threadId`, required `hostId` and native `send_message_to_thread`", prepare)
        self.assertIn("bounded active waiting", prepare)
        self.assertIn("explicitly accepted manual supervision", prepare)
        self.assertIn("host-required confirmation", prepare)
        self.assertIn("Every mode retains actionable blocker, required-gate and terminal delivery", prepare)
        self.assertIn("actual ready identity, host and latest wait cursor", prepare)
        self.assertIn("Reconcile uncertain outcomes before retrying", delivery)
        self.assertIn("not receiver assessment, validation or closure", delivery)
        self.assertIn("Never fabricate IDs, guess routes or switch operations to bypass failure", delivery)
        self.assertIn("timeout or uninspected manual state remains unobserved", delivery)
        ordinary = self.section(self.read("codex/skills/orchestrate-workers/SKILL.md"), "Existing manual ordinary-task exception")
        self.assertIn("direct request naming an ordinary implementation route plus actual creation authority", ordinary)
        self.assertIn("a feature-owner launch cannot use it", ordinary)
        self.assertIn("Return the launch response without waiting", ordinary)
        self.assertIn("same ID", ordinary)
        self.assertIn("must assess the handoff and act", ordinary)

    def test_reports_preserve_decisive_tested_evidence_and_resource_disposition(self) -> None:
        workers = self.section(self.read("codex/skills/orchestrate-workers/SKILL.md"), "Assess returns and obtain review")
        self.assertIn("exact working/tested repository/checkout/ref or dirty state, source/spec/input/environment", workers)
        self.assertIn("checks/results/coverage, limitations, resource disposition and needed decisions", workers)
        self.assertIn("Never treat a returned report as automatic success", workers)
        self.assertIn("Reuse checks while source/environment/assumptions/coverage apply", workers)
        owner = self.section(self.read("codex/skills/orchestrate-feature/SKILL.md"), "Owner messages and delivery")
        self.assertIn("one complete accessible handoff link", owner)
        self.assertIn("independent review target/verdict", owner)

    def test_dispatch_narration_rejects_unconditional_full_maps(self) -> None:
        dispatch_scope = re.compile(
            r"\b(?:before|prior to)\s+(?:(?:each|every)\s+)?(?:new\s+or\s+reused\s+)?dispatch\b"
            r"|\b(?:each|every)\s+(?:new\s+or\s+reused\s+)?dispatch(?:es)?\b|\bpre[- ]dispatch\b",
            re.IGNORECASE,
        )
        narration = re.compile(r"\b(?:state|report|echo|recite|restate|repeat|narrate|expose|disclose)\b", re.IGNORECASE)
        exception_only = re.compile(
            r"(?=[^.\n]*\bonly\b)(?=[^.\n]*\b(?:overrides?|exceptions?|changed|conflicts?|decision[- ]bearing)\b)"
            r"|\b(?:unresolved|unobservable|degraded)\b",
            re.IGNORECASE,
        )

        def assert_no_full_recital(text: str) -> None:
            for sentence in re.split(r"[.\n]", text):
                if not dispatch_scope.search(sentence) or not narration.search(sentence):
                    continue
                if not re.search(r"\b(?:lane|role map)\b", sentence, re.IGNORECASE):
                    continue
                fields = sum(bool(re.search(rf"\b{field}\b", sentence, re.IGNORECASE)) for field in ("route", "model", "effort", "provenance", "context", "default"))
                self.assertFalse(fields >= 3 and not exception_only.search(sentence), sentence)

        good = (
            "Before every dispatch, disclose only consequential role map overrides affecting route, model, effort, provenance and context.",
            "Before every dispatch, disclose unresolved route, model and effort controls.",
            "Send the worker a complete assignment contract with route, model, effort, provenance and context before every dispatch.",
            "Before each dispatch, state the worker route, model, effort and context in its assignment contract.",
            "When continuity is uncertain, recover the full assignment contract with route, model, effort and context.",
            "For routine follow-ups, report only changed constraints and decision-bearing deltas.",
        )
        bad = (
            "Before every dispatch, always echo the complete resolved role map, route, model, effort, provenance and context.",
            "Report the full lane and role map, route, model, effort and context before each dispatch.",
            "Every new or reused dispatch must restate the role map, route, model and effort when a worker launches.",
        )
        for path in ("codex/skills/orchestrate-feature/SKILL.md", "codex/skills/orchestrate-workers/SKILL.md"):
            text = self.read(path)
            assert_no_full_recital(text)
            for clause in good:
                with self.subTest(path=path, allowed=clause):
                    assert_no_full_recital(text + "\n" + clause)
            for clause in bad:
                with self.subTest(path=path, rejected=clause):
                    with self.assertRaises(AssertionError):
                        assert_no_full_recital(text + "\n" + clause)

    def test_reviewer_continuity_rejects_repeated_full_recitals(self) -> None:
        repeated_full_receipt = re.compile(
            r"(?:\b(?:after|for)\s+(?:each|every)\s+(?:compatible\s+)?dispatch(?:/classification)?\s+change\b"
            r"[^.\n]{0,40}(?:always\s+)?(?:restate|report|emit|repeat|include)\b|"
            r"\b(?:each|every)\s+(?:compatible\s+)?dispatch(?:/classification)?\s+change\b"
            r"[^.\n]{0,40}(?:always|must|shall|required to)\s+(?:restate|report|emit|repeat|include)\b)"
            r"(?=[^.\n]*\breviewer\s+identity\b)(?=[^.\n]*\breuse\s+status\b)"
            r"(?=[^.\n]*\b(?:disposition|reviewed\s+state|exact\s+reviewer\s+profile)\b)[^.\n]*",
            re.IGNORECASE,
        )
        uncertain_recovery = re.compile(r"\bonly\s+(?:when|if)\s+(?:reviewer\s+)?continuity\s+is\s+uncertain\b", re.IGNORECASE)

        def assert_no_repeated_receipt(text: str) -> None:
            for sentence in re.split(r"[.\n]", text):
                self.assertFalse(repeated_full_receipt.search(sentence) and not uncertain_recovery.search(sentence), sentence)

        good = (
            "When reviewer continuity is uncertain, recover the full reviewer identity, reuse status, last review ID, disposition, reviewed state and exact reviewer profile.",
            "After every compatible dispatch/classification change, report only decision-bearing reviewer state deltas.",
            "After every compatible dispatch change, report the full reviewer identity, reuse status, disposition and reviewed state only when continuity is uncertain.",
            "Send a complete review assignment with reviewer identity, reuse status, disposition, reviewed state and exact reviewer profile.",
        )
        bad = (
            "After every compatible dispatch/classification change, restate the full reviewer identity, reuse status, last review ID, disposition, reviewed state and exact reviewer profile.",
            "Every compatible dispatch/classification change must include the full reviewer identity, reuse status, disposition, reviewed state and exact reviewer profile.",
        )
        for path in ("codex/skills/orchestrate-workers/SKILL.md", "codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md"):
            text = self.read(path)
            assert_no_repeated_receipt(text)
            for clause in good:
                with self.subTest(path=path, allowed=clause):
                    assert_no_repeated_receipt(text + "\n" + clause)
            for clause in bad:
                with self.subTest(path=path, rejected=clause):
                    with self.assertRaises(AssertionError):
                        assert_no_repeated_receipt(text + "\n" + clause)

    def test_current_docs_reconcile_ownership_and_preserve_history_as_history(self) -> None:
        prd = self.read("docs/orchestrate-feature-prd.md")
        spec = self.read("docs/orchestrate-feature-spec.md")
        for text in (prd, spec):
            self.assertIn("Scope → Plan → Execute → Review → Close", text)
            self.assertIn("without a fixed", text)
            self.assertIn("intended-use validation", text)
            self.assertIn("pending assessment", text)
        history = self.section(prd, "Historical provenance")
        self.assertIn("supersedes", history)
        self.assertIn("T-42", history)
        self.assertIn("does not authorize", history)

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
