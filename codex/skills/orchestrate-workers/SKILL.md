---
name: orchestrate-workers
description: Configure a current-task coordinator with profiled native implementation workers, an optional separately requested ordinary task, and an independent reviewer only when explicitly operator-requested. Preserve coordinator profile and driver while owning decomposition, continuity, fresh context, evidence, routing, and acceptance. Defaults are native Luna/xhigh workers, coordinator self-review, and requested reviewer native Sol/high. Other profiles require explicit operator instruction or an operator-authorized launch contract. Use only after explicit invocation of orchestrate-workers or a relayed invocation in an operator-authorized feature launch.
---

# Orchestrate Workers

**Composition role: lens.** Keep the current task skill or workflow as driver. It decides whether delegation is allowed and retains lifecycle, success criteria, authority, and acceptance. This lens changes decomposition, delegation, context, evidence, and explicitly requested independent-review routing; it grants no authority and never changes the current coordinator's profile.

## Configure Only

If invoked without a resolved task and coherent delegation boundary, confirm provisional configuration, name what the coordinator must resolve, and return without launching. Activation applies to the current resolved task. A later task, or one resolved after provisional configuration, requires a fresh explicit invocation. A relayed invocation in an operator-authorized feature launch satisfies activation; another agent-relayed request does not.

## Terms And Profiles

- **Coordinator:** current task applying this lens; it may use any product-exposed profile and remains planner, integrator, primary reviewer, and acceptance authority.
- **Implementation worker:** selected native leaf subagent or separately operator-requested ordinary implementation task at the worker profile.
- **Independent reviewer:** separate operator-requested native leaf; never a worker.
- **Workstream:** coherent ownership lane. **Assignment:** one bounded worker contract. Names such as `main` and `additional` are assignment labels, not mandatory roles or launches. **Recycle:** stop reuse and create a fresh identity only on a named material boundary.
- **Creation profile:** model and effort selected while creating a new worker or reviewer identity. **Existing-task message:** a follow-up, reset, reuse assignment, correction, or callback that preserves the recipient's settings and omits both `model` and `thinking` fields entirely, including null or presumed-current values; a sender profile belongs in text metadata only when relevant.
- **Worker blocker:** a worker's stop/ask condition for its immediate coordinator; it is not automatically a driver or project blocker. **Task blocker:** a condition the coordinator cannot resolve within granted authority or whose consequence crosses the task boundary and therefore requires the governing driver or project orchestrator.

| Role | Activation | Default route | Model | Effort |
|---|---|---|---|---|
| Implementation worker | When delegated | Native subagent | `gpt-5.6-luna` | `xhigh` |
| Independent reviewer | Disabled unless explicitly operator-requested | Native subagent | `gpt-5.6-sol` | `high` |

Reviewer activation and profile are separate. Only an explicit operator request activates review; profile wording counts, and a launch contract must carry the request. While disabled, do not resolve or validate reviewer controls, identity, or protocol.

Use another enabled-role profile only on explicit operator instruction or an authorized launch contract. The ordinary task route always requires a separate explicit request; the launch contract does not authorize it. Resolve roles independently; one override never changes another role or the coordinator. Preserve coordinator model/effort. Before dispatch, resolve enabled-role controls and provenance internally. Disclose a profile override or any unresolved or unobservable control before dispatch; stop if an exact control cannot be validated. Never substitute, silently change effort, or claim independent readback. Creation profiles apply only at creation; existing-task messages preserve settings under the rule above.

For each actual implementation workstream, resolve model and effort independently in this order: the role default, an explicit general worker override, then an explicit named-workstream override. A missing named field inherits the resolved general field. A named override applies only to matching assignments and never changes the coordinator, another workstream, or any other role. A relayed feature launch must carry the resolved general profile, every explicit named overlay, and their provenance; a direct invocation derives any overrides from explicit operator instructions and otherwise uses the role defaults. This lens resolves the exact profile immediately before creating each actual worker. Labels alone never require decomposition or dispatch. Reuse requires compatibility with that exact resolved profile, and no follow-up or reset mutates an existing identity's settings.

Preserve permissions, approval policy, scope, stop gates, and no-worktree-without-operator-approval. Use only stable native behavior; do not fabricate syntax, controllers, registries, ledgers, daemons, queues, side-channel files, or delivery mechanisms.

## Operating Model

- Keep one visible acceptance boundary at the coordinator. The coordinator reviews integrated work by default. Worker reports are evidence, not acceptance; the same applies to any explicitly requested reviewer verdict.
- Let workers own bounded implementation and implementation-depth verification: governing contracts, full owned diff/artifacts, plausible wrong implementations, proportionate failure/recovery paths, and uncertainty.
- Perform a narrow coordinator gate over integrated state and decision-critical evidence. Reuse current scope-complete worker checks; run only missing, stale, contradicted, or decision-critical checks.
- Keep the task open until every planned lane, launched identity, and required handoff is classified and acceptance finishes. Savings never weaken scope, verification, authority, or review quality.
- Treat readiness or an accepted verdict as evidence, not a new approval gate, when the coordinator already has authority and the required checks and observable dependencies pass; neither grants authority. Preserve actual operator/driver gates, retry and launch limits, scientific or contract validity, and shared ownership, including any required acceptance step.

