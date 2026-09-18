# Orchestrate Feature — Product Requirements

## Status

Implemented initially under Agents Harness task T-36, hardened under T-38 after the first runtime handoff failure, generalized under T-39, refined under T-51 for named-workstream profiles and review continuity, and clarified under T-53 for the ordinary-owner/native-worker boundary. This document is the product contract for the Codex-only feature-orchestration skill family; it does not authorize a live skill installation or change Codex runtime configuration.

## Problem

Long-lived project discussions accumulate requirements, research interpretation, cross-feature dependencies, and user decisions that should remain available to one stable project-orchestrator task. Long implementation work produces a different kind of context: repository exploration, test output, failed attempts, diffs, and detailed verification evidence. Performing both kinds of work in the same task pollutes project context, while dispatching implementation directly from the project orchestrator to short-lived subagents removes the coherent feature owner that should plan, integrate, review, and accept the work.

The operating model separates three ownership levels: a long-lived project orchestrator preserves program context; one ordinary feature-owner task owns a substantial feature or research lane; and that owner uses and reuses native leaf subagents for bounded implementation, investigation, verification, and explicitly operator-requested independent review.

The first implementation coupled this topology to one fixed role map and named the outer skill `orchestrate-sol-feature`: Sol/high feature owner, Sol/medium implementation workers, and Sol/high independent reviewer. The topology is reusable independently of those defaults. Baking model choices into the entrypoint makes legitimate per-feature profile changes awkward, invites copied skills, and makes a non-Sol feature owner incompatible with the Sol-only inner lens.

## Observed Runtime Failure

The first production use also established that ordinary Codex tasks are peers rather than parent/child processes with automatic result delivery. The feature owner finished correctly in its own task, but the originating project orchestrator received no completion event. The immediate launch contract omitted the orchestrator's exact task identity and an executable callback action; the systemic gap allowed dispatch without either callback or practical active supervision.

T-38 corrected that boundary. Every feature lane must now select native callback by default, practical bounded active waiting, another product-validated delivery mechanism, or explicitly accepted manual supervision. Callback-specific identity and `send_message_to_thread` requirements apply only when callback is selected; every mode preserves sparse actionable-blocker, required-gate, and terminal events and represents observation truthfully.

## Task Messaging Boundary

Model and effort are creation-profile fields for new tasks or native identities. Messages to an existing task preserve its settings and omit both `model` and `thinking` entirely, including null or presumed-current values; a sender profile is text metadata only when relevant. Existing-task settings changes are separate operations requiring explicit operator authorization naming the exact target and requested values. Creation profiles, inherited context, delegated instructions, and callback permission never authorize a settings change.

Native workers and reviewers return only to their immediate parent through native collaboration or result tools by default. They do not message ordinary tasks, siblings, or higher orchestrators. A route exception requires explicit operator authorization naming the sender, recipient, and purpose; route authorization never includes settings changes. The feature owner alone owns the project-orchestrator callback and mediates internal native reports. Before an ordinary existing-task message, verify the recipient, route authority, and absence of both settings fields. If an override is supplied accidentally, report the exact target, supplied fields and values, and observed tool outcome to the parent or operator without unauthorized restoration.

## Product Decision

Make `orchestrate-feature` the only canonical outer entrypoint. It resolves one feature objective, one delivery contract, and an independent role-profile map, then creates or reuses one ordinary feature owner. The no-override behavior is feature owner `gpt-5.6-sol`/medium, implementation worker `gpt-5.6-luna`/xhigh, and feature-owner self-review. Independent review is disabled unless the operator explicitly requests it for the resolved feature; when requested without a profile override, the reviewer defaults to `gpt-5.6-sol`/high.

Create one generic worker helper named `orchestrate-workers`. It treats the current task uniformly as coordinator and owns worker decomposition, contracts, context, continuity, evidence, operator-requested reviewer routing, and worker-result handling for any product-exposed coordinator profile. Its defaults are native Luna/xhigh implementation workers with coordinator self-review; explicit operator requests may select other enabled-role profiles, an independent reviewer, or a separately requested ordinary implementation task when the current task has that creation authority. Do not duplicate the worker protocol in the outer skill.

Remove `orchestrate-sol-feature` from the source and catalog rather than keeping two ambiguous outer entrypoints. Managed scratch-upgrade/prune evidence must show that the old installed asset is removed while the new canonical asset and generic helper are installed.

