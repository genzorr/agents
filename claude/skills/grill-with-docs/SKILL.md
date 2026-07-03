---
name: grill-with-docs
description: Stress-test a plan or design against code, docs, ADRs, and project vocabulary. Use when the user asks to be grilled, wants a plan challenged, wants terminology sharpened, or wants decisions captured before implementation.
---

# Grill With Docs

Interview the user one decision at a time until the plan, design, or existing slice/task-set is
coherent enough to execute or reject. Maintain a private pool of possible questions, but ask only
the few that materially change the work; infer the rest from repo evidence and present those
inferences for verification.

## Targets

Grill a fresh **plan or design**, or an **existing slice/task-set** that has drifted (too broad,
horizontal, mis-ordered, or stale). When the target is an existing slice/task-set:

- Read the slice and its tasks first (`harness show <slice-id>` / `harness show <task-id>`) plus
  the active goal/board state, before asking anything.
- Write the Decision Summary **back into those tasks** — update their Context/Approach/acceptance
  criteria, or reorder/split/stop them — not into a free-floating plan doc. Use the board
  mechanics in `/harness-pick-work` → *Rescope / Replan The Board* for the exact transitions, and
  `/harness-add-tasks` for any net-new tracer-bullet tasks.

## Workflow

1. Read the user's plan and build an initial pool of unresolved decisions, risks, and fuzzy areas.
2. Explore the codebase or docs before asking anything answerable from local context.
3. Read relevant context/glossary docs, ADRs, harness task notes, and tests.
4. Classify the pool:
   - **Ask now** — a load-bearing branch where a wrong guess changes the implementation shape,
     ownership, data contract, migration/rollback path, or verification strategy.
   - **Infer + verify** — a question whose likely answer follows from code, docs, project
     vocabulary, prior task notes, or a low-risk conservative default.
   - **Fog** — an area that is probably relevant later but cannot be phrased sharply until another
     decision lands. Do not pre-split fog into fake questions.
5. Ask the single most important **Ask now** question. Include your recommended answer, why it
   matters, and any immediately relevant inferred defaults the user can correct.
6. After each answer, update and re-rank the pool. Promote fog only when it becomes a sharp
   question; demote questions whose answers are now inferable.
7. When no remaining **Ask now** question would materially change the work, stop grilling and emit
   the **Decision Summary** (see below),
   then recommend the durable capture path it identifies — a glossary/context update, an ADR
   for a durable tradeoff, an update to an existing harness task, or new task(s)/a slice for
   net-new work. Recommend the capture skill; do not create tasks yourself.

## Question Standard

Each question should expose a real branch in the design:

- different implementation shape;
- different module/interface ownership;
- different data contract;
- different migration or rollback path;
- different verification strategy.

Do not ask preference questions that the repo already answers.

## Inference Standard

Infer instead of asking when the evidence is strong enough for a future implementer to rely on:

- established local naming, glossary, ADR, or API vocabulary;
- existing module ownership and dependency direction;
- tests or nearby implementation patterns that show the expected contract;
- a conservative reversible default that can be called out explicitly.

Do not infer when the answer chooses product behavior, deletes or migrates user data, changes a
public contract, creates irreversible work, or would invalidate a plausible alternate architecture.
Those remain **Ask now** questions.

## Output While Grilling

```markdown
Question: <one question>
Recommended answer: <your recommendation>
Why it matters: <consequence of this branch>
Inferred defaults to verify:
- <inference> — <evidence/rationale>      # omit this section when there are none
```

## Decision Summary

When decisions stabilize, stop grilling and emit one self-contained summary so the result
becomes structured work instead of unstructured chat. It must stand alone — the next skill
(or a fresh agent) should be able to act on it without the conversation.

```markdown
## Decision summary — <topic>

### Resolved decisions
- <decision>: <chosen answer> — <one-line rationale> (<user-confirmed | inferred from evidence>)

### Inferred decisions to verify
- <decision>: <inferred answer> — <evidence/rationale, and what would change if wrong>
  (or "none")

### Open questions / stop gates
- <question or gate still unresolved> (or "none")

### Proposed work
- <task: one-line objective>            # one bullet per task; group under a slice if multi-task
  (or) No new task needed — <rationale: existing task T-N covers it / simple existing-task update / no-op>

### Implied acceptance criteria
- <testable criterion, mapped to a proposed task>

### Verification strategy
- <tests / seams / commands that will prove the work>

### Durable capture recommendation
- <one of: /harness-add-tasks (new tasks) · /harness-add-inbox → /harness-process-inbox (capture + triage) · /plan (file-level plan first) · ADR (durable tradeoff) · glossary update (use the target project's glossary location; for Harness homes see `/Users/example/dev/os/repos/harness/docs/harness-knowledge-homes.md`) · existing-task update/rescope · no-op> — and why.
```

Hand it off directly: the **Proposed work** + **Implied acceptance criteria** are written to
be pasted into `/harness-add-tasks` (or captured via `/harness-add-inbox`) without
re-explaining the discussion. This skill **recommends** the capture step — it does not create
tasks itself and does not duplicate `/harness-add-tasks` routing/sizing logic. When the result is
a no-op, a simple existing-task update, or a rescope of an existing slice/task-set, say so; do
not invent work to capture. For where each kind of durable knowledge lives, see
`/Users/example/dev/os/repos/harness/docs/harness-knowledge-homes.md`.

## Rules

- Ask one question and wait. Do not dump an interview checklist.
- If the answer is discoverable locally, discover it instead of asking.
- Build and maintain the broader question pool internally; surface only the top question plus
  concise inferred defaults that need verification.
- Do not ask just to confirm a low-risk inference. Put it in **Inferred decisions to verify** and
  let the user correct it before capture.
- Do not edit docs until the user confirms the decision or asks for capture.
- When the plan is ready, emit the Decision Summary and recommend its capture path (`/harness-add-tasks`, `/harness-add-inbox` → `/harness-process-inbox`, `/plan`, `/architecture-review`, ADR, glossary update, existing-task update/rescope, or no-op). Do not create tasks automatically.
