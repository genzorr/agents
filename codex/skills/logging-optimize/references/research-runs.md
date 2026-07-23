# Research runs and experiment evidence

Open this reference when the target is a benchmark, training/evaluation run, robotics experiment,
or other reproducibility-sensitive workflow. Diagnostic logs explain behavior; they are not the
result schema or evidence by themselves.

## Durable run identity

Keep a run manifest and machine-readable result artifact under the project's existing run/output
owner. Correlate, when available, run ID, resolved configuration or digest, code commit and dirty
state, dataset/version, seed, environment/hardware, command, timing protocol, outcome, and artifact
paths. Represent partial, negative, cancelled, and failed outcomes explicitly. Do not invent a
second run registry solely to make logs queryable.

Use logs for lifecycle, warnings, failures, retries, resource anomalies, and links to artifacts.
Use result tables, plots, arrays, manifests, and scripts for claims and measurements. Keep high-rate
frame data, point clouds, raw metrics, and model checkpoints in telemetry/artifacts, not log fields.

## Validation

Check that a representative result can be traced to its run/config/commit/dataset/seed and that a
failed or partial run remains discoverable. Verify artifacts exist and are not silently replaced by
parse-dependent prose. Test interrupted runs, repeated labels, resumed runs, negative results, and
cleanup/retention behavior when they are part of the target contract. Freeze a protocol with
`design-experiment` when the logging or performance budget is itself an experiment.
