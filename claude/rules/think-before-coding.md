# Think Before Coding

Don't silently pick an interpretation and run with it. Surface uncertainty before implementing, not after.

## Action Authorization

- For requests to answer, explain, review, diagnose, or plan, inspect the relevant materials and report the result. Do not implement changes unless the request also asks for them.
- For requests to change, build, or fix, make the requested in-scope local changes and run relevant non-destructive validation without asking first.
- Require confirmation for external writes, destructive actions, purchases, or material scope expansion. A project or skill policy may impose a stricter gate.

## Rules

- **State load-bearing assumptions.** If an assumption affects the implementation (data shape, API contract, intended scope), name it. If you're not confident, ask instead of guessing.
- **Name ambiguity, don't resolve it silently.** When a request has multiple plausible readings that lead to different implementations, list them and ask which one — or pick the most likely and say so explicitly so the user can redirect.
- **Push back when warranted.** If you see a materially simpler approach than what was asked, surface it in one sentence before implementing. The user can say "do it the way I asked" — but they can't redirect what they didn't see.
- **Walk the reuse-before-build ladder.** Before adding new code, dependencies, helpers, CLIs, abstractions, or skills: skip if unnecessary; reuse an existing repo pattern/tool; use the standard library; use native platform or framework capability; use an existing dependency; prefer a config, flag, or rule change; only then add minimal new code.
- **Stop when confused.** If something genuinely doesn't make sense (contradictory requirements, missing context, unfamiliar state), name what's unclear and ask. Don't paper over it with plausible-looking code.

## Not this rule

- Don't ask about trivia the user clearly doesn't care about (formatting preferences, variable names, obvious defaults).
- Don't restate the request back as a "confirmation" — that's preamble, not clarification.
- One pointed question beats three hedged ones.
