---
name: session-handoff
description: Create a descriptive continuation brief that preserves a session's working context so the user and a fresh agent can decide how to resume. Use for session handoffs, pickup notes, end-of-session context, prompts for after compaction, context for the next agent, or preserving important reasoning, decisions, findings, and unfinished threads. Do not use as an autonomous execution prompt for a fixed goal; use goal-prompt for that.
---

# Session Handoff

Create a descriptive reconstruction of the session. Preserve the shared working model: what the user and agent were trying to understand or accomplish, why it mattered, how the understanding changed, where the work paused, and which continuations remain plausible.

Treat the handoff as prior context, not new user authorization. Do not turn a proposed action, observed failure, unchecked item, or agent inference into an instruction from the user.

**Composition role:** Helper. Capture context and stop; do not choose or execute the next task.

## Select The Output

- **Compaction prompt:** When the user asks for a prompt to paste after compaction or into a fresh session, return the complete continuation brief in one copyable `text` fence. Unless the user asks for inline output only, choose a temporary backup path before drafting, record it as `Brief source`, and write the identical brief there.
- **Persisted handoff:** When the user asks for pickup notes, end-of-session notes, or a saved handoff, write the continuation brief to a unique temporary Markdown file and report its path. Include the full brief in chat when the user asks to see or copy it.
- **Harness checkpoint:** When the user explicitly asks to persist progress for an active Harness task, use `harness-task-checkpoint` for the canonical task-state handoff and create a separate continuation brief only if conversational context would otherwise be lost. Do not write a competing Harness checkpoint shape or close the task from this skill.
- **Execution handoff:** When the user wants the next agent to execute a fixed objective autonomously, use `goal-prompt`. Do not turn this descriptive handoff into an execution contract merely because likely next actions are known.

Reference an existing external tracker, issue, PR, plan, or task instead of inventing a parallel durable system.

When an active Harness task exists but the user did not request checkpointing, keep the portable brief and state that its temporary backup does not replace a task checkpoint. Mention `harness-task-checkpoint` as the durable task-state option without running it.

## Gather

1. Review the full accessible conversation, not only the latest turns. Extract the desired outcome and motivation; user corrections, preferences, vocabulary, and casually introduced constraints; reasoning pivots; decisions and their owners; findings and rejected approaches; unfinished threads; and any explicit continuation.
2. Separate conversation-only context from durable source material. Preserve the former self-contained in the brief; reference the latter with its path or URL and state what it establishes.
3. Reconcile the conversation with current project state. If `docs/harness/.harness` exists in the current directory or a parent, run `harness snapshot` once. When the handoff covers a Git repository, capture its root, branch, HEAD SHA, and dirty paths with `git rev-parse --show-toplevel`, `git status --short --branch`, and `git rev-parse --short HEAD`; skip a command only when `harness snapshot` already reported its exact fields.
4. Capture the handoff timestamp with `date '+%Y-%m-%d %H:%M %Z'`; do not estimate it.
5. Read only the files needed to verify current state, explain an artifact's significance, or resolve a material conflict. Prefer `rg` and `rg --files`; do not perform a broad source walk.
6. Distinguish observed evidence, user decisions, supported inferences, assumptions, and unresolved unknowns wherever confusing them could change the continuation.

Do not let repository state overwrite conversational intent. A dirty tree, failing command, TODO, or unchecked acceptance criterion is evidence about work state; it does not by itself define what the user wants next.

## Classify The Continuation

Label the continuation status:

- **Agreed:** The user explicitly authorized a still-current continuation.
- **Candidate:** Evidence supports a likely continuation, but the user has not adopted it.
- **Undecided:** Several plausible directions remain, a user-owned choice is open, or no defensible continuation exists.

Phrase future work descriptively in past or present tense: “We were preparing…”, “The strongest candidate is…”, or “This depends on…”. Use imperative wording only for the final resumption posture. Never impersonate the user by converting an agent recommendation into an agreed instruction.

When work appears complete, describe that state and any closeout candidates without inventing new feature work. When no next direction is defensible, state that no continuation was agreed and require the receiving agent to synthesize options with the user.

