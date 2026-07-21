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

<!-- The one question this experiment answers. -->

## baseline_ref

<!-- The `baseline` id of the baseline-manifest.md instance this Protocol compares against. -->

## units

<!-- Unit(s) of measurement/analysis. Flat list. -->

-

## metrics

<!-- Exact metric names this Protocol reports. Flat list. -->

-

## gates

<!-- One exact pass/fail (or non-regression) threshold per metric or decision, decided before any run. -->

-

## commands

<!-- Exact commands that produce the metrics and artifacts below. design-experiment freezes
     these; it never runs them. -->

-

## artifacts

<!-- Output paths/files the commands above must produce. -->

-

## abort_conditions

<!-- Conditions that stop execution early. -->

-

## deviation_policy

<!-- What counts as an allowed deviation during execution, and what instead forces a new Protocol. -->

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
