---
name: logging-optimize
description: Guides agents through inspect-first design, review, and minimal improvement of application diagnostic logging and structured events. Use when adding or reviewing logs, correlation, completion summaries, repeated-failure handling, asynchronous delivery, redaction, or logging overhead; classify metrics, traces, telemetry, audit records, and experiment evidence separately.
---

# Logging Optimize

Use this skill as the bounded driver for improving diagnostic logging. Follow the target
project's `AGENTS.md`/`CLAUDE.md`, safety rules, and native logger/framework contracts first.

## Scope

Apply it to application logs, diagnostic events, lifecycle and state-transition records,
completion summaries, operator-facing messages, and their delivery or queryability. It may
identify a requested “log” as another signal and hand off. Do not turn metrics-only, tracing-only,
high-rate sensor capture, audit/compliance-system design, experiment-result formatting, or
vendor/backend selection into a logging change.

## Inspect-first workflow

1. **Name the diagnostic decision.** Write the operator, developer, or researcher question that
   must become answerable. List one or two representative queries.
2. **Inspect target reality.** Map processes, threads, subprocess start methods, hot loops, GPU
   work, logger APIs, handlers, queues, sinks, stdout/stderr consumers, ROS or container
   contracts, run directories, retention, privacy boundaries, and existing query tools. Record
   what is measured versus inferred.
3. **Classify the signal.** Separate diagnostic logs/events, completion summaries, operator
   messages, metrics, traces/spans, high-rate telemetry, audit records, and experiment evidence.
   Preserve each signal's existing owner and contract.
4. **Choose the semantic operation.** Add a completion summary only when a unit has a bounded
   start and terminal outcome, an owner, a useful duration, and query value. A request, CLI run,
   worker lifecycle, command, transition, retry sequence, or experiment run may qualify; a frame
   or control tick qualifies only when its rate and volume are explicitly budgeted.
5. **Design the smallest contract.** Keep ordinary start, transition, warning, recovery, and
   crash-adjacent breadcrumbs. Add stable names, types, units, correlation, controlled outcomes,
   and bounded domain fields only when a query needs them. Open `references/event-contract.md`
   for field and schema details when designing machine-consumed events.
6. **Set failure and interference budgets.** Define permitted fields, maximum rate/bytes, queue
   overflow behavior, expected loss, retention, redaction, shutdown/flush limits, and latency or
   real-time constraints. Open the relevant reference before changing Python multiprocessing,
   robotics/GPU, research runs, privacy, or delivery behavior.
7. **Make native, minimal changes.** Reuse the project's logger hierarchy, handlers, ROS logging,
   Compose streams, run directories, and result artifacts. Do not introduce Loguru, structlog,
   OpenTelemetry, or a vendor merely to satisfy this skill. Do not globally configure a library's
   logging unless the project already owns that boundary.
8. **Verify the improvement.** Exercise success and failure paths, concurrency, cancellation or
   timeout, repeated failures and recovery, redaction, rate/volume limits, sink/queue failure,
   normal shutdown, abrupt termination where feasible, and runtime overhead. State untested
   failure modes and expected rather than impossible delivery guarantees.

## Core rules

- Structured events require stable semantics, not a universal format. Use JSON when a collector
  requires it; concise text remains valid for consoles, operator instructions, crash breadcrumbs,
  and byte-level stdout contracts. Keep a human `message` when useful.
- Preserve native severity semantics: debug detail, significant expected lifecycle at info,
  handled degradation/retry at warning, failed operations at error, and critical/fatal only where
  the native framework defines it. Never collapse everything to `info` and `error`.
- Record an exception once at the boundary that owns the outcome, preserving type, stack, and
  cause. Lower layers enrich and re-raise, or log only when they recover, retry, suppress, or
  materially change behavior. For repeated failures, emit an immediate transition, bounded
  summaries with counts and suppression totals, and a recovery transition.
- Prefer once-only, change-only, aggregation, throttling, and deduplication before sampling.
  Never sample safety transitions, failures, crash-adjacent lifecycle, audit records, experiment
  outcomes, or required reproduction evidence without an explicit loss policy.
- Queues and sinks are best-effort application infrastructure unless a separate fail-closed
  safety/audit design says otherwise. A `finally` block, flush, or graceful shutdown cannot promise
  delivery after hard termination, fatal runtime failure, queue loss, or sink failure.
- Logging must not perturb the behavior being observed: no blocking I/O or eager large-value
  formatting in hot paths, no unplanned synchronization for GPU timing, and no images, arrays,
  point clouds, or raw joint/sensor streams in ordinary log payloads.

## Progressive references

Open only the reference that matches the target and current decision:

- `references/event-contract.md` — fields, schema evolution, and diagnostic queries.
- `references/python-multiprocessing.md` — logger hierarchy, spawn/fork, queues, exceptions,
  exit status, and bounded shutdown tests.
- `references/robotics-realtime.md` — ROS/native logging, clock domains, control-loop/GPU
  budgets, safety transitions, and telemetry separation.
- `references/research-runs.md` — run manifests, result artifacts, correlation, and partial runs.
- `references/privacy-security.md` — allowlists, redaction, injection, retention, and secret tests.
- `references/performance-reliability.md` — rate/volume budgets, overflow, fallback, sink failure,
  flush/loss, and measurement recipes.
- `references/sources.md` — authoritative framework/standard sources and the pinned upstream
  skill's useful concepts and unsafe absolutes.

## Review and completion criteria

Reject a change that only serializes ambiguous prose. Accept it when the diff is minimal and
native, the requested diagnostic queries are answerable, ordinary lifecycle and operator output
remain correct, fields/types/units/outcomes and correlation are stable, privacy and size budgets
hold, and failure behavior is tested or explicitly bounded. Review at least success, handled and
unhandled failure, retry exhaustion, cancellation/timeout, orderly shutdown, forced termination,
concurrent producers, queue overflow, serialization fallback, sink failure, and recovery when
applicable. For real-time or GPU work, compare the project's relevant jitter, watchdog, real-time
factor, CPU, throughput, and synchronization measures against a stated budget.

Compose with `diagnose` when the logging request is driven by a bounded fault, `review-change`
for an independent diff review, and `design-experiment` when a performance or loss budget needs a
frozen protocol. This skill remains the driver for the logging task and does not relax another
skill's protocol.
