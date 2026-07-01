---
name: codex-project-init
description: Create or update a project-level AGENTS.md for Codex by inspecting the project and capturing commands, boundaries, and conventions.
---

# Codex Project Init

Use when the user wants to initialize Codex instructions for a project.

## Workflow

1. Inspect the project structure:
   - languages and versions
   - package manager and dependency files
   - test, lint, format, and run commands
   - source, docs, tests, scripts, and config layout
2. Read existing project instructions if present:
   - `AGENTS.md`
   - `.claude/CLAUDE.md`
   - `CLAUDE.md`
   - README and contributing docs
3. Ask one concise question only if a load-bearing choice is unclear, such as environment activation, expensive commands, or hard "do not" rules.
4. Write or update `AGENTS.md` with:
   - project purpose
   - key packages/modules and ownership boundaries
   - verified commands
   - coding conventions
   - safety constraints and prohibited changes
   - verification expectations
5. Keep project-specific rules in the project. Keep reusable workflow behavior in Codex skills.

## Rules

- Do not create `.claude/` files unless the user explicitly asks for Claude setup.
- Prefer concise, operational instructions over long essays.
- Put commands near the top.
- Use concrete "do not" rules only when they prevent real breakage.
- If an `AGENTS.md` already exists, preserve useful existing content and make a focused patch.