## Goals

- Preserve the long-lived orchestrator as the home for requirements, priorities, cross-feature coordination, user-owned choices, and program-level disposition.
- Give each substantial feature one coherent ordinary-task owner for detailed planning, implementation, integration, verification, and feature-level acceptance.
- Move bounded implementation-depth work into reusable native leaf subagents without allowing workers or reviewers to delegate.
- Resolve feature-owner and worker model/effort profiles independently; resolve a reviewer profile only after explicit operator activation, preserving Sol/high as the enabled reviewer default.
- Resolve each actual worker per field from role defaults, an explicit general worker override, and an explicit named-workstream override, without turning assignment labels into mandatory roles or launches.
- Treat the active project-orchestrator profile as immutable session state that the skill may validate but never change.
- Launch feature owners and native subagents with fresh context by default; inherited-turn subagent forks remain rare, bounded, named exceptions and full-history forks remain prohibited.
- Reuse compatible feature tasks and subagents without allowing stale scope, authority, assumptions, delivery contracts, profiles, or completion claims to carry silently.
- Preserve executable sparse delivery, bounded supervision, project instructions, sandbox and approval policy, checkout/worktree rules, Git authority, external-write gates, and task-specific workflow drivers.
- Keep model/effort selection and readback claims truthful: exact unsupported profiles stop rather than substitute, and validation is not misreported as independent metadata readback.
- Keep feature-owner/coordinator self-review as the default and never infer separate-review authorization from task size, importance, risk, ambiguity, evidence gaps, cross-worker boundaries, or agent judgment.
- Make the feature owner primarily an active orchestrator: the launch contract delegates coherent execution-depth work to configurable native workers whenever a safe boundary exists, while the owner retains architecture/risk decisions, integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo, acceptance, and terminal reporting.
- Give each shared mutable resource exactly one named writer at a time within already-granted authority; serialize every other writer, including the owner, and record a no-boundary reason for substantial direct owner execution in the in-task plan or worker-dispatch context and existing final handoff.
- Preserve parent-owned messaging: native workers and reviewers use only their immediate native parent route by default, while the feature owner alone uses the explicitly selected project-orchestrator callback and preserves recipient settings on existing-task messages.

## Non-Goals

- Do not create a daemon, queue, scheduler, automation, task registry, context database, status ledger, custom agent configuration, or new task controller.
- Do not infer a role profile from task size, cost, availability, a previous invocation, or another role's override.
- Do not treat `main`, `additional`, or another named workstream as a required worker count, role, or launch.
- Do not change the current project-orchestrator task's model or effort.
- Do not make every feature use a separate task; contained interactive work remains in the current task when a separate owner would add more handoff cost than context protection.
- Do not create feature owners by forking the project-orchestrator task or permit full-history subagent forks.
- Do not make the project orchestrator a duplicate feature-level reviewer or require it to rerun all accepted child verification.
- Do not create, resolve, validate, or load a separate reviewer unless the operator explicitly requests one for the resolved task; a driver requirement without that authorization stops at the review-dependent action, after authorized implementation and verification produce a concrete handoff; it never waives required independent acceptance.
- Do not add routine progress chatter or describe bounded `wait_threads` as a background watcher, durable subscription, or later-notification guarantee.
- Do not let an outer feature launch grant its owner ordinary-task creation. The generic worker helper may use an ordinary implementation task only when the operator directly and explicitly requests that route and the current coordinator already has task-creation authority.
- Do not authorize pushes, pull requests, merges, branch deletion, destructive cleanup, live skill installation, external writes, or worktrees beyond existing user and project authority.
- Do not add a Claude counterpart; ordinary Codex tasks, native subagents, model identifiers, and task-control surfaces are product-specific.

## Users And Invocation

The user is an operator maintaining a long-running Codex project-orchestrator task. The skill is explicit-only. A representative default invocation is:

```text
Use $orchestrate-feature to work on the feature we just defined.
```

The operator may add natural-language role overrides for this feature, for example:

```text
Use $orchestrate-feature for this feature. Feature owner: Terra/high. Workers: Sol/medium. Reviewer: Sol/high.
```

