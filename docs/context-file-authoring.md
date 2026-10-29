# Context File Authoring

Use this portable craft rubric when writing or revising standing instruction files and their conditional references. It covers wording, maintained ownership and provider loading; use the project's own setup policy and existing documentation owners for its procedures. No personal context repository is required. `docs/skill-authoring-principles.md` is the sibling rubric for skills.

## Create Or Update Project Instructions

For a request to initialize or maintain project instructions, use this document directly; no initializer skill or personal context repository is required. Inspect the actual project before writing: existing instructions, README/development docs, package and environment configuration, supported entrypoints, and checks. Verify commands and prerequisites where feasible; label anything unverified rather than inventing a command or constraint.

Keep `AGENTS.md` as the common project baseline. Preserve useful existing content and names, patch only the affected guidance, and add provider-specific files only for a requested or demonstrated runtime need. Capture purpose, consequential non-obvious constraints, ownership boundaries, and verified entry commands or links; do not enumerate the file tree or fill a template. Ask only when a load-bearing choice belongs to the operator and cannot be resolved from the project.

Make diagnosis discoverable from existing development docs: how to reproduce or inspect the relevant component, prerequisites, useful output or state, expected success signals, and safe recovery limits. Prefer the existing CLI or runbook; add a helper only for a demonstrated recurring gap. Generic `diagnose` and `logging-optimize` skills supply methods, not the project's commands. Verify these routes when writing instructions rather than substituting “debug carefully.”

## Current Guidance And Historical Records

Root instructions are entrypoints; maintained project docs own current architecture, commands, contracts, setup, and debugging guidance. Put a subsystem rule near that subsystem only when it genuinely differs. Investigation evidence, past decisions, experiment records, and completed work belong in the project's existing history store, including Harness where used; do not add a parallel `records/` store. Active plans and tasks remain working state. Personal preferences stay in the operator's context source; reusable procedures stay with their source owner.

When a change alters a documented command, contract, ownership boundary, or workaround, update its current authoritative guidance in the same change and link to it from other entrypoints. Preserve historical evidence; mark superseded guidance when it remains relevant to interpreting that history. A completed task or transient result is not automatically a new standing instruction.

A verified surprise is a consequential constraint an agent reasonably missed because it was hard to discover. First remove the trap in code, configuration, or a check when feasible. Otherwise place the actionable explanation where the next affected task will encounter it and retain decisive evidence in the existing project record. Repeated costly rediscovery or one consequential non-obvious failure can justify an instruction; an obvious convention cannot. Remove the workaround when its cause disappears. Do not append automatic lesson lists or rewrite unrelated instructions.

## Core Test

Standing instructions serve varied tasks; conditional references can be task-specific. Check both accuracy and operational value: what supported task changes because this instruction is present, and what would fail without it?

Ask of each line:

- Would the agent do something different without this line?
- Does an existing artifact already supply this information, and will the supported reader find it before acting?
- Does this contradict anything else the agent will load in the same session?
- Is it needed on *every* run, or only on some?

Resolve conflicting instructions at their maintained owner rather than expecting the agent to guess an exception. Use task-triggered routes for detailed guidance; an ordinary Markdown link does not itself load its target.

## Layers

Give each fact one maintained owner. A root may retain a short boundary or routing reminder when contributors cannot be assumed to load that owner. Remove duplicate procedures, conflicting copies and reminders with no distinct audience or trigger. Before deleting a project rule because a global file repeats it, verify the supported contributors' loading paths; essential standalone boundaries must remain reachable before the relevant action.

For repository-managed distribution, reuse portable skill bodies through the catalog rather than maintain separate source forks for each runtime output. Shared-home skills are discovered once as complete implementations; they are not bases for same-name provider overlays. A provider global instruction file can remain a deliberate counterpart when its tools, approvals or child behavior differ, as Pi's global `AGENTS.md` does. Edit the owning source and reconcile its installed outputs through the owning installer.

