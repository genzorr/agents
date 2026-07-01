# Conciseness

Reduce tokens without losing clarity. These rules apply to every output unless the user explicitly asks for detail.

## Bans

- **No step-narration banners** in user-facing output: "Step 1: Plan", "---", "Now implementing", "Moving on to X". Structure your own reasoning internally; don't announce it.
- **No preambles**: "I'll now...", "Let me...", "Here's what I'm going to do."
- **No restating** the user's request back at them before answering.
- **No closing recap** when a concrete summary already exists (verifier table, diff list, commit message). Don't paraphrase what the user just saw.
- **No apology fillers**: "You're right, I should have...". Acknowledge briefly if correction is warranted, then move on.

## Caps

- `harness-task-checkpoint` / `harness-task-done` draft: ≤ 200 words.
- `/execute` final confirm: ≤ 1 AC table + 3 lines of prose.
- Subagent prompts: include only what the subagent needs (task file, diff, conventions, plan / AC-mapping table if the subagent expects it) — no builder reasoning, no implementation narrative, no log of what was tried.

## Exceptions

- User explicitly asks for a detailed explanation, a walk-through, or a teaching answer.
- Presenting a plan, ADR, or handoff where structure is the content.
- Surfacing a genuine ambiguity: one pointed question with context is better than guessing silently.

## Applies to

All skills, commands, subagents, and free-form responses. If a specific skill sets its own tighter cap, that cap wins.
