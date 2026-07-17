# Model And Effort

Use model and effort as separate levers when creating workflows, delegated jobs, or handoff prompts.

## Rules

- Any script or workflow that invokes the upstream `claude` executable directly (including
  `claude -p` or `claude --print`) must pass an explicit `--model <model>` in argv for every
  invocation. Never rely on Claude settings, environment variables, or an inherited configured model
  for scripted execution. `claude-headless run --spec` requires a non-empty `model` in the
  JobRequest and passes it through; callers that bypass that interface remain outside its request
  validation.

- **Fix context first.** If an answer is poor because the prompt, scope, files, tools, or skills were wrong,
  improve those before changing model or effort.
- **Model is capability.** Use stronger models for ambiguity, unfamiliar domains, subtle bugs, architecture,
  security-sensitive reasoning, and final review. Use cheaper models for precise mechanical edits, bounded
  extraction, and checks where the needed context is already supplied.
- **Effort is thoroughness.** Raise effort when success depends on reading more files, trying multiple steps,
  running tests, or double-checking. Keep the model's default effort when unsure; lower effort only for
  mechanical, externally-checkable work.
- **Current-session settings are fixed.** You cannot change your own current model or effort mid-session; this
  guidance applies to spawned agents, workflows, and prompts you prepare for another session.
- **Keep platform terms distinct.** Claude effort is not Codex reasoning effort, and neither is the
  "minimum effort bar" used in research-loop specs.

## Applies to

Subagent prompts may choose a model when the tool exposes one. Workflow `agent()` calls, delegated Claude
jobs, and goal/workflow handoffs may also choose effort when that runtime exposes it. If a specific skill
gives tighter model/effort instructions, follow that skill.
