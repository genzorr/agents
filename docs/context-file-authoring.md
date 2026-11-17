# Context File Authoring

Use this reference when writing or revising agent instructions. The [project-document guide](project-documents.md) explains how to write the README, specs and architecture. This page owns instruction placement, local files, provider wrappers and loading mechanics. It works as an ordinary document; no initializer skill or private context repository is needed.

## Create Or Update Project Instructions

Read the actual project entry, relevant docs, command/configuration sources and applicable instructions before writing. Preserve useful names and local commitments. Verify commands where authorized; mark an unverified command or environment rather than inventing one.

Write the project purpose, consequential local boundaries and routes for the reader's tasks. A limited current-docs listing can help discovery; a complete source inventory usually cannot. Link the command owner for setup, checks and diagnosis. Add a narrower instruction only when the subsystem genuinely needs a different rule.

For example: “Before changing batch import, read `docs/import-batches.md` (example-only). Run the focused checks in `docs/development.md` (example-only). Use an isolated store for demonstrations.” This names the action, relevant owner and boundary before a write. “Follow best practices” does none of those jobs.

## Current Guidance And Historical Records

Keep current requirements, architecture, commands and recovery at their maintained project owners. Keep active plans and investigation results in the existing work system. Preserve original reports and evidence; a later correction adds context without changing what the original said.

Update a documented fact with the change that affects it. A repeated failure may reveal a missing instruction, but first consider fixing the command, configuration or check that creates the trap. Add the instruction where the next affected task will encounter it, and remove an obsolete workaround when its cause disappears. Finishing a task does not require a new standing rule.

## Core Test

Ask what the reader will do differently because of the passage. Keep it if it explains a real boundary, removes a likely mistake or helps find necessary information. If it repeats another page, link that page with a clear reason to open it.

Check that the supported reader reaches essential rules before acting. A short entry can still fail if the critical constraint is hidden behind an optional link. Resolve contradictory instructions at their source rather than making each agent guess which one matters.

## Layers

| Location | What belongs there | Example |
| --- | --- | --- |
| Provider global source | Cross-project working defaults and actual provider controls | How to continue an authorized fix; provider-specific permission/delegation behavior |
| Project root entry | Purpose, shared local constraints, relevant reading/command routes | Which record store and checkout to use; isolated demo requirement |
| Nested instructions | A real area-specific difference | A hardware subtree's required bench procedure before operation |
| Conditional document | Detailed explanation or procedure needed for certain tasks | Export recovery or instruction loading mechanics |
| Optional local binding | Necessary machine-specific paths or access routes | An existing output mount or canonical checkout locator |
| Skill | A reusable procedure with a clear trigger and observable result | Preparing unsettled behavior or reviewing a coherent change |

Use the narrowest location that still reaches everyone who needs it. Essential contributor constraints cannot depend solely on one person's private globals. A shared boundary reminder may be necessary at entry; do not duplicate its complete procedure there.

Installed files are outputs of their source owner. Change the owning source and reconcile through its supported installer. A shared skill is a complete implementation, not a base to combine with a same-name provider skill. Keep provider counterparts when tools, permissions, invocation or support files differ.

## Judgement Over Rules

Explain the behavior and reason in ordinary language. Prefer “Match the surrounding code's comment style; explain surprising constraints” to arbitrary sentence or line limits. Keep explicit safety, privacy, authority and operational rules when their consequence warrants them, with their actual scope and exceptions.

A short absolute is not necessarily simpler than a precise conditional rule. “Never run tests” hides useful distinctions; “Do not start the hardware test without the bench reservation and operator release” states a concrete boundary.

## Patterns To Reconsider

| Pattern | Better fit when applicable |
| --- | --- |
| Everything loaded at startup | Essential boundaries at entry, with task-specific links for details |
| A second full procedure in every project | One maintained procedure plus the project's concrete commands and limits |
| Root instructions as an investigation diary | Current routes here, original evidence in the existing record owner |
| Identical provider files maintained separately | Common project baseline plus supported wrappers or a real provider delta |
| A template with empty required sections | The information this project's readers actually need |
| A rule for every observed failure | Fix the recurring mechanism; preserve a scoped explanation only where needed |

## What Belongs In Root Project Instructions

State what the repository owns and what contributors must know before changes. Give task-directed routes to behavior, architecture, commands and records. Include a supported command directly when it is short and important to get right; otherwise route to its owner.

Keep the full architecture, volatile status and historical argument elsewhere. Do not strip an essential boundary merely because a global file repeats it; an independent contributor may not have that global file.

## Project Artifact Conventions

The project's development/operations page should identify supported input/output locations, prerequisites, large-work resource limits and retention responsibility. Use native flags and configuration. Name actual host and output locations in the existing task for substantial runs; a path in a record does not back up its bytes.

Preserve useful partial results, unpublished source and live dependencies before separately authorized cleanup. Shared caches, controller state and retained results can have different owners. A worktree or completed task does not grant deletion authority.

## Local Bindings

Create an ignored `AGENTS.local.md` only when there is real local information to keep there. A project with no machine-specific exceptions needs no local file or empty example. Local bindings hold locators and applicable setup facts, not credentials, a second policy or new permission.

Explicitly route the read before it matters: “Before a large run, read `AGENTS.local.md` if present, then resolve outputs through development guidance.” Missing local bindings do not block reading or ordinary small edits. Resolve a consequential unknown destination before executing the dependent run.

