# Model And Effort

Read this when choosing model or effort for a subagent, a workflow `agent()` call, a delegated Claude job, or a handoff prompt for another session.

The hard invariant — explicit `--model` in argv for every scripted `claude` invocation — lives in the always-on rule `~/.claude/rules/model-and-effort.md`, not here.

## Separate Levers

**Fix context first.** If an answer is poor because the prompt, scope, files, tools, or skills were wrong, improve those before reaching for a stronger model or higher effort. Model and effort do not compensate for missing context.

**Model is capability.** Use stronger models for ambiguity, unfamiliar domains, subtle bugs, architecture, security-sensitive reasoning, and final review. Use cheaper models for precise mechanical edits, bounded extraction, and checks where the needed context is already supplied.

**Effort is thoroughness.** Raise effort when success depends on reading more files, trying multiple steps, running tests, or double-checking. Keep the model's default effort when unsure. Lower effort only for mechanical work whose result is externally checkable.

## Constraints

- **Current-session settings are fixed.** You cannot change your own model or effort mid-session. This guidance applies only to agents, workflows, and prompts you prepare for another session.
- **Keep platform terms distinct.** Claude effort is not Codex reasoning effort, and neither is the "minimum effort bar" used in research-loop specs.
- A skill giving tighter model/effort instructions overrides this document.

## Agent Reuse

Prefer sending follow-up work to an agent that already holds the context over spawning a fresh one. An implementer that receives review findings should apply its own fixes. Spawning one agent per project, or a separate agent to fix what a reviewer found, multiplies cost for no added judgement.
