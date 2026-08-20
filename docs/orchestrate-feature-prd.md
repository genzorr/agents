# Orchestrate Feature — Product Requirements

## Status

Implemented initially under Agents Harness task T-36, hardened under T-38 after the first runtime handoff failure, and generalized under T-39. This document is the product contract for the Codex-only feature-orchestration skill family; it does not authorize a live skill installation or change Codex runtime configuration.

## Problem

Long-lived project discussions accumulate requirements, research interpretation, cross-feature dependencies, and user decisions that should remain available to one stable project-orchestrator task. Long implementation work produces a different kind of context: repository exploration, test output, failed attempts, diffs, and detailed verification evidence. Performing both kinds of work in the same task pollutes project context, while dispatching implementation directly from the project orchestrator to short-lived subagents removes the coherent feature owner that should plan, integrate, review, and accept the work.

The operating model separates three ownership levels: a long-lived project orchestrator preserves program context; one ordinary feature-owner task owns a substantial feature or research lane; and that owner uses and reuses native leaf subagents for bounded implementation, investigation, verification, and independent review.

The first implementation coupled this topology to one fixed role map and named the outer skill `orchestrate-sol-feature`: Sol/high feature owner, Sol/medium implementation workers, and Sol/high independent reviewer. The topology is reusable independently of those defaults. Baking model choices into the entrypoint makes legitimate per-feature profile changes awkward, invites copied skills, and makes a non-Sol feature owner incompatible with the Sol-only inner lens.

## Observed Runtime Failure

The first production use also established that ordinary Codex tasks are peers rather than parent/child processes with automatic result delivery. The feature owner finished correctly in its own task, but the originating project orchestrator received no completion event. The immediate launch contract omitted the orchestrator's exact task identity and an executable callback action; the systemic gap allowed dispatch without either callback or practical active supervision.

T-38 corrected that boundary. Every feature lane must now select native callback by default, practical bounded active waiting, another product-validated delivery mechanism, or explicitly accepted manual supervision. Callback-specific identity and `send_message_to_thread` requirements apply only when callback is selected; every mode preserves sparse actionable-blocker, required-gate, and terminal events and represents observation truthfully.

## Product Decision

Make `orchestrate-feature` the only canonical outer entrypoint. It resolves one feature objective, one delivery contract, and an independent role-profile map, then creates or reuses one ordinary feature owner. The current no-override profile map remains feature owner `gpt-5.6-sol`/high, implementation worker `gpt-5.6-sol`/medium, and independent reviewer `gpt-5.6-sol`/high.

Create one generic inner lens named `orchestrate-workers`. It owns worker decomposition, contracts, context, continuity, evidence, reviewer escalation, and acceptance rules for any product-exposed coordinator profile. Keep `sol-luna-orchestration` as a thin explicit compatibility preset that invokes the generic lens with its historical current-Sol coordinator requirement, Luna/xhigh implementation defaults, Sol/high reviewer default, and operator-requested ordinary Luna task route. Do not duplicate the inner protocol in the wrapper or outer skill.

Remove `orchestrate-sol-feature` from the source and catalog rather than keeping two ambiguous outer entrypoints. Managed scratch-upgrade/prune evidence must show that the old installed asset is removed while the new canonical asset and generic lens are installed.

## Goals

- Preserve the long-lived orchestrator as the home for requirements, priorities, cross-feature coordination, user-owned choices, and program-level disposition.
- Give each substantial feature one coherent ordinary-task owner for detailed planning, implementation, integration, verification, and feature-level acceptance.
- Move bounded implementation-depth work into reusable native leaf subagents without allowing workers or reviewers to delegate.
- Resolve feature-owner, worker, and reviewer model/effort profiles independently while preserving the current Sol/high, Sol/medium, Sol/high defaults.
- Treat the active project-orchestrator profile as immutable session state that the skill may validate but never change.
- Launch feature owners and native subagents with fresh context by default; inherited-turn subagent forks remain rare, bounded, named exceptions and full-history forks remain prohibited.
- Reuse compatible feature tasks and subagents without allowing stale scope, authority, assumptions, delivery contracts, profiles, or completion claims to carry silently.
- Preserve executable sparse delivery, bounded supervision, project instructions, sandbox and approval policy, checkout/worktree rules, Git authority, external-write gates, and task-specific workflow drivers.
- Keep model/effort selection and readback claims truthful: exact unsupported profiles stop rather than substitute, and validation is not misreported as independent metadata readback.

