# Text Prune Behavioral Conformance

**Method:** Single same-agent, source-bounded manual conformance pass against `shared/skills/text-prune/SKILL.md` and only the applicable mode reference for each fixture.

**Date:** 2026-08-24

**Result:** 21/21 PASS. This pass verifies the recorded routing, preservation, refusal, no-op, consumer-check, and role outcomes for the curated cases. It does not establish host-level trigger precision, general compression quality, a losslessness guarantee, or safe additional autonomy.

| Case | Result | Observed behavior |
|---|---|---|
| `plain-prose-no-op` | PASS | Returned the original sentence because every clause is operative; no ledger was imposed. |
| `plain-prose-ambiguous-repetition` | PASS | Kept the deadline at the point of action and flagged the uncertain summary occurrence instead of blindly deduplicating. |
| `report-deceptive-repetition` | PASS | Consolidated framing while retaining both provider observations, conditions, and counterevidence as distinct evidence units. |
| `report-preserved-caveat` | PASS | Tightened the result but retained the untested-cancellation caveat and the measured latency scope. |
| `report-evidence-separation` | PASS | Preserved separate observation, conclusion, and decision blocks. |
| `durable-stale-unproven` | PASS | Classified the paragraph as `FLAG`, retained it, and named the missing replacement authority. |
| `durable-exact-links-and-anchors` | PASS | Preserved the exact heading and both inbound links after consumer inspection. |
| `durable-exact-phrase-consumer` | PASS | Retained the phrase and flagged the blocked rewrite because the exact-string consumer was outside authorized scope. |
| `durable-authorized-paired-consumer` | PASS | Updated source and authorized consumer together, named the consumer in the ledger, and required the consequence-level test. |
| `durable-untouched-prose-no-reflow` | PASS | Deleted only the obsolete bullet and preserved neighboring line breaks. |
| `instruction-installed-home-refusal` | PASS | Refused the runtime-home edit and redirected to the physically owning source repository. |
| `instruction-boundary-preservation` | PASS | Retained the trigger, stop gate, authority, and completion contract without broadening permission. |
| `instruction-catalog-and-traveling-reference` | PASS | Inspected the catalog and installed reference closure and retained the operative pointer. |
| `comment-license` | PASS | Preserved license and copyright text. |
| `comment-doctest-example` | PASS | Preserved doctest syntax and expected output and required the doctest run after an edit. |
| `comment-tool-directive` | PASS | Preserved machine-consumed directives, generated marker, and non-obvious rationale. |
| `helper-beneath-driver` | PASS | Returned the proposed slim text, ledger, flags, and checks while leaving authorization, verification, and completion with the caller. |
| `route-prune-skills` | PASS | Routed the lifecycle decision to `skill-lifecycle`. |
| `route-prune-installed-assets` | PASS | Routed installed-state pruning to the owning installer contract. |
| `discovery-natural-language-positive` | PASS | Selected `text-prune` for an explicit tightening and deduplication request. |
| `discovery-unrelated-writing-negative` | PASS | Did not require `text-prune` for drafting new text without a compression request. |
