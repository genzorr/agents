---
name: orchestrate-feature
description: Dispatch or reuse one profiled feature-owner task from a long-lived project orchestrator, with reusable native workers and an independent reviewer only when explicitly operator-requested. Defaults are Sol/medium owner, Luna/xhigh workers, feature-owner self-review, and requested reviewer Sol/high. Allows explicit role-local overrides. Use only after the operator invokes orchestrate-feature or requests this topology. Invocation authorizes one feature lane; it never mutates the orchestrator or broadens project, Git, branch, worktree, external-write, or live-install authority.
---

# Orchestrate Feature

**Composition role: helper.** Keep the project-orchestrator protocol or workflow as driver. It retains program lifecycle, authority, priorities, and completion ownership; this helper owns bounded launch readiness, role-profile and delivery resolution, feature-task dispatch/reuse, and handoff routing. Stop if the driver forbids task creation, delegation, or the lifecycle change.

## Terms

- **Project orchestrator:** current long-lived task preserving program context and decisions.
- **Feature owner:** ordinary task at the resolved owner profile that owns one feature's detailed lifecycle and feature-level acceptance.
- **Role profile:** exact route when applicable, model identifier, effort, and default/override provenance for one role.
- **Role map:** immutable current-orchestrator observation plus independently resolved owner and worker profiles, reviewer activation, and the reviewer profile only when operator-requested.
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
| Feature owner | `gpt-5.6-sol` / `medium` |
| Implementation worker | Native `gpt-5.6-luna` / `xhigh` |
| Independent reviewer | Disabled; when explicitly requested, native `gpt-5.6-sol` / `high` |

Accept only explicit, unambiguous overrides tied to this feature. Owner and worker overrides may also come from a durable operator decision governing their roles. Reviewer activation is operator-only: only the current operator invocation or an authoritative operator decision explicitly scoped to this resolved feature can activate it; standing or global reviewer preferences never activate review. Resolve roles independently: owner and worker overrides change only their profiles; reviewer profile wording in an explicitly operator-authorized activation source activates review and changes only that profile. An omitted field inherits its enabled role's default, never another override. Never infer reviewer activation; a driver requirement without operator authorization stops at required review. Do not cascade, silently change effort, or convert a nickname into an unsupported identifier. An override never waives a governing profile requirement; conflict stops.

Keep map/provenance internal; disclose pre-dispatch only consequential profile overrides, inherited-context exceptions, unresolved/unobservable controls, degraded supervision, changed topology/authority/shared-state conflicts, or decision-bearing variation. Validate exact controls; never substitute or validate reviewer controls while disabled. Accepted creation is profile provenance, not independent readback.

## Select New Or Reused Ownership

Require one active durable writer per checkout by default, counting orchestrator and feature owners. Concurrent writers require disjoint paths and one named owner for Git state, generated artifacts, formatters, build outputs, test databases, ports, devices, and other shared resources, or explicit worktree authority. If writer state is unresolved, serialize or ask.

Reuse only an exact known idle feature identity with compatible feature, project, repository/checkout/branch, trust, authority, lifecycle role, owner model/effort, inner-lens contract, and acceptance boundary. Native inspection proves identity/reachability/state; the accepted launch record supplies profile provenance when readback is absent. A title or recollection is insufficient. A different owner profile requires a new task, never a follow-up override.

Before reuse, inspect state and revalidate the complete role map and delivery contract. Never send a reset or concurrent assignment to a running owner. Send an idle compatible owner a reset with prior disposition, allowed carry-over facts, invalidated scope/authority/decisions/assumptions/evidence/claims, and complete new objective, interfaces, success, verification, stop, notification, role-map, context, and return contracts. Old origin identity, callback action, wait cursor, event set, or profiles never carry implicitly. Never replace a running, stalled, failed, or blocked identity silently.

