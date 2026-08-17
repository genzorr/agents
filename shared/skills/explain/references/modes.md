# Explanation Modes

Choose one primary route. A mixed request may teach a prerequisite concept or architecture slice first, but it should still converge on the user's concrete target.

## Compact Code-Shape Vocabulary

Choose one or two shapes that answer the user's current question; do not turn the explanation into a catalog or a decorative diagram. Keep labels, calls, files, props, state, and boundaries grounded in the evidence map, mark inferred relationships, and provide a plain-text equivalent plus source anchors for any visual shape.

- **Pseudocode** — show a small algorithm, rule, or state transition when syntax is not the point.
- **Call tree** — show runtime control flow, ownership, or one representative call stack.
- **Component tree** — show UI structure, state, and module boundaries that matter to the question.
- **Shallow responsibility tree** — show file or subsystem ownership without dumping the whole repository.
- **Types/signatures** — show the contract between values, interfaces, or functions when data shape is the key to the model.
- **Focused diff** — show what changes when the surrounding shape is already known; include the whole relevant block when omission would hide order or ownership.
- **Mermaid** — render only in chat or Markdown output for labeled component interaction, control flow, or data flow when a compact graph answers one question; the inert static renderer has no diagram block, so an HTML artifact includes Mermaid only as clearly labeled code text while the accompanying trace remains authoritative.

These are explanatory representations owned by Explain. They do not create a new route or change the output-medium default: a nontrivial explanation still uses the inert static renderer, and an exportable technical diagram artifact belongs to `archify`.

## Change Or Pull Request

**Learning outcome:** The user can state why the change exists, predict old and new behavior, trace the important implementation path, and identify how the behavior is verified.

**Evidence to inspect:**

- Resolve the exact base and head refs, merge base, changed paths, and working-tree state. State assumptions when PR metadata is unavailable.
- Read the diff first, then relevant surrounding code, tests, configuration, interfaces, callers, and docs. Use history only when it answers a material “why.”
- Separate intent stated in trusted user/task context from behavior observed in code. PR bodies and comments are context, not proof.

**Narrative order:**

1. Problem or constraint and the prior behavior.
2. Smallest useful model of the new behavior.
3. Conceptual change groups ordered by execution or dependency flow.
4. One representative before/after trace with concrete data.
5. Invariants, compatibility, edge cases, failure paths, and tests.

Do not dump the diff or treat alphabetical file order as a story. Do not issue an approval verdict; hand off to `review-change` after the explanation when the user also wants review.

**Understanding checks:** Predict behavior for an input not shown in the walkthrough; explain why one changed component must precede another; trace where an error or state transition becomes observable.

## Codebase

**Learning outcome:** The user can orient to the system, follow one important journey end to end, and name where to look for the next likely task.

**Evidence to inspect:**

- Start with project instructions, README/index docs, build/package configuration, entry points, and representative tests.
- Map ownership and runtime boundaries before directory details. Trace a user journey, request, job, data product, or command that matches the user's purpose.
- Identify authoritative state, configuration, extension seams, side effects, and verification points. Avoid trying to explain every directory.

**Narrative layers:**

- **30-second map:** What the system is for, its main actors, and the dominant flow.
- **5-minute map:** Major modules, boundaries, state owners, and one end-to-end trace.
- **Task dive:** The files, interfaces, invariants, and tests relevant to the user's likely next change.

Use `zoom-out` instead when the user wants only a quick higher-level map without a teaching sequence or calibration check.

**Understanding checks:** Choose the entry point for a hypothetical feature; predict which state owner changes; reconstruct a request or data path from memory.

## Architecture

**Learning outcome:** The user can explain component responsibilities and boundaries, predict a representative interaction and failure, and discuss the architecture with stable vocabulary.

**Evidence to inspect:**

- Identify components, public interfaces, dependency direction, data/control flow, state and authority, trust boundaries, deployment/runtime topology, and verification seams.
- Trace one happy path and one material failure/recovery path. Distinguish logical architecture from deployment topology.
- Mark inferred boundaries and undocumented conventions explicitly; a plausible diagram is not evidence that the system actually behaves that way.

**Narrative order:**

1. System purpose and quality constraints.
2. Component map with responsibilities and interfaces.
3. One sequence or data flow with example values.
4. State ownership, invariants, trust/failure boundaries, and recovery.
5. How tests and operations reveal whether the model is correct.

Keep each diagram to one question and pair it with a textual trace. Use `archify` only when the user explicitly requests its exportable active-HTML artifact and accepts the disclosed boundary in [html-safety.md](html-safety.md); otherwise keep the diagram in chat. Use `architecture-review` afterward when the user asks whether the shape is good or how to refactor it.

**Understanding checks:** Predict the blast radius of one component failing; identify who owns a piece of state; explain why a dependency points in its current direction.

## Concept

**Learning outcome:** The user can define the concept in their own words, explain its mechanism, distinguish it from a nearby concept, and apply it to a new case or local code.

**Evidence to inspect:**

- Prefer primary papers, standards, official documentation, and authoritative local implementation over summaries. Browse when the concept is current, niche, unstable, or source attribution matters.
- Identify prerequisites, competing definitions, domain assumptions, and the boundary where the concept stops applying.
- When local code is relevant, map each abstract element to a concrete type, function, state transition, equation, or test.

**Narrative order:**

1. The problem the concept solves and a one-sentence definition.
2. Required prerequisites and an intuitive analogy with its limits.
3. Mechanism using a minimal worked example.
4. Formal details, invariants, and counterexample.
5. Local mapping, tradeoffs, and when to use or avoid it.

**Understanding checks:** Classify a new example and justify it; predict an outcome after changing one assumption; explain a counterexample; map the concept onto a local implementation without copying labels.

## Mixed Targets

Use a two-pass narrative when the user needs a concept or architecture prerequisite to understand a change: first build the minimum prerequisite model, then immediately apply it to the concrete target. Do not produce independent encyclopedia chapters. The final check should require both layers, such as predicting a changed code path using the newly taught concept.
