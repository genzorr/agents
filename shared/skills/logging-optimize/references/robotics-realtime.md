# Robotics, real-time, and GPU paths

Open this reference when logging touches ROS, control loops, simulation, sensors, watchdogs, or
GPU-sensitive code. Measure the target's behavior before and after; never assume a logger is free.

## Preserve native contracts

Keep the project's logger, ROS logging levels/throttling, operator messages, launch/container
stdout, safety transitions, and durable artifacts. A completion summary supplements a safety or
state-transition message; it never replaces an immediate operator signal. Do not rewrite every
`print` as JSON or change a byte-level stdout contract without proving that consumers allow it.

## Non-interference

Keep disk and console I/O out of hard real-time paths. For soft real-time or GPU-sensitive paths,
use a non-real-time handoff only when its queue, loss, and shutdown behavior are explicit. Avoid
eager formatting of arrays, images, point clouds, joint states, or sensor samples. Never add a
CUDA/device synchronization solely to timestamp a log or benchmark; use the project's established
timing method. Bound CPU time, allocations, queue operations, and record size in the path.

Prefer once-only, change-only, throttled, aggregated, or deduplicated diagnostics. If records drop,
expose a safe drop/suppression count outside the hot path. Safety events, failures, watchdog
transitions, and crash-adjacent records need an explicit loss policy and normally are not sampled.

## Clock and validation

Use a monotonic clock for durations. Label wall, steady/monotonic, ROS, simulation, sensor, and
device timestamps when they can diverge, pause, or jump. Do not infer causality by sorting unlike
clock domains.

Validate the actual risk: loop jitter, watchdog gaps, real-time factor, CPU and allocation cost,
GPU throughput, synchronization count, queue pressure, output volume, and operator readability.
Exercise repeated failure and recovery, sink/queue pressure, orderly shutdown, container or process
termination, and the safety path. If a real-time budget or loss guarantee cannot be tested, state
the limit and do not call the change verified.
