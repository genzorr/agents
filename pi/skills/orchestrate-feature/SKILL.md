---
name: orchestrate-feature
description: Create or reuse one separate ordinary Pi/T3 feature-owner conversation with native leaf workers and approval-gated return to main. Use only when the operator invokes this helper or requests this topology; preserve current profiles and existing authority.
disable-model-invocation: true
---

# Orchestrate Feature

A helper for the current main conversation; keep the project workflow as driver. Dispatch one separate ordinary user-openable Pi/T3 conversation, never a native subagent, retained child or transcript fork. The owner integrates, verifies and accepts its feature; main retains cross-feature decisions. Owners use [orchestrate-workers](../orchestrate-workers/SKILL.md), not this helper, and receive no ordinary-thread creation authority.

## Resolve before dispatch

Use only existing exposed T3 tools. Discover their advertised schemas; missing tools or unavailable approval UI means this route is unavailable, not permission to install/configure a bridge or use another runtime. Every T3 MCP call keeps the current approval policy. This helper uses approval-gated callbacks, not unattended cross-conversation messaging.

Read `orchestrator_capabilities({}).parentThreadId` for the current main identity, then `t3_thread_configuration({})` for its actual provider/model/options. Preserve main's selection. Resolve the owner's exact Pi provider/model/thinking at creation, worker defaults and named overrides independently from explicit operator choices or observable configured defaults. Never substitute an unavailable control or cascade one role's override. Reviewer activation is disabled unless explicitly requested for this feature; only then resolve its separate profile and acceptance target.

Resolve the objective, source/specification, existing checkout/branch, authority, success criteria, dependencies and one writer per shared resource, including Git/build artifacts. Do not infer worktree, commit, push, merge, live-install or additional delegation authority. A different feature requires a fresh invocation.

## Create or reuse the ordinary owner

Reuse only an exact known compatible idle owner. Inspect its thread and configuration: feature, project/checkout, authority, owner profile and unfinished scope must match. Send a complete reset for a new compatible assignment; same-assignment corrections carry only changed facts. Never silently replace a running or unreachable owner, or change its model/effort to make reuse fit.

For a new owner use `create_threads` with one entry, a feature title and the compiled launch contract. It inherits the caller's checkout; verify the intended workspace rather than falling back to `t3_thread_launch`, whose default is project root. Send an explicit Pi `target` with the advertised `providerInstanceId`, `model` and complete `options`; native Pi thinking is an option with `id: "thinking"`, not a guessed top-level effort field. Carry only the feature contract, without parent history. Use a stable `clientRequestId` for this logical creation. Retry that key only within the same live MCP caller; idempotency is scoped to that caller, not durable across provider restarts. After restart or uncertain caller continuity, inspect the retained ordinary thread before any retry; unresolved creation stays uncertain rather than creating another owner.

Read the exact ordinary `threadId` from model-visible result text and construct `[title](t3-thread://v1/<threadId>)`. Retain both in the existing task record; native worker run IDs are separate handles. Inspect `t3_thread_configuration({threadId: ownerId})` and public `t3_thread_read` state against the requested profile/workspace. Accepted creation is not proof of model adherence or successful work. A mismatch stops affected work rather than authorizing configuration mutation.

The launch contract contains:

- Objective, source/specification and selected decisions; non-goals, initial checkout/branch/state, owned interfaces and dependencies; verify expected startup controls before edits without disabling them.
- Exact granted edits, checks, Git/external/live effects and stop conditions; one named writer for shared resources.
- Owner integration/acceptance responsibility and the governing project workflow; activate `orchestrate-workers` for native leaves only, with fresh assignment context and required permission/instruction controls. Pass the resolved worker defaults/overrides and only an explicitly requested reviewer profile/target. Leaves return only to their owner and never receive main's callback.
- Observable success, proportionate verification and durable handoff location. Owner handles routine implementation/build/review/CI repairs within scope; escalate exhausted authority, genuine decisions or threatened shared state.
- Main's exact ordinary thread ID and the approval-gated return contract below. The owner must not invoke this feature helper or create another ordinary owner.

Report the owner identity/link, scope, creation profile/readback limits and return mode, then return so main stays available. Do not start a watcher or routinely poll the owner.

## Correct, recover and return

Address corrections or ordinary continuation with `t3_thread_send` using only `threadId`, `message`, `mode` and stable `clientRequestId`. `auto` uses native current-state delivery; inspect its actual receipt and state rather than assuming it started, queued or steered. Follow-ups/resets/resumes omit both `model` and `thinking`, and never call a configuration tool. A profile mismatch needs a user decision, not an implicit settings change.

Routine leaf results and recoverable friction stay inside the owner. Only a real blocker, required decision or classified terminal handoff uses `t3_thread_send` to the fixed main ID, with `mode: "auto"` and a stable request ID for that event. Obtain the normal per-call approval. The message identifies feature/status, outcome or exact decision, material limit and existing evidence link. An accepted send is dispatch, not proof that main consumed or acted on it. Send retry keys have the same live-caller limit as creation; after a caller restart, uncertain delivery requires inspection/manual reconciliation, not automatic resend. Child `contact_supervisor` is not this ordinary return route.

If approval is denied, unavailable or delivery is uncertain, preserve the outcome and receipt in the owner conversation/existing task record and report delivery pending. Do not claim notification, retry under a new identity or bypass approval. The user can open/read that ordinary owner manually; delivery remains unobserved until inspection.

On an explicit status request or missing-delivery recovery, inspect the exact known owner and its native run/result; use an advertised bounded wait only while actively supervising that identified run. Timeout is pending, not completion. Reopen/resume the same ordinary identity with its stored profile and scope; native status/configuration remains authoritative. No subscriptions, observer, parallel ledger, automatic restart replay or exactly-once guarantee is provided. Human UI, model behavior and compaction continuity require later-use qualification.
