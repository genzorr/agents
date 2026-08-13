---
name: tdd
description: Use test-driven development with a red-green-refactor loop. Use when the user asks for TDD, test-first work, red-green-refactor, regression tests before a fix, or behavior-focused test coverage.
---

# TDD

Use one vertical slice at a time: one failing behavior test, the smallest implementation, then refactor.

## Workflow

1. Identify the public interface or user-visible workflow that should carry the behavior.
2. Write one failing test through that interface. Prefer integration-style tests that exercise real code paths.
3. Run the test and confirm it fails for the expected reason.
4. Implement the smallest change that makes the test pass.
5. Run the focused test, then relevant broader checks.
6. Refactor only with passing tests, keeping behavior unchanged.
7. Repeat for the next behavior.

## Reviewed Behavior Spines

For a stable, meaningful behavior that spans states or artifacts, depends on a required non-event, or is likely to receive a substantial agent implementation, propose one small behavior spine before implementation. Skip this ceremony for a small local change or unstable interface where ordinary focused TDD gives sufficient evidence.

- Keep behavior authority separate from implementation: a human or independent specification owner approves the claim before the implementer treats it as fixed. The implementer may read production code but must not silently weaken the approved claim, oracle, or baseline tests.
- Name the stimulus, supported public seam, observable consequences and non-events, cross-state or cross-artifact integrity relationships, controlled external boundaries, prohibited shortcuts, independent oracle, and claim ceiling.
- Establish red-before-green evidence when changing behavior or fixing a defect. When adding a spine for behavior that already exists, record the pristine green baseline and challenge the oracle with a plausible semantic bypass.
- During review, demonstrate one legitimate implementation change that remains green and one plausible production defect that turns the spine red.

## Test Quality

- Good tests describe behavior, not implementation shape.
- Before proposing an assertion, name the production defect it would catch and the observable consequence it protects.
- Do not pin an exact value, relationship, text, or source shape when it could change legitimately without a production defect. Exact assertions remain appropriate when the value, text, or shape is itself a documented public, safety, compatibility, or shipped-artifact contract.
- An oracle that derives expected behavior from production identifiers, generated keys, internal paths, or source shape is implementation-derived rather than independent, unless that exact shape is itself the documented public, safety, compatibility, or shipped-artifact contract.
- Tests should survive internal refactors.
- Avoid mocking internal collaborators just because they are convenient.
- Mock true external systems, time, randomness, and slow/unavailable services when needed.
- Prefer fixtures and helpers that express domain concepts over setup that mirrors internals.

## Rules

- Do not write all tests first and then all implementation. That outruns the feedback loop.
- Do not add tests against private helpers unless the private helper is the real stable interface for this repo.
- If no good public seam exists, say so and consider `/architecture-review`.
- If the user asks to fix an existing bug, first reproduce it or preserve the provided repro as the regression test.
