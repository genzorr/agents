# Model And Effort

Scripted Claude calls must carry an explicit model: `claude-headless` requests require non-empty `model`, and direct `claude -p`/`claude --print` calls must pass `--model`.

When choosing model and effort for a subagent, workflow `agent()` call, delegated job, or handoff prompt, read `~/.claude/docs/model-and-effort.md`.
