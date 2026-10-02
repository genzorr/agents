---
name: test-audit
description: Audit a bounded existing test suite for meaningful detection, redundancy, and preservation-safe cleanup. Use only when the user explicitly invokes test-audit; ordinary test authoring and change review keep their existing owners.
---

# Test Audit

Audit the selected existing suite and produce findings with a preservation plan. A useful result may retain every test or add missing detectors; test count and LOC reduction are outcomes, not targets.

## Scope And Authority

Own existing-suite analysis and preservation planning. Default to a report without edits. If the current request already authorizes repair, consolidation, or pruning in that scope, continue through one coherent batch and validation without asking for the same authorization again. Product fixes, public API changes, and unselected architecture work need their own scope authority.

In Harness-backed work, `harness-work` remains the task driver and this skill is a bounded helper. Use `tdd` for test-first authoring when appropriate, `architecture-review` for substantive seam redesign, and `review-change` for resulting diff review under the project's existing review requirements. Do not create or finalize tasks, automate Git lifecycle actions, or activate an external review service.

## Audit

1. Bound the production behavior, test files, associated fixtures/support, overlapping proof, and exclusions. Read applicable project instructions, production owners and relevant callers/history. Inspect CI routing and establish available baseline results through permitted non-destructive checks. If execution is excluded or unavailable, state the inspection-only limit; do not claim a passing baseline.
2. Account for every in-scope declaration and meaningful parameter row as **retain**, **repair**, **consolidate**, **delete**, or **unresolved**. Read actual assertions and exercised paths; names alone do not establish coverage. Group rows only when they protect the same consequence and share a disposition. Complete the declared boundary before claiming the audit is complete; a bounded audit does not establish whole-suite coverage.
3. For each candidate, identify the credible defect it actually detects, the observable consequence, and the independent authority for its expectation. Compare overlapping tests by failure reach, not shared wording or invariant: another layer may uniquely protect wiring, transport, persistence, rejection, or recovery. Before removal, name the remaining detector and explain how it reaches that defect, or justify why no live contract remains. Missing preservation evidence means retain or unresolved.
4. Under existing cleanup authorization, execute one coherent batch. Transfer distinct assertions and establish replacement detection before deleting their predecessor. Inspect real callers, external consumers, and public compatibility before removing exported “test-only” seams; local test-only usage is insufficient proof. Preserve relevant CI routing when moving tests and remove only support made unused by this batch. Baseline failures stay diagnosis findings; do not delete them to make the audit green or fix unrelated production behavior silently.
5. Validate focused keepers and siblings, broadening for changed support, routing, or unresolved risks; complete project-required checks. Where material to the preservation claim, demonstrate that a plausible defect turns surviving proof red and a legitimate refactor remains green. Do not require a mutation exercise for every trivial deletion. Review the complete diff against the declared scope and preservation evidence before reporting the result.

Mocks, source strings, exact values, and slowness are inspection signals, never automatic deletion reasons. Preserve distinct public, security, compatibility, artifact, cross-layer, and scientific contracts even when their assertions look structural. If authority, oracle independence, or overlap is ambiguous, read [references/test-value.md](references/test-value.md) for discriminating examples and provenance.

## Report

Use the existing caller-owned report or task; no separate record store is required. Give scope and baseline, then a compact table:

| Location / parameter rows | Actual defect and observable consequence | Independent authority | Remaining detector / reach | Disposition | Support or seam changes | Risk and verification |
|---|---|---|---|---|---|---|

Report retained false positives, unresolved evidence, authorized edits, checks actually run and their results, baseline failures, and material execution gaps. If measurement is available, distinguish maintained contracts, fixture burden, and actual execution cost from raw test/LOC counts. No-change and unresolved conclusions are valid; do not invent follow-up campaigns or efficiency claims.
