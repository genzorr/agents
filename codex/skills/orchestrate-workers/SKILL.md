---
name: orchestrate-workers
description: Configure a current-task coordinator to use profiled native implementation workers, an optional separately operator-requested ordinary implementation task, and an independently profiled native reviewer. Own decomposition, continuity, fresh context, evidence, reviewer escalation, and acceptance without changing the coordinator profile or lifecycle driver. Defaults are native Sol/medium workers and native Sol/high reviewer; another exact profile requires explicit operator instruction, an operator-authorized launch contract, or the explicit sol-luna-orchestration preset, while the ordinary task route always requires a separate explicit operator request. Use only after explicit invocation of orchestrate-workers, a relayed invocation in an operator-authorized feature launch, or the explicit sol-luna-orchestration preset.
---

# Orchestrate Workers

**Composition role: lens.** Keep the current task skill or workflow as driver. It decides whether delegation is allowed and retains lifecycle, success criteria, authority, and acceptance. This lens changes decomposition, delegation, context, evidence, and independent-review routing; it grants no authority and never changes the current coordinator's profile.

## Configure Only

If invoked without a resolved task and coherent delegation boundary, confirm provisional configuration, name what the coordinator must resolve, and return without launching. Activation applies to the current resolved task. A later task, or one resolved after provisional configuration, requires a fresh explicit invocation. A relayed invocation in an operator-authorized feature launch or the explicit `sol-luna-orchestration` preset satisfies activation; another agent-relayed request does not.

## Terms And Profiles

- **Coordinator:** current task applying this lens; it may use any product-exposed profile and remains planner, integrator, primary reviewer, and acceptance authority.
- **Implementation worker:** selected native leaf subagent or separately operator-requested ordinary implementation task at the worker profile.
- **Independent reviewer:** separate native leaf identity at the reviewer profile, used only when the escalation rule or governing driver/operator requires it; never a worker.
- **Workstream:** coherent ownership lane. **Assignment:** one bounded worker contract. **Recycle:** stop reuse and create a fresh identity only on a named material boundary.

| Role | Default route | Model | Effort |
|---|---|---|---|
| Implementation worker | Native subagent | `gpt-5.6-sol` | `medium` |
| Independent reviewer | Native subagent | `gpt-5.6-sol` | `high` |

Use another worker/reviewer profile only on explicit operator instruction, an operator-authorized launch contract, or the explicit `sol-luna-orchestration` preset. The ordinary implementation-task route always requires a separate explicit operator request; neither a launch contract nor the preset authorizes that route by itself. Resolve roles independently; one override never changes the coordinator or another role. Preserve the coordinator's current model/effort. Before dispatch, state route, exact model, effort, context mode, and `default`/`operator override` provenance. Stop if an exact selected route/model/effort/context control cannot be set or validated; never substitute, raise/lower silently, or claim readback from request acceptance.

Preserve permissions, approval policy, scope, stop gates, and no-worktree-without-operator-approval. Use only stable native behavior; do not fabricate syntax, controllers, registries, ledgers, daemons, queues, side-channel files, or delivery mechanisms.

## Operating Model

- Keep one visible acceptance boundary at the coordinator. Worker/reviewer reports are evidence, not acceptance.
- Let workers own bounded implementation and implementation-depth verification: governing contracts, full owned diff/artifacts, plausible wrong implementations, proportionate failure/recovery paths, and uncertainty.
- Perform a narrow coordinator gate over integrated state and decision-critical evidence. Reuse current scope-complete worker checks; run only missing, stale, contradicted, or decision-critical checks.
- Keep the task open until every planned lane, launched identity, and required handoff is classified and acceptance finishes. Savings never weaken scope, verification, authority, or review quality.

## Decompose And Route

