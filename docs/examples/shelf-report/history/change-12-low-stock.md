# Change 12 — add a low-stock report

Fictional change record. The documents in this example describe the selected version 2 contract and design. This record does not claim implementation, executed tests, review or release.

## Request and decision

The workshop wants to find items below a chosen stock quantity. In this example, the maintainer chooses `--below N` with a strict comparison, an unfiltered default, and validation of the complete input before filtering. A threshold equal to an item's quantity excludes that item. An empty selection is a successful report.

The existing invalid-input preservation promise remains. There is no requirement to reorder the source file, contact a service or introduce a database. A future partial-import request would need a separate behavior decision.

## Connected changes

| Owner | Version 2 change | What remains stable |
| --- | --- | --- |
| [README](../README.md) | Show one filtered invocation and its expected output | Purpose and unfiltered entry path |
| [Export spec](../docs/export-stock-report.md) | Add EXP-5; clarify that EXP-2 covers all rows with a filter; add boundary and invalid-row examples | Existing IDs EXP-1 through EXP-4 |
| [Architecture](../docs/architecture.md) | Insert row selection after complete validation and before rendering | One publisher and preserved output on failure |
| [Development guidance](../docs/development.md) | Route checks to the expanded scenario table | Public CLI testing and independent expectations |
| [Agent entry](../AGENTS.md) | No change needed: its behavior/check routes already apply | Local boundaries and preservation of originals |
| Hypothetical implementation/tests | Add the optional argument and selection; exercise new cases and retained preservation cases | No claim that these source files exist in this package |

## Evidence and completion

The [v1 contract](export-v1.md) and [bug 07 original](bug-07/record.md) stay unchanged. The original failure explains the validation/publication concern, but gives no evidence for threshold filtering or a later implementation.

A real delivery would add its actual source/configuration, relevant command outputs, remaining limits and required review result here or at the existing issue owner. It would say separately whether the feature had been implemented, reviewed and released. It would not mark the new behavior checked merely because the documents agree.

The reading exercise is complete when a reader can find EXP-5, explain why a bad excluded row still fails, identify the public CLI checks and update the connected docs without reading a private discussion.
