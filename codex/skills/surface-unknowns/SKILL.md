---
name: surface-unknowns
description: Surface consequential unknowns in a problem or active task, build enough orientation to distinguish what is known, assumed, missing, and decision-relevant, and route each material gap to the cheapest reliable resolution. Use when the user asks for a blind-spot pass or help understanding an unfamiliar problem. Invoke autonomously only once per newly observed decision branch when evidence supports multiple plausible resolutions or a missing fact or authority cannot be recovered locally, those possibilities would materially change the work, and resolution is worth the inspection, delay, and interruption cost. Do not use when one interpretation dominates or for trivial, locally answerable, or safely reversible choices.
---

# Surface Unknowns

Run a bounded uncertainty pass that improves the user's or current agent's model of the problem and selects what should happen next. Surface consequential gaps; never promise a complete map.

## Composition Roles And Invariant

- **Explicit discovery pass:** Driver for the bounded orientation task. Own framing, inspection, minimum teaching, uncertainty triage, and one next-move recommendation, then stop.
- **Autonomous checkpoint:** Helper under the active driver. Apply the uncertainty lens, return a compact finding, and leave lifecycle ownership with that driver. Become a **router** only when explicitly transferring control to another driver.
- **No-op:** Make no role transition and create no separate output.
- Keep exactly one driver active. A handoff transfers control; a checkpoint that returns a finding or reversible default leaves the current driver in charge.
- Treat the four known/unknown quadrants from Thariq Shihipar's practitioner field guide as hypothesis-generating prompts, not empirically validated, exhaustive categories or mandatory stages. An item can move as evidence changes.
- Prefer the smallest intervention that can change the decision. The goal is useful orientation and safer progress, not maximum questioning.

## Choose Depth

- **Explicit discovery pass:** Use when the user invokes the skill, asks for a blind-spot pass, or says they know little about the problem. Build a visible problem orientation and uncertainty map before recommending one next move.
- **Autonomous checkpoint:** Run at a natural decision boundary or before difficult-to-reverse work only when the uncertainty is newly observed, evidence supports at least two plausible resolutions or a missing fact or authority cannot be recovered locally, the possibilities would lead to materially different actions, and resolution is worth the inspection, delay, and interruption cost.
- **No-op:** If inspection shows only trivial, locally answerable, or safely reversible gaps, state any load-bearing assumption in the surrounding work and continue without a separate artifact.

## Re-entry Guard

Run at most once for the same observed evidence and decision branch. A downstream workflow inherits the checkpoint result and may reopen it only when new evidence changes the frame, plausible alternatives, authority, consequence, or reversibility. Do not route to the already-active driver; return the finding to it.

## Workflow

1. **Frame the target.** Identify the goal or decision at stake, current phase, user's apparent starting point, decision authority, and bounded source surface. Infer low-risk context; ask only when a wrong frame would materially change the pass.
2. **Inspect before asking.** Read the available territory: project instructions, authoritative docs, source, tests, data, references, prior attempts, and current primary sources when the domain requires them. Record what was inspected and what remains inaccessible. Do not ask the user for facts the evidence can answer.
3. **Build minimum orientation.** Explain the problem in plain language, the few terms and mechanisms needed to reason about it, the main tensions, and what good could look like. When the user has little domain knowledge, teach enough structure before asking them to choose; do not interview them about facts they cannot yet evaluate. For a novice explicit pass, finish only when the user has enough structure to understand the next decision and why its plausible alternatives differ; use one concrete contrast or example when vocabulary alone is insufficient.
4. **Generate candidate unknowns.** Use four prompts:
   - What is settled by observed evidence or an explicit decision?
   - Which questions are already visible?
   - What tacit context, preference, or criterion may emerge only through concrete alternatives, examples, references, or prototypes?
   - Which failure paths, counterexamples, adjacent systems, external constraints, prior failed attempts, or missing coverage suggest blind-spot hypotheses?