Named workstreams may override individual general worker fields. This explicit invocation resolves a Sol/medium owner, Sol/medium `main` worker, Luna/xhigh `additional` workers, and an operator-requested Astra/medium reviewer without changing any default outside this feature:

```text
Use $orchestrate-feature for this feature. Feature owner: Sol/medium. Workers: Luna/xhigh generally; main workstream: Sol/medium; additional workstreams: Luna/xhigh. Require an Astra/medium reviewer.
```

Codex skills do not expose a typed parameter schema; the skill treats only explicit, unambiguous role-profile instructions in the current invocation or authoritative feature decision as overrides. Invocation authorizes creation or reuse of one resolved feature task. It is not standing authority for later features, unrelated work, model changes to the current task, or broader implementation/external writes.

Before dispatch, classify whether a separate feature owner has material value. The gate passes when the work is expected to be multi-phase, produce substantial implementation or evidence context, contain multiple coherent assignments, progress independently, or when the operator explicitly requests this topology. Otherwise recommend contained work in the current task and return.

## Choosing The Entrypoint

Use the ownership boundary, not task importance, to choose an entrypoint:

| Operator intent | Entrypoint | Ownership result |
| --- | --- | --- |
| Keep the current task as planner, integrator, primary reviewer, and acceptance authority while delegating bounded implementation or verification | `$orchestrate-workers` | The current task remains coordinator; native workers operate beneath it, and a separate reviewer is added only when explicitly requested. |
| Preserve the current project-orchestrator context while another ordinary task owns a substantial feature lifecycle | `$orchestrate-feature` | The current task remains project orchestrator; a separate feature owner applies `orchestrate-workers` internally. |
| Complete a small contained task whose handoff cost would exceed its delegation value | Neither | The current task performs the work directly. |

Direct `orchestrate-workers` use is appropriate when the design is already resolved in the current task and implementation plus fresh review would help without creating another ownership layer. For example, the operator can say: `Use $orchestrate-workers to implement this caching change in the current task. Delegate implementation to Sol/medium and require independent Sol/high review before acceptance.` The current task decomposes the work, sends the compact contract, integrates and checks the result, routes corrections, and alone accepts the change.

Native workers remain the default. An ordinary implementation task is available only when the same direct operator request explicitly asks for that route, for example: `Use $orchestrate-workers and create an ordinary Sol/high implementation task for this migration.` The helper never infers ordinary-task creation from task size or from a relayed feature launch.

It is also appropriate when the current task owns a migration or similarly coherent task with genuinely non-overlapping implementation lanes, such as application changes and independent test-fixture changes. Prefer one coherent worker; add workers only when each owns a distinct output that changes or accelerates a named downstream decision. The current task integrates all lanes and retains one visible acceptance boundary.

Invoking `orchestrate-workers` keeps review with the current coordinator. State `require independent review` when a separate reviewer must occur; reviewer profile wording also counts as an explicit request. No task characteristic or agent judgment activates review. New workers receive fresh context and a compact contract by default, every worker and requested reviewer remains a leaf, and one invocation applies to one resolved task. The skill changes no coordinator profile, permission, Git authority, worktree authority, or external-write authority.

When the operator invokes `$orchestrate-feature`, no separate `$orchestrate-workers` invocation is necessary. The launch contract activates the worker helper in the feature-owner task, grants no ordinary-task-creation authority, and contains no instruction or reference requiring the owner to read or apply `orchestrate-feature`. Both public skills remain explicit-only; intentional outer invocation authorizes the composed owner-and-worker topology without adding a confirmation gate at every layer.

## Topology Invariant

- Only the current project orchestrator applies `orchestrate-feature` for a feature lane.
- The project orchestrator creates or reuses exactly one ordinary feature owner through the host/project-authorized ordinary-task mechanism, never through a native subagent or inherited task fork.
- The feature-owner launch contract is the compiled output of the outer helper. It activates `orchestrate-workers` but never passes `orchestrate-feature` to the owner as an instruction, dependency, or operative provenance reference.
- `orchestrate-workers` always treats its current task as coordinator. It does not need a feature-owner mode and does not own that task's reporting relationship to any ordinary parent.
- The feature owner creates and steers its native workers and optional native feature reviewer. The project orchestrator does not create, steer, or duplicate those identities.
- The feature owner alone integrates native results and reports feature blockers, required gates, and the terminal handoff to the project orchestrator under the outer launch contract.