The table illustrates Claude's loading surfaces; for another provider, use its supported instruction and reference mechanisms rather than creating Claude files. Provider selection and exclusions matter; see [Loading notes](#loading-notes).

| Layer | Holds | Loading |
|---|---|---|
| Harness system prompt | Product behavior. Not yours to edit. | — |
| Global `~/.claude/CLAUDE.md` (runtime-home) | Cross-project Claude controls without a narrower rule file. | User instruction surface; actual selection depends on runtime configuration and agent type |
| `~/.claude/rules` (runtime-home) | Cross-project personal standards. | User rules; actual selection depends on runtime configuration and agent type |
| Project `CLAUDE.md` or selected `AGENTS.md` | Project purpose, essential boundaries and task routes. | Ancestor instructions at launch; nested instructions on demand, subject to selection and exclusions |
| Traveling docs (`~/.claude/docs` (runtime-home)) | Contracts and rubrics consulted mid-task. | Only when referenced |
| Skills | Opinionated procedures. | Metadata and body loading depend on runtime and invocation policy |
| `@` references | Specs, mockups, test suites, code to port. | Expanded with the importing instructions; imported text consumes context |

Push an instruction to the narrowest layer that still reaches the run that needs it.

## Judgement Over Rules

Use principles for choices that legitimately depend on context. Use explicit requirements for safety, authority and operational invariants; state their scope and exceptions. A prohibition with a concrete consequence can be clearer than an abstract principle.

Prefer:

- "Write code that reads like the surrounding code: match its comment density, naming, and idiom."

Avoid:

- "Default to writing no comments. Never write multi-line comment blocks — one short line max."

Keep destructive-command, credential-handling, external-effect and hard operational boundaries explicit. Style guidance should reflect the project's real contract rather than an arbitrary restriction.

An absolute that conflicts with legitimate tasks creates ambiguity; narrow its scope instead of expecting the agent to guess the exception.

## Patterns To Reconsider

Reconsider these patterns when they add irrelevant context or duplicate an existing interface; they are not universally obsolete.

| Pattern | Alternative when applicable |
|---|---|
| Enumerate rules for every case | State a scoped principle while retaining consequential requirements |
| Give examples of tool/format usage | Keep examples that disambiguate a non-obvious command, format or boundary; omit ones that duplicate a clear interface |
| Put everything upfront so it is never missed | Keep essential boundaries at entry; route detailed guidance by task |
| Repeat key instructions in several places | One maintained owner, with boundary reminders where audience or loading requires them |
| Size the file by project LOC | Include what supported tasks need, without line or word quotas |
| Ship a template to fill in | Write the specific repo's actual constraints |
| Instruction files as an investigation log | Retain standing guidance here; keep evidence and results in the existing record store |

## What Belongs In Root Project Instructions

Briefly say what the repo is for. Keep essential boundaries and consequential shared constraints, then route tasks to their detailed owners. A pure index can hide a boundary until after an action violates it.

Belongs:

- Non-obvious invariants ("`harness-core` must stay zero-dependency").
- Commands that are not guessable, and the ones that are expensive to get wrong.
- Traps with consequences ("killing the local orchestrator does not stop the remote run").
- Layout choices an agent would otherwise violate ("all types in one file, nowhere else").
- Required checks, their triggers and limits, or a direct route to their maintained commands.

Does not belong:

- Inventories and explanations that add no operational value beyond existing artifacts. A concise supported command or consequential constraint can still establish the project contract.
- Duplicate procedures or reminders with no distinct audience or trigger. Do not depend on an operator's private globals for essential project boundaries.
- Detailed architecture prose already owned by maintained project docs. Link its owner; do not substitute today's implementation for an intended contract.
- Volatile status. Derive it from the project's own tracking state.

## Local Bindings

For necessary user/host path exceptions, use an optional ignored `AGENTS.local.md`, with a small tracked example only when useful. Keep one canonical actual copy per host/checkout family accessible from worktrees; a checkout can link to it. Bindings point to existing configuration/access routes, carry no credentials or authority and cannot override shared policy. Include known remote bindings only where needed; avoid machine inventories and derivable values. Missing bindings do not block ordinary reading/small edits, but consequential unknown destinations must be resolved before launch.

