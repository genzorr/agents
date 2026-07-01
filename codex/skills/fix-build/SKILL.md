---
name: fix-build
description: Read a build or test log, identify failures, and apply the minimal source fixes needed to make the build pass.
---

# Fix Build

Use when the user provides a build, test, compiler, or linter log and wants the failures fixed.

## Workflow

1. Resolve the log path from the user's request. If the path is relative, treat it as relative to the current working directory.
2. Read the last 200 lines first. If that does not include the full failure context, read more targeted regions.
3. Identify every distinct failure, prioritizing:
   - compiler errors: `error:`, `fatal error:`, undefined reference
   - Python `TypeError`, `ImportError`, `AssertionError`
   - test failures: `FAILED`, assertion output, expected/actual mismatches
   - linker errors
   - linter/format errors
4. For each failure:
   - determine the root cause
   - inspect affected source files
   - apply the smallest fix that preserves existing behavior and test intent
5. If an API signature changed, search all call sites before editing.
6. Run the relevant failing command if it is available, then run the project checks expected by local instructions.
7. Report the fixed files and the verification result.

## Rules

- Fix all related failures from the log, not just the first one.
- Do not change the API itself unless the log proves the API implementation is wrong.
- Preserve test intent; update tests only when expectations are stale or call signatures changed.
- If a failure is ambiguous, fix the most likely root cause and state the ambiguity.
- Keep the final response to one short summary plus verification.
