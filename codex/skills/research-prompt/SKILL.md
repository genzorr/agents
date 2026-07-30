---
name: research-prompt
description: Generate a comprehensive prompt for deep research tools, with project context and expected deliverables.
---

# Research Prompt

Use when the user wants a structured prompt for external deep research.

## Workflow

1. Extract the topic, target audience/tool if specified, and any constraints.
2. Ask at most three clarifying questions when the scope, project context, or desired output is unclear.
3. Suggest splitting the topic if it spans several independent domains, compares more than five methods, or mixes deep theory with implementation detail.
4. Gather project context when working inside a repo:
   - `AGENTS.md`, `README.md`
   - `docs/`, `research/`, `drafts/`
   - relevant architecture notes, ADRs, specs, config schemas, or key source files
5. Identify 5-15 relevant local files to pass alongside the prompt.
6. Save the generated prompt to `research/prompts/YYYYMMDD-topic-slug.md` when inside a project. Create the directory if needed. If outside a project, output the prompt directly.

## Prompt Structure

```markdown
# Research Prompt: <topic>

## Context

<project background, current state, goals, constraints>

## Problem Statement

<core challenge>

## Decision To Inform

<decision, action, or downstream use this research will inform>

## What We Already Know

<prior findings, decisions, relevant local docs>

## What Needs Research

### 1. <research area>

Questions:
- ...

## Research Questions Summary

1. ...

## Key Papers, Docs, and Resources to Review

- ...

## Expected Research Output

- comparison tables
- recommendations with tradeoffs
- implementation guidance
- risks and validation steps

## Local Context Files To Include

- `path`
```

## Rules

- Target 250-400 lines; stop and propose splits before exceeding 500 lines.
- Make the prompt specific enough for another model to run without this conversation.
- Separate known project facts from questions to research.
- State the concrete decision, action, or downstream use the research will inform.
- Require a source hierarchy that prefers primary evidence such as official documentation, source code, papers, standards, filings, and changelogs; treat secondary commentary as supporting context rather than equivalent proof.
- Require the result to separate verified facts, supported inferences, contradictions, and unresolved uncertainty.
- Require one final gap review after the draft identifies unanswered questions, contradictions, and consequential single-source claims; use an additional search where it could materially close a gap, otherwise leave the gap explicitly unresolved.
- Do not perform the deep research yourself unless the user asks.
