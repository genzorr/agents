# Performance and delivery reliability

Open this reference when the change affects rate, bytes, queueing, serialization, sinks, shutdown,
or application latency. Establish a baseline before changing behavior.

## Bound the stream

Define a budget per operation and per second: record count, retained bytes, formatting/allocation
cost, queue depth, and acceptable loss. Prefer once-only, change-only, aggregation, throttling, and
deduplication before sampling. Summaries should include first/last time, count, and suppressed
count. Any sampling needs a documented loss budget, deterministic correlation, and exclusions for
failure, safety, audit, crash-adjacent, and experiment-evidence records.

For a queue, explicitly choose block, drop, spill, or degrade behavior. Make drops observable
from a safe context and keep the drop path non-recursive. Bound event size and serialization time;
on serialization failure, emit a minimal safe fallback and count the failure. Do not put large
values into a record merely because the sink accepts them.

## Sinks and shutdown

Treat logging failure as isolated from ordinary application behavior unless a separate safety or
audit contract requires fail-closed behavior. Test missing collectors, permission errors, disk full,
rotation, slow sinks, broken pipes, sink exceptions, queue full, and malformed values. Normal
shutdown should stop listeners and flush/drain with a bounded timeout, then report what was dropped.
Do not claim delivery after hard termination or a fatal runtime failure.

## Measurement recipe

Capture the smallest relevant before/after set: latency or throughput, CPU, allocations, records,
bytes, suppression/drop counts, queue depth, and shutdown duration. For control/GPU work, also
capture the target's jitter, watchdog margin, real-time factor, GPU throughput, and synchronization
count. Use the project's normal benchmark and timing method; do not add synchronization merely to
measure logging. A change is an improvement only if it answers the diagnostic query within the
budget and preserves required application behavior.
