# Orchestrate Sol Feature — Product Requirements

## Status

Proposed for implementation under Agents Harness task T-36. This document is the product contract for one Codex-only personal skill; it does not authorize a live skill installation or change Codex runtime configuration.

## Problem

Long-lived project discussions accumulate requirements, research interpretation, cross-feature dependencies, and user decisions that should remain available to one stable project-orchestrator task. Long implementation work produces a different kind of context: repository exploration, test output, failed attempts, diffs, and detailed verification evidence. Performing both kinds of work in the same task pollutes the project context, while dispatching implementation directly from the project orchestrator to short-lived subagents removes the coherent feature owner that should plan, integrate, review, and accept the work.

The operator has repeatedly established a three-level operating model:

1. A long-lived project orchestrator preserves project context and owns program-level decisions.
2. A separate ordinary Sol/high Codex task owns one long feature or research lane.
3. That feature owner uses and reuses native Sol/medium subagents for bounded implementation, investigation, and verification assignments.

The existing `sol-luna-orchestration` skill supplies the inner delegation, worker-continuity, evidence, and review lens for the current Sol task. It does not own creation, reuse, or supervision of the outer ordinary feature task. A separate outer skill is needed to encode that boundary and prevent the project orchestrator from becoming the implementation owner.

## Product Decision

Add an explicit-only Codex skill named `orchestrate-sol-feature`. When the operator invokes it after discussing a feature, the current long-lived Sol task resolves a launch contract and creates or reuses one ordinary `gpt-5.6-sol` / `high` feature task. The feature task is explicitly instructed to apply `sol-luna-orchestration` with the operator-authorized worker override `gpt-5.6-sol` / `medium` and to use only native leaf subagents for delegated work.

Do not create a copied `sol-sol-orchestration` worker skill. Reuse the existing inner lens and make only the bounded terminology clarification required for its already-supported explicit alternate worker profiles.

## Goals

- Preserve the long-lived orchestrator as the home for requirements, priorities, cross-feature coordination, user-owned choices, and project-level disposition.
- Give each substantial feature one coherent Sol/high owner for detailed planning, implementation, integration, verification, and feature-level acceptance.
- Move bounded implementation-depth work into reusable Sol/medium subagents without allowing workers to delegate further.
- Launch new feature tasks with a distilled context contract and durable references rather than inherited parent-chat history.
- Reuse compatible feature tasks and compatible subagents without allowing stale scope, authority, assumptions, or completion claims to carry silently.
- Preserve project instructions, sandbox and approval policy, checkout/worktree rules, Git authority, external-write gates, and task-specific workflow drivers.
- Keep reporting sparse and decision-bearing: genuine blockers, explicitly requested phase boundaries, and final handoffs.
- Make task identity and model observability claims truthful when the product validates a requested profile but does not expose an independent readback.

## Non-Goals

- Do not create a daemon, queue, scheduler, automation, task registry, context database, status ledger, custom agent configuration, or new task controller.
- Do not replace project task tracking, Harness, PRDs, specifications, issues, or repository documentation.
- Do not make every feature use a separate task; contained interactive work remains in the current task when a separate owner would add more handoff cost than context protection.
- Do not make the project orchestrator a duplicate code reviewer for every child diff or require it to rerun all child verification.
- Do not permit subagents to spawn subagents or ordinary Codex tasks.
- Do not authorize pushes, pull requests, merges, branch deletion, destructive cleanup, live skill installation, external writes, or worktrees beyond existing user and project authority.
- Do not add a Claude skill counterpart; ordinary Codex tasks and native Codex subagents are product-specific.
- Do not rename or deprecate `sol-luna-orchestration`, change its Luna/xhigh default, or weaken its acceptance and independent-review rules.

## Users And Invocation

The user is an operator maintaining a long-running Codex project-orchestrator task. The skill is user-invoked only. A representative prompt is:

```text
Use $orchestrate-sol-feature to work on the feature we just defined.
```

Explicit invocation authorizes the outer skill to create or resume one resolved ordinary feature task. It is not a standing instruction for later unrelated features and does not broaden implementation or external-write authority.

Before dispatch, classify whether a separate feature owner has material value. The gate passes when the work is expected to be multi-phase, produce substantial implementation or evidence context, contain multiple coherent assignments, progress independently from the orchestrator, or when the operator explicitly requests the separate-task topology despite a contained scope. If none applies, report that the work should remain in the current task and return without dispatch.

If invocation occurs before the objective, project target, start state, material decisions, acceptance boundary, or stop gates can be resolved safely, the skill must prepare the smallest missing launch decision and return without creating a task. It should recover locally answerable facts and use reversible project defaults before asking the user about a genuinely user-owned or difficult-to-reverse choice.

## Operating Model

```text
Long-lived project orchestrator — existing Sol task
└── Ordinary feature owner — gpt-5.6-sol / high
    └── Reusable native workers — gpt-5.6-sol / medium
```

### Project orchestrator

The project orchestrator owns project priorities, requirements, cross-feature dependencies, shared-resource coordination, user decisions, material scope or architecture changes, task launch/reuse/stop decisions, external landing decisions, and project-level disposition of the feature handoff. It prepares or selects durable feature authority before launch when the work is multi-phase, experimental, architecture-sensitive, or otherwise too consequential for a chat-only summary.

The project orchestrator must not directly spawn an implementation worker for the feature. It may continue useful program-level work while the feature task runs and may resolve ordinary blockers within existing authority by steering the same feature owner.

### Feature owner

The ordinary Sol/high task owns detailed architecture within the launch contract, decomposition, native subagent assignments, integration, owned-state inspection, verification, feature-level review, and feature-level acceptance. It uses the applicable project workflow as its driver and `sol-luna-orchestration` only as a delegation and review lens.

The feature owner should delegate coherent mid-sized or small implementation-depth assignments when delegation meaningfully protects its context or accelerates work. It may perform trivial local actions itself when writing a worker contract would cost more than the action. It must reuse a compatible idle worker for sequential assignments and create independent workers only for non-overlapping ownership lanes.

The feature owner must not create another ordinary feature task, delegate project-level authority, or treat a worker report as acceptance.

### Sol/medium workers

Workers own bounded questions, files, components, tests, or evidence packets under the existing compact worker contract. They receive fresh context by default, cannot delegate, and return only blockers or a final classified report to the feature owner. Their reports are evidence for feature-owner acceptance.

## Launch Readiness Contract

Before creating or resuming a feature owner, resolve and communicate every applicable field:

- Objective and observable feature outcome.
- Durable authorities: task, issue, PRD, specification, decision record, source paths, and project instructions.
- User decisions, supported assumptions, unresolved unknowns, and explicit non-goals.
- Project identity, repository path, intended base/ref or working-tree state, and applicable checkout/worktree policy.
- Owned feature scope and sibling or shared-state boundaries.
- Checkout-level mutable-state ownership: active writers, Git state, generated artifacts, formatters, build outputs, test databases, ports, devices, and serialized commands.
- Local edit, validation, commit, push, pull-request, merge, lifecycle, external-write, and delegation authority exactly as granted.
- Acceptance criteria, required artifacts, verification expectations, and plausible wrong implementations the evidence must distinguish when material.
- Stop/ask gates for user-owned decisions, architecture/contract changes, unsafe expansion, missing infrastructure or authority, shared-resource conflicts, and invalidated dependencies.
- Reporting events and the exact return route when the native product exposes it.

Use existing durable authority when sufficient. For multi-phase or high-consequence work without an adequate source, create or update the smallest appropriate project-owned task, PRD, or specification before launch under the current driver and authority. Do not create a generic orchestration ledger.

## New Versus Reused Feature Ownership

