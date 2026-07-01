---
name: grill-with-docs
description: Stress-test a plan or design against code, docs, ADRs, and project vocabulary. Use when the user asks to be grilled, wants a plan challenged, wants terminology sharpened, or wants decisions captured before implementation.
---

# Grill With Docs

Interview the user one decision at a time until the plan, design, or existing slice/task-set is
coherent enough to execute or reject.

## Targets

Grill a fresh **plan or design**, or an **existing slice/task-set** that has drifted (too broad,
horizontal, mis-ordered, or stale). When the target is an existing slice/task-set:

- Read the slice and its tasks first (`harness show <slice-id>` / `harness show <task-id>`) plus
  the active goal/board state, before asking anything.
- Write the Decision Summary **back into those tasks** — update their Context/Approach/acceptance
  criteria, or reorder/split/stop them — not into a free-floating plan doc. Use the board
  mechanics in `harness-pick-work` → *Rescope / Replan The Board* for the exact transitions, and
  `harness-add-tasks` for any net-new tracer-bullet tasks.

## Workflow

1. Read the user's plan and identify the highest-risk unresolved decision.
2. Explore the codebase or docs before asking anything answerable from local context.
3. Read relevant context/glossary docs, ADRs, harness task notes, and tests.
4. Ask one pointed question at a time. Include your recommended answer and why it matters.
5. After each answer, update the decision tree and ask the next load-bearing question.
6. When decisions stabilize, stop grilling and emit the **Decision Summary** (see below),
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

## Output While Grilling

```markdown
Question: <one question>
Recommended answer: <your recommendation>
Why it matters: <consequence of this branch>
```

## Decision Summary

When decisions stabilize, stop grilling and emit one self-contained summary so the result
becomes structured work instead of unstructured chat. It must stand alone — the next skill
(or a fresh agent) should be able to act on it without the conversation.

```markdown
## Decision summary — <topic>

### Resolved decisions
- <decision>: <chosen answer> — <one-line rationale>

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
- <one of: harness-add-tasks (new tasks) · harness-add-inbox → harness-process-inbox (capture + triage) · harness-plan (file-level plan first) · ADR (durable tradeoff) · glossary update (use the target project's glossary location; for Harness homes see `/Users/example/dev/os/repos/harness/docs/harness-knowledge-homes.md`) · existing-task update/rescope · no-op> — and why.
```

Hand it off directly: the **Proposed work** + **Implied acceptance criteria** are written to
be pasted into `harness-add-tasks` (or captured via `harness-add-inbox`) without
re-explaining the discussion. This skill **recommends** the capture step — it does not create
tasks itself and does not duplicate `harness-add-tasks` routing/sizing logic. When the result is
a no-op, a simple existing-task update, or a rescope of an existing slice/task-set, say so; do
not invent work to capture. For where each kind of durable knowledge lives, see
`/Users/example/dev/os/repos/harness/docs/harness-knowledge-homes.md`.

## Rules

- Ask one question and wait. Do not dump an interview checklist.
- If the answer is discoverable locally, discover it instead of asking.
- Do not edit docs until the user confirms the decision or asks for capture.
- When the plan is ready, emit the Decision Summary and recommend its capture path (`harness-add-tasks`, `harness-add-inbox` → `harness-process-inbox`, `harness-plan`, `architecture-review`, ADR, glossary update, existing-task update/rescope, or no-op). Do not create tasks automatically.