5. **Prioritize by decision leverage.** Keep a gap when plausible resolutions would lead to different actions or a missing fact or authority blocks safe progress. Weigh consequence if wrong, difficulty of reversal, evidence gap, and resolution cost; prefer the route with the highest expected decision value net of inspection, delay, and interruption cost. Use qualitative judgment without invented probabilities.
6. **Assign authority and route.** Distinguish facts the territory owns, reversible discretion the agent owns, product or value choices the user owns, and external gates another authority owns. Select the cheapest reliable route from the table below.
7. **Hand off or return.** Produce the proportionate output contract and recommend one next move. An explicit pass then stops. An autonomous checkpoint either returns the finding to the current driver or transfers control to one selected driver; do not absorb that workflow into this skill.

## Resolution Routes

| Unknown concerns | Route |
|---|---|
| Facts, existing behavior, or constraints | Inspect authoritative sources, code, tests, runtime evidence, or official current sources. |
| A consequential plan or product decision | Recommend an answer and ask one pointed question; use `grill-with-docs` when several design decisions need a structured interview. |
| Tacit taste or “I will know it when I see it” | Present concrete alternatives or use `prototype`. |
| Feasibility | Use `prototype`; do not claim the probe proves adoption or correctness. |
| A quantitative or causal claim | Use `design-experiment`. |
| Broken or unexplained runtime behavior | Use `diagnose`. |
| Architecture quality | Use `architecture-review`. |
| A bounded code or reference example answering one active question | Inspect it directly and return a semantics map to the current driver. |
| A substantive external source requiring keep/reject/defer adaptation | Use `distill-source`. |
| Implementation correctness | Use tests and `review-change`. |
| A code or system map | Use `zoom-out`. |
| The user's learning outcome is the task | Use `explain`. |

Use this skill when orientation serves to expose decision-changing gaps and select a next move. Let `zoom-out` drive when a code or system map is the requested outcome, and let `explain` drive when building and testing the user's mental model is the requested outcome.

## Phase Rules

- **Before work:** Find only the uncertainties likely to change scope, solution shape, evidence requirements, or user-visible behavior. Use cheap inspection or probes before expensive implementation.
- **During work:** When new evidence invalidates the plan, stop for user-owned, high-impact, or difficult-to-reverse changes. For contained reversible deviations, choose a defensible default, record the evidence and reason in the current workflow's notes or handoff, and continue.
- **After work:** Separate correctness gaps from comprehension gaps. Tests and review establish implementation evidence; explanation and transfer questions probe understanding. Neither substitutes for the other.

## Output Contracts

For an explicit discovery pass, return:

```markdown
## Problem orientation

Problem: <plain-language formulation>
Why it is difficult: <important mechanisms and tensions>
Minimum vocabulary: <only terms needed to reason about it>
What good could look like: <criteria, examples, and source of each>
Coverage: <what was and was not inspected>

## Current knowledge

Observed:
- <claim with evidence>

Decided:
- <explicit decision and owner>

Inferred or assumed:
- <claim, basis, and consequence if wrong>

## Consequential unknowns

| Unknown | Why it matters | Authority | Resolution or trigger |
|---|---|---|---|

Blind-spot hypotheses:
- <hypothesis and why it deserves attention>

Recommended next move: <one action>
```

For an autonomous checkpoint, return to the current driver with only:

```markdown
Material uncertainty: <one sentence, or none>
Basis: <observed evidence versus inference or assumption>
Route: <continue with disclosed reversible default | inspect | ask | named skill/workflow>
Residual risk or trigger: <what would require revisiting the choice>
```

Treat `Material uncertainty` plus `Basis` as the checkpoint identity for the re-entry guard. Omit empty sections. Create a durable ledger only when the user requests it or the active project workflow already owns one.

## Guardrails

- Never claim exhaustive discovery of unknown unknowns. Report coverage and residual limits.
- Do not force every quadrant, technique, or phase onto every task.
- Do not turn ordinary reversible implementation discretion into a user approval gate.
- Do not close a material user-owned decision silently; do batch locally answered facts instead of making the user approve each one.
- Cite real evidence for territory claims and label invented examples or synthetic data.
- Do not use HTML, subagents, or persistent artifacts by default.
- Do not treat model self-report, confidence, a polished artifact, or a same-session quiz as correctness evidence.
