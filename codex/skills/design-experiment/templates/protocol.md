# Experiment Protocol

<!-- protocol_template_version: 1 -->
<!-- protocol_readout_contract_version: 1 -->
<!-- Frozen by design-experiment. Every field below is fixed at freeze time.
     A content change requires a new `protocol` id from a fresh design-experiment
     run — never edit these fields in place after freezing. -->

- protocol:
- protocol_sha256:
- mode: <!-- exploratory | confirmatory | regression -->
- created_at: <!-- ISO 8601, set at freeze time -->

## question

<!-- Decision, bounded question/claim, expected mechanism, credible competing explanations, observations that would falsify the explanation, the weakest non-vacuous positive claim a valid result could support, and the stronger claim this Protocol cannot establish. The later decision remains separate from claim selection. -->

## baseline_ref

<!-- The `baseline` id of the baseline-manifest.md instance this Protocol compares against. -->

## units

<!-- Unit(s) of analysis; factors/levels; control; sources of variation; planned seeds, trials,
     tasks, datasets, and environments; and the coverage/count rationale. Flat list. -->

-

## metrics

<!-- Exact metric names, prefixed primary:, guardrail:, diagnostic:, or resource:. Flat list. -->

-

## gates

<!-- Practical thresholds and guardrails, permitted claim boundary, exact rejection scope of a negative result, inconclusive/invalid outcome, and next discriminator, all decided before any run. -->

-

## commands

<!-- Exact commands plus source/data/config/environment identities that produce the metrics
     and artifacts below. design-experiment freezes these; it never runs them. -->

-

## artifacts

<!-- Raw-output, provenance, and applicable validation paths/files the commands above must produce. -->

-

## abort_conditions

<!-- Invalid, unsafe, futile, or over-budget conditions that stop execution early. -->

-

## deviation_policy

<!-- Predeclared aggregation, uncertainty treatment, exclusions, missing-run handling, validity
     threats, and what forces a new Protocol or weaker claim. -->

## run_set

<!-- Closed at freeze time: the finite list of run/commit references this Protocol declares as
     belonging to it. Amend only by creating a successor Protocol — never by appending to a
     frozen Protocol. May be empty at freeze time if runs are not yet scheduled; the list is
     still closed, not an open one waiting to be appended to. -->

-

<!--
protocol_sha256 covers exactly, in this order: mode, question, baseline_ref, units, metrics,
gates, commands, artifacts, abort_conditions, deviation_policy. It does not cover protocol,
run_set, or created_at. See the parent skill's SKILL.md for the canonicalization recipe.
-->
