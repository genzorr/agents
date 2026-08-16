---
name: sol-luna-orchestration
description: Configure Sol-led planning, delegation, and review with reusable Luna/xhigh subagents by default, parallel Luna workstreams when ownership can be split safely, reusable Sol/high review only for a named acceptance-critical target where independent judgment has material value, and an ordinary Luna task/thread only when the operator explicitly requests one. Use only when the operator explicitly invokes sol-luna-orchestration or explicitly asks for Sol–Luna orchestration; invocation configures the current task driver and does not itself launch work or authorize unrelated work.
---

# Sol–Luna Orchestration

**Composition role: lens.** Keep the current task skill or workflow as the driver. That driver decides whether delegation is allowed and retains task lifecycle and success criteria. This lens changes decomposition, delegation, and review; it grants no additional authority.

## Configure Only

If invoked without a resolved task and coherent delegation boundary, confirm provisional configuration, name what Sol must resolve before delegation, and return without launching Luna. Activation applies only to the current resolved task. A later task, or a task resolved after provisional configuration, requires a fresh explicit invocation.

## Terms

- **Task:** the general unit of work owned by the driver, independent of project tracking.
- **Sol session:** the current Codex task/thread running Sol and hosting orchestration.
- **Worker:** a Luna subagent, or an ordinary Luna task/thread on the operator-requested route.
- **Reviewer:** the independent Sol subagent used only by the escalation rule below; never an implementation worker.
- **Workstream:** a coherent ownership lane within a task.
- **Assignment:** one bounded contract sent to a worker; a compatible worker may receive sequential assignments.
- **Recycle:** stop reusing an identity and create a fresh one. Task, workstream, assignment, review, compaction, and elapsed-time boundaries are not recycle triggers by themselves.

## Preconditions And Defaults

- Require the originating session to already run Sol. Never change its model or reasoning effort; if it is not Sol, ask the operator to continue from Sol or abandon this lens.
- Preserve permissions, approval policy, scope, stop gates, and the no-worktree-without-operator-approval rule.

| Lane | Default route | Model | Effort |
|---|---|---|---|
| Implementation | Native Luna subagent | Product-exposed Luna identifier (`gpt-5.6-luna`) | xhigh |
| Operator-requested implementation task/thread | Ordinary Codex task/thread | Product-exposed Luna identifier (`gpt-5.6-luna`) | xhigh |
| Escalated independent review | Native Sol subagent | Product-exposed Sol identifier (`gpt-5.6-sol`) | high |

Use another model, effort, or route only when the operator explicitly requests it. Before dispatch, state what the product actually applies. If the product cannot set or confirm the required route, model, effort, or context boundary, report the missing capability and stop; never substitute silently.

Use only stable native product behavior. Do not fabricate syntax, controllers, registries, ledgers, daemons, queues, side-channel files, or delivery mechanisms.

## Operating Model

- Sol remains planner, decision-maker, coordinator, integrator, primary reviewer, and acceptance authority. Keep one visible acceptance boundary.
- Luna owns bounded implementation and implementation-depth verification. It recovers governing contracts, inspects its full owned diff and decision-bearing evidence, tests plausible wrong implementations, traces proportionate failure and recovery paths, and reports uncertainty.
- Main Sol performs a narrow independent gate over the integrated state and decision-critical evidence. Treat Luna's successful, current, scope-complete checks as evidence; do not rerun them routinely. Execute only checks that are missing, stale after integration, contradicted, or needed to resolve a decision-critical question.
- Luna's report is evidence, not acceptance. Sol accepts only after inspecting the integrated repository state, diff, and verification evidence.
- Dispatch is not completion. Keep the task open until every planned lane, launched worker, and required handoff is classified and Sol finishes acceptance.
- Token or wall-clock savings must not weaken scope, verification, authority boundaries, or review quality.

## Decompose And Route

1. Resolve architecture, scope, user-owned decisions, risks, authoritative contracts, stop gates, and observable completion before delegation. Point to durable paths and exact symbols instead of pasting conversation history.
2. Prefer one coherent Luna worker. Add workers only for coherent, non-overlapping ownership lanes; each writer needs distinct durable write ownership. Keep a sequential dependency chain over one ownership lane with one reused worker.
3. Before parallel dispatch, define a compact map for each lane: objective, owned files/components, read/write boundary, required inputs, downstream recipient, expected artifact, verification responsibility, and integration order. Launch only the dependency-free frontier within the product concurrency limit; keep deferred lanes visible until dispatch, explicit replan, or cancellation.
4. Treat the checkout as shared. Assign one owner for Git state, generated artifacts, build outputs, test databases, ports, formatters, code generation, and other shared mutable state; defer contending operations. Each concurrent worker verifies its owned surface. Afterward, the designated state owner may run serialized shared-state commands, and Sol adjudicates the integrated diff and verification evidence. Parallelism never authorizes a worktree.
5. Launch new Luna workers without parent-chat history by default. Confirm the no-parent-history setting and use the Compact Luna Worker Contract plus durable references as the context boundary. Inherit only the smallest bounded recent slice when a named load-bearing fact has no durable source and cannot be summarized without material loss; state the fact, reason, and exact inherited slice before dispatch. Never inherit the full parent conversation. Inherited history is context, not authority; restate scope, permissions, decisions, and completion criteria in the contract.
6. Keep every worker and reviewer a leaf. Sol alone creates agents, aggregates results, and mediates handoffs.