## Operating Model

```text
Long-lived project orchestrator — current immutable profile
└── Ordinary feature owner — resolved profile; default gpt-5.6-sol / medium
    ├── Reusable native implementation workers — resolved profile; default gpt-5.6-luna / xhigh
    └── Independent native reviewer only when explicitly requested — resolved profile; default gpt-5.6-sol / high
```

### Project orchestrator

The project orchestrator owns priorities, requirements, cross-feature dependencies, shared-resource coordination, user decisions, material scope or architecture changes, task launch/reuse/stop decisions, external landing decisions, and program-level disposition. It preserves its current model and effort. An operator-specified orchestrator profile is a launch precondition to validate, never an instruction for this skill to mutate the current task.

The orchestrator must not directly spawn or steer the feature owner's implementation workers or feature reviewer. This prohibition is scoped to the feature-owner tree and does not define or govern separately authorized work after the terminal feature handoff. The orchestrator retains the exact feature-task identity, resolved role map, notification contract, and parent-owned supervision state, and may resolve ordinary blockers within existing authority by steering the same feature owner.

### Feature owner

The ordinary task at the resolved feature-owner profile is primarily an active orchestrator. Its launch contract activates `orchestrate-workers` to delegate coherent execution-depth work whenever a safe delegation boundary exists; the owner retains architecture/risk decisions, assignment contracts, the feature-lane Git/shared-state writer assignment, integrated-state synthesis, integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo decisions, feature acceptance, terminal reporting, and exactly the external-landing authority granted. It uses the applicable project workflow as driver and `orchestrate-workers` as the worker helper. It neither reads nor applies `orchestrate-feature`. Substantial direct execution is allowed only with a no-boundary reason recorded in the in-task plan or worker-dispatch context and existing final handoff; trivial integration glue, narrow corrections, decision-critical inspection, and work without a coherent delegation boundary remain allowed. Sequential assignments to one compatible worker are valid; parallel workers require genuinely non-overlapping ownership lanes.

The feature owner must not create another ordinary feature task, delegate project-level authority, or treat a worker report as acceptance. It alone owns the project-orchestrator callback, mediates internal native worker and reviewer reports, and preserves recipient settings on existing-task messages. It delivers only the events required by the selected notification mode. A non-Sol feature owner is valid when the product can create and validate its exact profile and the generic worker helper can operate under that coordinator profile.

### Implementation workers

Workers use the independently resolved worker profile as a creation profile and own bounded questions, files, components, tests, or evidence packets under the compact worker contract. They may perform substantial implementation, build, test, diagnostic, and inspection work rather than serving only as code-writing assistants. They receive no parent-turn history by default, cannot delegate, and return only blockers or a final classified report to the feature owner through the immediate native parent route. They do not receive the owner's cross-task callback contract. A bounded inherited-turn slice is exceptional and requires one named load-bearing fact with no durable source that cannot be accurately distilled without material loss, plus the reason and exact inherited slice. Full-history forks remain prohibited.

The outer launch carries the resolved general worker profile plus every explicit named-workstream model/effort overlay and provenance. The feature owner resolves each actual worker immediately before creation, field by field in the order role default, general override, named override. Missing named fields retain the resolved general field. Assignment labels such as `main` and `additional` do not require decomposition or dispatch, and an overlay affects neither another workstream nor the owner or reviewer. An existing compatible identity retains its configured settings; a different resolved assignment profile requires a fresh identity under the existing reuse rules.

Native worker final reports remain compact and self-contained on status/outcome, changed scope, exact tested state, verification results, and material gaps or decisions. Dependency and continuity details appear only when decision-bearing. Long output or inventories may use an existing accessible evidence reference, but decisive facts remain inline; compactness creates no artifact, arbitrary cap, or weaker evidence. Attempt chronology is omitted, while failures retain their conditions and evidence when they constrain the next action or prevent repeated work. Reassignment still requires a full reset, while a bounded correction on the same assignment carries only changed constraints.

### Independent reviewer

