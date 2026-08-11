---
name: research-prompt
description: Generate a project-grounded prompt for an external deep research tool, with a clear decision, evidence standard, scope, sufficiency bar, and expected deliverables.
---

# Research Prompt

Create a structured prompt for external deep research. Do not perform the research unless the user asks.

## Input

- Extract the research topic, target tool or audience, user constraints, prior knowledge, and desired output.
- Use current conversation context when it already resolves the task.
- Ask at most three questions, only when the answer materially changes the decision, scope, evidence standard, or sufficiency bar.
- Suggest focused sub-prompts when the request spans independent domains, mixes deep theory with detailed implementation, or compares too many unrelated alternatives for one coherent answer.

## Research Quality Contract

Before drafting, define this compact contract inside the prompt:

- **Decision or downstream action:** what the research must enable, change, reject, or leave undecided.
- **Evidence standard:** which sources count as primary evidence and what corroboration, recency, provenance, or direct inspection the important claims require.
- **Scope boundaries:** systems, alternatives, timeframes, jurisdictions, repositories, interfaces, constraints, and explicit non-goals.
- **Sufficiency bar:** the coverage needed to answer responsibly, such as required alternative families, representative cases, contradiction checks, implementation implications, or decision-relevant comparison dimensions.
- **Unresolved/stop condition:** uncertainty that must remain explicit, trigger another targeted search, or prevent a recommendation instead of being guessed away.

Do not score research numerically. Keep the contract proportional; it replaces vague requests for “comprehensive” coverage rather than adding ceremony.

## Workflow

1. Gather only the project context needed to make the research decision-specific: applicable `AGENTS.md`, README, architecture notes, ADRs, specs, prior research, configuration schemas, and key source entry points.
2. Separate project facts, user decisions, assumptions, hypotheses, and open research questions.
3. Identify 5–15 relevant local files when working inside a repository. Include only files that exist and explain their relevance briefly.
4. Draft the prompt using the structure below, omitting empty or inapplicable sections.
5. Save it to `research/prompts/YYYYMMDD-topic-slug.md` inside a project. Outside a project, return it directly.
6. Report the saved path and the matching local-context file list.

## Prompt Structure

```markdown
# Research Prompt: <topic>

## Context
<project background, current state, selected decisions, and constraints>

## Problem Statement
<decision-relevant problem>

## Research Quality Contract
- Decision or downstream action: ...
- Evidence standard: ...
- Scope boundaries: ...
- Sufficiency bar: ...
- Unresolved/stop condition: ...

## What We Already Know
<verified facts, prior findings, assumptions, and unresolved contradictions kept distinct>

## Research Questions
1. ...

## Sources And Resources To Inspect
- ...

## Required Analysis And Deliverables
- comparisons and tradeoffs
- recommendation or explicit no-decision result
- implementation or validation implications where relevant
- contradictions, uncertainty, and evidence gaps

## Relevant Project Files
- `path` — relevance
```

## Rules

- Make the prompt executable without this conversation, but do not paste material already available in referenced files.
- Prefer official documentation, source code, papers, standards, filings, datasets, benchmarks, and changelogs as primary evidence. Use secondary commentary as context, not equivalent proof.
- Require the result to distinguish verified facts, supported inferences, contradictions, assumptions, and unresolved uncertainty.
- Require a final gap review. Run another targeted search only when it could materially close a decision-relevant gap; otherwise preserve the gap explicitly.
- Keep requested tables, recommendations, implementation guidance, risks, and validation steps tied to the stated downstream decision.
- Target roughly 250–400 lines only when the subject genuinely needs that depth. Split before exceeding 500 lines; do not pad a bounded question to meet a quota.
