# Sources and source selection

Open this reference when checking a domain claim or choosing a framework-specific implementation.
Use authoritative sources for behavior and keep production practice separate from standards and
opinion. The skill does not require adopting any named runtime.

## Primary guidance

- OpenTelemetry: [logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/),
  [resource conventions](https://opentelemetry.io/docs/specs/semconv/resource/),
  [schema evolution](https://opentelemetry.io/docs/specs/otel/schemas/), and
  [exception conventions](https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/).
- Python: [logging](https://docs.python.org/3/library/logging.html),
  [logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html),
  [handlers](https://docs.python.org/3/library/logging.handlers.html),
  [multiprocessing](https://docs.python.org/3/library/multiprocessing.html), and
  [exit-handler limits](https://docs.python.org/3/library/atexit.html).
- OWASP: [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
- Robotics/GPU: [ROS logging](https://docs.ros.org/en/ros2_documentation/jazzy/Concepts/Intermediate/About-Logging.html),
  [ROS clocks](https://design.ros2.org/articles/clock_and_time.html),
  [ROS real-time background](https://design.ros2.org/articles/realtime_background.html), and
  [PyTorch CUDA timing](https://docs.pytorch.org/docs/stable/notes/cuda.html).
- Reproducibility: [JMLR checklist](https://jmlr.org/papers/v22/20-303.html) and
  [SIGMOD guidance](https://reproducibility.sigmodconf.hosting.acm.org/).

## Production pattern and upstream evaluation

Stripe's [canonical log lines](https://stripe.com/blog/canonical-log-lines) support a useful
completion-summary pattern in addition to ordinary traces, with best-effort failure isolation.
Treat it as a context-dependent practice, not a delivery guarantee.

The evaluated upstream is
`boristane/agent-skills@8aa14dd16a1340a6049e6d7cd58e2ed52333a550`,
`skills/logging-best-practices/`. Retain its useful ideas—stable context, correlation, completion
summaries, and query-oriented fields—but do not copy its web/SaaS absolutes: one event per request
as a universal model, always-high-cardinality/business context, JSON everywhere, one logger object,
only `info`/`error`, or `finally` as delivery assurance. This skill's native, bounded, failure-aware
rules are the deliberate adaptation.