The reviewer is a separate native leaf identity at the independently resolved reviewer profile. It is disabled by default and created or reused only after an explicit operator request for the resolved task. Reviewer profile wording itself activates review. Task size, importance, risk, ambiguity, missing oracles, cross-worker boundaries, agent judgment, reviewer availability, or a generic driver preference cannot activate it. A driver requirement without explicit operator authorization stops at the review-dependent action, after authorized implementation and verification produce a concrete handoff; it never waives required independent acceptance. When activated, reviewer independence comes from separate identity, fresh context, no implementation ownership, and the review protocol; changing its profile never permits reuse of an implementation worker as reviewer.

An identity's first review covers the complete target. On correction rounds, the same compatible reviewer may carry demonstrably applicable prior coverage only after the exact reviewed baseline and complete subsequent delta, including uncommitted changes, are established. It inspects affected interfaces, invariants, callers or consumers, unresolved findings, and new verification. Every implementation mutation invalidates the verdict and requires a new verdict for the complete current target that identifies carried and new coverage. Missing baseline or coverage, changed assumptions, or broader consequences require expanded inspection; compaction alone does not force a restart when sufficient evidence survives.

## Role Profile Contract

Resolve this map before every new or reused dispatch:

| Role | Default | Override behavior |
| --- | --- | --- |
| Project orchestrator | Current task profile | Validate an explicit requirement; never mutate |
| Feature owner | `gpt-5.6-sol` / medium | Explicit per-feature model and/or effort override |
| Implementation worker | `gpt-5.6-luna` / xhigh | Explicit general and/or named-workstream model/effort override, resolved per actual assignment |
| Independent reviewer | Disabled; when explicitly requested, `gpt-5.6-sol` / high | Explicit request activates review; optional per-feature model and/or effort override |

An override affects only its named role. Missing owner and enabled-reviewer fields inherit that role's default, not another role's value; worker fields follow the hierarchy below. A reviewer override in the current invocation or an authoritative operator decision explicitly scoped to the resolved feature constitutes reviewer activation; a standing or global reviewer preference does not. Absent activation, no reviewer profile is resolved or validated. Never cascade a feature-owner override to workers or reviewer, never upgrade or downgrade a role silently, and never convert a model nickname into an unsupported identifier. An explicit override does not waive a governing driver or project requirement for a particular role profile; conflicting requirements stop at readiness. Retain the complete map internally and disclose it before dispatch only when an override, unresolved or unobservable control, degraded supervision, changed topology/authority/shared-state ownership or conflict, or other decision-bearing variation could change the launch.

Within the implementation-worker role, resolve model and effort separately in the order role default, explicit general worker override, explicit named-workstream override. A named field overrides only the corresponding general field for matching assignments; all other fields and workstreams retain their prior resolved values. `Main`, `additional`, and similar names are assignment labels rather than new roles. They neither require a worker nor authorize a launch. The outer launch carries the general profile, named overlays, and provenance; the feature owner matches them to actual workstreams and resolves each creation profile before dispatch.

Use only model identifiers, effort values, routes, and context controls exposed by the current native product. If an explicit current-orchestrator requirement cannot be observed, stop rather than guess; without an explicit requirement, report the observability limitation and preserve the task. If another exact requested profile cannot be set or validated, stop and report the missing capability. A successful creation or spawn request is profile provenance; if the product lacks independent post-creation readback, state that limitation rather than inventing it.

## Launch Readiness Contract

Before creating or resuming a feature owner, resolve and communicate every applicable field:

- Objective, observable outcome, durable authorities, user decisions, assumptions, unknowns, and non-goals.
- Project identity, repository path, intended base/ref or working-tree state, and checkout/worktree policy.
- Owned scope, interfaces, dependencies, sibling boundaries, active writers, and shared mutable resources.
- Local edit, validation, commit, push, pull-request, merge, lifecycle, external-write, and delegation authority exactly as granted.
- Acceptance criteria, required artifacts, verification, decision-bearing evidence, and plausible wrong implementations when material.
- Stop/ask gates for user-owned choices, architecture/contract changes, unsafe expansion, missing infrastructure/authority, dependency invalidation, and shared-resource conflicts.
- Complete resolved role-profile map with default/override provenance, general worker profile, named-workstream overlays, and current-orchestrator precondition result.
- Notification mode, route-specific mechanism/target/action, mandatory and extended events, message shape, parent supervision state, and truthful fallback.
- Fresh ordinary feature task and fresh native subagents by default; any exceptional inherited-turn worker slice names its fact, reason, and exact extent.

