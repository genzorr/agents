# Surgical Changes

Every changed line must trace to the user's request.

## Rules

- **Target-fit first.** The smallest good change is the smallest one that actually implements the requested behavior, state, or mechanism — not the smallest one that's merely safe, bounded, and easy to review. A narrow diff that misses the real target isn't surgical, it's a proxy substitution.
- **No drive-by edits.** Don't reformat, rename, or "improve" adjacent code, comments, or imports that your task didn't touch. No opportunistic refactors of working code.
- **Match existing style** even if you'd write it differently. Consistency with the surrounding file beats your preference.
- **Clean up your own orphans, not others'.** Remove imports, variables, helpers, and types that *your* edit made unused. Leave pre-existing dead code alone — mention it in your summary if it's notable, but don't delete it unless asked.
- **Don't touch unrelated files.** If a change in file A reveals a problem in file B that wasn't part of the task, surface it; don't fix it silently.

## The test

Look at the diff before reporting done. If a reviewer asked "why did this line change?" for any line, you should have a one-sentence answer that points back to the user's request. If you don't, revert that line. Also ask: does this diff, taken as a whole, address what the user actually asked for — or just the easiest thing near it?

## Not this rule

- Fixing a bug your edit introduced is not a drive-by — it's part of the task.
- Updating call sites of a function you intentionally changed is not a drive-by.
- If the user explicitly asked for cleanup or refactoring, this rule doesn't gate that work.