Explicitly route reading from shared project instructions, for example: “Before substantial generated work, read `AGENTS.local.md` if present (worktrees use the canonical checkout copy), then resolve outputs through README's configured output locations; record actual host/path in the task.” Name the real canonical route when adopting this example. Do not assume automatic additive loading or use `AGENTS.override.md` to replace the root baseline. Keep detailed output/retention rules at existing project owners, using supported flags and native roots rather than another settings system.

## Dual Surface: CLAUDE.md And AGENTS.md

`AGENTS.md` is the common project baseline. Claude's project-instruction selection can load it directly or use `CLAUDE.md`; a compatibility file must preserve access to the baseline. A repo serving both must not hand-maintain two copies; they drift, and the drift is silent.

- Content identical → a regular `CLAUDE.md` containing only `@AGENTS.md` is a first-class compatibility option, including when there is no Claude-specific delta. Prefer this import-only wrapper for repositories supporting Windows.
- A **symlink** from `CLAUDE.md` to `AGENTS.md` is also appropriate when every supported checkout preserves symlinks. Keep a working link in such an environment rather than changing it for symmetry.
- A genuine Claude-only delta exists → `CLAUDE.md` holds `@AGENTS.md` plus only the delta.

With Git symlink support disabled, Windows can check out a committed link as a regular file containing its target filename rather than the baseline instructions. A regular import wrapper avoids that failure. See Anthropic's [shared-file guidance](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools); wrapper contents and import-path resolution can be checked locally, while actual loading must be confirmed in the target provider session.

A Claude-only delta is real when it concerns harness-specific behavior: background tasks, subagent delegation, tool semantics. It is not real when it is the same repo knowledge reworded.

Claude `@` imports keep one maintained source. Imported text expands with the importing instructions and consumes context; a startup import is not progressive disclosure. Resolve paths relative to the importing file, not the working directory; nesting is limited to four hops. Remove unnecessary text or defer genuinely conditional material instead of moving it into an unconditional import.

## Progressive Disclosure

Move genuinely conditional material out of the always-loaded layer; check the actual loading chain. Choose by trigger, not a universal ranking:

- **Task-directed link:** name when to open a maintained document. Use it when relevance follows a task rather than a path. This rubric's [Claim breadth](#claim-breadth) route names when to open `docs/claim-discipline.md`, the maintained owner for generalizing observations into reusable guidance.
- **Runtime import:** loads the target with the importing instructions. Use it to preserve a common baseline, not to defer unrelated procedures.
- **Path-scoped or nested instructions:** use a real subsystem boundary and the target provider's supported discovery behavior. A filename's location alone does not establish that every runtime discovers it before an action.

Keep routes reachable before the relevant action. Avoid reading loops and blanket instructions to read every linked guide. Do not externalize material needed on every run just to shorten a file.

## Loading Notes

The Codex and Claude notes follow official documentation checked on 2026-10-07; they describe supported mechanics, not proof of loading in a local session. The Pi entry records separately version-qualified installed-source and native-loader evidence.

