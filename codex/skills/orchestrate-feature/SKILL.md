---
name: orchestrate-feature
description: Dispatch or reuse one ordinary feature-owner task from a long-lived project orchestrator, relaying the profiles under which that owner uses orchestrate-workers for native leaf execution and review. Defaults are Sol/medium owner, Luna/xhigh workers, feature-owner self-review, and requested reviewer Sol/high. Allows explicit role-local overrides. Use only after the operator invokes orchestrate-feature or requests this topology. Invocation authorizes one feature lane; it never mutates the orchestrator or broadens project, Git, branch, worktree, external-write, or live-install authority.
---

# Orchestrate Feature

**Composition role: helper.** Keep the project-orchestrator protocol or workflow as driver. It retains program lifecycle, authority, priorities, and completion ownership; this helper owns bounded launch readiness, role-profile and delivery resolution, feature-task dispatch/reuse, outer supervision, and handoff routing. Stop if the driver forbids task creation, delegation, or the lifecycle change.

## Topology Invariant

- Only the current project orchestrator applies `orchestrate-feature` for a feature lane.
- Create or reuse exactly one ordinary feature owner through the host/project-authorized ordinary-task mechanism; never use a native subagent or inherited task fork for the feature owner.
- The feature-owner launch packet is compiled output. It activates `orchestrate-workers` but never instructs, passes, or refers the owner to `orchestrate-feature`.
- The worker helper always treats the feature owner as its current coordinator. The feature owner receives no ordinary-task-creation authority.
- The outer helper owns owner creation/reuse, role/profile compilation, callback and supervision, and terminal project handoff; native worker/reviewer decomposition and returns remain with `orchestrate-workers`.

## Terms

- **Project orchestrator:** current long-lived task preserving program context and decisions.
- **Feature owner:** ordinary task at the resolved owner profile that owns one feature's detailed lifecycle and feature-level acceptance.
- **Role profile:** exact route when applicable, model identifier, effort, and default/override provenance for one role.
- **Role map:** immutable current-orchestrator observation plus independently resolved owner and worker profiles, reviewer activation, and the reviewer profile only when operator-requested.
- **Named-workstream override:** explicit model and/or effort for one operator-named worker assignment label; `main`, `additional`, and similar labels describe assignments and never require a role or launch by themselves.
- **Launch contract:** authoritative context, scope, state, authority, role map, success, verification, stop, and notification packet sent to the feature owner.
- **Notification contract:** selected delivery mode/target/action, mandatory and extended events, message shape, and truthful fallback; callback identity/action fields apply only to callback.
- **Supervision state:** ready feature identity, host when required, and latest wait cursor retained after creation; do not fabricate it in the initial child packet.
- **Bounded active wait:** current `wait_threads` operations while the orchestrator remains attached, never a persistent watcher, background subscription, or future-wakeup guarantee.
- **Fork:** inherited task or parent-turn context; feature-task forks are outside this topology, bounded subagent inheritance is exceptional, and full-history forks are prohibited.
- **Reset:** complete reassignment overlay before compatible reuse. **Recycle:** select a fresh identity only on a named material boundary or explicit operator request.
- **Feature blocker:** a condition the feature owner cannot resolve within granted authority or whose consequence crosses the feature boundary and therefore needs the project orchestrator.

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

Accept only explicit, unambiguous overrides tied to this feature. Owner and worker overrides may also come from a durable operator decision governing their roles. Reviewer activation is operator-only: only the current operator invocation or an authoritative operator decision explicitly scoped to this resolved feature can activate it; standing or global reviewer preferences never activate review. Resolve roles independently: owner and worker overrides change only their profiles; reviewer profile wording in an explicitly operator-authorized activation source activates review and changes only that profile. For owner and enabled reviewer profiles, an omitted field inherits its enabled role's default, never another override; worker fields follow the general-to-named hierarchy below. Never infer reviewer activation; a driver requirement without operator authorization stops at required review. Do not cascade, silently change effort, or convert a nickname into an unsupported identifier. An override never waives a governing profile requirement; conflict stops.

