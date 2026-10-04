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

Do not load Pro-only GitHub, connector, pinned-commit, or report requirements into plain external research. Do not use a plain prompt when the user needs a self-contained local bundle; use `ask-oracle` for that case.

## Recover The Intended Consultation

For a short invocation after discussion, recover the intended outcome and the decision or deliverable this consultation must support from the relevant user steering, discussion, and current project records. Do not substitute the latest assistant proposal for that intent. Distinguish selected directions from tentative suggestions, and earlier decisions from ones the user has reopened. Preserve the prior evidence that changes the question, including relevant work in another repository; state the specific remaining gap rather than presenting an already-investigated question as new. Retrieve only context that can change this consultation, not an exhaustive conversation history.

Express the result in the prompt's opening: what the user needs to decide or obtain, what must remain in scope, and what the researcher may challenge. Add a short user quotation or source pointer when paraphrasing would change its meaning. Do not create a separate intent document or require confirmation of this reconstruction. Resolve locally available facts first and apply the shared clarification rule below.

Choose detail for the intended reader and artifact. Require a specific basis for calling a material proposed addition, investigation, constraint, or amendment necessary for the user's outcome or an applicable requirement; otherwise distinguish its possible benefit from an obligation. Verifying a fact does not by itself establish that the fact belongs in the deliverable. Preserve enough specificity to remain accurate and usable, not the greatest or least possible detail.

## Research Stage And Outcome

For research consultations, preserve the user's current stage and the programme outcome it serves. **Baseline selection** chooses an established method; **baseline establishment** produces a credible reference result from the chosen method; **faithful reproduction** implements and evaluates the reference without intended semantic changes; **adaptation** changes it for the project context; **diagnosis** explains an observed gap; and **novel improvement** introduces an intended research contribution. Use a primary stage and mention a supporting stage only when it changes the requested work. State what decision the consultation should change or leave unresolved.

Do not silently turn selection or establishment of a strong literature-backed baseline into invention of a small mechanism or discriminator. An established baseline does not need to be novel. Faithful reproduction preserves the method's essential components and evaluation semantics; if the current code hooks cannot support them, expose that mismatch and the resulting choice instead of stripping components to fit. Adaptation must identify its deltas from the reference method and the consequence for comparability. A causal scout or small discriminator remains legitimate when the user explicitly requests it or it answers the stated decision without displacing the programme outcome.

For experimental work, distinguish evaluating a coherent strategy, testing interactions, and attributing an effect to a component. Specify treatments and measurements for the claim being sought. A strategy can be worth testing before its ingredients are individually attributed; a package result does not establish component causation. A narrow test is appropriate when it answers the intended decision. When staging work, identify what is answered now, what is deferred and why, and which particular action depends on each validity check; do not let an implementation convenience silently redefine the scientific question.

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

Both routes must identify the downstream decision or action, set an evidence standard, bound scope, state a proportional sufficiency bar, and preserve an explicit unresolved or stop condition. Neither route invents sources, constraints, repository facts, or authority to mutate external systems. Before drafting, ask concise questions when the answers would materially improve the decision, scope, evidence selection, or requested deliverable and available context cannot resolve them. Use disclosed reversible assumptions for nonblocking gaps when asking would add little value; wait for answers when missing input would make the handoff misleading or prevent identifying the task or required evidence. Do not make an interview or approval of an intent summary a routine gate. Before finalizing, ask: could the requested deliverable succeed while missing the user's intended outcome? If yes, correct the framing or surface the conflict rather than handing off a narrower substitute.

## Return Boundary

Keep the original prompt available with the consultation's existing task context. When the answer returns, use `integrate-research` when available; provide the report, original prompt, and relevant user steering from before and after the outgoing handoff to that workflow. Otherwise compare them with current project evidence before proposing adoption. This preparation skill does not accept recommendations, change project direction, or authorize implementation merely by producing a handoff.
