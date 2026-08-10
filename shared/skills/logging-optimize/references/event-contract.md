# Event contract

Open this reference when a machine-consumed diagnostic event, completion summary, or schema
change is being designed. A contract is useful only if it makes a real diagnostic query easier.

## Minimal fields

Use the project's native names where they already exist. For new structured events, prefer:

| Field | Rule |
| --- | --- |
| `timestamp` | Record source wall time; document its precision and timezone. |
| `event.name` | Stable lower-case name, such as `worker.completed`; required for structured events. |
| `severity` | Preserve the native level and its operational meaning. |
| `component.name` or `service.name` | Stable producer identity, not only a PID or container name. |
| `event.schema_version` | Add when machines depend on the event; omit for ephemeral debug text. |
| `outcome` | Controlled value such as `success`, `failure`, `cancelled`, `timeout`, or `degraded` for terminal events. |
| `duration_ms` | Use a monotonic clock for timed operations; do not subtract wall timestamps. |
| `message` | Optional concise human rendering; keep attributes independently queryable. |

Add `service.version`, `code.commit`, `deployment.environment`, `run.id`, `operation.id`,
`trace.id`, `span.id`, `process.pid`, worker identity, attempt count, error type/code/stack,
and domain fields only when they exist and answer a query. Label clock domains when wall,
monotonic, ROS, simulation, sensor, or device time could be confused. Keep domain values to
bounded scalars or short enums; never put images, arrays, point clouds, or arbitrary objects in a
diagnostic event.

## Compatibility

Keep names, types, units, and controlled values stable. Add optional fields compatibly. A breaking
rename, type/unit change, or outcome change needs a schema/event version, migration or dual-read
plan, and updated representative queries. Do not invent tracing IDs when the target has no trace
system; use the existing run or operation ID instead.

Normalize only what the target needs. A small helper may add common fields and safe fallback
serialization, but do not make every logging call a heavyweight typed API. If serialization fails,
emit a minimal safe fallback and a visible counter without recursively logging the serializer error.

## Query-driven examples

Choose fields by writing the query first. Useful queries include:

- Which worker ended, was it expected, and did it succeed, raise, receive a signal, or get stopped?
- Which startup step first failed, on which process, and did traffic later recover?
- Which operation timed out, how many attempts ran, and what was the last error class?
- Which run/config/commit/dataset/seed produced this result, and where are its durable artifacts?
- How many records were suppressed or dropped, and did shutdown drain the queue?

If a field does not help answer a concrete query or correlate with an existing owner, leave it out.
