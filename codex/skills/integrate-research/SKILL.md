---
name: integrate-research
description: Compare completed research outputs with source evidence and current project documentation, then summarize findings or apply already-authorized documentation updates while preserving provenance, conflicts, and uncertainty.
---

# Integrate Research

Use this skill for completed research outputs. Use `distill-source` when a supplied paper, article, documentation page, repository, or skill file still needs to be analyzed for what the project should adapt.

## Input

Accept one or more PDF, Markdown, text, or directory paths, an optional `--prompt <path>` for the original research prompt, and free-text guidance. Parse flags and paths separately from ordinary guidance.

## Workflow

1. Read the research output and original prompt when supplied. Keep source paths, dates, versions, citations, and other provenance attached to the claims they support; an uncited assertion is not project fact.
2. Read the relevant `AGENTS.md` or `CLAUDE.md`, README, current docs/research/drafts, ADRs/specs, and named source or configuration. Compare research claims and citations with current documents and source evidence before deciding what carries over.
3. Preserve selected decisions and explicit constraints unless the user asks to reopen them. Keep verified claims, project evidence, inferences, recommendations, conflicts, stale assumptions, counterevidence, and uncertainty distinct; when reusable claims or guidance are involved, read [claim discipline](docs/claim-discipline.md). For experiment protocols or readouts, preserve the applicable checks from the experiment owner.
4. If documentation updates are already authorized, identify the affected files and apply only the in-scope changes without asking again. Otherwise report the comparison, implications, conflicts, uncertainty, and evidence gaps in chat, with proposals where useful.

## Scope and output

Update only documentation or other files explicitly placed in scope. Leave research source files, source code, and configuration unchanged unless separately authorized. Preserve provenance, conflicts, and uncertainty on important claims and updates, and preserve a no-decision result when the sufficiency bar is unmet. Do not create a maintained findings file automatically; create the requested format/path only when the user requests a findings artifact or an already-authorized workflow requires it.