## Non-Goals

- Do not create a daemon, queue, scheduler, automation, task registry, context database, status ledger, custom agent configuration, or new task controller.
- Do not infer a role profile from task size, cost, availability, a previous invocation, or another role's override.
- Do not change the current project-orchestrator task's model or effort.
- Do not make every feature use a separate task; contained interactive work remains in the current task when a separate owner would add more handoff cost than context protection.
- Do not create feature owners by forking the project-orchestrator task or permit full-history subagent forks.
- Do not make the project orchestrator a duplicate feature-level reviewer or require it to rerun all accepted child verification.
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
| Keep the current task as planner, integrator, primary reviewer, and acceptance authority while delegating bounded implementation or verification | `$orchestrate-workers` | The current task remains coordinator; native workers and any required independent reviewer operate beneath it. |
| Preserve the current project-orchestrator context while another ordinary task owns a substantial feature lifecycle | `$orchestrate-feature` | The current task remains project orchestrator; a separate feature owner applies `orchestrate-workers` internally. |
| Complete a small contained task whose handoff cost would exceed its delegation value | Neither | The current task performs the work directly. |

Direct `orchestrate-workers` use is appropriate when the design is already resolved in the current task and implementation plus fresh review would help without creating another ownership layer. For example, the operator can say: `Use $orchestrate-workers to implement this caching change in the current task. Delegate implementation to Sol/medium and require independent Sol/high review before acceptance.` The current task decomposes the work, sends the compact contract, integrates and checks the result, routes corrections, and alone accepts the change.

It is also appropriate when the current task owns a migration or similarly coherent task with genuinely non-overlapping implementation lanes, such as application changes and independent test-fixture changes. Prefer one coherent worker; add workers only when each owns a distinct output that changes or accelerates a named downstream decision. The current task integrates all lanes and retains one visible acceptance boundary.

Invoking `orchestrate-workers` does not guarantee an independent reviewer unless the operator or governing driver requires one or the named escalation conditions fire. State `require independent review` when review must occur. New workers receive fresh context and a compact contract by default, every worker and reviewer remains a leaf, and one invocation applies to one resolved task. The skill changes no coordinator profile, permission, Git authority, worktree authority, or external-write authority.

When the operator invokes `$orchestrate-feature`, no separate `$orchestrate-workers` invocation is necessary. The operator-authorized feature launch explicitly activates the inner lens in the feature-owner task and forbids its optional ordinary implementation-task route. Both public skills remain explicit-only; intentional outer invocation authorizes the composed owner-and-worker topology without adding a confirmation gate at every layer.

## Operating Model

```text
Long-lived project orchestrator — current immutable profile
└── Ordinary feature owner — resolved profile; default gpt-5.6-sol / high
    ├── Reusable native implementation workers — resolved profile; default gpt-5.6-sol / medium
    └── Independent native reviewer when escalation fires — resolved profile; default gpt-5.6-sol / high
```

### Project orchestrator

The project orchestrator owns priorities, requirements, cross-feature dependencies, shared-resource coordination, user decisions, material scope or architecture changes, task launch/reuse/stop decisions, external landing decisions, and program-level disposition. It preserves its current model and effort. An operator-specified orchestrator profile is a launch precondition to validate, never an instruction for this skill to mutate the current task.

The orchestrator must not directly spawn the feature's implementation workers or reviewer. It retains the exact feature-task identity, resolved role map, notification contract, and parent-owned wait state, and may resolve ordinary blockers within existing authority by steering the same feature owner.

### Feature owner