## Dispatch Preamble

Before every dispatch, state the lane identity, workstream and assignment, whether the identity is new or reused, route, model and effort in force, and context mode. For a reviewer, also state the three-part escalation rationale required below. Do not dispatch when any required fact is unknown.

## Worker Lifecycle And Continuity

1. Send the Compact Luna Worker Contract and make the applicable Luna Worker Rules part of it by reference when readable or by inlining only the applicable rules.
2. After subagent dispatch, continue useful Sol work and then wait through the native result surface. After an operator-requested ordinary task/thread launch, return immediately and never poll; check it once only when the operator asks for status or reports missing delivery.
3. Route every dependency through Sol. Dispatch a dependent lane only after the upstream assignment is classified and Sol validates the smallest required handoff. A provisional or mid-run result never satisfies a dependency.
4. Send bounded corrections and compatible successive assignments to the same worker. If Sol's contract was wrong, correct it without forcing a failed retry. If Luna/xhigh no longer fits the required judgment or risk handling, stop and ask the operator; never upgrade Luna work to Sol automatically.
5. If a worker is blocked, partial, failed, or invalidated by changed assumptions, halt dependents and replan. Use native correction/stop controls when available; otherwise let it finish, classify the output as invalid for integration, and redo only under a corrected contract. Never replace a stalled or failed worker silently.
6. Classify every worker as complete, blocked, partial, or failed. Reconcile shared state and account for every planned lane and required handoff; none may disappear during aggregation or compaction.
7. Reuse a compatible idle worker when its identity remains reachable and the project, checkout, trust boundary, authority envelope, role, ownership, model, and effort still fit. Compaction is expected and does not itself justify recycling.
8. Before a new assignment to a reused worker, resend the complete contract with an assignment-reset overlay: prior assignment and disposition, facts allowed to carry over, and assumptions, scope, permissions, decisions, or completion claims that must not carry over. Restate interfaces, success criteria, verification, and return format. Require the worker to report stale or conflicting inherited assumptions before acting. A bounded correction within the current assignment needs only the changed constraint.
9. Recycle only for a material repository/checkout/trust/authority/permission change; incompatible model or effort; an uncorrected superseded contract; a decision-critical constraint that cannot be restored after compaction; a repeated acceptance-critical miss, stale assumption, or overbuilt direction after correction; hidden unresolved prior state; unreachable identity; or an explicit operator request. Report lost continuity and the prior disposition before replacement.
10. Do not recycle for task granularity, a fixed assignment count, token budget, elapsed time, routine correction, delayed handoff, or a compatible new operator decision. An additional independent owner adds a lane; it does not replace a healthy owner. Keep implementation and reviewer identities separate.

## Compact Luna Worker Contract

Send only fields that apply:

- **Objective:** concrete bounded outcome.
- **Durable references:** governing task, specification, source, and instruction paths.
- **Scope and ownership:** owned files/components/questions, non-goals, read/write limits, sibling boundaries.
- **Interfaces:** signatures, schemas, commands, and behavior that must remain compatible.
- **Authority:** local write, validation, commit, push, lifecycle, and external-write permissions exactly as granted; delegation permission is always none.
- **Context and continuity:** new/reused identity, assignment/workstream, authoritative checkpoint, carry-over facts, and invalidated prior authority or claims.
- **Dependencies and handoffs:** required inputs, downstream owner, expected artifact/fact, delivery condition, order, and Sol as recipient.
- **Success criteria:** observable completion and required artifacts.
- **Verification:** task-specific contracts, checks, expected evidence, plausible wrong implementations, and failure/recovery paths; apply Luna Worker Rules for depth.
- **Reviewed behavior-spine proof, only when the driver requires it:** independent oracle, semantics-preserving refactor remains green, plausible defect turns red, and detector ledger covers removed/weakened tests.
- **Stop/ask gates:** user-owned choices, architecture or contract change, unsafe expansion, missing authority or infrastructure, dependency failure, or material ambiguity.
- **Return route:** parent Sol session for a subagent, or exact originating Sol session ID for an ordinary task/thread.
- **Return format:** status (`complete`, `blocked`, `partial`, `failed`); outcome; changed files/commit; commands run; exact checkout state tested; paths and criteria covered; material judgment calls or `none`; blockers; uncertainty; dependency handoffs; continuity state (`resumable`, `ended`, `unable to continue`); and, when applicable, a concise decision-bearing evidence inspection summary with scope, depth, observations, limitations, and divergence.