If several worktrees use one binding, identify the real canonical copy and make it reachable by the project's supported arrangement. Do not assume all providers load `AGENTS.local.md` automatically. Do not use a provider's override filename as an additive local note; it may replace the shared baseline.

## Dual Surface: CLAUDE.md And AGENTS.md

Use one common project baseline. In a project that needs a Claude compatibility entry, the regular file can contain:

```text
@AGENTS.md
```

Put a genuine Claude-only delta below the import. A working symlink can remain where supported; a regular import wrapper avoids reliance on Git symlink support in Windows checkouts. Do not maintain two copies of the same project prose. Provider global files remain separate artifacts.

## Progressive Disclosure

The [document-writing page](project-documents.md#find-the-document-before-reading-it) owns filename discovery and task-based reading. For instructions, distinguish these mechanisms:

- A **task-directed Markdown link** says when to open a document; it is not an automatic import.
- A **runtime import** loads text with the importing file. It preserves a shared baseline but does not defer its context cost.
- **Nested or path-scoped instructions** depend on the provider's actual discovery and access rules. A file existing in a directory does not prove it was loaded before every tool action.

Keep essential pre-action rules reachable. Avoid a link cycle that sends a reader from the project guide to the authoring guide and back before either answers the question. Do not externalize always-needed text merely to meet a line quota.

## Loading Notes

The Codex and Claude notes follow official documentation checked on 2026-10-07; they describe supported mechanics, not proof of loading in a local session. The Pi entry records separately version-qualified installed-source and native-loader evidence.

- **Codex:** [startup discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) builds the instruction chain once per run. It selects the first non-empty global `AGENTS.override.md` or `AGENTS.md`, then at most one instruction file per directory from the project root to the starting working directory, with overrides and configured fallback names. Do not assume arbitrary nested files open automatically during a task or that Claude's `@` semantics apply.
- **Claude Code:** [project selection](https://code.claude.com/docs/en/memory#agentsmd) can read `AGENTS.md` natively from v2.1.277, subject to version/session support and the Project instructions setting. By default, a `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above selects Claude files instead; an import wrapper preserves the shared baseline in that case. Ancestor instructions load at launch; nested project instructions load on demand. [Path-scoped rules](https://code.claude.com/docs/en/memory#path-specific-rules) trigger on matching Read, Write or Edit access, not every tool use. Subagents may skip project instructions. Consult the official documentation for settings and exclusions rather than assuming every session or agent loads the same chain.

- **Pi:** installed Pi 1.3.0 source and native loader checks verified on 2026-10-17 load global context from the selected agent home (`PI_CODING_AGENT_DIR`, default `~/.pi/agent` (runtime-home)) and project context from the working directory's ancestors. Pi selects one recognized context filename per directory (`AGENTS.override.md`, `AGENTS.md`, `AGENTS.MD`, `CLAUDE.md`, or `CLAUDE.MD`); existing project `AGENTS.md` files need no conversion. Reading a descendant file does not prove that its directory's instructions were loaded, so inspect applicable narrower instructions before editing. Do not assume Claude `@` imports work in Pi context files or replace Pi's normal `SYSTEM.md` for ordinary instructions. Child global/project instruction and skill inheritance depends separately on the installed subagent extension and agent settings; parent loading does not establish child loading. Project resource trust and context loading are separate mechanisms.

For other providers, check their supported discovery and reference mechanisms before choosing a surface. This guide does not establish Devin's automatic loading behavior.

## Claim breadth

When observations are becoming a reusable instruction or default, open [Claim Discipline](claim-discipline.md). The broader the loading surface, the more evidence is required that the rule applies across that surface. Keep project-specific evidence scoped to that project unless a broader basis supports a broader rule. Preserve actual privacy, authority and scientific commitments; uncertainty about effectiveness does not remove those boundaries.

## Environment Activation

Start with the existing execution path. A native launcher, `uv run` or an explicit environment interpreter may already select dependencies correctly. Prefer repairing that path over a repeated reminder to activate something before each call.

A provider hook is a conditional implementation choice when the supported launcher genuinely needs it. Inspect that provider's current documented interface and the selected environment before adding or changing a hook. This guide adds no startup hook or runtime setting.

## References

Read code/configuration for implemented behavior, specs for intended behavior, checks for exercised outcomes and records for provenance. None universally replaces the others. The [skill authoring reference](skill-authoring-principles.md) applies when the work is a reusable skill; it is not required for ordinary project docs.

## Pruning

Remove duplicated procedures, obsolete workarounds and text that does not help the supported task. Preserve essential boundary reminders for distinct readers. Inspect affected links, wrapper targets and distributed dependencies before removing a source.

Walk representative tasks after rewriting. A static link or catalog check establishes reachability/packaging; it does not show that a provider loaded the file or followed it. A loader change needs a fresh supported runtime check under its actual permissions. Use the applicable authority for protected settings, transcripts or credentials when performing that check.

## Attribution

The reconsideration framing and judgement-over-rules examples are adapted from Thariq Shihipar's [“The new rules of context engineering for Claude 5 generation models”](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/), published 2026-07-24. It reports prompt reduction on particular Claude models and coding evaluations; it does not establish that every example, prohibition or repeated boundary is defective, or measure this repository's guidance. No effectiveness improvement follows merely from a shorter file.