Reuse an existing ordinary feature task only when its exact identity is known and the feature, project, repository, checkout/worktree, branch, trust boundary, authority envelope, model and effort, lifecycle role, and acceptance boundary remain compatible. The current orchestrator task's own recorded accepted launch result is the model/effort authority; native inspection establishes the exact task's identity, reachability, and current state but need not provide profile readback. Do not infer compatibility from a title or unsupported recollection. If launch provenance is unavailable after compaction or handoff, create a new owner or obtain an operator decision rather than asserting compatibility.

Before reuse, send a complete assignment-reset contract that classifies the previous assignment, states facts allowed to carry over, invalidates stale assumptions and authority, and restates the objective, interfaces, success criteria, verification, stop gates, and return format. Preserve the task's configured model and effort rather than overriding a compatible existing task on every message.

Create a new feature task for a materially different feature, repository or checkout, incompatible model/effort, changed trust or permission boundary, unrecoverable superseded contract, repeated acceptance-critical miss after correction, hidden unresolved prior state, unreachable identity, or explicit operator request.

Do not replace a stalled, failed, or blocked feature owner silently. Inspect and classify it, then replan or obtain the required decision.

## Context Boundary

A new ordinary feature task receives a fresh prompt, not the full project-orchestrator history. The launch contract must summarize load-bearing chat-only decisions and point to durable project paths for everything that can be recovered there. Conversation history is context, never authority.

If a named load-bearing fact has no durable source, include the smallest accurate statement of that fact, its provenance as a user decision or supported inference, and any uncertainty. Do not paste exploratory narration, failed-attempt logs, or unrelated project history.

## Model And Product Contract

- Preserve the current orchestrator's model and reasoning effort. Consult the native model/status surface when available and require a product-exposed Sol session. If the product does not expose current-model identity, proceed with a stated observability limitation unless available evidence indicates a non-Sol session; on evidence of a non-Sol session, report the mismatch rather than changing it silently.
- Create a new ordinary feature owner with the product-exposed identifier `gpt-5.6-sol` and reasoning effort `high`.
- In the feature-owner prompt, explicitly invoke `sol-luna-orchestration` for the resolved feature task and state that the operator selected `gpt-5.6-sol` / `medium` as the worker profile. Do not use Luna unless the operator later requests a different profile.
- Before each native worker dispatch, the feature owner states the actual model and effort requested and follows the inner lens's context and dispatch contract.
- If the product cannot set or validate an exact required route, model, effort, or context boundary, stop and report the missing capability. Never substitute silently.
- Distinguish a product-validated creation or spawn request from an independent metadata readback. If metadata does not expose the selected profile afterward, state that limitation instead of claiming readback.

## Project And Git Boundaries

Resolve the target through the native project/task surface and inspect applicable project instructions before selecting a local checkout or app-managed worktree. User invocation authorizes task creation, not a worktree forbidden by project or operator policy. Personal OS and repositories it manages use the existing local checkout by default and require explicit operator approval for a worktree. Other projects follow their applicable instructions and then the native product default when no stricter rule exists.

Never invent a starting branch or ref. Use the intended existing base/ref or explicitly intended working-tree state. If the available states support materially different implementations and the correct base cannot be recovered, stop at the launch boundary.

The feature task inherits only the authority already granted for local edits, validation, commits, pushes, pull requests, merges, or branch operations. The launch prompt must make absent authority explicit when it matters.

Allow one active durable writer per checkout by default, counting the project orchestrator and every feature owner. While a feature owner writes, the orchestrator performs no concurrent durable writes in that checkout unless the launch contract assigns disjoint paths and names one owner for Git state and other shared mutable resources. Concurrent feature owners follow the same rule; otherwise serialize them or obtain explicit authority for a separate worktree. If active-writer state cannot be recovered from the orchestrator's recorded launches and native inspection, treat it as unresolved and serialize or ask.