Use existing durable authority when sufficient. For multi-phase or high-consequence work without an adequate source, create or update the smallest appropriate project-owned task, PRD, or specification only under the current driver and authority. Do not create an orchestration ledger.

## New Versus Reused Ownership

Reuse a feature owner only when its exact identity is known, it is idle, and the feature, project, repository, checkout/worktree, branch, trust boundary, authority envelope, lifecycle role, feature-owner profile, acceptance boundary, and selected worker-helper contract remain compatible. Native inspection establishes identity, reachability, and state; the orchestrator's accepted launch record establishes profile provenance when independent readback is unavailable. A title or unsupported recollection is never sufficient.

Before reuse, revalidate the complete role map and notification contract. Never send a reset or concurrent assignment to a running feature owner. Send an idle compatible owner a full reset that classifies the prior assignment, states allowed carry-over facts, invalidates stale scope/authority/assumptions/decisions/evidence/completion claims, and restates the objective, interfaces, success, verification, stop gates, notification mode, reporting events, context policy, role profiles, and return format. Preserve the configured feature-owner profile by omitting per-message overrides; if it differs, create a new owner rather than attempting to mutate the task.

The feature owner applies the same rules to workers and reviewer. Reuse requires compatible role, project, checkout, trust, authority, ownership, model, effort, and route. A profile change is an incompatibility, not an instruction to override an existing identity. Keep implementation and reviewer identities separate.

Create or recycle only on the existing named material boundaries: different feature/project/repository/checkout, changed trust or permission boundary, incompatible role profile, unrecoverable superseded contract, repeated acceptance-critical miss after correction, hidden unresolved state, unreachable identity, or explicit operator request. Never replace a stalled, failed, or blocked identity silently.

## Context Boundary

Create a new feature owner with fresh context through the host/project-authorized ordinary-task creation mechanism, never through a native subagent or inherited task fork. Distill load-bearing chat-only decisions and point to durable project paths. Conversation history is context, never authority. An operator-requested task fork is a different topology and requires an explicit boundary decision.

Create new native workers and reviewers with no parent turns by default. Inherit only the smallest bounded recent slice for one named load-bearing fact with no durable source that cannot be accurately distilled without material loss; state the fact, reason, and extent before dispatch. Independent reviewers never receive inherited history. Full parent-history inheritance is prohibited.

## Worker Helper

`orchestrate-workers` is the canonical generic worker helper. It always treats its current task as coordinator and does not vary its worker lifecycle based on whether that coordinator is a feature owner. A feature-owner launch contract activates it for the resolved feature, passes the resolved general worker profile, every named-workstream overlay and provenance, and reviewer activation as `disabled` or `operator-requested`, and, only when review is requested, carries the exact operator-request provenance, acceptance target, and separate reviewer profile/provenance. The launch grants no ordinary-task-creation authority. The helper owns worker/reviewer decomposition, per-assignment profile resolution, contracts, context, continuity, evidence, optional-review routing, and immediate-parent returns; the outer contract alone owns the feature owner's callback and terminal reporting to the project orchestrator.

If the operator invokes both outer feature ownership and an ordinary implementation-task route for the same unresolved feature, stop and ask for one owner topology. `goal-prompt` remains the owner of durable autonomous goal handoffs; an existing goal artifact may be durable feature authority but does not replace native task/profile/delivery resolution.

## Project And Git Boundaries

Resolve the target through native project/task surfaces and inspect project instructions before selecting a checkout or app-managed worktree. Honor project requirements to use an existing checkout unless the operator explicitly authorizes a worktree. Otherwise follow user/project policy and then native defaults. Never invent a starting branch/ref.

Invocation inherits only authority already granted for edits, validation, commits, pushes, pull requests, merges, branch operations, external writes, task creation, and delegation. It never broadens those permissions.

Allow one active durable writer per checkout by default, counting the project orchestrator and feature owners. Concurrent writers require disjoint paths plus one named owner for Git state and other shared mutable resources, or explicit separate-worktree authority. If active-writer state cannot be recovered, serialize or ask.

## Reporting And Supervision

Before dispatch, select one delivery mode internally and preserve only required phase gates, genuine actionable blockers, and terminal `complete`, `blocked`, `partial`, or `failed` handoffs. Recoverable implementation friction, routine progress, unchanged status, and repeated messages are not delivery events.

