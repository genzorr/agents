---
name: orchestrate-feature
description: Dispatch or reuse one ordinary profiled feature-owner task from a long-lived project orchestrator and configure reusable native profiled workers plus an independently profiled reviewer through orchestrate-workers. Defaults are Sol/high owner, Sol/medium workers, and Sol/high reviewer; explicit role-local overrides are allowed for one feature. Use only after the operator explicitly invokes orchestrate-feature or requests this exact topology. Invocation authorizes one resolved feature lane; it never mutates the current orchestrator or broadens project, Git, branch, worktree, external-write, or live-install authority.
---

# Orchestrate Feature

**Composition role: helper.** Keep the project-orchestrator protocol or workflow as driver. It retains program lifecycle, authority, priorities, and completion ownership; this helper owns bounded launch readiness, role-profile and delivery resolution, feature-task dispatch/reuse, and handoff routing. Stop if the driver forbids task creation, delegation, or the lifecycle change.

## Terms

- **Project orchestrator:** current long-lived task preserving program context and decisions.
- **Feature owner:** ordinary task at the resolved owner profile that owns one feature's detailed lifecycle and feature-level acceptance.
- **Role profile:** exact route when applicable, model identifier, effort, and default/override provenance for one role.
- **Role map:** immutable current-orchestrator observation plus independently resolved owner, worker, and reviewer profiles.
- **Launch contract:** authoritative context, scope, state, authority, role map, success, verification, stop, and notification packet sent to the feature owner.
- **Notification contract:** selected delivery mode/target/action, mandatory and extended events, message shape, and truthful fallback; callback identity/action fields apply only to callback.
- **Supervision state:** ready feature identity, host when required, and latest wait cursor retained after creation; do not fabricate it in the initial child packet.
- **Bounded active wait:** current `wait_threads` operations while the orchestrator remains attached, never a persistent watcher, background subscription, or future-wakeup guarantee.
- **Fork:** inherited task or parent-turn context; feature-task forks are outside this topology, bounded subagent inheritance is exceptional, and full-history forks are prohibited.
- **Reset:** complete reassignment overlay before compatible reuse. **Recycle:** select a fresh identity only on a named material boundary or explicit operator request.

## Activate And Resolve Readiness

Use this invocation for one resolved feature. Another feature requires a fresh invocation and role-map resolution.

1. Confirm a separate owner has material value because work is multi-phase, context-heavy, has multiple coherent assignments, can progress independently, or the operator explicitly requests this topology. Otherwise recommend contained work and return.
2. Confirm the current task is the project orchestrator, not a feature owner or child created by this topology. Refuse nested ordinary feature-task creation.
3. Inspect the native current-profile/status surface when exposed. Preserve the current model and effort. Treat an operator-specified orchestrator profile only as a precondition: mismatch stops, and unobservable explicit requirements stop rather than becoming a mutation request or guess.
4. Resolve objective, durable authority, start state, scope/shared ownership, operational authority, success, verification, stop gates, fresh-context mode, notification contract, and complete role map. Inspect the governing driver, project instructions, saved-project metadata, repository, checkout/worktree policy, and active durable writers.
5. Recover locally answerable gaps and reuse durable authority. Create or update the smallest project-owned task/specification only when needed and allowed; never create an orchestration ledger.
6. Require callback, practical bounded active waiting, another product-validated mechanism/target, or explicitly accepted manual supervision before every new or reused dispatch.
7. Return without dispatch for an unresolved user-owned/difficult-to-reverse choice, conflicting governing profile requirement, or unavailable exact route/model/effort/context/delivery capability.
8. If outer feature ownership and an ordinary implementation-task route are both requested for the same unresolved feature, stop and ask the operator to choose one owner topology.

## Resolve Role Profiles

Use this no-override map:

| Role | Default |
|---|---|
| Project orchestrator | Current task model / current effort; immutable |
| Feature owner | `gpt-5.6-sol` / `high` |
| Implementation worker | Native `gpt-5.6-sol` / `medium` |
| Independent reviewer | Native `gpt-5.6-sol` / `high` |