The task environment assigned by the product at ordinary-task creation follows operator and project policy and then the native default where permitted. The inner lens's no-worktree-without-operator-approval rule governs additional worktrees the feature owner or its workers might create; it does not retroactively invalidate a task environment selected under the outer launch policy.

## Relationship To The Existing Ordinary Thread Route

The `sol-luna-orchestration` operator-requested ordinary thread route remains an inner implementation route: the current Sol driver retains planning, integration, review, and acceptance while an ordinary Luna/xhigh task performs implementation. `orchestrate-sol-feature` creates a different owner boundary: an ordinary Sol/high task becomes the feature-level planner, integrator, reviewer, and acceptance authority and may use only native Sol/medium leaf subagents.

The new skill never invokes the inner ordinary Luna task/thread route, and its feature-owner launch contract forbids that route from creating another ordinary task. If both routes are requested for the same unresolved feature, stop and ask the operator to select one owner topology; never launch both.

`goal-prompt` remains the owner of durable autonomous goal handoffs and completion contracts. `orchestrate-sol-feature` does not delegate launch-contract authoring to it because this helper performs native task selection/creation, exact model/effort routing, and a fresh in-product prompt without requiring a durable goal file; an existing goal artifact may still be cited as durable feature authority.

## Reporting And Supervision

The feature owner reports only:

- A genuine user-owned, architectural, authority, infrastructure, dependency, or shared-resource blocker.
- A phase boundary the launch contract explicitly requires the project orchestrator to adjudicate.
- A final status of `complete`, `blocked`, `partial`, or `failed`.

The final handoff includes outcome, exact repository/branch/commit/checkout state, changed files or artifacts, commands and checks, criteria covered, material decisions or divergence, blockers, residual uncertainty, downstream action, and continuity state.

Use the exact originating task identity and native continuation mechanism when available. Never invent or store a side-channel task identity. If the origin identity is unavailable, retain the returned feature-task identity in the orchestrator response and use native task inspection or waiting when the operator requests status or the product surfaces completion. Do not create a polling loop.

The project orchestrator verifies the integrated handoff at the program boundary: exact state, criterion coverage, decision-bearing evidence, unresolved risks, and downstream landing decision. It does not routinely repeat current scope-complete child checks or reconstruct implementation detail already accepted by the feature owner.

After dispatch and before a handoff, the lane state is `launched, awaiting handoff`. The orchestrator makes no completion, health, or progress claim from that resting state. It inspects the task only on operator request, product-surfaced completion or attention, or a required project gate.

## Success Measures

- The operator can invoke one memorable skill after a feature discussion and reliably obtain the intended three-level task topology.
- The project orchestrator no longer dispatches the feature's implementation workers directly.
- Feature tasks start with sufficient authoritative context without full parent-history inheritance.
- Exact Sol/high and Sol/medium profiles are requested and reported truthfully.
- Feature and worker identities are reused when compatible and reset before new assignments.
- Project policies and authorization gates remain unchanged.
- Static and behavior-oriented tests reject plausible topology regressions.

## Risks And Mitigations

- Handoff loss: require a complete launch contract and durable references.
- Task proliferation: apply an explicit substantial-feature threshold and reuse compatible feature owners.
- Stale reused context: require assignment-reset overlays and recycle on material boundary changes.
- Duplicate review: separate feature-level acceptance from project-level disposition and reuse current verification evidence.
- Authority drift: restate exact permissions at launch and preserve stop gates.
- Product observability gaps: report validation versus readback precisely and retain exact returned task identity.
- Skill overlap: keep the outer skill focused on ordinary feature-task lifecycle and reuse the existing inner lens for worker orchestration.

## Release Boundary

The source change belongs in the Agents repository as a Codex-only catalog asset. Validate against isolated scratch homes. Opening a pull request is permitted by T-36; merging it or installing it into the live `~/.codex` home requires separate operator authorization.
