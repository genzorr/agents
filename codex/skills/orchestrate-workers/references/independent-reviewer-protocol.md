# Independent Reviewer Protocol

Read this reference only after the escalation rule in `SKILL.md` requires independent review.

## Prepare

Dispatch only after implementation is integrated, the coordinator has inspected the accumulated diff, required verification is complete, and the checkout is quiescent. Keep it quiescent throughout review. Any implementation mutation invalidates the verdict and requires reintegration and verification before a new review.

Use a compatible idle reviewer identity. For a new reviewer, apply the skill's no-parent-history rule with no bounded-history exception. State new/reused identity, route, resolved reviewer model/effort, and profile provenance.

## Review Packet

Send:

- review ID;
- named target and three-part escalation rationale;
- operator goal and acceptance criteria;
- exact accumulated change set or revisions;
- interfaces, constraints, and nonclaims;
- raw evidence locations and permitted non-mutating commands;
- material risks and uncertainty;
- return route and result format;
- explicit read-only, no-mutation, no-delegation instructions.

For reuse, add prior review ID, disposition (`ship`, `fix-first`, `rethink`, `blocked`, `failed`, `voided`), and reviewed state. Invalidate the prior verdict; carry only confirmed project invariants and relevant findings.

Require inspection of actual files, artifacts, and complete current diff before the coordinator's interpretation. Do not provide only fixes, summaries, or worker reports. Complete state-writing tests/builds/generation before dispatch; use isolated scratch state outside the reviewed checkout when reviewer execution is necessary and authorized.

## Isolation And Result

Treat read-only isolation as enforced only when the product reports it. Under broader policy, proceed only when hard isolation is unnecessary, record exact before/after state, and disclose residual risk. Non-mutating inspection is allowed.

Require one outcome:

- `ship`: evidence supports acceptance, with decisive reason and residual risk.
- `fix-first`: precise findings require correction.
- `rethink`: architecture or scope returns to the coordinator.
- `blocked`: review could not complete; include reason, missing inputs, and current state. Not a verdict.
- `failed`: dispatch ended without verdict or blocked report; no review evidence.
- `voided`: reviewer mutated checkout or durable state; discard verdict.

If mutation occurs, report it, recycle the reviewer, and restore state only within authority. Stop if restoration is incomplete. Re-establish and verify the integrated baseline before review or acceptance.

When review is required, withhold acceptance until the coordinator resolves the disposition and receives a valid verdict or the operator explicitly waives review. Re-dispatch failed review to the same compatible reviewer when reachable; otherwise recycle it. The verdict is evidence; the coordinator remains acceptance authority.

Send `fix-first` corrections to the original implementation worker when resumable, then integrate and verify. `rethink` returns decisions to the coordinator. Any implementation change invalidates the verdict, not reviewer identity; when review remains required, send a reset packet against new state.

## Reviewer Continuity

After each dispatch/classification change, restate reviewer identity, reuse status, last review ID, disposition, reviewed state, and exact reviewer profile in visible coordinator state. This is the compaction recovery point.

Reuse across fixes and later compatible tasks only within the same reviewer role, project, checkout, trust, authority, isolation, route, model, and effort. Never assign concurrent reviews. Compaction, task boundaries, elapsed time, and prior verdicts do not justify recycling.

Recycle only for unreachable identity; incompatible reviewer profile; repository/checkout/trust/authority/isolation change; mutation or implementation ownership; irrecoverable stale/anchored conclusions; repeated acceptance-critical misses; or explicit fresh/second-opinion request.
