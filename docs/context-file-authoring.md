# Context File Authoring

Use this as the craft rubric when writing or slimming the always-on context layer: `CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, and `@` references. `skill-authoring-principles.md` is the sibling rubric for skills; this document covers everything that loads *before* the agent knows the task.

Calibrated for the Claude 5 generation (Opus 5, Fable 5). Older models needed guardrails these files should no longer carry.

## Core Test

Context is loaded across every request, so it cannot be as specific as a prompt. The question is never "is this true?" but "does this change behavior on a run where I did not anticipate the task?"

Ask of each line:

- Would the agent do something different without this line?
- Is this already implied by the harness system prompt, the file tree, or the code itself?
- Does this contradict anything else the agent will load in the same session?
- Is it needed on *every* run, or only on some?

The last two questions do most of the work. Contradiction costs reasoning budget, not just tokens: an agent holding "leave documentation as appropriate" and "DO NOT add comments" must resolve the conflict before it can act.

## Layers

Place each instruction in exactly one layer. Duplication across layers is the most common defect.

| Layer | Holds | Cost |
|---|---|---|
| Harness system prompt | Product behavior. Not yours to edit. | — |
| `~/.claude/rules/` | Cross-project personal standards. | Always-on, every session **and every subagent** |
| Project `CLAUDE.md` | What this repo is; its gotchas. | Always-on in this repo and all descendants |
| Traveling docs (`~/.claude/docs/`) | Contracts and rubrics consulted mid-task. | Only when referenced |
| Skills | Opinionated procedures. | Description always-on; body on invocation |
| `@` references | Specs, mockups, test suites, code to port. | Inlined at launch when imported |

Push an instruction to the narrowest layer that still reaches the run that needs it.

## Judgement Over Rules

Write the principle, not the prohibition. A hard rule is wrong for some subset of prompts, and the agent cannot tell which subset it is in.

Prefer:

- "Write code that reads like the surrounding code: match its comment density, naming, and idiom."

Avoid:

- "Default to writing no comments. Never write multi-line comment blocks — one short line max."

Reserve absolute rules for cases where the worst outcome is unacceptable and judgement genuinely cannot substitute: destructive commands, credential handling, external-effect gates, hard operational invariants. Those stay explicit. Style preferences do not.

A rule stated as an absolute that the agent will correctly violate teaches it to discount the whole file.

## Retired Practices

These were correct for earlier models and are now defects.

| Retired | Current |
|---|---|
| Enumerate rules for every case | State the principle; let the model judge |
| Give examples of tool/format usage | Design expressive interfaces; examples narrow the exploration space |
| Put everything upfront so it is never missed | Progressive disclosure — a tree of files loaded when relevant |
| Repeat key instructions in several places | One home per meaning; put tool guidance in the tool description |
| Size the file by project LOC | Size by how many real gotchas exist |
| Ship a template to fill in | Write the specific repo's actual constraints |
| `CLAUDE.md` as durable memory | Memory, artifacts, and skills — or an explicit capture surface |

## What Belongs In A Project CLAUDE.md

Briefly say what the repo is for, then spend the tokens on **gotchas**: the things that are costly to discover and not visible from the file tree.

Belongs:

- Non-obvious invariants ("`harness-core` must stay zero-dependency").
- Commands that are not guessable, and the ones that are expensive to get wrong.
- Traps with consequences ("killing the local orchestrator does not stop the remote run").
- Layout choices an agent would otherwise violate ("all types in one file, nowhere else").
- Verification that must run, when it is not discoverable from CI config.

Does not belong:

- Anything readable from the file tree, `pyproject.toml`, or the lockfile.
- Restating the harness system prompt or a global rule.
- Architecture prose that will drift out of date. Point at code instead.
- Volatile status. Derive it from the project's own tracking state.

## Dual Surface: CLAUDE.md And AGENTS.md

Claude Code reads `CLAUDE.md` only — it does **not** read `AGENTS.md`. Codex reads `AGENTS.md`. A repo serving both must not hand-maintain two copies; they drift, and the drift is silent.

- Content identical → make `CLAUDE.md` a **symlink** to `AGENTS.md`. Zero drift, zero maintenance.
- A genuine Claude-only delta exists → `CLAUDE.md` holds `@AGENTS.md` plus only the delta.

A Claude-only delta is real when it concerns harness-specific behavior: background tasks, subagent delegation, tool semantics. It is not real when it is the same repo knowledge reworded.

`@` imports **do not save tokens** — the imported file is inlined at launch, at the same cost as pasting it. Import for one-source-of-truth, never for context savings. Savings come only from deleting content. Imports nest to 4 hops.

## Progressive Disclosure

Always-on cost is paid on every session and every subagent, including runs where the content is irrelevant. Move conditional material out.

Three mechanisms, in order of preference:

1. **`paths:` frontmatter on a rule** — the rule loads only when the agent reads a matching file. Native and free. Use it when relevance tracks file location.
2. **A traveling doc referenced from the skills that need it** — use when relevance tracks *task type* rather than file path, which `paths:` globs cannot express.
3. **Nested `CLAUDE.md` in a subdirectory** — loads on demand when the agent reads there. Good for per-package conventions in a monorepo.

Do not externalize material needed on every run just to shorten a file. That trades one always-on cost for an always-on cost plus a round-trip.

## Claim breadth

When a context-file proposal generalizes from observed behavior, conditionally open the Agents-owned `docs/claim-discipline.md` reference before choosing its loading layer. The broader the loading surface, the more evidence is required that the rule applies across that surface. Keep behavior project-, path-, task-, or skill-specific until independent evidence justifies broader placement.

## Environment Activation

Not a context file, but the piece of project setup that is easiest to get wrong and least visible when it is missing. A project with a virtual environment needs its activation appended to `$CLAUDE_ENV_FILE` at session start, or every Bash call silently runs against the wrong interpreter:

```json
"hooks": {
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "echo 'ACTIVATION_CMD' >> \"$CLAUDE_ENV_FILE\""
    }]
  }]
}
```

Do not document the activation command in `CLAUDE.md` as a step for the agent to remember. Make the environment correct instead.

## References

Prefer references in code. A language the model already knows carries higher fidelity than prose about it.

- An HTML mockup beats a description of a design or a screenshot of one.
- A test suite is a better spec than a spec document.
- A function in another codebase is the clearest instruction for porting.
- A rubric lets a verifier agent check taste that prose cannot pin down.

Reach for prose only for intent and constraints that no artifact encodes.

## Pruning

Duplication, sediment, no-op, and sprawl are defined in `skill-authoring-principles.md` §Pruning and apply here unchanged. Two failure modes are specific to context files:

- **Cross-layer duplication** — the same meaning in a global rule and a project file, or in a file and the system prompt. Delete the broader copy; keep the one closest to where it applies.
- **Stale authority** — a context file that confidently describes an architecture the code has since moved past. It outranks the code in the agent's attention and produces confidently wrong work. Prefer pointing at code over describing it.

When cutting, verify what actually loaded with `/context` rather than assuming.

## Attribution

The retired-practices framing and the judgement-over-rules examples are adapted from Anthropic's "The new rules of context engineering for Claude 5 generation models" (Thariq Shihipar, July 2026).