- **Codex:** [startup discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) builds the instruction chain once per run. It selects the first non-empty global `AGENTS.override.md` or `AGENTS.md`, then at most one instruction file per directory from the project root to the starting working directory, with overrides and configured fallback names. Do not assume arbitrary nested files open automatically during a task or that Claude's `@` semantics apply.
- **Claude Code:** [project selection](https://code.claude.com/docs/en/memory#agentsmd) can read `AGENTS.md` natively from v2.1.277, subject to version/session support and the Project instructions setting. By default, a `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above selects Claude files instead; an import wrapper preserves the shared baseline in that case. Ancestor instructions load at launch; nested project instructions load on demand. [Path-scoped rules](https://code.claude.com/docs/en/memory#path-specific-rules) trigger on matching Read, Write or Edit access, not every tool use. Subagents may skip project instructions. Consult the official documentation for settings and exclusions rather than assuming every session or agent loads the same chain.

- **Pi:** installed Pi 1.3.0 source and native loader checks verified on 2026-10-17 load global context from the selected agent home (`PI_CODING_AGENT_DIR`, default `~/.pi/agent` (runtime-home)) and project context from the working directory's ancestors. Pi selects one recognized context filename per directory (`AGENTS.override.md`, `AGENTS.md`, `AGENTS.MD`, `CLAUDE.md`, or `CLAUDE.MD`); existing project `AGENTS.md` files need no conversion. Reading a descendant file does not prove that its directory's instructions were loaded, so inspect applicable narrower instructions before editing. Do not assume Claude `@` imports work in Pi context files or replace Pi's normal `SYSTEM.md` for ordinary instructions. Child global/project instruction and skill inheritance depends separately on the installed subagent extension and agent settings; parent loading does not establish child loading. Project resource trust and context loading are separate mechanisms.

For other providers, check their supported discovery and reference mechanisms before choosing a surface. This guide does not establish Devin's automatic loading behavior.

## Claim breadth

When a context-file proposal generalizes from observed behavior, conditionally open the Agents-owned `docs/claim-discipline.md` reference before choosing its loading layer. The broader the loading surface, the more evidence is required that the rule applies across that surface. Keep behavior project-, path-, task-, or skill-specific until independent evidence justifies broader placement.

## Environment Activation

Inspect the project's actual execution path before adding activation. A virtual environment alone does not imply a session hook: commands such as `uv run`, an explicit environment interpreter, or an existing launcher can already select the correct environment. Preserve a working path and verify that supported commands use the intended interpreter and dependencies.

For Claude Code only, when project commands depend on shell activation that is otherwise missing, a `SessionStart` hook can append the verified activation command to `$CLAUDE_ENV_FILE` for subsequent Bash calls. This is a conditional Claude configuration example, not a requirement for Codex or Devin projects:

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

Prefer a reliable launcher or runtime-supported environment setup over a reminder to activate before every call. Document the supported execution command and prerequisites; do not add Claude hooks to a Codex/Devin-only project or replace a working explicit environment command merely because a virtual environment exists.

## References

Prefer the artifact that answers the question: code for implemented behavior, tests for checked outcomes, specifications for intended contracts, and prose for purpose, rationale and constraints. Mockups, porting examples and rubrics can make an ambiguous target concrete. Link maintained owners rather than copying them; no artifact type universally outranks the others.

## Pruning

Use the duplication, sediment, no-op and sprawl questions in `docs/skill-authoring-principles.md` §Pruning, with the ownership and reach qualifications in [Layers](#layers). Two failure modes need particular care in context files:

- **Cross-layer duplication** — remove competing procedures and copies without a distinct consumer; preserve essential standalone boundary reminders. Verify supported loading paths before deleting a broader or narrower copy.
- **Stale authority** — resolve disagreement between current guidance, accepted contracts and implementation at the affected owner. Code shows implemented behavior; it does not automatically override an intended contract or safety boundary. Mark proposals and superseded guidance explicitly.

Inspect the full affected diff, links, wrapper targets and distributed reference closure. Walk representative tasks from entry to the affected owner, retaining boundaries, prerequisites, checks and recovery limits without unrelated loading. Use existing proportional checks; do not add tests that merely freeze prose. Verify actual loading in a fresh target-provider session when runtime behavior changes: Claude's `/context` lists memory files. Static link and packaging checks are not live loading evidence; protected runtime files and transcripts retain their applicable read gates.

## Attribution

The reconsideration framing and judgement-over-rules examples are adapted from Thariq Shihipar's [“The new rules of context engineering for Claude 5 generation models”](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/), published 2026-07-24. It reports prompt reduction on particular Claude models and coding evaluations; it does not establish that every example, prohibition or repeated boundary is defective, or measure this repository's guidance. No effectiveness improvement follows merely from a shorter file.
