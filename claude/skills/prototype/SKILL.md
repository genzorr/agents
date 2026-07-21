---
name: prototype
description: Build a throwaway prototype to answer a design question before committing to production code. Use when the user asks to prototype, mock up, sanity-check a state model, compare UI designs, or let them try an idea quickly.
---

# Prototype

A prototype is throwaway code that answers one question. Make the question explicit before building.

## Choose A Branch

- **Logic/state question**: build a tiny runnable script or terminal app that drives the state machine through realistic cases and prints state after each action.
- **UI question**: build a temporary route or isolated page with multiple distinct variants and a simple switcher.
- **Workflow question**: build the narrowest end-to-end path that lets the user exercise the uncertain step.

If the branch is ambiguous and the user is not available, choose the branch that matches the surrounding code and state the assumption.

## Rules

- Mark prototype files clearly with names like `prototype`, `scratch`, or `spike`.
- Put the prototype close to the code it informs, unless the repo has a scratch/prototype convention.
- Provide one command or URL to run it.
- Keep persistence in memory unless persistence is the thing being tested.
- Skip production polish, broad tests, and reusable abstractions.
- Surface relevant state directly in the prototype output or UI.
- When the question is answered, record the decision in the conversation, issue, ADR, or task notes, then delete or absorb the prototype.

## Experiment composition

- A prototype is feasibility work only. It may explore an idea, but it cannot
  make a confirmatory or regression claim, write a traveling or canonical
  Readout, mutate the singleton Area Brief, promote legacy `E-*` knowledge, or
  authorize adoption/defaults.
- Make the feasibility question and its limits explicit in the output. If the
  result justifies a decision-bearing experiment, route the next step to
  `design-experiment` to freeze a Protocol; do not create Protocol fields or a
  Readout inside the prototype.

## Boundaries

- Do not present prototype code as production-ready.
- Do not let prototype dependencies leak into runtime deps without explicit approval.
- If the prototype reveals a durable architecture issue, suggest `/architecture-review` before folding it into production code.
