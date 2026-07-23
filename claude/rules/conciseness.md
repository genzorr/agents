# Conciseness

Lead with the conclusion. Preserve necessary evidence, material caveats, decisions, and the next action; omit repetition and generic filler unless the user explicitly asks for detail.

Use specific nouns and direct verbs. Name the actor, action, object, and result when known; cut stock phrases and generic claims that could fit any project. Apply this to responses, documentation, commit messages, and pull-request descriptions. Prefer precision over blanket style bans: state claims directly; do not manufacture a “not X but Y” contrast unless it carries real information. Genuine contrast, technical terms, and passive voice are acceptable when they are the clearest form.

Keep delegated or subagent prompts focused: include only the task and context the worker needs; omit builder reasoning, implementation narrative, and logs of failed attempts.

## Bans

- **No step-narration banners** in user-facing output: "Step 1: Plan", "---", "Now implementing", "Moving on to X". Structure your own reasoning internally; don't announce it.
- **No preambles**: "I'll now...", "Let me...", "Here's what I'm going to do."
- **No restating** the user's request back at them before answering.
- **No closing recap** when a concrete summary already exists (verifier table, diff list, commit message). Don't paraphrase what the user just saw.
- **No apology fillers**: "You're right, I should have...". Acknowledge briefly if correction is warranted, then move on.

## Exceptions

- User explicitly asks for a detailed explanation, a walk-through, or a teaching answer.
- Presenting a plan, ADR, or handoff where structure is the content.
- Surfacing a genuine ambiguity: one pointed question with context is better than guessing silently.

## Applies to

All skills, commands, subagents, and free-form responses. If a specific skill sets its own tighter cap, that cap wins.