- Callback, the default: the feature owner alone uses native `send_message_to_thread` to the exact originating task; accepted terminal send establishes delivery. Before sending, verify the sender, exact recipient, authorized callback purpose, and absence of both `model` and `thinking` fields.
- Practical bounded active waiting: native attention state carries required gates/blockers and terminal state carries the final handoff while the orchestrator remains attached; observation establishes delivery and timeout does not.
- Product-validated replacement: the notification contract names mechanism and target and preserves the same event floor.
- Explicitly accepted manual supervision: the same events remain in native attention/terminal state for later inspection; delivery is unobserved until inspection and no automatic-return claim is allowed.

The orchestrator retains the feature identity, host when required, and latest wait cursor. It uses bounded `wait_threads` only as immediate race coverage or active supervision while attached, never as a durable watcher, and does not poll repeatedly. It may add named phase/risk/budget/decision gates but cannot remove actionable-blocker and terminal delivery, weaken selected-mode semantics, or introduce routine reporting.

The final handoff includes outcome, exact repository/branch/commit/checkout state, changed artifacts, commands/checks, criteria coverage, material decisions/divergence, blockers, residual uncertainty, downstream action, continuity state, and the resolved role map actually used. The project orchestrator verifies only the smallest program boundary required for disposition.

## Migration And Release Boundary

T-39 renamed the canonical outer source, catalog ID, install target, metadata, docs, and tests from `orchestrate-sol-feature` to `orchestrate-feature`, kept `orchestrate-workers` as the Codex-only generic helper, and removed the redundant `sol-luna-orchestration` source and catalog entry. Those migration requirements are historical invariants; T-53 does not recreate the retired assets or their former installation baseline.

T-53 scratch validation starts from the current canonical `main`, installs the current branch into an isolated Codex home, proves that both canonical orchestration skills and their managed metadata match source, and proves that an unmanaged sentinel remains untouched. The earlier deleted-asset behavior remains covered by the installer engine's existing prune-history test rather than by fabricating a retired-asset fixture from current `main`.

T-39 stopped before merge and live installation. For T-53, the operator separately authorizes commit, push, pull request, squash merge after conceptual and check readiness, local and remote feature-branch deletion, and live project installation from updated `main`.

## Success Measures

- One memorable `orchestrate-feature` invocation produces the intended ownership topology with explicit, independently resolved role profiles.
- No-override behavior preserves Sol/medium feature ownership, Luna/xhigh workers, feature-owner self-review, and no separate reviewer dispatch.
- Non-Sol feature owners can use the generic worker helper truthfully without copied protocol or a Sol-only precondition.
- Exact profile requests, validation, and readback limitations are reported truthfully; no override cascades or mutates the current orchestrator.
- Mixed general and named-workstream overrides resolve independently per field and do not create workstreams by implication.
- Native worker handoffs remain compact without losing decisive tested-state, verification, gap, failure-condition, or decision evidence.
- Correction rounds preserve independent complete-target verdicts while reusing only recoverable and demonstrably applicable prior coverage.
- Feature owners, workers, and reviewers reuse only compatible identities and receive complete resets.
- Every feature lane preserves executable sparse delivery, bounded supervision, fresh context, leaf topology, authority, and acceptance boundaries.
- The old outer installed asset has a tested managed prune path and no ambiguous source/catalog twin remains.

## Risks And Mitigations

- Generic-name overreach: keep one fixed topology and explicit role map; do not turn the skill into a general task controller.
- Profile drift: retain complete defaults/overrides internally, disclose consequential variation, validate exact profiles, prevent cascading, and key reuse by role profile.
- Redundant compatibility: keep the generic protocol and its Luna/xhigh defaults in `orchestrate-workers` without retaining a duplicate preset.
- Reviewer overuse or weakening: require explicit operator activation, avoid reviewer-only resolution/loading while disabled, and preserve separate identity, fresh context, and the acceptance protocol after activation.
- Handoff loss: preserve T-38 route-specific delivery and bounded-supervision tests unchanged.
- Context contamination: prohibit feature-task forks and full-history subagent forks; keep inherited turns exceptional and named.
- Migration residue: remove the old outer catalog/source and verify managed prune behavior in scratch state.
- Authority drift: restate exact permissions at launch and keep model selection separate from operational authority.