## Decompose And Route

1. Resolve architecture, scope, user decisions, risks, authorities, stop gates, observable completion, and selected profiles before delegation. Point to durable paths and symbols instead of conversation history.
2. Prefer one coherent worker. Add workers only for non-overlapping ownership lanes; keep sequential assignments over one lane on one compatible worker.
3. Before parallel dispatch, map objective, owned files/components, read/write boundary, inputs, downstream recipient, artifact, verification owner, and integration order. Launch only the dependency-free frontier within concurrency limits.
4. Treat the checkout as shared. Assign one owner for Git state, generated/build artifacts, test databases, ports, formatters, code generation, and other shared state; defer contention. Parallelism never authorizes a worktree.
5. Launch new workers with no parent turns by default and confirm that setting. Treat an inherited-turn fork as exceptional: use only the smallest bounded recent slice for one named load-bearing fact with no durable source that cannot be accurately distilled without material loss; state the fact, reason, and exact slice. Never inherit full parent history. Inherited context is not authority; restate scope, permissions, decisions, and criteria.
6. Keep every worker and reviewer a leaf. The coordinator alone creates agents, aggregates results, and mediates handoffs.

## Dispatch Readiness

Before every dispatch, internally resolve and validate the lane, workstream/assignment, new or reused identity, route, exact model and effort for the dispatched role, provenance, context mode, root work it substitutes for, unique output, downstream decision affected, and non-duplicative rationale. For an implementation worker, apply the per-field default/general/named precedence before this validation. Send the complete worker contract with those facts. Disclose them before dispatch only for a consequential profile override, inherited-context exception, unresolved or unobservable control, degraded supervision or delivery, changed topology/authority/shared-state ownership or conflict, or other decision-bearing variation. For a reviewer, disclose the explicit operator request and exact acceptance target. Do not dispatch with unknown required facts.

## Worker Lifecycle And Continuity

1. Send the Compact Worker Contract and applicable Worker Rules.
2. After native subagent dispatch, continue useful coordinator work and wait through the native result surface. After an explicitly requested ordinary task launch, return immediately and never poll; inspect only on operator status request or missing-delivery report.
3. Route dependencies through the coordinator. Launch a dependent lane only after upstream classification and validation of the smallest required handoff; provisional results satisfy no dependency.
4. Send bounded corrections and compatible successive assignments to the same worker. Correct a bad coordinator contract without forcing a failed retry. Existing-task messages preserve the selected worker profile. Never change the selected worker profile without an explicit operator instruction and a separate authorized settings operation.
5. On blocked/partial/failed work or invalidated assumptions, halt dependents and replan. If an upstream handoff or evidence is urgently invalidated, preserve the original and invalidating records, contain dependent lanes, and report the consequence; unaffected authorized lanes may continue. Correct/stop natively when available; otherwise classify output invalid and redo under a corrected contract. Routine diagnosis, acceptance correction, and an authorized same-purpose repair stay with the coordinator/owner. Escalate a worker blocker to the governing driver only when authority or recovery is exhausted, a contract/scientific decision must change, another task/shared resource/evidence is threatened, or the decision is irreducible. Never replace a stalled/failed worker silently.
6. Classify every worker `complete`, `blocked`, `partial`, or `failed`; reconcile shared state and every planned lane/handoff.
7. Reuse a compatible idle worker only when identity is reachable and role, project, checkout, trust, authority, ownership, route, model, and effort still fit. Profile change is incompatibility. Compaction does not justify recycling.
8. Before reuse, resend the full contract with an assignment-reset overlay: prior assignment/disposition, allowed carry-over facts, invalid assumptions/scope/permissions/decisions/claims, interfaces, success, verification, return format, and stale-conflict reporting. Send it as an existing-task message. A bounded current-assignment correction needs only changed constraints and preserves recipient settings.
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
- **Return route:** include exactly one applicable route below; never copy fields from the other route.
- **Native subagent route:** worker or reviewer returns only to its immediate parent through native collaboration/results; no ordinary task, sibling, higher-orchestrator, or cross-task callback route. Parent delivery failure returns natively.
- **Separately authorized ordinary-task route:** only after a separate explicit operator request. Verify the exact recipient and authorized callback purpose, plus the absence of both `model` and `thinking`; include exact originating coordinator `threadId` and `hostId` when required plus the explicit native `send_message_to_thread` action. Accepted blocker/terminal sends establish delivery; rejection or unavailability remains local delivery failure. Route permission never includes settings changes.
- **Return format:** status and outcome; changed scope; exact tested repository/artifact state; verification commands and results; and material gaps, decisions, or constraints. Include dependency and continuity details only when they affect a decision, reuse, integration, or the next action.

