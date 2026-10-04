---
name: integrate-research
description: Compare completed research outputs with source evidence and current project documentation, then summarize findings or apply already-authorized documentation updates while preserving provenance, conflicts, and uncertainty.
---

# Integrate Research

Use this skill for completed research outputs. Use `distill-source` when a supplied paper, article, documentation page, repository, or skill file still needs to be analyzed for what the project should adapt.

## Input

Accept one or more PDF, Markdown, text, or directory paths, an optional `--prompt <path>` for the original research prompt, and free-text guidance. Parse flags and paths separately from ordinary guidance.

## Workflow

1. Read the research output and recover the intended outcome from the original prompt, relevant user steering before and after it, and available task context. The prompt records the outgoing handoff; it does not override user steering or selected decisions. Compare against that outcome, not only the report’s framing. If the prompt or earlier context is unavailable, state that limit and assess what the available evidence supports; ask only when the missing intent changes the next consequential action. Keep source paths, dates, versions, citations, and other provenance attached to the claims they support; an uncited assertion is not project fact.
2. Read the relevant `AGENTS.md` or `CLAUDE.md`, README, current docs/research/drafts, ADRs/specs, and named source or configuration. Compare research claims and citations with current documents and source evidence before deciding what carries over.
3. Before disposition, distinguish factual support from relevance and necessity for the requested artifact or decision. Identify material scope that the report or your proposed uptake omits, adds, replaces, or defers, and why. Bound empirical claims to the observed evidence and justify a design or policy recommendation’s applicability separately; bounded observations neither require an incident-only patch nor establish that a broader design will improve outcomes. Choose recommendation scope from the intended outcome and design rationale. Preserve the report’s uncertainty and optionality; an accurate observation is not automatically a required change. For research, distinguish strategy utility from component attribution and scope prerequisites to the treatment or claim they actually support. State the resulting keep, change, defer, or reject decisions where useful, not as a mandatory ledger. Classify each material conclusion as an evidence update, a recommendation, or a proposed change to the user's goal, chosen baseline, method semantics or essential components, or requested deliverable. A recommendation is advice, not authority. Identify material deviations from the current direction and resolve them under existing authorization: when the user has already delegated the choice and the evidence meets the sufficiency bar, decide and record the rationale; otherwise preserve the deviation as a proposal and ask only when the next action depends on it. Do not silently promote a recommendation into settled project direction or a worker assignment.
4. Preserve selected decisions and explicit constraints unless the user asks to reopen them or has already delegated that decision. Keep verified claims, project evidence, inferences, recommendations, conflicts, stale assumptions, counterevidence, and uncertainty distinct; when reusable claims or guidance are involved, read [claim discipline](docs/claim-discipline.md). For experiment protocols or readouts, preserve the applicable checks from the experiment owner.
5. If documentation updates are already authorized, identify the affected files and apply only the in-scope changes without asking again. Otherwise report the comparison, implications, conflicts, uncertainty, and evidence gaps in chat, with proposals where useful.

## Scope and output

Update only documentation or other files explicitly placed in scope. Leave research source files, source code, and configuration unchanged unless separately authorized. Preserve provenance, conflicts, and uncertainty on important claims and updates, and preserve a no-decision result when the sufficiency bar is unmet. Do not create a maintained findings file automatically; create the requested format/path only when the user requests a findings artifact or an already-authorized workflow requires it.
