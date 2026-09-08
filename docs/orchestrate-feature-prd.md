# Orchestrate Feature — Product Requirements

## Status

Implemented initially under Agents Harness task T-36, hardened under T-38 after the first runtime handoff failure, and generalized under T-39. This document is the product contract for the Codex-only feature-orchestration skill family; it does not authorize a live skill installation or change Codex runtime configuration.

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

Create one generic inner lens named `orchestrate-workers`. It owns worker decomposition, contracts, context, continuity, evidence, operator-requested reviewer routing, and acceptance rules for any product-exposed coordinator profile. Its defaults are Luna/xhigh implementation workers with coordinator self-review; explicit operator requests may select other enabled-role profiles or an independent reviewer. Do not duplicate the inner protocol in the outer skill.

Remove `orchestrate-sol-feature` from the source and catalog rather than keeping two ambiguous outer entrypoints. Managed scratch-upgrade/prune evidence must show that the old installed asset is removed while the new canonical asset and generic lens are installed.

## Goals

- Preserve the long-lived orchestrator as the home for requirements, priorities, cross-feature coordination, user-owned choices, and program-level disposition.
- Give each substantial feature one coherent ordinary-task owner for detailed planning, implementation, integration, verification, and feature-level acceptance.
- Move bounded implementation-depth work into reusable native leaf subagents without allowing workers or reviewers to delegate.
- Resolve feature-owner and worker model/effort profiles independently; resolve a reviewer profile only after explicit operator activation, preserving Sol/high as the enabled reviewer default.
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
- Do not change the current project-orchestrator task's model or effort.
- Do not make every feature use a separate task; contained interactive work remains in the current task when a separate owner would add more handoff cost than context protection.
- Do not create feature owners by forking the project-orchestrator task or permit full-history subagent forks.
- Do not make the project orchestrator a duplicate feature-level reviewer or require it to rerun all accepted child verification.
- Do not create, resolve, validate, or load a separate reviewer unless the operator explicitly requests one for the resolved task; a driver requirement without that authorization stops at the review-dependent action, after authorized implementation and verification produce a concrete handoff; it never waives required independent acceptance.
- Do not add routine progress chatter or describe bounded `wait_threads` as a background watcher, durable subscription, or later-notification guarantee.
- Do not permit feature owners, workers, or reviewers to create nested ordinary tasks except the generic lens's separately operator-requested ordinary implementation route; `orchestrate-feature` explicitly forbids that route inside its feature owner.
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

It is also appropriate when the current task owns a migration or similarly coherent task with genuinely non-overlapping implementation lanes, such as application changes and independent test-fixture changes. Prefer one coherent worker; add workers only when each owns a distinct output that changes or accelerates a named downstream decision. The current task integrates all lanes and retains one visible acceptance boundary.

Invoking `orchestrate-workers` keeps review with the current coordinator. State `require independent review` when a separate reviewer must occur; reviewer profile wording also counts as an explicit request. No task characteristic or agent judgment activates review. New workers receive fresh context and a compact contract by default, every worker and requested reviewer remains a leaf, and one invocation applies to one resolved task. The skill changes no coordinator profile, permission, Git authority, worktree authority, or external-write authority.

When the operator invokes `$orchestrate-feature`, no separate `$orchestrate-workers` invocation is necessary. The operator-authorized feature launch explicitly activates the inner lens in the feature-owner task and forbids its optional ordinary implementation-task route. Both public skills remain explicit-only; intentional outer invocation authorizes the composed owner-and-worker topology without adding a confirmation gate at every layer.

## Operating Model

```text
Long-lived project orchestrator — current immutable profile
└── Ordinary feature owner — resolved profile; default gpt-5.6-sol / medium
    ├── Reusable native implementation workers — resolved profile; default gpt-5.6-luna / xhigh
    └── Independent native reviewer only when explicitly requested — resolved profile; default gpt-5.6-sol / high
```

### Project orchestrator

The project orchestrator owns priorities, requirements, cross-feature dependencies, shared-resource coordination, user decisions, material scope or architecture changes, task launch/reuse/stop decisions, external landing decisions, and program-level disposition. It preserves its current model and effort. An operator-specified orchestrator profile is a launch precondition to validate, never an instruction for this skill to mutate the current task.

The orchestrator must not directly spawn the feature's implementation workers or reviewer. It retains the exact feature-task identity, resolved role map, notification contract, and parent-owned wait state, and may resolve ordinary blockers within existing authority by steering the same feature owner.

### Feature owner

