# Bug 07 — original invalid-input observation

**Fictional evidence record. No program was executed.** This page demonstrates what an unchanged original work record can contain. Its attached bytes are part of the teaching example.

Basis: hypothetical version 1 exporter, the [v1 contract](../export-v1.md), and [this exact input](input.csv). The input has `Adapter,three` on line 2. The selected report initially contained [report-before.md](report-before.md).

Illustrative command used in the story:

```sh
uv run shelf-report export input.csv --output report.md
```

Recorded outcome in the fictional story: exit 2 with an invalid-quantity error at line 2; the report was truncated to zero bytes, retained as [report-after.md](report-after.md). The expected outcome was unchanged report bytes. The failure concerned validation/publication ordering.

The record captures a failure; it does not prove a fix. No `--below` option existed in this basis. Later changes must not edit this record to imply otherwise. Their own results should link this original, identify the changed source and report the checks actually performed.
