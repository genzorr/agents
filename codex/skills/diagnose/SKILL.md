---
name: diagnose
description: Diagnose hard bugs, failing behavior, flaky tests, and performance regressions through a disciplined feedback-loop-first process. Use when the user says diagnose/debug, reports something broken or slow, provides an error/log, or asks for root-cause analysis before fixing.
---

# Diagnose

Find the cause before changing code. Prefer a fast, deterministic pass/fail loop over code-reading guesses.

## Workflow

1. **Build the loop.** Create or identify the smallest reliable signal that reproduces the symptom: a failing test, CLI command, fixture replay, browser script, benchmark, log assertion, or trace comparison. If runtime reproduction is unavailable, use the supplied logs, traces, failing assertions, fixtures, source invariants, or history for a bounded diagnosis. Distinguish verified evidence from unverified reports and state what remains inaccessible; ask for a missing artifact or environment only when that gap blocks useful progress.
2. **Reproduce or verify.** Run the loop when one is available and confirm whether it matches the reported symptom. When no runtime loop exists, verify the diagnosis against the available evidence and say explicitly that runtime reproduction is unverified. For flaky failures, raise reproduction rate with repetition, stress, fixed seeds, or narrower setup.
3. **Hypothesize.** List plausible, falsifiable causes in proportion to the evidence; do not force a fixed number. If one cause is supported, test that cause directly. If multiple material causes remain open, gather the cheapest discriminating evidence and state the unresolved gap.
4. **Instrument.** Probe one hypothesis at a time. Use debugger/REPL inspection first when practical, then targeted logs or metrics. Tag temporary logs with a unique prefix so cleanup is reliable.
5. **Fix only when authorized.** If the user asked for a fix (for example, "debug and fix") or an active implementation contract authorizes it, turn the minimized repro or other meaningful observable evidence into a regression test before the fix when that test protects a plausible production defect. For a tiny textual or configuration repair where source and existing checks provide the relevant evidence, use proportional verification instead of adding a generic test. Otherwise report the root cause and regression-test direction without editing source or tests. If no seam exists, note that as an architecture/testing gap.
6. **Verify and clean up.** Re-run the original loop when available and run meaningful regression checks for the changed behavior. State which evidence is verified and which remains unverified, remove temporary instrumentation/prototypes, and state the confirmed or bounded root cause.

## Rules

- Do not fix a guessed cause: apply a fix only when the cause is supported by the repro or available evidence; otherwise investigate the competing causes or explain what evidence is missing.
- For performance regressions, measure baseline first; do not add broad logging in hot paths.
- If the loop is too slow or noisy, improve the loop before continuing.
- Keep temporary files clearly named and delete them before reporting done unless the user asked to keep them.
- If the diagnosis exposes a module/interface problem, recommend `architecture-review` after the immediate bug is understood.