Resolve worker model and effort independently in this order: role defaults, then an explicit general worker override, then an explicit override for the named workstream. Each field inherits separately, so a workstream-only model retains the resolved general effort and a workstream-only effort retains the resolved general model. A named-workstream override changes only matching assignments; it does not change the owner, another workstream, or any disabled role. Resolve and retain the general worker profile plus every explicit named-workstream profile/provenance before launch. These labels are routing inputs rather than a required decomposition: the feature owner may create only the actual assignments justified by the work.

Keep map/provenance internal; disclose pre-dispatch only consequential profile overrides, inherited-context exceptions, unresolved/unobservable controls, degraded supervision, changed topology/authority/shared-state conflicts, or decision-bearing variation. Validate exact controls; never substitute or validate reviewer controls while disabled. Accepted creation is profile provenance, not independent readback.

## Select New Or Reused Ownership

Require one active durable writer per checkout by default, counting orchestrator and feature owners. Concurrent writers require disjoint paths and one named owner for Git state, generated artifacts, formatters, build outputs, test databases, ports, devices, and other shared resources, or explicit worktree authority. If writer state is unresolved, serialize or ask.

Reuse only an exact known idle feature identity with compatible feature, project, repository/checkout/branch, trust, authority, lifecycle role, owner model/effort, worker-helper contract, and acceptance boundary. Native inspection proves identity/reachability/state; the accepted launch record supplies profile provenance when readback is absent. A title or recollection is insufficient. A different owner profile requires a new task, never a follow-up override.

Before reuse, inspect state and revalidate the complete role map and delivery contract. Never send a reset or concurrent assignment to a running owner. Send an idle compatible owner a reset with prior disposition, allowed carry-over facts, invalidated scope/authority/decisions/assumptions/evidence/claims, and complete new objective, interfaces, success, verification, stop, notification, role-map, context, and return contracts. Old origin identity, callback action, wait cursor, event set, or profiles never carry implicitly. Never replace a running, stalled, failed, or blocked identity silently.

Recycle only for a different feature/project/repository/checkout, trust/permission change, incompatible role profile, unrecoverable superseded contract, repeated acceptance-critical miss after correction, hidden unresolved state, unreachable identity, or explicit operator request. Classify prior disposition and lost continuity.

## Launch A New Feature Owner

1. Resolve callback identity/action only under callback; otherwise resolve selected delivery mechanism and target without fabricating an origin route.
2. Use the host/project-authorized ordinary-task creation mechanism with fresh context, never a native subagent spawn or inherited task fork. An operator-requested task fork is a different topology and requires an explicit boundary decision.
3. Select the exact resolved owner model and effort and resolve saved project/environment first. Honor project requirements to use the existing checkout unless the operator explicitly authorizes a worktree. Otherwise follow user and project policy, then the native default when no stricter rule exists. The worker helper's no-worktree-without-operator-approval rule governs an additional worktree created after launch, not a task environment already assigned under this compliant outer policy. Use exact intended existing branch/ref or explicitly intended working-tree state; never invent either.
4. Send only the complete launch contract to a project-and-feature title. Distill chat-only facts and point to durable paths; never inherit or paste parent history. Conversation history is context, not authority.
5. Distinguish pending from ready identity and request validation from readback. Retain ready identity, host, and latest wait cursor; perform only host-required creation/progress confirmation unless bounded active waiting was selected. Never imply persistent monitoring. A timeout or unobserved state leaves `launched, awaiting handoff` and supports no later-notification claim.
6. Post-launch, report one compact truthful receipt: identity, objective, role map, environment/context, delivery route, wait state, fallback, and readback limitations.

## Feature Owner Launch Contract

Include every applicable field whose absence can change behavior or authority:

- **Objective and durable references:** outcome; task/specification/decision/source/instruction paths.
- **Decisions, assumptions, unknowns, and non-goals:** classification and provenance.
- **Project and starting state:** project, repository, checkout/worktree policy, branch/ref, exact working tree.
- **Scope and shared state:** ownership, interfaces, dependencies, sibling boundaries, writers, Git/generated/build/test/port/device ownership.
- **Authority:** edit, validation, commit, push, PR, merge, branch/lifecycle, external-write, task-creation, and delegation authority exactly as granted; never broaden worktree, Git, live-install, or external-write authority.
- **Driver and worker helper:** project workflow remains driver; activate `orchestrate-workers` under this operator-authorized launch.
- **Resolved role map, reviewer request, and worker-helper route:** complete role map; reviewer activation recorded as `disabled` or `operator-requested`; when requested, exact operator-request provenance, acceptance target, and separate reviewer profile/provenance; native leaf workers only; the feature owner receives no ordinary-task-creation authority and the optional ordinary implementation-task route is forbidden.
- **Worker profile resolution:** resolved general worker model/effort plus every explicit named-workstream overlay and provenance; require the owner to match actual workstreams and resolve each worker per field immediately before creation.
- **Success, artifacts, verification, and evidence:** observable criteria, commands, decision-bearing artifacts, plausible wrong implementations, and failure/recovery paths where material.
- **Stop/ask and reporting gates:** user-owned decisions, architecture/contract change, unsafe expansion, missing authority/infrastructure, dependency invalidation, shared-resource conflict, and required phase gates.
- **Notification and return contract:** selected target/action, mandatory blocker/gate/terminal events, message shape, extended gates, and fallback. Under callback include exact originating `threadId`/`hostId` when required plus native `send_message_to_thread`; accepted terminal send establishes delivery. Under active waiting use native attention for gates/blockers and terminal result for final handoff while attached; observation establishes delivery, timeout does not. A replacement names its validated mechanism/target. Manual supervision remains unobserved until later inspection. The feature owner alone owns this callback; native children return only to it through native collaboration/results and receive no callback; existing-task messages omit both `model` and `thinking` fields.
- **Final handoff:** `complete`, `blocked`, `partial`, or `failed`; outcome; exact repository/branch/commit/checkout/tested state; artifacts; checks; criteria; decisions/divergence; blockers/uncertainty; downstream action; continuity; actual role map and readback limits.

State that the owner owns integration, default self-review, and feature acceptance; may create only native leaf workers and an operator-requested reviewer; cannot delegate authority or create an ordinary task; and treats reports as evidence. It must use `orchestrate-workers` to delegate coherent execution-depth work—broad investigation, implementation, implementation-depth diagnostics, builds, focused tests, and owned-diff inspection—to configurable native workers when a safe delegation boundary exists. Workers may perform substantial implementation, build, test, diagnostic, and inspection work; they are not limited to code-writing. It retains architecture/risk decisions, assignment contracts, feature-lane Git/shared-state writer assignment, synthesis and integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo, acceptance, reporting; external-landing authority stays exactly as granted.

It names exactly one writer—owner or worker—per shared mutable resource within granted authority; it serializes all others, including itself, and evaluates evidence. It records substantial direct work and its no-boundary reason in its in-task plan or worker-dispatch context and existing final handoff `decisions/divergence`; it creates no new file, ledger, side channel, or notification event. It may perform trivial glue, narrow corrections, decision-critical inspection, or work without a coherent delegation boundary.

## Compose Worker Helper

The launch contract activates `orchestrate-workers` under the feature owner's project workflow. Pass the resolved general worker profile, every explicit named-workstream overlay and provenance, and reviewer activation as `disabled` or `operator-requested`; only when requested, pass the exact operator-request provenance, acceptance target, and reviewer profile/provenance. The contract grants no ordinary-task-creation authority.

`orchestrate-workers` owns native worker/reviewer decomposition, contracts, context, continuity, evidence, review routing, and immediate-parent returns. The feature owner remains that helper's coordinator; the outer helper alone owns the project-orchestrator callback, supervision, blocker escalation, and terminal handoff. Do not duplicate the worker helper's lifecycle or reviewer protocol here.

