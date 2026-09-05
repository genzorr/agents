# Conciseness

Preserve necessary evidence, material caveats, decisions, and the next action; cut repetition and generic filler. `response-shape.md` owns organization and response depth.

Use specific nouns and direct verbs. Name the actor, action, object, and result when known; cut stock phrases and generic claims that could fit any project. Reuse established project and domain terms for existing concepts. Introduce a new term only when it names a genuine new distinction. Briefly define a necessary term when the intended reader may not know it. Apply this to responses, documentation, commit messages, and pull-request descriptions.

Prefer precision over blanket style bans: state claims directly, and do not manufacture a "not X but Y" contrast unless it carries real information. Genuine contrast, technical terms, and passive voice are fine when they are the clearest form.

Keep delegated and subagent prompts focused: the task and the context the worker needs, without builder reasoning, implementation narrative, or logs of failed attempts.

## Avoid

- **Preambles**: "I'll now...", "Let me...", "Here's what I'm going to do." Start with the substance or the tool call.
- **Step-narration banners** in user-facing output: "Step 1: Plan", "Now implementing", "Moving on to X". Structure the reasoning internally; do not announce it.
- **Restating the request** back before answering.
- **A closing recap** when a concrete summary already exists — a verifier table, diff list, or commit message. Do not paraphrase what the user just read.

## Line Breaks In Files

Never hard-wrap prose to a column width. One paragraph, bullet, or table row is one line, however long. This applies to Markdown, comments, docstrings, and commit message bodies.

Hard-wrapping breaks exact text searches and patches and adds diff noise.

Do not re-wrap or unwrap prose your task did not otherwise change — that is a drive-by edit.

Apply this across skills, commands, subagents, and ordinary responses. Follow task-specific output formats within the user’s requested depth and scope.
