# Independent Reviewer Protocol

Read this reference only after the operator explicitly requests independent review for the resolved task.

## Prepare

Schedule requested review at meaningful integration or delivery checkpoints, or when a demonstrated material safety, authority, durable-state, or public-contract risk requires it before relying on the affected result. Routine in-scope corrections use owner self-review and focused consequence tests; an active review request does not require a new dispatch after each edit or suspend authorized development. Preserve explicit operator and governing acceptance requirements.

Dispatch after the named target is integrated, the coordinator has inspected its accumulated diff, and required verification is complete. Keep the review target and its decision-bearing dependencies and evidence stable through a recoverable snapshot or serialized writes to that surface. The reviewer inspects that stable surface. Disjoint authorized work may continue when it cannot alter that surface. If overlapping work changes the live target, bind the result to the captured revision and resolve the delta before affected acceptance; never claim a review of mixed or unseen bytes. Quiesce the whole checkout only when the review surface or shared-state risk requires it.

Establish a recoverable exact target baseline: commit/ref, target's uncommitted changes, and decision-bearing generated or external artifacts. Use existing revisions, scoped patches or copies, and relevant artifact identities/digests in proportion to the changed surface and credible blast radius. Preserve applicable evidence across rounds; do not repeatedly inventory or hash the whole workspace, freeze unrelated artifacts, or rerun broad checks without a relevant change, failure, insufficient evidence, or governing requirement.

Use a compatible idle reviewer identity. For a new reviewer, apply the skill's no-parent-history rule with no bounded-history exception. State new/reused identity, route, resolved reviewer model/effort, and profile provenance.

## Review Packet

Send:

- review ID;
- named acceptance target and explicit operator-request provenance;
- operator goal and acceptance criteria;
- exact accumulated change set or revisions;
- interfaces, constraints, and nonclaims;
- raw evidence locations and permitted non-mutating commands;
- material risks and uncertainty;
- return route and result format;
- explicit read-only, no-mutation, no-delegation instructions.

The reviewer uses immediate-parent native route; no cross-task fallback. Existing-task review messages omit both `model` and `thinking` (including null/presumed-current values) and preserve settings. Settings changes require user authorization naming target and values; profiles, inherited context, delegated instructions, and callback permission never authorize them.

For a correction round with established continuity, send decision-bearing deltas referencing the prior packet: prior review ID/disposition, exact reviewed baseline, complete subsequent target delta, unresolved findings, affected surfaces, and new verification. Reuse unchanged goal, criteria, constraints, authority, route, and settings. Restore the full packet when continuity or required facts cannot be recovered. Carry only confirmed project invariants, demonstrably applicable coverage, and relevant findings; retain the prior verdict as evidence about its reviewed revision.

On the first or expanded full review, require inspection of actual files, artifacts, and the complete target diff before the coordinator's interpretation. On a correction round with valid carried coverage, require inspection of the complete delta and every affected surface under the rules below. Do not provide only fixes, summaries, or worker reports. Complete target-affecting tests/builds/generation before dispatch; use isolated scratch state outside the reviewed checkout when reviewer execution is necessary and authorized.

## Complete Target And Correction Rounds

The first review of an acceptance target inspects the complete target. The same compatible reviewer identity may reuse valid prior inspection coverage on a correction round only after recovering the exact previously reviewed baseline and inspecting the complete subsequent delta, including uncommitted changes. Inspect every affected interface, invariant, caller or consumer, unresolved finding, and new or changed verification. Carry prior coverage only when its target, assumptions, and evidence remain demonstrably applicable.

A verdict describes the reviewed revision. Later edits do not erase applicable coverage or extend that verdict to unseen changes. The owner classifies the complete subsequent target delta, self-reviews routine corrections, and verifies their consequences. Return to the independent reviewer at the next meaningful required checkpoint, or before affected acceptance when material risk, acceptance-critical findings, or the operator/governing contract requires it. A request for independent review of the final state requires a final delta review if the target changed after the last review; owner checks cannot replace it. No edit count or fixed review frequency substitutes for this judgment.

When a correction-round review is required, issue a verdict for the complete current target and identify which coverage was carried forward and which coverage was newly performed. Expand inspection when the prior baseline or coverage cannot be recovered, a relevant assumption changed, or the consequences of the delta reach beyond the proven prior surface; use a complete fresh inspection when scoped recovery is insufficient. Compaction alone does not require restarting the review when the exact baseline, coverage, findings, delta, and evidence remain sufficiently preserved.

## Isolation And Result

Treat read-only isolation as enforced only when the product reports it. Under broader policy, proceed only when hard isolation is unnecessary, compare before/after state for the review target and mutation-sensitive shared or durable state in proportion to the credible blast radius, and disclose residual risk and detection limits. Non-mutating inspection is allowed. Distinguish authorized concurrent writes from reviewer mutation; unresolved attribution withholds affected acceptance.

Require one outcome:

- `ship`: evidence supports acceptance, with decisive reason and residual risk.
- `fix-first`: precise findings require correction.
- `rethink`: architecture or scope returns to the coordinator.
- `blocked`: review could not complete; include reason, missing inputs, and current state. Not a verdict.
- `failed`: dispatch ended without verdict or blocked report; no review evidence.
- `voided`: reviewer mutated checkout or durable state; discard verdict.

If reviewer mutation occurs, report it, recycle the reviewer, and restore affected state only within authority while preserving other owners' authorized changes. Stop affected review or acceptance if restoration is incomplete. Re-establish and verify the affected baseline before review or acceptance.

When review is operator-requested, withhold the required acceptance until the coordinator resolves the disposition and receives a valid verdict at the required review boundary or the operator explicitly waives review. Continue unaffected authorized development while review is pending. Re-dispatch failed review to the same compatible reviewer when reachable; otherwise recycle it. The verdict is evidence; the coordinator remains acceptance authority.

Send `fix-first` corrections to the original implementation worker when resumable, then integrate and verify under the correction-round rules. Acceptance-critical findings require independent confirmation of closure before affected acceptance. `rethink` returns decisions to the coordinator. Final acceptance identifies the independently reviewed revision and coverage, later changes and their owner verification, any required delta-review result, and remaining gaps; never present owner-checked later edits as independently reviewed.

## Reviewer Continuity

When reviewer identity or continuity is established, recycled, recovered, or uncertain, emit a full continuity receipt naming identity, reuse status, last review ID, disposition, reviewed state, and exact reviewer profile. Use the full receipt for genuine compaction recovery and fail safe to it whenever the event cannot establish that continuity remains intact. After continuity is established, later compatible dispatch or classification changes need only decision-bearing deltas. This receipt remains the compaction recovery point.

Reuse across fixes and later compatible tasks only within the same reviewer role, project, checkout, trust, authority, isolation, route, model, and effort. Never assign concurrent reviews. Compaction, task boundaries, elapsed time, and prior verdicts do not justify recycling.

Recycle only for unreachable identity; incompatible reviewer profile; repository/checkout/trust/authority/isolation change; mutation or implementation ownership; irrecoverable stale/anchored conclusions; repeated acceptance-critical misses; or explicit fresh/second-opinion request.