The ordinary task at the resolved feature-owner profile owns detailed architecture within the launch contract, decomposition, native subagent assignments, integration, owned-state inspection, verification, feature-level review, and feature-level acceptance. It uses the applicable project workflow as driver and `orchestrate-workers` only as a delegation and review lens.

The feature owner must not create another ordinary feature task, delegate project-level authority, or treat a worker report as acceptance. It delivers only the events required by the selected notification mode. A non-Sol feature owner is valid when the product can create and validate its exact profile and the generic inner lens can operate under that coordinator profile.

### Implementation workers

Workers use the independently resolved worker profile and own bounded questions, files, components, tests, or evidence packets under the compact worker contract. They receive no parent-turn history by default, cannot delegate, and return only blockers or a final classified report to the feature owner. A bounded inherited-turn slice is exceptional and requires one named load-bearing fact with no durable source that cannot be accurately distilled without material loss, plus the reason and exact inherited slice. Full-history forks remain prohibited.

### Independent reviewer

The reviewer is a separate native leaf identity at the independently resolved reviewer profile. It is created or reused only when the generic lens's named escalation rule fires or a governing driver/operator requires it. Reviewer independence comes from separate identity, fresh context, no implementation ownership, and the review protocol; changing its profile never permits reuse of an implementation worker as reviewer or weakens the escalation gate silently.

## Role Profile Contract

Resolve this map before every new or reused dispatch:

| Role | Default | Override behavior |
| --- | --- | --- |
| Project orchestrator | Current task profile | Validate an explicit requirement; never mutate |
| Feature owner | `gpt-5.6-sol` / high | Explicit per-feature model and/or effort override |
| Implementation worker | `gpt-5.6-sol` / medium | Explicit per-feature model and/or effort override |
| Independent reviewer | `gpt-5.6-sol` / high | Explicit per-feature model and/or effort override |

An override affects only its named role. Missing fields inherit that role's default, not another role's value. Never cascade a feature-owner override to workers or reviewer, never upgrade or downgrade a role silently, and never convert a model nickname into an unsupported identifier. An explicit override does not waive a governing driver or project requirement for a particular role profile; conflicting requirements stop at readiness. Before dispatch, echo the complete resolved map and distinguish an explicit override from a default.

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

## Inner Lens And Compatibility Preset

`orchestrate-workers` is the canonical generic lens. The feature-owner launch contract explicitly invokes it for the resolved feature, passes the resolved worker and reviewer profiles, forbids its optional ordinary implementation-task route, and preserves the feature owner as planner, integrator, primary reviewer, and acceptance authority. The lens owns worker/reviewer decomposition, contracts, context, continuity, evidence, escalation, and acceptance rules.

`sol-luna-orchestration` remains an explicit-only preset for direct current-task use. It requires a current Sol coordinator, supplies native Luna/xhigh implementation and Sol/high reviewer defaults, preserves the separately operator-requested ordinary Luna task route, and delegates all generic lifecycle rules to `orchestrate-workers`. For that generic ordinary-task route, exact callback means the exact originating coordinator `threadId` and `hostId` when required plus explicit native `send_message_to_thread`; an accepted blocker/terminal send establishes delivery, while rejection or unavailability remains local delivery failure. The preset contains no second copy of the generic protocol.

If the operator invokes both outer feature ownership and an ordinary implementation-task route for the same unresolved feature, stop and ask for one owner topology. `goal-prompt` remains the owner of durable autonomous goal handoffs; an existing goal artifact may be durable feature authority but does not replace native task/profile/delivery resolution.

## Project And Git Boundaries

Resolve the target through native project/task surfaces and inspect project instructions before selecting a checkout or app-managed worktree. Personal OS and repositories it manages use the existing checkout unless the operator explicitly authorizes a worktree. Other projects follow user/project policy and then native defaults. Never invent a starting branch/ref.

Invocation inherits only authority already granted for edits, validation, commits, pushes, pull requests, merges, branch operations, external writes, task creation, and delegation. It never broadens those permissions.