The project orchestrator must not spawn or steer the feature owner's native workers or reviewer directly. All feature-lane child dispatch, correction, reuse, aggregation, and acceptance stay at the feature-owner coordinator boundary.

## Supervise And Complete

Expose only required phase gates, genuine user-owned/architectural/authority/infrastructure/dependency/shared-resource blockers, or final classified handoffs. Every event identifies the assignment and feature task when exposed and carries the smallest self-contained packet. Routine progress, recoverable friction, unchanged status, and repeated messages are not events.

Resolve at the owning boundary first. The feature owner handles routine work within the launch contract's retry, scope, and validation authority. Escalate a feature blocker only when that authority or recovery is exhausted, a user/contract/scientific decision must change, another task or shared resource/evidence is threatened, or no authorized interpretation remains. If handed-off evidence is urgently invalidated, stop dependent consumers, preserve the original and invalidating records, and report the consequence promptly; unaffected authorized work may continue. A valid negative is a result to preserve, not permission to tune or rerun; a frozen source, inputs, intervention, criteria, or protocol remain unchanged, and changing them is new authorized work.

Keep the callback compact and the durable handoff complete. A callback normally contains assignment/status and outcome, consequence or material caveat, the next action or exact decision, and one durable task/readout/artifact link. Put the full decision-bearing evidence—commands, hashes, test inventories, receipts, acceptance history, limitations, and artifact locations—in the existing handoff or linked record rather than requiring its inventory inline. This message shape does not reduce mandatory blocker/terminal delivery or evidence requirements. If terminal callback delivery fails, preserve the callback payload, stable identity/state, and evidence link in that record; do not guess a route or retry under a different operation, and do not proceed past a blocked decision.

Readiness, an accepted verdict on the reviewed artifact, and normal authorized resource wait/acquisition/release are not another approval or ACK gate when the existing authority, checks, and observable dependencies cover the next action; proceed without another GO/readiness callback, and never treat these signals as granting authority. Preserve actual user/driver gates, retry and launch limits, scientific validity, shared ownership, and any required acceptance step. Use existing project resource tools and their observable status/receipts for waits, acquisition, and safe release. An explicit priority dependency is exceptional: name and verify the predecessor; a quiet resource or unrelated idle state does not satisfy it. Unknown cleanup or ownership fails closed and escalates without force-unlocking or bypassing the manager.

- **Callback, default:** only the feature owner calls native `send_message_to_thread` to the exact origin. Verify the exact recipient and authorized callback purpose and omit both `model` and `thinking` before sending. Accepted terminal send establishes delivery; rejection/unavailability is local delivery failure.
- **Practical bounded active waiting:** while attached through bounded `wait_threads`, expose gates/blockers through attention and final handoff through terminal result. Observation establishes delivery; timeout does not.
- **Product-validated replacement:** name mechanism/target and preserve the same actionable-blocker, required-gate, and terminal floor.
- **Explicit manual supervision:** expose the same events in attention/terminal state for later inspection. It is a degradation with no automatic-delivery claim; delivery remains unobserved until inspection.

Use bounded waits only as race coverage or active supervision while attached, never a watcher/subscription. Do not poll repeatedly. If callback fails, select active waiting or a validated replacement when practical; otherwise stop or require explicit manual-supervision acceptance. The orchestrator may add named gates but cannot remove blocker/terminal delivery, weaken selected-mode semantics, or introduce routine reporting.

At handoff the project orchestrator reviews only the smallest integration boundary and downstream consequence: exact integrated state, criterion coverage, decision-bearing evidence, risks, continuity, downstream action, and actual role map. It does not revisit every already-accepted internal fix or request raw evidence inventories, but it retains result interpretation, lifecycle/accountability, lane accounting, and program disposition. Do not routinely rerun accepted scope-complete child checks. Keep the lane accounted for until terminal classification and preserve existing external-landing authority.
