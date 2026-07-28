# Model And Effort

Any script or workflow that invokes the upstream `claude` executable directly — including `claude -p` and `claude --print` — must pass an explicit `--model <model>` in argv on every invocation. Never rely on Claude settings, environment variables, or an inherited configured model for scripted execution. `claude-headless run --spec` requires a non-empty `model` in the JobRequest and passes it through; callers bypassing that interface are outside its request validation.

When choosing model and effort for a subagent, workflow `agent()` call, delegated job, or handoff prompt, read `~/.claude/docs/model-and-effort.md`.
