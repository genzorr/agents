# Experiment Ledger

<!-- experiment_ledger_template_version: 1 -->
<!-- Execution/accounting state only: what ran, when, against which Protocol. This is never a
     Readout, an Evidence ledger, or a current-knowledge store — it records that a run happened,
     not what it means. -->

One row per run/commit reference declared in the Protocol's `run_set` (or a single `planned`
placeholder row if `run_set` is still empty at freeze time).

| run_ref | protocol | protocol_sha256 | started_at | status | notes |
|---|---|---|---|---|---|
|  |  |  |  | planned |  |

<!-- status: planned | ran | aborted -->