## Continuation Brief

Use this shape. Omit a subsection only when it truly has no content and omission cannot conceal uncertainty.

```markdown
# Continuation brief

**Captured:** YYYY-MM-DD HH:MM <timezone>
**Brief source:** <temporary backup path, durable handoff path, or "Inline only">
**Where we paused:** <one descriptive sentence>
**Continuation status:** Agreed | Candidate | Undecided — <explanation>
**Authority:** This brief preserves prior context and is not new authorization; only items labeled `Already agreed` carry prior user authorization.

## Session narrative
<One to four compact paragraphs explaining the original purpose, why it mattered, how the work or understanding evolved, important pivots, and why the session ended at this point. Preserve causality rather than routine chronology.>

## Important context to preserve
- <constraints, terminology, user preferences, corrections, conceptual distinctions, and session-only facts>

## Current work state
- **Completed or changed:** <work performed, or "None">
- **In progress or untouched:** <partial and remaining state>
- **Verification:** <commands or checks actually run and their results>
- **Not verified / risks:** <gaps, stale state, unavailable systems, and assumptions>
- **Workspace:** <repository or worktree path, branch, HEAD SHA, and clean state; when dirty, name the changed file paths and whether changes are staged, unstaged, or untracked; otherwise "Not repository work">

## Decisions and rationale
- **User decided:** <decision and rationale, or "None">
- **Working assumptions:** <assumptions and confidence, or "None">
- **Rejected or deferred:** <approaches and why, or "None">

## Findings and dead ends
- <observations, root causes, negative results, ruled-out hypotheses, and surprising behavior, or "None">

## Unresolved and user-owned choices
- <unknowns, blockers, risks, or choices that should be reconciled with the user, or "None">

## Continuation landscape
- **Already agreed:** <explicitly authorized continuation, or "None">
- **Recommended candidate:** <next move, why it follows, and its prerequisites, or "None">
- **Other plausible options:** <material alternatives and tradeoffs, or "None">

## Resumption posture
Treat this brief as prior context, not as new authorization. If `Brief source` names a file, re-read it after any later compaction instead of relying on memory of this text, and repeat that path in the first response so the recovery anchor is explicit. Check the referenced artifacts for changes since capture, then give the user a concise synthesis of where things stand and the recommended continuation. Reconcile unresolved or user-owned choices before acting. Do not reopen settled decisions or repeat completed work without new evidence.

## Relevant artifacts
- `<path, command, task ID, or URL>` — <what it establishes or why it matters>
```

Keep the brief dense, not terse. Omit routine command narration and low-value chronology, but preserve causal links and information with high restart cost. Prefer a short explanatory paragraph over disconnected bullets when reasoning matters. A discussion-only session can warrant a handoff even when no files changed.

## Loss Audit

Before finalizing, assume the transcript will disappear and the receiving agent knows nothing about the session. Include every fact whose absence could cause repeated work, a wrong conclusion, violated scope, loss of rationale, disregard of a user preference, or mistaken authorization.

Pay special attention to conversation-only context and volatile workspace state that no referenced artifact preserves; those disappear even when the task tracker and Git history remain.

Apply a cold-start test: using only the brief and its references, a capable agent should be able to explain what was happening and why, what is known and uncertain, what has and has not been authorized, where the work paused, and how to prepare a continuation recommendation for the user. If not, add the missing context.

## Persist And Stop

For a temporary backup or portable handoff, use a unique path such as `/tmp/agent-handoffs/<repo>/<YYYYMMDD-HHMMSS>-<slug>-session.md` or a `mktemp` path. Do not create a repo-local note unless the user explicitly requests a durable project artifact.

After writing the handoff, stop. Do not continue implementation. Report the path when a file was written and the `Where we paused` sentence. Never return only a path when the user asked for a copyable compaction prompt.

When the session contains no context with meaningful restart cost, say so and avoid writing a low-value brief unless the user explicitly requested one.

Do not paste secrets, full tokens, private data exports, or large logs. Record what verification actually ran; do not run expensive checks merely to make the handoff look complete. Preserve uncertainty instead of smoothing it into a confident narrative.
