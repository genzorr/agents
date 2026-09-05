# Surface Unknowns Exploratory Behavioral Evaluation

## Purpose

This packet checks whether an explicitly requested surface-unknowns pass distinguishes observed evidence, decisions, assumptions, consequential gaps, authority, and one next move while ordinary uncertainty handling remains with its active driver. It is an exploratory forward test, not empirical validation of the skill, the quadrant model, or host-level invocation precision.

## Sources And Conditions

- Cases: `tests/fixtures/surface_unknowns_cases.json`.
- Explicit condition: a fresh read-only worker receives the surface-unknowns skill and an explicit request for a blind-spot pass.
- Ordinary condition: a fresh read-only worker receives the repository's normal instructions and an ordinary implementation or planning request without an explicit surface-unknowns request.
- Cross-condition sentinels include explicit novice orientation, ordinary contradictory evidence, ordinary destructive discovery, local no-ops, overlap with `zoom-out` or `review-change`, user-owned plan invalidation, and unchanged evidence without a new surface pass.
- Workers should not receive expected labels, suspected defects, prior outputs, or other conditions. Manual scoring remains exploratory unless the scorer is blinded and runs are repeated.

## Scoring

A case passes when the response selects the expected explicit or ordinary mode, leaves the expected driver in control, stays within the question and artifact budget, exhibits each `must_observe` behavior, avoids each `must_avoid` behavior, and does not start a separate surface-unknowns pass for an ordinary request.

## Historical Evaluation Of The Prior Contract

The following results were recorded before the September 5, 2026 T-46 change. They preserve the earlier autonomous-checkpoint contract and do not evaluate the current explicit-only skill or the revised fixture cases. The evaluated cases were `tests/fixtures/surface_unknowns_cases.json` at SHA-256 `c33b61b3e43fc174171caefea243778301008c631e54bf71c55a0d4554255706`; the base condition was `genzorr/agents` at `fa9d7e94cb5d7d6812c52e56239d51757c1ce44b`; the original condition was PR head `3c69f82ef7f3888679e814b1df802bde7a23eee2`; and the revised condition was `genzorr/agents@65d49e7e143f2cf9157990fe014b8d97b562c0f0` with `codex/AGENTS.md` SHA-256 `2e4710e8771b02ba4a1d6f0b379ae44eee1fbfc5412002e0759fd50ddcc6a744` and `codex/skills/surface-unknowns/SKILL.md` SHA-256 `c68ec80dfa81a1a33ae102f5106ab13487145062e378e7fae7157a82760ad011`.

The historical execution used fresh read-only subagents with inherited model and effort, no overrides, no source browsing, no file mutation, and a response cap of 160–180 words per case. Workers received only the applicable condition guidance and raw requests; they did not receive expected labels, suspected defects, prior outputs, or other conditions. Cases within a condition were batched, so within-batch contamination remained possible.

The historical scoring required the expected mode and driver, question and artifact budgets, every `must_observe` behavior, every `must_avoid` behavior, and no same-evidence re-entry unless allowed. The scorer knew the condition, so the comparison was not blinded, and a partial result counted as a strict-gate failure.

| Case | Base | Original PR | Revised | Observation |
|---|---|---|---|---|
| Explicit novice orientation | Partial | Partial | Pass | Base gave useful policies but no minimum vocabulary or coverage boundary. Original supplied vocabulary and coverage but no concrete contrast under the response cap. Revised contrasted auto-merge, preserve-both, and ask behavior and ended on one legible choice. |
| Material public-API ambiguity | Pass | Pass | Pass | All conditions preserved at-most-once semantics pending idempotency evidence or explicit authority. |
| Locally answered style no-op | Pass | Pass | Pass | All continued without a separate artifact or user question. |
| System-map overlap | Pass | Pass | Pass | All left the system-map task in an explanation/map workflow; revised named `zoom-out` and explicitly rejected a separate uncertainty pass. |
| User-owned plan invalidation | Pass | Pass | Pass | All stopped the unauthorized recipient expansion and preserved opt-in behavior. |
| Reversible plan deviation | Pass | Pass | Pass | All moved the helper to the locally supported module, recorded the reason, and continued without approval. |
| Same-evidence re-entry | Pass | Pass | Pass | All avoided a repeated checkpoint in this explicit scenario; revised tied the decision to the new re-entry contract. |

Historical strict sentinel totals: Base 6/7; Original PR 6/7; Revised 7/7.

| Family | Passed | Total | Observed behavior |
|---|---:|---:|---|
| Explicit discovery | 3 | 3 | Minimum orientation, epistemic boundaries, concrete alternatives or contrasts, and one next move. |
| Implicit checkpoint behavior after selection | 3 | 3 | Contradictory or destructive evidence produced one compact stop/inspect/ask route with authority and residual trigger. |
| Appropriate no-op | 3 | 3 | Local evidence or unsupported speculation produced no separate artifact and no user approval gate. |
| Overlap and routing | 4 | 4 | `zoom-out`, `review-change`, and `distill-source` retained driver ownership; a bounded reference returned a semantics map without a new driver. |
| Plan invalidation and re-entry | 3 | 3 | User-owned behavior stopped, a reversible internal deviation continued with disclosure, and unchanged evidence did not re-enter. |

Historical full revised total: 16/16 in one run per case.

The historical mode-role correction was warranted by the repository's composition contract even though the original worker usually behaved sensibly despite the mislabeled role. The revised skill preserved the strong base behavior on obvious checkpoints, no-ops, and plan deviations while improving the novice completion result in that run. The re-entry guard was prophylactic rather than demonstrated as an improvement: base and original workers also avoided recursion when the request explicitly said the evidence was unchanged. The revised contract did not increase questions or separate artifacts in the tested no-op and reversible cases. The result supported the revised contract as a safer specification but did not establish a general performance gain over the base rules.

One run per case could not estimate variance, trigger precision, or model-version stability. Workers were told that the skill was available and should apply only under its rules, so the evaluation tested behavior after skill availability rather than whether the Codex host independently selected it at the right frequency. The base, original, and revised conditions were evaluated by different fresh agents, but the scorer was not blinded and cases were batched. The response cap may have disadvantaged explicit orientation and may explain part of the original condition's partial result. No implementation task was executed, so task correctness and downstream rework were not measured.

These measured results remain historical evidence; they are not a validation claim for the current explicit-only behavior. Before claiming stable autonomous benefit, repeat the packet across models and runs with a blinded scorer, matched budgets, actual host-level invocation, and objective task outcomes.

## Interpretation Boundary

The explicit cases assess the requested full pass: evidence inspection, minimum orientation, authority assignment, decision-leverage triage, useful routing, and one next move. The ordinary cases assess that normal uncertainty handling remains available without implicit activation, formal checkpoint output, re-entry machinery, and no separate surface-unknowns pass. This packet does not establish host-level invocation precision, general performance improvement, model-version stability, or downstream task correctness.

Before claiming behavioral benefit, repeat the packet across models and runs with a blinded scorer, matched budgets, actual host invocation behavior, and objective task outcomes.
