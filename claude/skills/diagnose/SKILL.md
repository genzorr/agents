---
name: diagnose
description: Diagnose hard bugs, failing behavior, flaky tests, and performance regressions through a disciplined feedback-loop-first process. Use when the user says diagnose/debug, reports something broken or slow, provides an error/log, or asks for root-cause analysis before fixing.
---

# Diagnose

Find the cause before changing code. Prefer a fast, deterministic pass/fail loop over code-reading guesses.

## Workflow

1. **Build the loop.** Create or identify the smallest reliable signal that reproduces the symptom: a failing test, CLI command, fixture replay, browser script, benchmark, log assertion, or trace comparison. If no loop is possible, stop and ask for the missing artifact or environment.
2. **Reproduce.** Run the loop and confirm it matches the user's reported symptom. For flaky failures, raise reproduction rate with repetition, stress, fixed seeds, or narrower setup.
3. **Hypothesize.** List 3–5 ranked, falsifiable causes. Each must predict what evidence would confirm or disprove it.
4. **Instrument.** Probe one hypothesis at a time. Use debugger/REPL inspection first when practical, then targeted logs or metrics. Tag temporary logs with a unique prefix so cleanup is reliable.
5. **Fix only when authorized.** If the user asked for a fix (for example, "debug and fix") or an active implementation contract authorizes it, turn the minimized repro into a regression test before the fix. Otherwise report the root cause and regression-test direction without editing source or tests. If no seam exists, note that as an architecture/testing gap.
6. **Verify and clean up.** Re-run the original loop and regression checks, remove temporary instrumentation/prototypes, and state the confirmed root cause.

## Rules

- Do not skip directly to a fix unless the cause is already proven by the repro.
- For performance regressions, measure baseline first; do not add broad logging in hot paths.
- If the loop is too slow or noisy, improve the loop before continuing.
- Keep temporary files clearly named and delete them before reporting done unless the user asked to keep them.
- If the diagnosis exposes a module/interface problem, recommend `/architecture-review` after the immediate bug is understood.
