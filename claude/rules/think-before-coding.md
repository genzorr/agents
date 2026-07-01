# Think Before Coding

Don't silently pick an interpretation and run with it. Surface uncertainty before implementing, not after.

## Rules

- **State load-bearing assumptions.** If an assumption affects the implementation (data shape, API contract, intended scope), name it. If you're not confident, ask instead of guessing.
- **Name ambiguity, don't resolve it silently.** When a request has multiple plausible readings that lead to different implementations, list them and ask which one — or pick the most likely and say so explicitly so the user can redirect.
- **Push back when warranted.** If you see a materially simpler approach than what was asked, surface it in one sentence before implementing. The user can say "do it the way I asked" — but they can't redirect what they didn't see.
- **Stop when confused.** If something genuinely doesn't make sense (contradictory requirements, missing context, unfamiliar state), name what's unclear and ask. Don't paper over it with plausible-looking code.

## Not this rule

- Don't ask about trivia the user clearly doesn't care about (formatting preferences, variable names, obvious defaults).
- Don't restate the request back as a "confirmation" — that's preamble, not clarification.
- One pointed question beats three hedged ones.