1. Resolve architecture, scope, user decisions, risks, authorities, stop gates, observable completion, and selected profiles before delegation. Point to durable paths and symbols instead of conversation history.
2. Prefer one coherent worker. Add workers only for non-overlapping ownership lanes; keep sequential assignments over one lane on one compatible worker.
3. Before parallel dispatch, map objective, owned files/components, read/write boundary, inputs, downstream recipient, artifact, verification owner, and integration order. Launch only the dependency-free frontier within concurrency limits.
4. Treat the checkout as shared. Assign one owner for Git state, generated/build artifacts, test databases, ports, formatters, code generation, and other shared state; defer contention. Parallelism never authorizes a worktree.
5. Launch new workers with no parent turns by default and confirm that setting. Treat an inherited-turn fork as exceptional: use only the smallest bounded recent slice for one named load-bearing fact with no durable source that cannot be accurately distilled without material loss; state the fact, reason, and exact slice. Never inherit full parent history. Inherited context is not authority; restate scope, permissions, decisions, and criteria.
6. Keep every worker and reviewer a leaf. The coordinator alone creates agents, aggregates results, and mediates handoffs.

## Dispatch Preamble

Before every dispatch, state lane, workstream/assignment, new/reused identity, route, model, effort, provenance, and context mode. For a worker, also name the root work it substitutes for, unique output, downstream decision affected, and why the lane is non-duplicative. For a reviewer, state the three-part escalation rationale below. Do not dispatch with unknown required facts.

## Worker Lifecycle And Continuity

1. Send the Compact Worker Contract and applicable Worker Rules.
2. After native subagent dispatch, continue useful coordinator work and wait through the native result surface. After an explicitly requested ordinary task launch, return immediately and never poll; inspect only on operator status request or missing-delivery report.
3. Route dependencies through the coordinator. Launch a dependent lane only after upstream classification and validation of the smallest required handoff; provisional results satisfy no dependency.
4. Send bounded corrections and compatible successive assignments to the same worker. Correct a bad coordinator contract without forcing a failed retry. Never change the selected worker profile without an explicit operator instruction.
5. On blocked/partial/failed work or invalidated assumptions, halt dependents and replan. Correct/stop natively when available; otherwise classify output invalid and redo under a corrected contract. Never replace a stalled/failed worker silently.
6. Classify every worker `complete`, `blocked`, `partial`, or `failed`; reconcile shared state and every planned lane/handoff.
7. Reuse a compatible idle worker only when identity is reachable and role, project, checkout, trust, authority, ownership, route, model, and effort still fit. Profile change is incompatibility. Compaction does not justify recycling.
8. Before reuse, resend the full contract with an assignment-reset overlay: prior assignment/disposition, allowed carry-over facts, invalid assumptions/scope/permissions/decisions/claims, interfaces, success, verification, return format, and stale-conflict reporting. A bounded current-assignment correction needs only changed constraints.
9. Recycle only for material repository/checkout/trust/authority/permission change; incompatible role/route/model/effort; uncorrected superseded contract; unrecoverable decision-critical constraint; repeated acceptance-critical miss/stale/overbuilt direction after correction; hidden unresolved state; unreachable identity; or operator request. Report lost continuity and prior disposition.
10. Do not recycle for granularity, assignment count, token budget, elapsed time, routine correction, delayed handoff, or compatible operator decisions. Keep implementation and reviewer identities separate.

## Compact Worker Contract

Send only applicable fields:

- **Objective and durable references:** bounded outcome; task/specification/source/instruction paths.
- **Scope and interfaces:** owned files/components/questions, non-goals, boundaries, signatures, schemas, commands, compatible behavior.
- **Authority:** local write, validation, commit, push, lifecycle, external-write permissions; delegation is always none.
- **Context and continuity:** identity, assignment/workstream, checkpoint, carry-over facts, invalid prior authority/claims, exact worker profile.
- **Dependencies and handoffs:** inputs, downstream owner, artifact/fact, delivery condition/order, coordinator recipient.
- **Success and verification:** observable criteria/artifacts, checks/evidence, plausible wrong implementations, failure/recovery paths, and driver-required reviewed behavior-spine proof.
- **Stop/ask gates:** user decisions, architecture/contract change, unsafe expansion, missing authority/infrastructure, dependency failure, material ambiguity.
- **Return route:** parent coordinator for a native subagent. An ordinary task requires the exact originating coordinator `threadId` and `hostId` when required plus the explicit native `send_message_to_thread` action; accepted blocker/terminal sends establish delivery, while rejection or unavailability remains local delivery failure.
- **Return format:** status; outcome; files/commit; commands; exact tested state; paths/criteria; judgments; blockers/uncertainty; dependency handoffs; continuity; and applicable decision-bearing evidence summary.

