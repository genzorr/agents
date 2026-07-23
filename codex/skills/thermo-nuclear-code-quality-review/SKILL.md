---
name: thermo-nuclear-code-quality-review
description: Apply an explicitly requested thermo-nuclear structural-maintainability lens to a code review. Use only when the user asks for a thermo-nuclear or thermonuclear structural review, harsh maintainability audit, or deep simplification critique; `review-change` remains the general review driver.
---

# Thermo-Nuclear Code Quality Review

Apply this lens to a review driven by `review-change` or another active project review driver. If no review driver is active, start or use `review-change` as the driver, then apply this lens. Default to read-only review; do not edit code unless the user explicitly asks to fix findings.

This skill adds structural-maintainability checks; it does not resolve the target, own the review lifecycle, replace general correctness review, or define a separate final output contract. The active driver owns those responsibilities.

## Structural lens

- Read the project instructions, relevant docs/ADRs, tests, and nearby code needed to understand the shape of the change.
- Inspect the diff and surrounding callers for structural consequences. Measure file-size pressure when the driver is reviewing substantial additions; a source file crossing from below 1000 lines to above 1000 lines is a presumptive decomposition issue.
- Search for existing canonical helpers, modules, ownership layers, state models, and type contracts before accepting new bespoke logic.
- Look for simplification moves that preserve behavior while deleting concepts, branches, modes, wrappers, or orchestration steps.
- Feed a few high-conviction structural findings and concrete remedies back through the driver's output contract.

## Review Standards

- Be ambitious about structural simplification. Ask whether the implementation can be reframed so whole branches, helpers, modes, or layers disappear.
- Do not accept ad-hoc conditional growth in already busy flows. Treat scattered feature checks, nullable modes, and one-off flags as design problems unless the local pattern clearly supports them.
- Prefer deleting complexity over reorganizing it. A refactor that moves the same number of concepts around has not earned much.
- Prefer direct, boring code over magical generic mechanisms. Flag wrappers, identity adapters, reflection, or broad fallback behavior when they hide a simple data shape.
- Keep logic in the canonical layer. Push feature logic toward the module that owns the concept, not into shared paths as incidental special cases.
- Protect type and boundary clarity. Question unnecessary `any`, `unknown`, casts, optional fields, and silent fallbacks when an explicit contract would simplify control flow.
- Treat avoidable sequential orchestration and non-atomic updates as maintainability smells when independent work or grouped updates would be clearer.
- Demand decomposition for unjustified file sprawl, especially when a PR pushes a source file past 1000 lines.

## What To Flag

Escalate findings when you see:

- a complicated implementation where a cleaner reframing could delete meaningful complexity;
- new branches bolted into unrelated or already crowded flows;
- feature-specific logic leaking into shared or lower-level code;
- thin abstractions that add vocabulary without hiding complexity;
- duplicated logic or bespoke helpers where a canonical utility already exists;
- new code, dependencies, helpers, CLIs, abstractions, or skills that should have been avoided by reusing repo/native/stdlib capability or by changing configuration instead;
- cast-heavy or optional-heavy contracts that obscure the real invariant;
- special-case edge handling embedded in a function that already has too many reasons to change;
- partial-update flows that can leave related state harder to reason about;
- file growth that weakens scanability or mixes unrelated responsibilities;
- refactors that pass tests but make the code less modular, less local, or harder to explain.

## Preferred Remedies

When a finding is valid, suggest the cleaner shape:

- delete an unnecessary layer instead of polishing it;
- reframe the state model so conditionals disappear;
- move logic to the package, service, module, or component that already owns the concept;
- extract a focused helper or pure function when it reduces repeated reasoning;
- split a large file by cohesive responsibility, not by arbitrary layer;
- collapse duplicate branches into one clearer flow;
- replace condition chains with a typed model, explicit dispatcher, or policy object only when it reduces total complexity;
- make type boundaries explicit so fallback and casting paths can be removed;
- parallelize independent work or group related updates when that makes the orchestration easier to reason about.

When active, report structural findings through the driver's output contract. Do not issue a second full-review verdict; if no blocking structural issue is found, say so within the driver's review result and preserve its verification gaps.