Recycle only for a different feature/project/repository/checkout, trust/permission change, incompatible role profile, unrecoverable superseded contract, repeated acceptance-critical miss after correction, hidden unresolved state, unreachable identity, or explicit operator request. Classify prior disposition and lost continuity.

## Launch A New Feature Owner

1. Resolve callback identity/action only under callback; otherwise resolve selected delivery mechanism and target without fabricating an origin route.
2. Use native `create_thread` with fresh context, never a native subagent spawn or `fork_thread`. An operator-requested task fork is a different topology and requires an explicit boundary decision.
3. Select the exact resolved owner model and effort and resolve saved project/environment first. Personal OS-managed repositories use the existing checkout unless the operator explicitly authorizes a worktree. Other projects follow user and project policy, then the native default when no stricter rule exists. The inner lens's no-worktree-without-operator-approval rule governs an additional worktree created after launch, not a task environment already assigned under this compliant outer policy. Use exact intended existing branch/ref or explicitly intended working-tree state; never invent either.
4. Send only the complete launch contract to a project-and-feature title. Distill chat-only facts and point to durable paths; never inherit or paste parent history. Conversation history is context, not authority.
5. Distinguish pending from ready identity and request validation from readback. Retain ready identity, host, and latest wait cursor; perform one bounded `wait_threads` wait/snapshot for immediate completion, failure, or attention. Timeout leaves `launched, awaiting handoff` and supports no later-notification claim.
6. Post-launch, report one compact truthful receipt: identity, objective, role map, environment/context, delivery route, wait state, fallback, and readback limitations.

## Feature Owner Launch Contract

Include every applicable field whose absence can change behavior or authority:

- **Objective and durable references:** outcome; task/specification/decision/source/instruction paths.
- **Decisions, assumptions, unknowns, and non-goals:** classification and provenance.
- **Project and starting state:** project, repository, checkout/worktree policy, branch/ref, exact working tree.
- **Scope and shared state:** ownership, interfaces, dependencies, sibling boundaries, writers, Git/generated/build/test/port/device ownership.
- **Authority:** edit, validation, commit, push, PR, merge, branch/lifecycle, external-write, task-creation, and delegation authority exactly as granted; never broaden worktree, Git, live-install, or external-write authority.
- **Driver and lens:** project workflow remains driver; explicitly invoke `orchestrate-workers` under this operator-authorized launch.
- **Resolved role map, reviewer request, and inner route:** complete role map; reviewer activation recorded as `disabled` or `operator-requested`; when requested, exact operator-request provenance, acceptance target, and separate reviewer profile/provenance; native leaf workers only; forbid the optional ordinary implementation-task route.
- **Success, artifacts, verification, and evidence:** observable criteria, commands, decision-bearing artifacts, plausible wrong implementations, and failure/recovery paths where material.
- **Stop/ask and reporting gates:** user-owned decisions, architecture/contract change, unsafe expansion, missing authority/infrastructure, dependency invalidation, shared-resource conflict, and required phase gates.
- **Notification and return contract:** selected target/action, mandatory blocker/gate/terminal events, message shape, extended gates, and fallback. Under callback include exact originating `threadId`/`hostId` when required plus native `send_message_to_thread`; accepted terminal send establishes delivery. Under active waiting use native attention for gates/blockers and terminal result for final handoff while attached; observation establishes delivery, timeout does not. A replacement names its validated mechanism/target. Manual supervision remains unobserved until later inspection. The feature owner alone owns this callback; native children return only to it through native collaboration/results and receive no callback; existing-task messages omit both `model` and `thinking` fields.
- **Final handoff:** `complete`, `blocked`, `partial`, or `failed`; outcome; exact repository/branch/commit/checkout/tested state; artifacts; checks; criteria; decisions/divergence; blockers/uncertainty; downstream action; continuity; actual role map and readback limits.