Accept only explicit, unambiguous overrides tied to this feature or a durable user decision. Resolve each role independently: an owner override changes only owner creation, a worker override changes only the inner worker profile, and a reviewer override changes only the independent reviewer profile. An omitted model or effort inherits its own role's default, never another role's override. Do not cascade, infer from task size/cost/availability/history, silently upgrade/downgrade, or convert a nickname into an unsupported identifier. An override never waives a governing role-profile requirement; conflict stops.

Echo the complete map with `default` or `operator override` provenance before dispatch. Feature-detect exact route, model, effort, and context controls. Stop when a selected value cannot be set or validated; never substitute. Treat accepted creation/spawn as profile provenance, not independent post-creation readback, and disclose a missing readback surface.

## Select New Or Reused Ownership

Require one active durable writer per checkout by default, counting orchestrator and feature owners. Concurrent writers require disjoint paths and one named owner for Git state, generated artifacts, formatters, build outputs, test databases, ports, devices, and other shared resources, or explicit worktree authority. If writer state is unresolved, serialize or ask.

Reuse only an exact known idle feature identity with compatible feature, project, repository/checkout/branch, trust, authority, lifecycle role, owner model/effort, inner-lens contract, and acceptance boundary. Native inspection proves identity/reachability/state; the accepted launch record supplies profile provenance when readback is absent. A title or recollection is insufficient. A different owner profile requires a new task, never a follow-up override.

Before reuse, inspect state and revalidate the complete role map and delivery contract. Never send a reset or concurrent assignment to a running owner. Send an idle compatible owner a reset with prior disposition, allowed carry-over facts, invalidated scope/authority/decisions/assumptions/evidence/claims, and complete new objective, interfaces, success, verification, stop, notification, role-map, context, and return contracts. Old origin identity, callback action, wait cursor, event set, or profiles never carry implicitly. Never replace a running, stalled, failed, or blocked identity silently.

Recycle only for a different feature/project/repository/checkout, trust/permission change, incompatible role profile, unrecoverable superseded contract, repeated acceptance-critical miss after correction, hidden unresolved state, unreachable identity, or explicit operator request. Classify prior disposition and lost continuity.

## Launch A New Feature Owner

1. Resolve callback identity/action only under callback; otherwise resolve the selected delivery mechanism and target without fabricating an origin route.
2. Use native `create_thread` with fresh context, never a native subagent spawn or `fork_thread`. An operator-requested task fork is a different topology and requires an explicit boundary decision.
3. Select the exact resolved owner model and effort and resolve saved project/environment first. Personal OS-managed repositories use the existing checkout unless the operator explicitly authorizes a worktree. Other projects follow user and project policy, then the native default when no stricter rule exists. The inner lens's no-worktree-without-operator-approval rule governs an additional worktree created after launch, not a task environment already assigned under this compliant outer policy. Use the exact intended existing branch/ref or explicitly intended working-tree state; never invent either.
4. Send only the complete launch contract to a concise project-and-feature title. Distill chat-only facts and point to durable paths; never inherit or paste parent history. Conversation history is context, not authority.
5. Distinguish pending from ready identity and request validation from readback. Retain ready identity, host, and latest wait cursor; perform one bounded `wait_threads` wait/snapshot for immediate completion, failure, or attention. Timeout leaves `launched, awaiting handoff` and supports no later-notification claim.
6. Report identity, objective, requested owner profile, worker/reviewer profiles, environment/context, delivery route, wait state, fallback, and every readback limitation.

## Feature Owner Launch Contract

Include every applicable field whose absence can change behavior or authority:

- **Objective and durable references:** outcome; task/specification/decision/source/instruction paths.
- **Decisions, assumptions, unknowns, and non-goals:** classification and provenance.
- **Project and starting state:** project, repository, checkout/worktree policy, branch/ref, exact working tree.
- **Scope and shared state:** ownership, interfaces, dependencies, sibling boundaries, writers, Git/generated/build/test/port/device ownership.
- **Authority:** edit, validation, commit, push, PR, merge, branch/lifecycle, external-write, task-creation, and delegation authority exactly as granted; never broaden worktree, Git, live-install, or external-write authority.
- **Driver and lens:** project workflow remains driver; explicitly invoke `orchestrate-workers` under this operator-authorized launch.
- **Resolved role map and inner route:** immutable orchestrator observation/requirement plus exact owner, worker, and reviewer profiles/provenance; native leaf workers only; forbid the optional ordinary implementation-task route.
- **Success, artifacts, verification, and evidence:** observable criteria, commands, decision-bearing artifacts, plausible wrong implementations, and failure/recovery paths where material.
- **Stop/ask and reporting gates:** user-owned decisions, architecture/contract change, unsafe expansion, missing authority/infrastructure, dependency invalidation, shared-resource conflict, and required phase gates.
- **Notification and return contract:** selected target/action, mandatory blocker/gate/terminal events, message shape, extended gates, and fallback. Under callback include exact originating `threadId`/`hostId` when required plus native `send_message_to_thread`; accepted terminal send establishes delivery. Under active waiting use native attention for gates/blockers and terminal result for final handoff while attached; observation establishes delivery, timeout does not. A replacement names its validated mechanism/target. Manual supervision remains unobserved until later inspection.
- **Final handoff:** `complete`, `blocked`, `partial`, or `failed`; outcome; exact repository/branch/commit/checkout/tested state; artifacts; checks; criteria; decisions/divergence; blockers/uncertainty; downstream action; continuity; actual role map and readback limits.

State that the owner owns integration, primary review, and feature acceptance; may create only native leaf workers and the separately escalated native reviewer; cannot delegate authority or create an ordinary task; and treats worker reports as evidence, not acceptance.

## Constrain Inner Delegation

Require the feature owner to apply `orchestrate-workers` while its project workflow or launch contract remains driver. The relayed invocation in this operator-authorized launch satisfies explicit activation for this feature. Pass the resolved worker and reviewer profiles independently. The generic lens owns decomposition, contracts, fresh context, continuity, evidence, escalation, and acceptance; do not duplicate its protocol here.

The project orchestrator must not spawn or duplicate the feature owner's implementation workers or reviewer directly. All feature-lane child dispatch, correction, reuse, and aggregation stays with the feature owner.

Create native workers with no parent turns by default. An inherited-turn fork is exceptional: use only the smallest bounded recent slice for one named load-bearing fact with no durable source that cannot be accurately distilled without material loss, and state the fact, reason, and exact slice. Independent reviewers receive fresh context with no exception. Full parent-history inheritance is prohibited. Keep every worker and reviewer a leaf and keep their identities separate.

The owner remains planner, integrator, primary reviewer, and acceptance authority. It must not create another feature task, use the optional ordinary implementation-task route, delegate authority, or treat worker/reviewer profile names as proof of acceptance or independence.

## Supervise And Complete

Expose only required phase gates, genuine user-owned/architectural/authority/infrastructure/dependency/shared-resource blockers, or final classified handoffs. Every event identifies the assignment and feature task when exposed and carries the smallest self-contained packet. Routine progress, recoverable friction, unchanged status, and repeated messages are not events.

- **Callback, default:** call native `send_message_to_thread` to the exact origin. Accepted terminal send establishes delivery; rejection/unavailability is local delivery failure.
- **Practical bounded active waiting:** while attached through bounded `wait_threads`, expose gates/blockers through attention and final handoff through terminal result. Observation establishes delivery; timeout does not.
- **Product-validated replacement:** name mechanism/target and preserve the same actionable-blocker, required-gate, and terminal floor.
- **Explicit manual supervision:** expose the same events in attention/terminal state for later inspection. It is a degradation with no automatic-delivery claim; delivery remains unobserved until inspection.

Use bounded waits only as race coverage or active supervision while attached, never a watcher/subscription. Do not poll repeatedly. If callback fails, select active waiting or a validated replacement when practical; otherwise stop or require explicit manual-supervision acceptance. The orchestrator may add named gates but cannot remove blocker/terminal delivery, weaken selected-mode semantics, or introduce routine reporting.

At handoff verify only the smallest program boundary: exact integrated state, criterion coverage, decision-bearing evidence, risks, continuity, downstream action, and actual role map. Do not routinely rerun accepted scope-complete child checks. Keep the lane accounted for until terminal classification and preserve existing external-landing authority.
