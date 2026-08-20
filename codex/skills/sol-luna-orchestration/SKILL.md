---
name: sol-luna-orchestration
description: Configure the current Sol task through orchestrate-workers with Luna/xhigh workers, self-review, an optional explicitly requested Sol/high reviewer, and an ordinary Luna/xhigh task only when separately requested. Use only when the operator invokes sol-luna-orchestration or asks for Sol–Luna orchestration. Configures one task without launching work, changing the coordinator, authorizing unrelated work, or replacing the driver.
---

# Sol–Luna Orchestration

**Composition role: explicit preset lens.** Keep the current task skill or workflow as driver. This preset supplies historical profiles and routes to `orchestrate-workers`; that generic lens owns decomposition, worker/reviewer contracts, context, continuity, evidence, optional-review routing, acceptance, and lifecycle rules. This preset grants no additional authority and contains no second copy of that protocol.

## Configure Only

Require the current coordinator to run Sol. Preserve its exact model and reasoning effort; never change it. If current identity is not Sol, ask the operator to continue from Sol or abandon this preset.

If invoked without a resolved task and delegation boundary, confirm provisional configuration, name what Sol must resolve, and return without launching a worker. Activation applies only to the current resolved task. A later task, or one resolved after provisional configuration, requires a fresh explicit invocation. Invoke `orchestrate-workers` explicitly for the resolved task under this operator-authorized preset.

Preserve permissions, approval policy, scope, stop gates, and no-worktree-without-operator-approval. The current Sol coordinator remains planner, integrator, primary reviewer, and acceptance authority.

## Historical Profile Preset

Pass this default profile map to `orchestrate-workers`:

| Role | Activation | Route | Model | Effort |
|---|---|---|---|---|
| Implementation worker | When delegated | Native Luna subagent | `gpt-5.6-luna` | `xhigh` |
| Independent reviewer | Disabled unless explicitly operator-requested | Native Sol subagent | `gpt-5.6-sol` | `high` |

Luna/xhigh is the worker default; Sol self-reviews. Explicit operator review or reviewer-profile wording activates a Sol/high reviewer. Another enabled-role profile requires explicit instruction and changes only that role. State enabled controls and provenance before dispatch; do not resolve disabled reviewer controls. Stop if a selection cannot be validated; never substitute, cascade, silently change effort, or claim independent readback.

## Ordinary Luna Implementation Route

Enable the ordinary Codex implementation task route only when the operator separately requests it for the resolved task. Pass ordinary task/thread route plus `gpt-5.6-luna`/`xhigh` to `orchestrate-workers`; keep independent reviewer activation unchanged and apply that lens's exact callback identity, action, acceptance, and delivery-failure contract; return the launch response immediately, do not wait or poll, and send only a genuine blocker or final handoff. Across tasks require fresh preset invocation and another explicit ordinary-route request.

Use this historical response shape after a ready launch:

```text
Launched Luna task/thread <thread-id> for <bounded objective>. It will implement, validate, and report back to this Sol task for review.
```

Apply every generic context, leaf topology, shared-checkout ownership, reset/reuse/recycle, verification, operator-requested reviewer, and acceptance rule from `orchestrate-workers`. Only when the operator activates independent review, use its generic `references/independent-reviewer-protocol.md`; do not recreate a Sol-specific reviewer protocol here.
