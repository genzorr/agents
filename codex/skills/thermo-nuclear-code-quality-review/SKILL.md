---
name: thermo-nuclear-code-quality-review
description: Run an extremely strict maintainability review for structural code quality, abstraction quality, file sprawl, spaghetti branching, type-boundary drift, and missed simplification opportunities. Use when the user asks for a thermo-nuclear or thermonuclear review, harsh code-quality audit, deep maintainability review, or ambitious structural review of a branch, PR, diff, or implementation.
---

# Thermo-Nuclear Code Quality Review

Review the change as a strict maintainability gate. Default to read-only review; do not edit code unless the user explicitly asks to fix findings.

This skill is narrower than `review-change`: prioritize structure, simplicity, locality, abstraction quality, and long-term maintainability. Still flag correctness risk when it follows from tangled structure, unclear invariants, or leaky boundaries.

## Workflow

1. Resolve the review target:
   - explicit PR URL/number, branch, commit range, path list, or user-provided diff;
   - otherwise current working tree diff;
   - otherwise current branch compared to the merge base with the default upstream/base branch.
2. If there is no discoverable review target, ask one concise question for the target.
3. Read project instructions, relevant docs/ADRs, tests, and nearby code needed to understand the shape of the change.
4. Inspect the diff first, then read surrounding files and callers for changed behavior.
5. Measure file-size pressure when the diff adds substantial code. Treat a source file crossing from below 1000 lines to above 1000 lines as a presumptive decomposition issue.
6. Search for existing canonical helpers, modules, ownership layers, state models, and type contracts before accepting new bespoke logic.
7. Look for simplification moves that preserve behavior while deleting concepts, branches, modes, wrappers, or orchestration steps.
8. Produce findings first, ordered by severity and maintainability impact. Prefer a few high-conviction findings over a long list of cosmetic notes.

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

## Output

Lead with findings:

```markdown
Findings:
- [P1] Title
  File: path/to/file.ext:123
  Problem: What structural issue the change introduces or preserves.
  Impact: Why this makes the codebase harder to change, test, or reason about.
  Cleaner shape: Concrete restructuring direction.
  Verification: Focused checks that should prove behavior is preserved.

Open questions:
- ...

Verification:
- Ran: ...
- Not run: ... because ...
```

If there are no blocking structural issues, say that clearly and note any residual review or verification gaps. Do not approve merely because behavior appears correct if there is an obvious simpler structure, unjustified file-size explosion, spaghetti branching, leaky boundary, or hacky abstraction.