The ordinary task at the resolved feature-owner profile is primarily an active orchestrator. Its launch contract requires `orchestrate-workers` to delegate coherent execution-depth work whenever a safe delegation boundary exists; the owner retains architecture/risk decisions, assignment contracts, the feature-lane Git/shared-state writer assignment, integrated-state synthesis, integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo decisions, feature acceptance, terminal reporting, and exactly the external-landing authority granted. It uses the applicable project workflow as driver and `orchestrate-workers` as the delegation and review lens. Substantial direct execution is allowed only with a no-boundary reason recorded in the in-task plan or worker-dispatch context and existing final handoff; trivial integration glue, narrow corrections, decision-critical inspection, and work without a coherent delegation boundary remain allowed. Sequential assignments to one compatible worker are valid; parallel workers require genuinely non-overlapping ownership lanes.

The feature owner must not create another ordinary feature task, delegate project-level authority, or treat a worker report as acceptance. It alone owns the project-orchestrator callback, mediates internal native worker and reviewer reports, and preserves recipient settings on existing-task messages. It delivers only the events required by the selected notification mode. A non-Sol feature owner is valid when the product can create and validate its exact profile and the generic inner lens can operate under that coordinator profile.

### Implementation workers

Workers use the independently resolved worker profile as a creation profile and own bounded questions, files, components, tests, or evidence packets under the compact worker contract. They may perform substantial implementation, build, test, diagnostic, and inspection work rather than serving only as code-writing assistants. They receive no parent-turn history by default, cannot delegate, and return only blockers or a final classified report to the feature owner through the immediate native parent route. They do not receive the owner's cross-task callback contract. A bounded inherited-turn slice is exceptional and requires one named load-bearing fact with no durable source that cannot be accurately distilled without material loss, plus the reason and exact inherited slice. Full-history forks remain prohibited.

### Independent reviewer

The reviewer is a separate native leaf identity at the independently resolved reviewer profile. It is disabled by default and created or reused only after an explicit operator request for the resolved task. Reviewer profile wording itself activates review. Task size, importance, risk, ambiguity, missing oracles, cross-worker boundaries, agent judgment, reviewer availability, or a generic driver preference cannot activate it. A driver requirement without explicit operator authorization stops at the review-dependent action, after authorized implementation and verification produce a concrete handoff; it never waives required independent acceptance. When activated, reviewer independence comes from separate identity, fresh context, no implementation ownership, and the review protocol; changing its profile never permits reuse of an implementation worker as reviewer.

## Role Profile Contract

Resolve this map before every new or reused dispatch:

| Role | Default | Override behavior |
| --- | --- | --- |
| Project orchestrator | Current task profile | Validate an explicit requirement; never mutate |
| Feature owner | `gpt-5.6-sol` / medium | Explicit per-feature model and/or effort override |
| Implementation worker | `gpt-5.6-luna` / xhigh | Explicit per-feature model and/or effort override |
| Independent reviewer | Disabled; when explicitly requested, `gpt-5.6-sol` / high | Explicit request activates review; optional per-feature model and/or effort override |

An override affects only its named role. Missing fields inherit that enabled role's default, not another role's value. A reviewer override in the current invocation or an authoritative operator decision explicitly scoped to the resolved feature constitutes reviewer activation; a standing or global reviewer preference does not. Absent activation, no reviewer profile is resolved or validated. Never cascade a feature-owner override to workers or reviewer, never upgrade or downgrade a role silently, and never convert a model nickname into an unsupported identifier. An explicit override does not waive a governing driver or project requirement for a particular role profile; conflicting requirements stop at readiness. Retain the complete map internally and disclose it before dispatch only when an override, unresolved or unobservable control, degraded supervision, changed topology/authority/shared-state ownership or conflict, or other decision-bearing variation could change the launch.

Use only model identifiers, effort values, routes, and context controls exposed by the current native product. If an explicit current-orchestrator requirement cannot be observed, stop rather than guess; without an explicit requirement, report the observability limitation and preserve the task. If another exact requested profile cannot be set or validated, stop and report the missing capability. A successful creation or spawn request is profile provenance; if the product lacks independent post-creation readback, state that limitation rather than inventing it.

## Launch Readiness Contract

Before creating or resuming a feature owner, resolve and communicate every applicable field:

- Objective, observable outcome, durable authorities, user decisions, assumptions, unknowns, and non-goals.
- Project identity, repository path, intended base/ref or working-tree state, and checkout/worktree policy.
- Owned scope, interfaces, dependencies, sibling boundaries, active writers, and shared mutable resources.
- Local edit, validation, commit, push, pull-request, merge, lifecycle, external-write, and delegation authority exactly as granted.
- Acceptance criteria, required artifacts, verification, decision-bearing evidence, and plausible wrong implementations when material.
- Stop/ask gates for user-owned choices, architecture/contract changes, unsafe expansion, missing infrastructure/authority, dependency invalidation, and shared-resource conflicts.
- Complete resolved role-profile map with default/override provenance and current-orchestrator precondition result.
- Notification mode, route-specific mechanism/target/action, mandatory and extended events, message shape, parent supervision state, and truthful fallback.
- Fresh ordinary feature task and fresh native subagents by default; any exceptional inherited-turn worker slice names its fact, reason, and exact extent.

Use existing durable authority when sufficient. For multi-phase or high-consequence work without an adequate source, create or update the smallest appropriate project-owned task, PRD, or specification only under the current driver and authority. Do not create an orchestration ledger.

## New Versus Reused Ownership

Reuse a feature owner only when its exact identity is known, it is idle, and the feature, project, repository, checkout/worktree, branch, trust boundary, authority envelope, lifecycle role, feature-owner profile, acceptance boundary, and selected inner-lens contract remain compatible. Native inspection establishes identity, reachability, and state; the orchestrator's accepted launch record establishes profile provenance when independent readback is unavailable. A title or unsupported recollection is never sufficient.

Before reuse, revalidate the complete role map and notification contract. Never send a reset or concurrent assignment to a running feature owner. Send an idle compatible owner a full reset that classifies the prior assignment, states allowed carry-over facts, invalidates stale scope/authority/assumptions/decisions/evidence/completion claims, and restates the objective, interfaces, success, verification, stop gates, notification mode, reporting events, context policy, role profiles, and return format. Preserve the configured feature-owner profile by omitting per-message overrides; if it differs, create a new owner rather than attempting to mutate the task.

The feature owner applies the same rules to workers and reviewer. Reuse requires compatible role, project, checkout, trust, authority, ownership, model, effort, and route. A profile change is an incompatibility, not an instruction to override an existing identity. Keep implementation and reviewer identities separate.

Create or recycle only on the existing named material boundaries: different feature/project/repository/checkout, changed trust or permission boundary, incompatible role profile, unrecoverable superseded contract, repeated acceptance-critical miss after correction, hidden unresolved state, unreachable identity, or explicit operator request. Never replace a stalled, failed, or blocked identity silently.

## Context Boundary

Create a new feature owner through native `create_thread` with fresh context, never `fork_thread`. Distill load-bearing chat-only decisions and point to durable project paths. Conversation history is context, never authority. An operator-requested task fork is a different topology and requires an explicit boundary decision.

Create new native workers and reviewers with no parent turns by default. Inherit only the smallest bounded recent slice for one named load-bearing fact with no durable source that cannot be accurately distilled without material loss; state the fact, reason, and extent before dispatch. Independent reviewers never receive inherited history. Full parent-history inheritance is prohibited.

## Inner Lens

`orchestrate-workers` is the canonical generic lens. The feature-owner launch contract explicitly invokes it for the resolved feature, passes the resolved worker profile and reviewer activation as `disabled` or `operator-requested`, and, only when review is requested, carries the exact operator-request provenance, acceptance target, and separate reviewer profile/provenance. It forbids the optional ordinary implementation-task route and preserves the feature owner as planner, integrator, default reviewer, and acceptance authority. The lens owns worker/reviewer decomposition, contracts, context, continuity, evidence, optional-review routing, and acceptance rules.

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

Rename the canonical outer source, catalog ID, install target, metadata, docs, and tests from `orchestrate-sol-feature` to `orchestrate-feature`. Do not keep the old outer source or catalog entry. Keep `orchestrate-workers` as the Codex-only generic lens and remove the redundant `sol-luna-orchestration` source and catalog entry.

Scratch migration validation must model an existing managed installation containing `skills/orchestrate-sol-feature`, run the Codex installer in dry-run/diff prune mode, and show removal of the old managed asset plus installation of `skills/orchestrate-feature` and `skills/orchestrate-workers` without touching foreign/unmanaged assets. The PR does not authorize live installation.

T-39 authorizes the current branch, reviewed source implementation, commits, push, and pull request. Merge, live installation, branch deletion, and destructive cleanup remain outside this task.

## Success Measures

- One memorable `orchestrate-feature` invocation produces the intended ownership topology with explicit, independently resolved role profiles.
- No-override behavior preserves Sol/medium feature ownership, Luna/xhigh workers, feature-owner self-review, and no separate reviewer dispatch.
- Non-Sol feature owners can use the generic inner lens truthfully without copied protocol or a Sol-only precondition.
- Exact profile requests, validation, and readback limitations are reported truthfully; no override cascades or mutates the current orchestrator.
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
