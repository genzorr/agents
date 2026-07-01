---
description: Restate requirements, assess risks, and create step-by-step implementation plan. WAIT for user CONFIRM before touching any code.
---

# Plan Command

Invoke the **planner** subagent to create an implementation plan. Do NOT write any code until the user confirms.

> **Cross-tree divergence (intentional).** The Codex counterpart `codex/skills/harness-plan/SKILL.md`
> plans inline (Codex has no cheap subagents). Claude delegates to the `planner` subagent; the
> divergence is deliberate.

## Process

1. Spawn the `planner` agent with the user's request: $ARGUMENTS
2. Present the plan to the user
3. **WAIT for explicit confirmation** before proceeding
4. If the user says "modify" — adjust and re-present
5. Only after "yes"/"proceed"/confirmation — begin implementation