Allow one active durable writer per checkout by default, counting the project orchestrator and feature owners. Concurrent writers require disjoint paths plus one named owner for Git state and other shared mutable resources, or explicit separate-worktree authority. If active-writer state cannot be recovered, serialize or ask.

## Reporting And Supervision

Before dispatch, select one delivery mode and preserve only required phase gates, genuine actionable blockers, and terminal `complete`, `blocked`, `partial`, or `failed` handoffs. Recoverable implementation friction, routine progress, unchanged status, and repeated messages are not delivery events.

- Callback, the default: the feature owner uses native `send_message_to_thread` to the exact originating task; accepted terminal send establishes delivery.
- Practical bounded active waiting: native attention state carries required gates/blockers and terminal state carries the final handoff while the orchestrator remains attached; observation establishes delivery and timeout does not.
- Product-validated replacement: the notification contract names mechanism and target and preserves the same event floor.
- Explicitly accepted manual supervision: the same events remain in native attention/terminal state for later inspection; delivery is unobserved until inspection and no automatic-return claim is allowed.

The orchestrator retains the feature identity, host when required, and latest wait cursor. It uses bounded `wait_threads` only as immediate race coverage or active supervision while attached, never as a durable watcher, and does not poll repeatedly. It may add named phase/risk/budget/decision gates but cannot remove actionable-blocker and terminal delivery, weaken selected-mode semantics, or introduce routine reporting.

The final handoff includes outcome, exact repository/branch/commit/checkout state, changed artifacts, commands/checks, criteria coverage, material decisions/divergence, blockers, residual uncertainty, downstream action, continuity state, and the resolved role map actually used. The project orchestrator verifies only the smallest program boundary required for disposition.

## Migration And Release Boundary

Rename the canonical outer source, catalog ID, install target, metadata, docs, and tests from `orchestrate-sol-feature` to `orchestrate-feature`. Do not keep the old outer source or catalog entry. Add `orchestrate-workers` as a Codex-only generic lens and retain `sol-luna-orchestration` as the compact compatibility preset.

Scratch migration validation must model an existing managed installation containing `skills/orchestrate-sol-feature`, run the Codex installer in dry-run/diff prune mode, and show removal of the old managed asset plus installation of `skills/orchestrate-feature` and `skills/orchestrate-workers` without touching foreign/unmanaged assets. The PR does not authorize live installation.

T-39 authorizes the current branch, reviewed source implementation, commits, push, and pull request. Merge, live installation, branch deletion, and destructive cleanup remain outside this task.

## Success Measures

- One memorable `orchestrate-feature` invocation produces the intended ownership topology with explicit, independently resolved role profiles.
- No-override behavior preserves the current Sol/high owner, Sol/medium worker, and Sol/high reviewer map.
- Non-Sol feature owners can use the generic inner lens truthfully without copied protocol or a Sol-only precondition.
- Exact profile requests, validation, and readback limitations are reported truthfully; no override cascades or mutates the current orchestrator.
- Feature owners, workers, and reviewers reuse only compatible identities and receive complete resets.
- Every feature lane preserves executable sparse delivery, bounded supervision, fresh context, leaf topology, authority, and acceptance boundaries.
- The old outer installed asset has a tested managed prune path and no ambiguous source/catalog twin remains.

## Risks And Mitigations

- Generic-name overreach: keep one fixed topology and explicit role map; do not turn the skill into a general task controller.
- Profile drift: echo complete defaults/overrides, validate exact profiles, prevent cascading, and key reuse by role profile.
- Misleading compatibility: move generic protocol to `orchestrate-workers`; keep `sol-luna-orchestration` only as a thin historical preset.
- Reviewer weakening: preserve separate identity, fresh context, escalation rationale, and acceptance protocol independently of profile.
- Handoff loss: preserve T-38 route-specific delivery and bounded-supervision tests unchanged.
- Context contamination: prohibit feature-task forks and full-history subagent forks; keep inherited turns exceptional and named.
- Migration residue: remove the old outer catalog/source and verify managed prune behavior in scratch state.
- Authority drift: restate exact permissions at launch and keep model selection separate from operational authority.