Keep the final report compact but self-contained on every decisive fact. Reference existing accessible evidence for long output or inventories, while retaining inline the result, tested state, evidence-bearing condition, and consequence needed to act. Do not create an artifact solely to shorten the message, impose an arbitrary size cap, or trade away evidence quality. Omit chain-of-thought, builder reasoning, long history, and attempt chronology. Preserve a failure with its condition and evidence when it constrains the next action or prevents repeated work. Return only a genuine blocker/stop or final report.

For the separately authorized ordinary-task callback, keep the message compact: status/outcome, consequence or material caveat, next action or exact decision, and one durable artifact or handoff link. The linked existing record retains the complete decision-bearing evidence and final handoff; compactness never removes required blocker/terminal delivery or its evidence. If terminal callback delivery fails, preserve the payload, stable identity/state, and evidence link there; do not guess a route or retry under a different operation, and do not proceed past a blocked decision. Native result returns still use the complete Return format above.

## Worker Rules

- Recover and cite governing contracts; do not substitute an internally consistent interpretation.
- Inspect the complete owned diff and every non-interchangeable decision-bearing artifact. Report foreign changes without claiming them.
- Sample only interchangeable items with basis/limits. Inspect artifacts, not producer signals, when claims rest on them.
- Run consequence tests against plausible wrong implementations. Reject implementation-derived oracles unless exact shape is the documented contract.
- Trace fail-closed, error, retry, and recovery behavior proportionately. Challenge nonclaims and report uncertainty/divergence.
- Preserve sibling ownership and operator work. Escalate architecture/contract changes, unsafe rewrites, authority/infrastructure gaps, and dependency conflicts.
- Use existing project resource tools and observable status/receipts for authorized waits, acquisition, and safe release; do not invent a manager, queue, daemon, polling loop, or force-unlock path. An explicit priority dependency is exceptional and must name and verify its predecessor; an unrelated idle resource does not satisfy it. Unknown cleanup or ownership fails closed and escalates. Keep frozen source, inputs, intervention, criteria, and protocol unchanged; changing them is new authorized work, and a valid negative is preserved rather than tuned into a rerun.
- Never broaden authority, delegate, or claim success with missing evidence.

## Operator-Requested Independent Review

The coordinator reviews and accepts by default. Only an explicit operator request for this task activates a reviewer. No other signal—including task characteristics, evidence gaps, driver preference, or agent judgment—authorizes review. An unauthorized driver requirement is a stop-and-ask condition only when the next action requires independent review. Complete already-authorized implementation and verification first, then leave a concrete review handoff; do not claim independent acceptance or waive the driver’s review requirement. An acceptance verdict confirms the reviewed artifact and never grants authority or creates another permission round when the coordinator can take the next authorized action. The native reviewer uses the immediate-parent route above and never falls back to a cross-task route.

Do not resolve or validate reviewer route/model/effort, read the reviewer protocol, or create/reuse a reviewer while disabled. When activated, record the operator request and exact acceptance target before dispatch. Reuse one compatible idle reviewer keyed by exact reviewer role, project, checkout, trust, authority, isolation, route, model, and effort. Create a fresh reviewer only when operator-requested review is active and no compatible identity is reachable. New reviewers always receive fresh context with no history exception. Independence comes from separate identity, fresh context, no implementation ownership, and protocol—not model name. The ordinary implementation route never changes reviewer activation or routing.

When the operator activates review, read [references/independent-reviewer-protocol.md](references/independent-reviewer-protocol.md) completely and follow it.

## Operator-Requested Ordinary Implementation Route

Use only on a separate explicit operator request; an operator-authorized feature launch may explicitly forbid it. Resolve the exact originating coordinator `threadId` and `hostId` when required from native status and require the explicit native `send_message_to_thread` action; never invent/store a side-channel route. Verify the exact recipient, authorized callback purpose, and absence of both `model` and `thinking` before an ordinary send; route permission never authorizes an existing-task settings change. Use the resolved worker creation profile and the same decomposition, ownership, dependency, reset, and contract rules. Do not create a worktree without approval.

After launch, return the launch response immediately and do not wait or poll. The task sends only a genuine blocker or final handoff to the exact coordinator through native callback, with no `model` or `thinking` fields. An accepted blocker/terminal send establishes delivery; rejection or unavailability remains local delivery failure. Reuse only for compatible assignments after reset; across tasks require fresh lens invocation and explicit ordinary-route request. Create a new task only on explicit request or recycle trigger.

## Coordinator Depth Budget

- Spend coordinator effort on architecture/risk decisions, dependencies, contract quality, integration, decision-critical evidence, and acceptance.
- Let workers own broad scans, implementation, diagnostics, implementation-depth checks, owned-diff inspection, and task verification.
- Add lanes only when output changes or accelerates a named downstream decision. Do not infer reviewer authorization from task characteristics or evidence gaps.
- Treat worker facts rediscovered by the coordinator as handoff feedback. Report decision-bearing state changes; do not poll or repeat unchanged progress.
