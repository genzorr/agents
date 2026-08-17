---
name: architecture-review
description: Find architecture, module-boundary, interface, and refactor opportunities in a codebase. Use when the user asks about scalability, modularity, large files, bad seams, testability, refactoring, deepening modules, or whether a design/codebase shape is good, or explicitly requests a comprehensive, exhaustive, repo-wide, or entire-codebase architecture audit.
---

# Architecture Review

Surface architectural friction and deepening opportunities; do not implement by default.

## Vocabulary

Use these terms consistently in findings.

- **Module**: anything with an interface and an implementation: function, class, package, CLI command, UI view, or feature slice.
- **Interface**: everything callers must know to use the module correctly: types, invariants, ordering, errors, config, side effects, and performance expectations.
- **Implementation**: the hidden work behind the interface.
- **Depth**: leverage at the interface. A deep module hides substantial behavior behind a small, stable interface.
- **Seam**: a place behavior can be changed or tested without editing every caller.
- **Adapter**: one concrete implementation behind a seam.
- **Leverage**: what callers get from depth: more capability per fact they must learn.
- **Locality**: what maintainers get from depth: change, bugs, knowledge, and verification concentrated in one place.

## Principles

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was likely pass-through. If complexity reappears across callers, it was earning its keep.
- **The interface is the test surface**: tests should cross the same seam callers use. Testing past the interface signals the module may be the wrong shape.
- **One adapter is a hypothetical seam; two adapters make a real seam**: do not introduce ports/adapters unless something actually varies.
- **Deepening beats shuffling**: prefer changes that put behavior behind a stronger interface over splitting files by layer or vocabulary alone.

## Workflow

1. Read the user's concern, planned change, or upcoming work. If this is a harness task, also read `harness snapshot`, the active task, and the parent slice. Use those sources to scope the review. When none supplies a scope, inspect recent Git history to prioritize repeatedly changed paths; treat churn as a priority signal, not evidence of an architecture defect.
   If the user explicitly asks for a comprehensive, exhaustive, repo-wide, or entire-codebase audit, open [docs/comprehensive-codebase-audit.md](docs/comprehensive-codebase-audit.md) and follow that protocol; ordinary scoped reviews continue with this workflow, and Architecture Review remains the owner and selection authority.
2. Read relevant docs, findings, ADRs, glossary/context docs, and tests. Respect existing decisions unless there is concrete friction.
3. Trace callers, data flow, configuration, side effects, and verification seams. Use `rg` first; avoid broad rewrites.
4. When the target area changes integration topology, a shared substrate, cross-component coordination, or failure containment, open `docs/whole-system-review.md` and apply its optional lens. Skip it for contained local refactors.
5. When the reviewed change adds an entrypoint or touches durable behavior reachable from two or more entrypoints, open `docs/multi-entrypoint-capability-review.md` and apply its ownership, bypass, effect, and proof checks. Skip it when work stays behind one existing interface, entrypoints share only a product-free primitive, or the project already has one proven behavior path and the new work does not change it.
6. Look for signals:
   - callers must understand too much implementation detail;
   - one behavior is scattered across many files;
   - tests need private helpers, mocks of internals, or duplicated setup;
   - a large file mixes unrelated reasons to change;
   - a wrapper adds vocabulary but no leverage;
   - a seam has only one real adapter;
   - adding the next feature would require editing many callers.
7. Classify dependency shape for each candidate:
   - **In-process**: pure computation or in-memory state. Deepen and test through the new interface.
   - **Local-substitutable**: local test stand-ins exist, such as temp files or in-memory stores. Keep the seam internal and test with the stand-in.
   - **Remote but owned**: define a port at the seam, with production and in-memory adapters.
   - **True external**: inject a port for the third-party dependency and use a mock/test adapter.
8. Keep only candidates with concrete friction and a change that earns its abstraction under the principles above. It is valid to return no candidates; do not fill a quota.
9. Present ranked opportunities. For each, include files, current friction, proposed shape, why it improves locality/leverage/testability, dependency shape, risk, and suggested verification.
10. Stop for selection. Route one user-selected candidate at a time to `grill-with-docs` to resolve its seam and acceptance contract before implementation; do not develop implementation detail for or schedule unselected candidates.

## Output

```markdown
Verdict: <short overall judgment>

Candidates:
1. <name>
   Files: <paths>
   Problem: <current friction>
   Proposed shape: <plain-English change>
   Dependency shape: <in-process | local-substitutable | remote-owned | true-external>
   Why it helps: <locality/leverage/testability>
   Risk: <main risk or migration concern>
   Verification: <focused checks>

Recommended next step: <select one candidate for grill-with-docs | No action>
```

When no candidate clears the bar, keep the `Verdict:` line, replace the candidate list with `Candidates: None — <why no candidate cleared the bar>`, and set `Recommended next step: No action`; omit candidate subfields.

For large architecture reviews, offer to turn the candidates into a temp-file report and use `archify` for requested diagram artifacts. Do not create report files unless the user asks for that artifact.

## Rules

- Do not propose a new abstraction unless it hides real complexity or matches an existing pattern.
- Do not suggest horizontal "split by layer" work when a vertical task would be safer.
- Do not edit code unless the user explicitly asks for implementation.
- If the selected candidate's grilling yields concrete work, let `grill-with-docs` recommend its durable capture path; do not create tasks directly. If the user wants unselected candidates retained, use `harness-record` to capture them as inbox items without elaborating or scheduling them.
