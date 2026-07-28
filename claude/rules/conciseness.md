# Conciseness

Lead with the conclusion. Preserve necessary evidence, material caveats, decisions, and the next action; omit repetition and generic filler unless the user asks for detail.

Use specific nouns and direct verbs. Name the actor, action, object, and result when known; cut stock phrases and generic claims that could fit any project. Apply this to responses, documentation, commit messages, and pull-request descriptions.

Prefer precision over blanket style bans: state claims directly, and do not manufacture a "not X but Y" contrast unless it carries real information. Genuine contrast, technical terms, and passive voice are fine when they are the clearest form.

Keep delegated and subagent prompts focused: the task and the context the worker needs, without builder reasoning, implementation narrative, or logs of failed attempts.

## Avoid

- **Preambles**: "I'll now...", "Let me...", "Here's what I'm going to do." Start with the substance or the tool call.
- **Step-narration banners** in user-facing output: "Step 1: Plan", "Now implementing", "Moving on to X". Structure the reasoning internally; do not announce it.
- **Restating the request** back before answering.
- **A closing recap** when a concrete summary already exists — a verifier table, diff list, or commit message. Do not paraphrase what the user just read.

## Line Breaks In Files

Never hard-wrap prose to a column width. One paragraph, bullet, or table row is one line, however long. This applies to Markdown, comments, docstrings, and commit message bodies.

No formatter in these repos wraps Markdown, so every wrapped line is an authoring choice, and wrapping actively breaks things: a phrase split across a newline plus indentation no longer matches `grep`, `Edit`'s `old_string`, `sed`, or a substring assertion. `tests/test_bounded_cognition_contracts.py` pins exact phrases from these very rule files, and re-wrapping has broken it. Reflowing also inflates diffs, hiding the real change.

Do not re-wrap or unwrap prose your task did not otherwise change — that is a drive-by edit.

## Exceptions

- The user asks for a detailed explanation, walk-through, or teaching answer.
- Presenting a plan, ADR, or handoff where structure is the content.
- Surfacing a genuine ambiguity: one pointed question with context beats guessing silently.

Applies to all skills, commands, subagents, and free-form responses. A skill's own tighter cap wins.
