# Conciseness

Use familiar nouns and direct verbs. Say what changes, who acts and what happens next. Explain a technical term when it helps the reader; do not invent a name for an ordinary action.

For project documents, start with the reader's task and show a concrete example. A README should help someone begin. A behavior spec should let them predict an outcome. Architecture should explain responsibilities and important tradeoffs. Development guidance should make the supported commands and recovery usable.

Keep evidence, uncertainty and consequential limits where they affect the conclusion. Link the detailed owner instead of repeating its procedure. Use headings, lists, tables or code examples when they help. Match the requested depth; being concise does not mean omitting the explanation the reader asked for.

Before returning a substantial document, follow one representative reader task through it. Rewrite a passage that makes the reader decode process vocabulary or guess the next action. Do not substitute a style checklist for editing the actual prose.

`response-shape.md` owns response organization and depth.

Keep delegated and subagent prompts focused on the task and needed context. Omit routine implementation narrative and irrelevant debugging logs; retain or link original failed, invalid and contrary evidence when it can change the assignment’s decision or conclusion. Keep producer interpretations and prior verdicts separate, introducing them at the appropriate point for the review mode.

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
