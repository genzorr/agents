---
name: session-handoff
description: Create a concise handoff so a fresh agent or future session can continue. Works in any repo; uses harness checkpoint/close when an active harness task exists, otherwise writes a portable temporary Markdown handoff. Use when the user asks for a handoff, pickup notes, end-of-session notes, context for the next agent, or to prepare for compaction.
---

# Session Handoff

Create a continuation note. The goal is transfer quality, not lifecycle ceremony.

This skill works in any repo:

- Harness repo with an active task: persist through `harness checkpoint` or, only when explicitly finishing a completed task, `harness close --done`.
- Non-harness repo: write a portable temporary Markdown file and report its path.
- Existing external tracker: reference issues, PRs, docs, or task files by path/URL; do not invent a parallel durable system unless the user asks.

## Gather

1. Check whether this is a harness repo:
   - Look for `docs/harness/.harness` in the current directory or parents.
   - If present, run `harness snapshot` once. If it fails, fall back to the non-harness path and mention the failure.
2. Check git state with `git status --short` unless `harness snapshot` already reported it.
3. Review the conversation and any visible command/test results.
4. Read only files needed to name changed artifacts, verification, or unresolved blockers. Prefer `rg`/`rg --files`; do not do a broad source walk.

## Determine Next Focus

Do not invent intent. Derive `Next focus` from the strongest available source, in this order:

1. Explicit user instruction for what to do next.
2. A failing command, unfinished edit, merge conflict, blocked tool call, or unresolved error.
3. Open acceptance criteria or unchecked task items.
4. Existing `Last Session`, TODO, issue, PR, or plan next-step text.
5. The obvious continuation from modified files and verification state.

If none of those sources gives a defensible focus, write:

```markdown
**Next focus:** Unspecified. The next session should ask for direction before making changes.
```

If the work appears complete, prefer a closeout focus such as verification, review, checkpoint, commit, or task close instead of inventing new feature work.

## Handoff Shape

Use this shape for both harness and portable handoffs:

```markdown
**Date:** YYYY-MM-DD

**Next focus:** <one sentence, or the unspecified sentence above>

**Current state:**
- <active/done/blocked state, current branch if useful, and whether the tree is dirty>

**What changed:**
- <concrete changes made this session>

**Verified:**
- <commands/checks run, with pass/fail/skipped>

**Not verified / risks:**
- <gaps, flaky checks, unavailable systems, assumptions>

**Decisions:**
- <decisions made, or "None">

**Open questions / stop gates:**
- <questions that should stop the next agent before action, or "None">

**Next steps:**
- <ordered concrete actions>

**Relevant artifacts:**
- <paths, commands, issue/PR URLs; no large pasted content>
```

Keep it concise. Link or name artifacts instead of duplicating their contents.

## Harness Persistence

When `harness snapshot` shows an active task:

1. Build the handoff using the standard shape.
2. If the user asked to finish/close and all acceptance criteria are met, use `harness close --task <id> --done --file <handoff-file>`.
3. Otherwise use `harness checkpoint --task <id> --file <handoff-file>`.
4. Append durable discoveries with `harness findings` only when they will remain true next session: root causes, ruled-out hypotheses, measured limits, accepted invariants. Do not append ordinary progress.
5. Do not commit unless the user explicitly asked.

If the active task cannot be identified, use the portable path.

## Portable Persistence

When no active harness task is available:

1. Write the handoff to a temp file, for example `/tmp/session-handoff-<slug>.md` or a `mktemp` path.
2. Report the path and a one-line summary.
3. Do not create repo-local notes, task files, or docs unless the user explicitly asked for a durable repo artifact.

## Output

After writing:

```markdown
Handoff written: <path or harness task id>

Next focus: <same one-sentence focus>
```

If there were no changes or useful context to preserve, say so and avoid creating a low-value file unless the user explicitly requested one.

## Rules

- A handoff is not an implementation step; do not continue coding after writing it.
- Do not hide uncertainty. Put uncertainty in `Not verified / risks` or write `Next focus: Unspecified...`.
- Do not paste secrets, full tokens, private data exports, or large logs. Reference paths and redacted summaries.
- Do not run expensive verification just to make the handoff look complete. Record what was actually run.
- Do not ask for trivial preferences. Ask only if writing a durable repo artifact would establish a new convention.
