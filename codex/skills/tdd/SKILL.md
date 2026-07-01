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

## Test Quality

- Good tests describe behavior, not implementation shape.
- Tests should survive internal refactors.
- Avoid mocking internal collaborators just because they are convenient.
- Mock true external systems, time, randomness, and slow/unavailable services when needed.
- Prefer fixtures and helpers that express domain concepts over setup that mirrors internals.

## Rules

- Do not write all tests first and then all implementation. That outruns the feedback loop.
- Do not add tests against private helpers unless the private helper is the real stable interface for this repo.
- If no good public seam exists, say so and consider `architecture-review`.
- If the user asks to fix an existing bug, first reproduce it or preserve the provided repro as the regression test.