State that the owner owns integration, default self-review, and feature acceptance; may create only native leaf workers and an operator-requested reviewer; cannot delegate authority or create an ordinary task; and treats reports as evidence. It must use `orchestrate-workers` to delegate coherent execution-depth work—broad investigation, implementation, implementation-depth diagnostics, builds, focused tests, and owned-diff inspection—to configurable native workers when a safe delegation boundary exists. Workers may perform substantial implementation, build, test, diagnostic, and inspection work; they are not limited to code-writing. It retains architecture/risk decisions, assignment contracts, feature-lane Git/shared-state writer assignment, synthesis and integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo, acceptance, reporting; external-landing authority stays exactly as granted.

It names exactly one writer—owner or worker—per shared mutable resource within granted authority; it serializes all others, including itself, and evaluates evidence. It records substantial direct work and its no-boundary reason in its in-task plan or worker-dispatch context and existing final handoff `decisions/divergence`; it creates no new file, ledger, side channel, or notification event. It may perform trivial glue, narrow corrections, decision-critical inspection, or work without a coherent delegation boundary.

## Constrain Inner Delegation

Require the owner to apply `orchestrate-workers` under its project workflow or launch contract. This relayed invocation activates the lens for the feature. Pass the worker profile and reviewer activation as `disabled` or `operator-requested`; only when requested, also pass the exact operator-request provenance, acceptance target, and reviewer profile/provenance. The lens owns decomposition, contracts, context, continuity, evidence, review routing, and acceptance; do not duplicate it.

The project orchestrator must not spawn or duplicate the feature owner's implementation workers or reviewer directly. All feature-lane child dispatch, correction, reuse, and aggregation stays with the feature owner.

Create native workers with no parent turns by default. An inherited-turn fork is exceptional: use only the smallest bounded recent slice for one named load-bearing fact with no durable source that cannot be accurately distilled without material loss, and state the fact, reason, and exact slice. Independent reviewers receive fresh context with no exception. Full parent-history inheritance is prohibited. Keep every worker and reviewer a leaf and keep their identities separate.

Owner must primarily orchestrate through synthesis, integration, integrated-diff inspection, evidence judgment, and retain-or-redo/acceptance. It cannot create another feature task, use the ordinary task route, delegate authority, or treat profile names as proof; it must delegate execution-depth work at safe boundaries. Sequential compatible-worker assignments remain valid; parallel workers require non-overlapping lanes.

## Supervise And Complete

Expose only required phase gates, genuine user-owned/architectural/authority/infrastructure/dependency/shared-resource blockers, or final classified handoffs. Every event identifies the assignment and feature task when exposed and carries the smallest self-contained packet. Routine progress, recoverable friction, unchanged status, and repeated messages are not events.

- **Callback, default:** only the feature owner calls native `send_message_to_thread` to the exact origin. Verify the exact recipient and authorized callback purpose and omit both `model` and `thinking` before sending. Accepted terminal send establishes delivery; rejection/unavailability is local delivery failure.
- **Practical bounded active waiting:** while attached through bounded `wait_threads`, expose gates/blockers through attention and final handoff through terminal result. Observation establishes delivery; timeout does not.
- **Product-validated replacement:** name mechanism/target and preserve the same actionable-blocker, required-gate, and terminal floor.
- **Explicit manual supervision:** expose the same events in attention/terminal state for later inspection. It is a degradation with no automatic-delivery claim; delivery remains unobserved until inspection.

Use bounded waits only as race coverage or active supervision while attached, never a watcher/subscription. Do not poll repeatedly. If callback fails, select active waiting or a validated replacement when practical; otherwise stop or require explicit manual-supervision acceptance. The orchestrator may add named gates but cannot remove blocker/terminal delivery, weaken selected-mode semantics, or introduce routine reporting.

At handoff verify only the smallest program boundary: exact integrated state, criterion coverage, decision-bearing evidence, risks, continuity, downstream action, and actual role map. Do not routinely rerun accepted scope-complete child checks. Keep the lane accounted for until terminal classification and preserve existing external-landing authority.
