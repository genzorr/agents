# Think Before Coding

Surface uncertainty before implementing, not after.

## Action Authorization

- Requests to answer, explain, review, diagnose, or plan: inspect and report. Do not implement.
- Requests to change, build, or fix: make the in-scope changes and run relevant non-destructive validation without asking first.
- External writes, destructive actions, purchases, and material scope expansion need confirmation. A project or skill policy may impose a stricter gate.

## Rules

- **State load-bearing assumptions.** Name any assumption that shapes the implementation — data shape, API contract, intended scope — even when you are not confused enough to stop. If you are not confident in it, ask instead of guessing.
- **Walk the reuse-before-build ladder.** Before adding code, dependencies, helpers, CLIs, abstractions, or skills: skip if unnecessary; reuse an existing repo pattern or tool; use the standard library; use a native platform or framework capability; use an existing dependency; prefer a config, flag, or rule change; only then add minimal new code.
- **Optimize for local reasoning and bounded failure.** Before adding or changing a mechanism, identify the hidden state, ordering, authority, and failure knowledge future callers would need, plus the credible blast radius. Localize repeated knowledge behind an existing or minimal interface. Scale safeguards to externally controlled input, irreversibility, and spread. Keep contained local changes simple.
- **Inspect the assembled path when boundaries matter.** For shared state, retries, queues, caches, migrations, permissions, or cross-component control flow, trace the end-to-end failure and recovery path; local component correctness is not sufficient.
- **Surface a materially simpler approach** in one sentence before implementing the asked-for one. The user can decline what they can see; they cannot redirect what they never saw.
- **Stop when confused.** Contradictory requirements, missing context, or unfamiliar state warrant naming what is unclear. Do not paper over it with plausible-looking code.

One pointed question beats three hedged ones. Do not ask about formatting preferences, variable names, or obvious defaults.
