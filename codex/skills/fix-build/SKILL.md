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
   - determine the root cause from the log and affected source, and distinguish verified evidence from unverified reports
   - inspect affected source files
   - apply the smallest fix that preserves existing behavior and test intent
5. If an API signature changed, search all call sites before editing.
6. Run the relevant failing command if it is available, then run the project checks expected by local instructions.
7. Report the fixed files, the evidence status, and the verification result.

## Rules

- Fix all related failures from the log, not just the first one.
- Do not change the API itself unless the log proves the API implementation is wrong.
- Preserve test intent; update tests only when expectations are stale or call signatures changed.
- Do not fix a guessed cause: apply a fix only when log and source evidence support it; otherwise investigate the competing causes or state what evidence is missing.
- Run meaningful regression verification for changed behavior when it exists. A tiny textual or configuration repair does not require a generic new test when source inspection and existing checks provide the relevant evidence.
- Keep the final response to one short summary plus verification.
