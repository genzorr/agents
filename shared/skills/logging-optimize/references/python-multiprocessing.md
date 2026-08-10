# Python and multiprocessing

Open this reference when the target uses Python logging, worker processes, subprocesses, queues,
or asynchronous sinks. Preserve the application's existing configuration ownership.

## Configuration and ownership

Python's hierarchical named loggers are compatible with central configuration; importing one
global logger everywhere is not a requirement. Configure handlers at the process boundary that
owns them. A library should normally create named loggers and never configure the root logger or
change application handlers as a side effect.

With `spawn`, child processes do not inherit usable application state in the same way as `fork`:
initialize logger context and handlers deliberately after start. With `fork`, inherited handlers,
locks, and open file descriptors can duplicate records or deadlock. Document the chosen start
method, process identity, run/operation correlation, and who owns each sink.

## Queues and exceptions

For asynchronous delivery, specify full-queue behavior: block, drop, spill, or degrade. A hot
worker must not block on logging without an explicit budget. Count drops from a safe context and
avoid recursive logging from the queue or serializer failure path. Preserve exception type, stack,
cause, and child exit status. The parent must not call a dead child “finished” without classifying
its exit code, signal, exception, or coordinated stop.

Log an exception once at the boundary that handles or terminates the operation. A lower layer may
enrich and re-raise, or log when it recovers, retries, suppresses, or materially changes behavior.
For repeated child failures, keep the first stack-bearing transition, periodic count/suppression
summaries, and a recovery event.

## Shutdown and tests

Normal shutdown should stop listeners, drain or explicitly bound the remaining queue, flush with a
timeout, and report drops. Do not claim delivery after `SIGKILL`, a fatal crash, `os._exit`,
`Process.terminate()`, or a broken sink. Test the expected loss behavior instead.

Use in-process capture for field/level assertions and subprocess fixtures for process boundaries.
Cover normal exit, unhandled exception, signal/forced termination, coordinated shutdown, multiple
workers, duplicate-handler prevention, queue overflow, serialization fallback, sink failure, and
listener drain. Assert the diagnostic query, not only that a line was emitted.
