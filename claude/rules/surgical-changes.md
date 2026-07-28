# Surgical Changes

Every changed line must trace to the user's request.

## Rules

- **Target-fit first.** The smallest good change is the smallest one that actually implements the requested behavior — not the smallest one that is merely safe and easy to review. A narrow diff that misses the real target is not surgical, it is a proxy substitution.
- **A small diff is not automatically contained.** Reject a change that spreads hidden operational knowledge across callers, or enlarges the failure surface without a task-related reason and proportionate safeguards.
- **No drive-by edits.** Do not reformat, rename, re-wrap, or improve adjacent code, comments, or imports the task did not touch. No opportunistic refactors of working code.
- **Clean up your own orphans, not others'.** Remove imports, variables, helpers, and types that *your* edit made unused. Leave pre-existing dead code alone — mention it if notable.
- **Do not touch unrelated files.** If a change in file A reveals a problem in file B, surface it rather than fixing it silently.

## The Test

Look at the diff before reporting done. For any line, a reviewer asking "why did this change?" should get a one-sentence answer pointing back to the request. If there is no such answer, revert the line. Then ask whether the diff as a whole addresses what was asked — or just the easiest thing near it.

Not covered by this rule: fixing a bug your edit introduced, updating call sites of a function you intentionally changed, or cleanup the user explicitly asked for.