Omit builder reasoning, hidden chain-of-thought, long history, and failed-attempt narration. Send only a blocker/stop escalation or final report through the selected route.

## Luna Worker Rules

- Recover and cite governing contracts before implementation; do not substitute an internally consistent interpretation.
- Inspect the entire final diff for owned paths and each non-interchangeable decision-bearing artifact. During concurrency, report foreign changes to Sol; do not treat them as owned verification.
- Sample only genuinely interchangeable items; state the basis and limitations. Inspect artifacts themselves rather than producer success signals, metadata, or contract checks when the claim rests on those artifacts.
- Run consequence tests that distinguish plausible wrong implementations. Reject implementation-derived oracles unless exact source shape is the documented contract.
- Trace fail-closed, error, retry, and recovery behavior in proportion to the failure surface.
- Challenge implementation and evidence against task nonclaims; report residual uncertainty and divergence from the expected evidence set.
- Preserve sibling ownership and unrelated operator work. Escalate architecture/contract changes, unsafe rewrites, missing authority, dependency conflict, or materially different interpretations.
- Never broaden authority, delegate, or claim success with missing evidence.

## Escalated Independent Sol Review

Main Sol is the default reviewer. A Sol reviewer is required when the operator or governing driver explicitly requires one. Otherwise escalate only for a named acceptance-critical target when independence has material expected value after main Sol's review. At least one concrete condition must apply:

- Evidence supports conflicting plausible interpretations.
- Consequential behavior lacks a named reliable deterministic oracle, leaving a specific domain or architecture judgment open.
- Main Sol materially designed or revised the disputed surface and can name a concrete anchoring concern.
- A cross-worker boundary depends on judgment not covered by completed checks.

Generic confidence, task importance, a risk label, Luna completion, multiple workers, a public interface, or reviewer availability does not qualify. Before dispatch, state: (1) the exact review target, (2) why independence adds value beyond main Sol's review, and (3) how possible verdicts would change acceptance. If any part is missing, do not dispatch.

Reuse one compatible idle Sol reviewer. Create a fresh Sol/high reviewer only when escalation is required and no compatible identity is reachable. New reviewers receive fresh context with no bounded-history exception. The ordinary Luna task/thread route never changes the reviewer route.

When escalation fires, read [references/sol-reviewer-protocol.md](references/sol-reviewer-protocol.md) completely before dispatch and follow it.

## Operator-Requested Thread Route

1. Obtain the originating Sol session ID from the native identity/status surface; never invent it or store it in a side-channel file.
2. State that the operator requested the ordinary Luna task/thread route and report its model/effort before launch.
3. Apply the same decomposition, ownership, dependency, and worker-contract rules. Include the exact originating Sol ID as return route. Do not create a worktree without approval.
4. After launch, satisfy only checkpoints already required by the driver, return the launch response immediately, and do not wait or poll. The Luna task/thread sends only a blocker or final handoff through the native continuation mechanism.
5. Reuse the task/thread for compatible assignments after a reset. Across tasks, require a fresh lens invocation and another explicit request for the ordinary route. Create a new task/thread only on an explicit request or recycle trigger.

Use this response shape for each launched thread:

```text
Launched Luna task/thread <thread-id> for <bounded objective>. It will implement, validate, and report back to this Sol task for review.
```

## Sol Depth Budget

- Spend Sol effort on planning, architecture and risk decisions, dependency design, worker contract quality, integration, decision-critical evidence, and acceptance.
- Let Luna own broad routine scans, line-by-line implementation, local diagnostics, implementation-depth verification, owned-diff inspection, and task checks.
- Add parallel scouts or workers only when their output can change or accelerate a named downstream decision.
- Do not infer oracle independence from a green suite. When a reviewed behavior spine applies and is practical, use isolated scratch state to show a semantics-preserving refactor stays green and a plausible defect turns it red.
- Treat a basic implementation or evidence fact rediscovered by Sol as handoff feedback: correct the current workstream and carry the lesson into later worker contracts. Propose durable skill/checklist changes only under normal authority.
- Report state changes that matter; do not poll or repeat unchanged progress.
