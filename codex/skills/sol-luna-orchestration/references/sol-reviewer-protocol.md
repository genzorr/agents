# Sol Reviewer Protocol

Read this reference only after the escalation rule in `SKILL.md` requires an independent Sol review.

## Prepare

Dispatch only after implementation is integrated, main Sol has inspected the accumulated diff, required verification is complete, and the checkout is quiescent. Keep it quiescent throughout review. Any implementation mutation invalidates the verdict and requires reintegration and verification before a new review.

Use the persistent reviewer identity when compatible and idle. For a new reviewer, apply the skill's no-parent-history launch and confirmation rule with no bounded-history exception. State whether the reviewer is reused or new plus its route, Sol model, and effort.

## Review Packet

Send:

- review ID;
- named review target and three-part escalation rationale;
- operator goal and acceptance criteria;
- exact accumulated change set or revisions;
- interfaces, constraints, and nonclaims;
- raw evidence locations and permitted non-mutating inspection commands;
- material risks and uncertainty;
- return route and required result format;
- explicit read-only, no-mutation, no-delegation instructions.

For a reused reviewer, add the prior review ID, disposition (`ship`, `fix-first`, `rethink`, `blocked`, `failed`, `voided`), and reviewed state. Invalidate the prior verdict; carry forward only confirmed project invariants and still-relevant findings.

Require the reviewer to inspect actual files, artifacts, and the complete current diff before reading main Sol's interpretation. Do not provide only changed fixes, summaries, or worker reports.

Complete state-writing tests, builds, or generation before dispatch. When reviewer execution is necessary and authorized, use isolated scratch state outside the reviewed checkout.

## Isolation And Result

Treat read-only isolation as enforced only when the product reports it. Under a broader policy, proceed only when hard isolation is unnecessary, record exact before/after state, and disclose residual risk. Non-mutating inspection is allowed.

Require one of these outcomes:

- `ship`: evidence supports acceptance, with decisive reason and residual risk.
- `fix-first`: precise findings must be corrected before acceptance.
- `rethink`: architecture or scope must return to main Sol.
- `blocked`: review could not complete; include reason, missing inputs, and current review state. This is not a verdict.
- `failed`: dispatch terminated without a verdict or blocked report; it supplies no review evidence.
- `voided`: reviewer mutated the checkout or durable state; discard its verdict.

If mutation occurs, report it, recycle the reviewer, and restore state only within existing authority. If restoration is incomplete, stop and escalate to the operator. Re-establish and verify the integrated baseline before review or acceptance.

When review is required, withhold acceptance until main Sol resolves the disposition and receives a valid verdict or the operator explicitly waives review. Re-dispatch failed review to the same compatible reviewer when reachable; otherwise recycle it. The reviewer verdict is evidence; main Sol remains acceptance authority.

Send `fix-first` corrections to the original implementation worker when resumable, then integrate and verify again. `rethink` returns decisions to main Sol. Any implementation change invalidates the verdict, not the reviewer identity; when review remains required, send a reset packet against the new state.

## Reviewer Continuity

After each dispatch or classification change, restate reviewer identity, reuse status, last review ID, disposition, and reviewed state in visible Sol session state. This is the recovery point across compaction.

Reuse the reviewer across fixes and later tasks within the same compatible repository, checkout, trust boundary, authority envelope, isolation boundary, and Sol session. Never assign concurrent reviews. Compaction, task boundaries, elapsed time, and prior verdicts do not justify recycling.

Recycle only when the identity is unreachable; model/effort is incompatible; repository, checkout, trust, authority, or isolation changes; the reviewer mutates state or assumes implementation ownership; a reset cannot correct stale or anchored conclusions; it repeatedly misses acceptance-critical issues; or the operator requests a fresh reviewer or independent second opinion. One healthy reviewer may persist for the compatible Sol session's lifetime.
