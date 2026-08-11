# research-prompt authoring reference

Open this only when writing the research prompt. `SKILL.md` owns the trigger, workflow, Research Quality Contract, file discovery, and output contract. This file supplies a proportional template and section-specific checks.

## Template

Use only the sections that help the research tool answer the stated decision.

```markdown
# Research Prompt: <topic>

## Context
<project background, current state, selected decisions, and constraints>

## Problem Statement
<the decision-relevant problem in one or two sentences>

## Research Quality Contract
- **Decision or downstream action:** <what the result must enable, change, reject, or leave undecided>
- **Evidence standard:** <primary sources, corroboration, recency, provenance, and direct-inspection requirements>
- **Scope boundaries:** <systems, alternatives, timeframes, interfaces, constraints, and non-goals>
- **Sufficiency bar:** <coverage and comparison needed for a responsible answer>
- **Unresolved/stop condition:** <gap that must remain explicit, trigger targeted search, or prevent a recommendation>

## What We Already Know

### Verified facts and selected decisions
- ...

### Assumptions, hypotheses, and contradictions
- ...

## Research Questions

### <area>
1. ...

## Sources And Resources To Inspect
- **<source>** — <why it is primary or decision-relevant>

## Required Analysis And Deliverables
1. <comparison or synthesis tied to the decision>
2. <recommendation, rejection, or explicit no-decision result>
3. <implementation, validation, risk, or migration implications when relevant>
4. <contradictions, uncertainty, and evidence gaps>
5. <final gap review and any justified targeted follow-up search>

## Relevant Project Files

### Documentation
- `path` — relevance

### Source Code
- `path` — relevance

### Prior Research
- `path` — relevance
```

## Section Checks

### Context

- Keep only background that changes the research question, evidence interpretation, or downstream decision.
- State user-selected decisions as constraints rather than reopening them silently.
- Separate repository facts from prior summaries and hypotheses.

### Problem Statement

- Name the real decision-relevant problem, not only the first suspected mechanism.
- Avoid “everything about X” or broad educational framing when the user needs a concrete choice.

### Research Quality Contract

- The decision determines which evidence and comparison dimensions matter.
- The evidence standard should prefer primary sources and state when recency, replication, direct source inspection, or multiple independent sources are needed.
- Scope boundaries should prevent adjacent topics from consuming the research without hiding a material dependency.
- The sufficiency bar should name coverage, not a numerical score.
- The unresolved/stop condition should distinguish a gap that blocks recommendation from one that can remain explicitly unresolved.

### What We Already Know

- Preserve provenance for important prior findings.
- Keep facts, selected decisions, assumptions, hypotheses, contradictions, and unknowns distinct.
- Do not present prior model synthesis as primary evidence.

### Research Questions

- Ask specific comparative or causal questions whose answers could change the downstream action.
- Group questions by coherent area and remove questions answerable by a trivial local lookup.
- Avoid mixing implementation tasks into the research request unless implementation guidance is an explicit deliverable.

### Sources And Resources

- Prefer official documentation, source code, papers, standards, filings, datasets, benchmarks, and changelogs.
- Treat secondary commentary as orientation or corroboration, not equivalent proof.
- Name a source only when it is known and relevant; do not fabricate a reading list.

### Required Analysis And Deliverables

- Tie every table, comparison, recommendation, and roadmap to the stated decision.
- Require verified facts, supported inferences, contradictions, assumptions, and unresolved uncertainty to remain distinguishable.
- Require a final gap review. Request another targeted search only when it could materially close a decision-relevant gap.
- Permit an explicit no-decision result when the sufficiency bar is not met.

### Relevant Project Files

- Include 5–15 existing files at most.
- Use repository-relative paths, group by type, and give one short relevance note per file.
- Keep the prompt's file list exactly aligned with the list returned to the user.

## Anti-Patterns

- Vague questions such as “How does X work?” when a specific comparison is possible.
- Padding the prompt to hit a length target.
- Reopening selected decisions without authorization.
- Treating secondary commentary or a prior AI report as primary evidence.
- Requesting a recommendation when the unresolved/stop condition says evidence is insufficient.
- Listing files, papers, or tools that were not verified to exist.
