# Plain External Research

Read this reference only when the user needs a standalone prompt for an external researcher and direct ChatGPT Pro/GitHub inspection is not needed.

## Route

Return the prompt in chat by default. Save it only when the user requests a file or the surrounding workflow already authorizes a durable artifact. Do not require a 5–15 file context list, a line or word quota, GitHub refs, a Pro consultation, an Oracle bundle, or a mandatory findings file. There is no fixed word or line range, context-file quota, GitHub/Pro workflow, bundle workflow, or save step.

Ask only questions whose answers materially change the decision, scope, evidence standard, sufficiency bar, or requested deliverable. Otherwise use the current conversation and available project context.

## Prompt Shape

This reference defines the handoff artifact. Its `Required Analysis And Deliverables` section must ask the downstream researcher for the research result, comparisons, evidence, and decision support; it must not ask that researcher to generate another research prompt.

Include only sections that contain useful information:

```markdown
# Research Prompt: [topic]

## Context
[Project background, current state, selected decisions, constraints, and relevant provenance.]

## Problem Statement
[The decision-relevant problem.]

## Research Quality Contract
- Decision or downstream action: [what the result must enable, change, reject, or leave undecided]
- Evidence standard: [primary sources, corroboration, recency, provenance, and direct-inspection requirements]
- Scope boundaries: [systems, alternatives, timeframes, interfaces, constraints, and non-goals]
- Sufficiency bar: [coverage and comparison needed for a responsible answer]
- Unresolved/stop condition: [what must remain explicit or block a recommendation]

## What We Already Know
[Verified facts, selected decisions, assumptions, hypotheses, contradictions, and unknowns kept distinct.]

## Research Questions
1. [Question whose answer could change the downstream action.]

## Sources And Resources To Inspect
- [Known primary or decision-relevant source, with why it matters.]

## Required Analysis And Deliverables
- [Comparisons, recommendation or explicit no-decision result, implementation implications, risks, validation, and final gap review as relevant.]

## Relevant Project Context (optional)
- [Existing file, source, decision record, or prior research] — [why it changes the question or evidence interpretation.]
```

## Checks

- Prefer official documentation, source code, papers, standards, filings, datasets, benchmarks, and changelogs as primary evidence; treat secondary commentary as context or corroboration.
- Do not score research numerically. Keep the sufficiency bar qualitative and proportional to the downstream decision.
- Keep facts, selected decisions, assumptions, hypotheses, contradictions, supported inferences, recommendations, and unresolved uncertainty distinct.
- Tie comparisons, recommendations, implementation guidance, risks, and validation to the downstream decision.
- Require a final gap review. Request another targeted search only when it could materially close a decision-relevant gap; otherwise preserve the gap explicitly.
- Permit an explicit no-decision result when the sufficiency bar is not met.
- Do not invent sources, project facts, constraints, or file paths. Name only context and sources that exist or were supplied.
- Preserve user-requested output formats and deliverables; do not infer a PDF, saved file, or other artifact when the user did not request it.

## Boundary

Use `distill-source` when the user supplies a particular paper, article, docs page, GitHub repository, or skill file and asks what this project should adapt from that source. Use this plain mode for a completed research question or a new external research handoff; use `integrate-research` for completed research output that must be compared with current project evidence and documentation.