Omit chain-of-thought, builder reasoning, long history, and failed-attempt narration. Return only a genuine blocker/stop or final report.

## Worker Rules

- Recover and cite governing contracts; do not substitute an internally consistent interpretation.
- Inspect the complete owned diff and every non-interchangeable decision-bearing artifact. Report foreign changes without claiming them.
- Sample only interchangeable items with basis/limits. Inspect artifacts, not producer signals, when claims rest on them.
- Run consequence tests against plausible wrong implementations. Reject implementation-derived oracles unless exact shape is the documented contract.
- Trace fail-closed, error, retry, and recovery behavior proportionately. Challenge nonclaims and report uncertainty/divergence.
- Preserve sibling ownership and operator work. Escalate architecture/contract changes, unsafe rewrites, authority/infrastructure gaps, and dependency conflicts.
- Never broaden authority, delegate, or claim success with missing evidence.

## Escalated Independent Review

The coordinator is the default reviewer. Require independent review when the operator or driver does; otherwise escalate only for a named acceptance-critical target where fresh judgment has material expected value and at least one condition applies:

- Evidence supports conflicting plausible interpretations.
- Consequential behavior lacks a named reliable deterministic oracle and leaves a specific judgment open.
- The coordinator materially designed/revised the disputed surface and names a concrete anchoring concern.
- A cross-worker boundary depends on judgment not covered by checks.

Generic confidence, importance, risk label, worker completion/count, public interface, or reviewer availability does not qualify. Before dispatch state (1) exact target, (2) why independence adds value beyond coordinator review, and (3) how verdicts change acceptance. If any is missing, do not dispatch.

Reuse one compatible idle reviewer keyed by exact reviewer role, project, checkout, trust, authority, isolation, route, model, and effort. Create a fresh reviewer only when escalation is required and no compatible identity is reachable. New reviewers always receive fresh context with no history exception. Independence comes from separate identity, fresh context, no implementation ownership, and protocol—not model name. The ordinary implementation route never changes reviewer routing.

When escalation fires, read [references/independent-reviewer-protocol.md](references/independent-reviewer-protocol.md) completely and follow it.

## Operator-Requested Ordinary Implementation Route

Use only on a separate explicit operator request; an operator-authorized feature launch may explicitly forbid it. Resolve the exact originating coordinator `threadId` and `hostId` when required from native status and require the explicit native `send_message_to_thread` action; never invent/store a side-channel route. Use the resolved worker profile and the same decomposition, ownership, dependency, reset, and contract rules. Do not create a worktree without approval.

After launch, return the launch response immediately and do not wait or poll. The task sends only a genuine blocker or final handoff to the exact coordinator through native callback. An accepted blocker/terminal send establishes delivery; rejection or unavailability remains local delivery failure. Reuse only for compatible assignments after reset; across tasks require fresh lens invocation and explicit ordinary-route request. Create a new task only on explicit request or recycle trigger.

## Coordinator Depth Budget

- Spend coordinator effort on architecture/risk decisions, dependencies, contract quality, integration, decision-critical evidence, and acceptance.
- Let workers own broad scans, implementation, diagnostics, implementation-depth checks, owned-diff inspection, and task verification.
- Add lanes only when output changes or accelerates a named downstream decision. Do not infer oracle independence from a green suite.
- Treat worker facts rediscovered by the coordinator as handoff feedback. Report decision-bearing state changes; do not poll or repeat unchanged progress.
