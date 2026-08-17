# Comprehensive Codebase Audit

Open this reference only when the operator explicitly asks for a comprehensive, exhaustive, repo-wide, or entire-codebase architecture audit. An ordinary scoped Architecture Review does not use this protocol. Architecture Review remains the owner and keeps its existing lifecycle and stop-for-selection authority; this is not a new skill, router, or invocation taxonomy.

## Boundary and coverage contract

This is an audit-only pass; read-only applies to the audited repository. Inspect implementation, interfaces, call sites, and tests, but do not edit audited files, run tests, implement recommendations, commit, push, install, or mutate external state.

Before reviewing lanes, the first ledger entry declares the audited boundary: in-scope paths plus excluded vendored, generated, and foreign-owned trees. Coverage checks omissions only inside that boundary. The coordinator then records a baseline repository status and diff and maintains one canonical run-local ledger outside the repository when scratch writes are available. That outside-repo ledger is the explicit scratch exemption from the no-report-in-the-audited-repository rule; it is not a persistent routing corpus or repository artifact. If scratch writes are unavailable, keep the ledger in visible session state, disclose the limitation, and do not invent persistence.

Inventory every identifiable subsystem, including frontend, backend, shared infrastructure, platform bridges, generated-contract ownership, and test/tooling infrastructure when materially relevant. Do not use a broad catch-all row as proof of coverage. Give each row a stable ID and name, exact ownership boundary, key implementation files, relevant public interfaces, major call sites, tests, and one status: `queued`, `in review`, `recommend`, or `skip`.

The inventory is the coverage contract. Record explicit skip decisions, confirmed findings, cross-cutting patterns, duplicates and superseded findings, dependencies, final priorities, and an audit log in the same run-local ledger. A row is complete only when its lane returns recommendations or an explicit `skip`.

## Bounded review lanes

Create a fresh read-only lane for each inventory row, with a distinct stable ID and an exact boundary that does not overlap another lane. A lane may flag a cross-subsystem concern, but it must not expand its ownership or solve work outside the assigned boundary. The coordinator actively coordinates bounded lanes and treats lane output as evidence, not acceptance.

Keep concurrent lanes bounded to the number the coordinator can actively manage, and schedule remaining inventory rows in explicit batches. Do not claim complete coverage while a queued batch or required handoff remains unreviewed.

If the platform cannot create fresh independent read-only lanes, disclose that limitation in the ledger and final handoff and mark the audit `partial`; do not claim independently validated comprehensive completion.

Lanes use the host's ordinary authorized fresh read-only subagents; scaled orchestration follows the host's existing route (`prepare-dynamic-workflow` on Claude when warranted and explicitly invoked Sol–Luna on Codex when applicable), and this reference grants no new mechanism or authority while the existing Sol-review escalation rule remains in force.

The lane contract is a fixed maximum of two material findings or `skip` per lane. Review up to two materially useful simplifications in data structures, state representation, control flow, algorithms, or ownership; it may return fewer than two. If nothing clears the Architecture Review threshold, return `skip`; do not fill a quota. If a row is too dense for this cap, split it into narrower inventory rows and review each in its own lane; never exceed the cap.

Use the existing Architecture Review deletion, interface-test-surface, earned-seam, and deepening principles. Look for invalid state combinations, repeated object-shape assumptions, duplicated branching, unclear ownership, repeated scans or lookups, and stale or contradictory lifecycle/concurrency state. Do not recommend a change for style, hypothetical extensibility, minor line-count reduction, or moving existing branching behind a new type.

During a comprehensive audit, also open `docs/whole-system-review.md` when its existing cross-component, shared-substrate, coordination, or recovery trigger applies, and open `docs/multi-entrypoint-capability-review.md` when its existing multi-entrypoint durable-behavior trigger applies. Apply those references as conditional lenses; do not duplicate them or change ordinary Architecture Review ownership.

## Finding contract

Give every recommendation a stable finding ID tied to its authoritative subsystem. A finding must use the Architecture Review schema below; `Verdict` and `Confidence` are finding-level fields, not only lane summaries.

