# Global Claude Instructions
<!-- managed-by: genzorr/agents; asset: claude-claude-md -->

This file is the global Claude Code layer installed to `~/.claude/CLAUDE.md`; project-level `CLAUDE.md` instructions take precedence over anything here.

## Scope

Cross-project standards that already have rule files live in `~/.claude/rules` (runtime-home); this file contains only Claude-wide controls without a rule-file twin.

## Background and Long-Running Jobs

- Prefer a tool's native wait or completion signal over a manual check: a background Bash task's completion notice, the Monitor tool, and a spawned subagent's task notification each report back on their own.
- Do not tight-poll a background Bash task, Monitor stream, subagent, Harness Run, or CI check every few seconds; it burns tokens without adding information.
- When polling is unavoidable, use minutes rather than seconds.
- While state is unchanged, emit no update; report only completion, failure, a blocker, an explicit status request, or new actionable output.
- After 10-15 minutes without change, one brief status line is allowed; do not repeat it on a fixed cadence.

## Preserve Thread Model

- Preserve an existing session or thread's model and effort; omit overrides when sending to an existing thread.
- For new subagents or delegated jobs, use requested settings or preserve configured defaults; never upgrade Luna or Terra work to Sol automatically.
- State intentional model or effort overrides before launching new work.

## Permission Denials

- A denied tool call means the user declined it; distinguish that from an application failure before deciding what to do next.
- Do not retry verbatim, broaden the command, invent a workaround, or synthesize a fresh approval gate for an action the user already authorized elsewhere.
