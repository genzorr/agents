# Test Value: Ambiguous Cases

Use these comparisons when appearance does not settle a candidate's detection value. The authority for an expectation must stand independently of the implementation being tested: a supported contract, specification, regression evidence, analytical result, or reference implementation can supply it. An independent oracle does not require an independent agent.

| Inspection signal | Discriminating question | Preservation consequence |
|---|---|---|
| Same invariant at two layers | Can one fail through broken wiring, transport, persistence, rejection, or recovery while the other stays green? | Retain distinct reach; consolidate only after the keeper detects the displaced failures. |
| Expected value comes from the helper under test | Would a constant return or shared mistake satisfy both sides? | Repair the oracle using independent evidence before claiming meaningful detection; do not discard an otherwise valid contract. |
| Mock or spy assertion | Does it check an observable protocol or required ordering, or does the mock supply the behavior supposedly proved? | Preserve the protocol detector; repair vacuous proof at an appropriate real boundary. |
| Exact strings, paths, manifests, or source inspection | Are these shipped bytes, supported APIs, release artifacts, safety limits, or user-facing instructions themselves the contract? | Preserve independent artifact checks; implementation-derived expectations need a separately justified replacement. |
| Exact numerical value or tolerance | Does independent analytical/reference evidence support the units, rounding, clamp order, and tolerance? | Preserve scientific expectations; baseline agreement proves preservation, not scientific validity. |
| Slow test or large fixture | What unique consequence does it protect, and can cheaper proof reach the same failure? | Measure cost when available; transfer detection before replacing it. Slowness alone does not justify removal. |
| Export used only by local tests | Is it supported for external consumers or needed for compatibility, dependency injection, or another public contract? | Inspect external/public evidence before removing the seam; unresolved consumers block removal. |
| Failing baseline | Is this a product defect, environment issue, flaky behavior, or stale expectation against independent authority? | Classify and preserve the evidence; green cleanup is not a reason to remove the detector. |

For example, a packet hash test that compares two calls to the same helper can pass when that helper always returns a constant. A standard-library digest expectation can repair that oracle, but a caller test may still fail to cover the helper's input variants or artifact placement. Packet layout and overwrite refusal can protect public artifact shape and evidence integrity independently; their structural appearance does not make them redundant.

## Provenance

The bounded audit mechanism is re-authored from [OpenClaw test-audit at aa31aeefb745aba23a8393ea50ddb26251132c31](https://github.com/openclaw/openclaw/blob/aa31aeefb745aba23a8393ea50ddb26251132c31/.agents/skills/test-audit/SKILL.md), with its [MIT notice](../LICENSE). This adaptation retains consequence-based candidate evidence and preservation reasoning. It excludes upstream always-on authoring gates, campaign orchestration, fixed toolchains, remote runners, foreign review services, and landing automation. The upstream executable dependency closure was not fully screened; this is a prose adaptation, not an upstream installation or an effectiveness claim.