```markdown
Finding: <stable ID and short name>
Verdict: recommend | skip
Confidence: high | medium | low
Files: <exact paths and line references>
Problem: <current friction, complexity, or invalid states, grounded in the files>
Proposed shape: <smallest credible representation or ownership change and affected interfaces>
Dependency shape: <in-process | local-substitutable | remote-owned | true-external>
Why it helps: <locality, leverage, testability, or simpler state/behavior ownership>
Risk: <regression, migration, compatibility, concurrency, or recovery concern>
Verification: <existing and additional consequence-level checks>
```

`Files` and `Problem` must provide exact evidence. `Proposed shape` must name the smallest credible implementation scope without becoming an implementation plan. `Dependency shape` uses the Architecture Review vocabulary. A lane that returns `skip` records why no finding met the materiality bar; it does not fabricate empty finding fields.

## Coordinator verification and synthesis

The coordinator independently verifies every finding against the current repository and exact file/line evidence before accepting it. Reject, narrow, or demote findings that are vague, duplicate another finding, misunderstand intentional semantics, merely relocate complexity, or propose an abstraction without earned leverage.

Deduplicate overlapping findings and assign each accepted finding to one authoritative subsystem. Preserve the inventory boundary that owns the evidence; do not hide an omission or overlap by broadening a completed row. Update the ledger with accepted, narrowed, demoted, rejected, superseded, and explicit-skip outcomes.

## Fresh validation passes

After all inventory rows are complete, run fresh independent read-only validation lanes for each of these passes:

- **Coverage:** find missing subsystem boundaries and material frontend, backend, infrastructure, platform, generated-contract, or test/tooling areas. A real omission adds a new explicit row and requires that row to be audited.
- **Overlap and duplication:** find lane-boundary overlap, duplicate or superseded findings, and findings assigned to the wrong authoritative subsystem.
- **Materiality and over-abstraction:** reject stylistic, hypothetical, pass-through, or complexity-relocating proposals that do not clear the Architecture Review bar.
- **Schema completeness:** check every accepted finding for stable identity, exact `Files`, `Problem`, `Proposed shape`, `Dependency shape`, `Why it helps`, `Risk`, `Verification`, finding-level `Verdict`, and `Confidence`.
- **Dependency-aware ranking:** rank accepted findings by concrete impact, confidence, implementation effort, blast radius, and prerequisites; make dependencies and best first slices internally consistent.

Under an explicitly invoked Sol–Luna task, these validation passes are fresh Luna lanes. They do not automatically escalate to a Sol reviewer; any Sol review still follows the governing Sol–Luna escalation rule and named acceptance-critical rationale.

## Completion and handoff

The audit is complete only when every inventory row is `recommend` or `skip`, every accepted finding is independently verified and schema-complete, overlap and weak abstractions are removed, and priorities and dependencies are consistent. Unchanged-repository completion requires comparing the final repository status and diff with the baseline: the repository must be unchanged by the audit, including no generated report or routing corpus in the checkout.

Return the normal Architecture Review `Verdict`, then render each accepted finding as exactly one numbered entry under the normal `Candidates:` heading. Each entry retains `Finding`, `Verdict`, `Confidence`, `Files`, `Problem`, `Proposed shape`, `Dependency shape`, `Why it helps`, `Risk`, and `Verification`; do not group findings into unnumbered prose.

```markdown
Verdict: <short overall judgment>

Candidates:
1. <short name>
   Finding: <stable finding ID and short name>
   Verdict: recommend
   Confidence: high | medium | low
   Files: <exact paths and line references>
   Problem: <current friction>
   Proposed shape: <plain-English change>
   Dependency shape: <in-process | local-substitutable | remote-owned | true-external>
   Why it helps: <locality/leverage/testability>
   Risk: <main risk or migration concern>
   Verification: <focused checks>

Recommended next step: <select one candidate for grill-with-docs | No action>
```

If no accepted finding clears the bar, use the existing `Candidates: None — <why no candidate cleared the bar>` form. Stop for selection. Only after the operator selects one candidate may the existing `grill-with-docs` skill resolve its seam, acceptance contract, and detailed implementation plan; do not develop implementation detail for or schedule unselected candidates.
