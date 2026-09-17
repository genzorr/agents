---
name: ask-chatgpt-pro
description: Prepare an evidence-grounded external research handoff through either a manual ChatGPT Pro GitHub consultation or a plain external research prompt. Use when the user needs direct repository inspection or a standalone research handoff.
---

# Ask ChatGPT Pro

## Goal

Prepare an evidence-grounded external research handoff, not an answer to the underlying task. Preserve the user's requirements, selected decisions, preferences, evidence, hypotheses, uncertainty, and requested deliverable as separate kinds of context.

Choose exactly one route from the evidence surface:

- **Pro repository consultation:** when ChatGPT Pro should inspect GitHub repositories, refs, branches, PRs, or named files directly. Read [references/pro-consult.md](references/pro-consult.md), apply the shared constraints below, and follow only that route's workflow.
- **Plain external research:** when a standalone prompt for outside facts, comparisons, or source review is sufficient. Read [references/plain-research.md](references/plain-research.md), apply the shared constraints below, and follow only that route's workflow.

Do not load Pro-only GitHub, connector, pinned-commit, report, or PDF requirements into plain external research. Do not use a plain prompt when the user needs a self-contained local bundle; use `ask-oracle` for that case.

## Research Stage And Outcome

For research consultations, preserve the user's current stage and the programme outcome it serves. **Baseline selection** chooses an established method; **baseline establishment** produces a credible reference result from the chosen method; **faithful reproduction** implements and evaluates the reference without intended semantic changes; **adaptation** changes it for the project context; **diagnosis** explains an observed gap; and **novel improvement** introduces an intended research contribution. Use a primary stage and mention a supporting stage only when it changes the requested work. State what decision the consultation should change or leave unresolved.

Do not silently turn selection or establishment of a strong literature-backed baseline into invention of a small mechanism or discriminator. An established baseline does not need to be novel. Faithful reproduction preserves the method's essential components and evaluation semantics; if the current code hooks cannot support them, expose that mismatch and the resulting choice instead of stripping components to fit. Adaptation must identify its deltas from the reference method and the consequence for comparability. A causal scout or small discriminator remains legitimate when the user explicitly requests it or it answers the stated decision without displacing the programme outcome.

Ask the researcher to challenge an unsound framing explicitly and with evidence. Treat that challenge or any recommendation as advice: it may inform a decision, but it does not itself change the user's goal, selected baseline, method semantics, requested deliverable, or implementation authority.

## Shared Context Authority

Sort supplied context before writing either handoff:

1. **Primary evidence** — source code, configuration, tests, exact repository records, directly recorded measurements, commands, artifacts, and provenance.
2. **User requirements and constraints** — desired outcomes, compatibility requirements, deadlines, operational limits, non-goals, and acceptance criteria.
3. **Working synthesis** — prior conclusions, architectural models, review summaries, or design reasoning to evaluate rather than treat as source truth.
4. **Hypotheses** — suspected causes, tentative explanations, or proposed mechanisms.
5. **Selected decisions** — user-chosen directions to preserve unless explicitly reopened.
6. **Preferences and decision criteria** — softer user-owned values, priorities, and tradeoffs.
7. **Assumptions and unknowns** — provisional defaults, inaccessible evidence, unresolved facts, and uncertain interpretations.

Keep these categories distinct. Preserve hard requirements and selected decisions, use preferences as comparison criteria, and label inferences, recommendations, contradictions, and unresolved gaps.

## Shared Invariants

Both routes must identify the downstream decision or action, set an evidence standard, bound scope, state a proportional sufficiency bar, and preserve an explicit unresolved or stop condition. Neither route invents sources, constraints, repository facts, or authority to mutate external systems. Ask a question only when a blocking ambiguity cannot be handled by a reversible assumption; otherwise preserve uncertainty in the handoff. Before finalizing, ask: could the requested deliverable succeed while missing the user's intended outcome? If yes, correct the framing or surface the conflict rather than handing off a narrower substitute.
