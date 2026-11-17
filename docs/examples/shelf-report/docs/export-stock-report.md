# Export a stock report

Status: agreed version 2 behavior in this fictional project. This page says what export must do; [architecture](architecture.md) explains the selected implementation. Examples specify expected outcomes and are not executed receipts.

<a id="EXP-1"></a>

## EXP-1 — Read a complete stock file

`export INPUT --output OUTPUT` reads UTF-8 CSV with the header `item,quantity` and at least one data row. Each item name is nonempty and unique, using case-sensitive comparison. A quantity is a base-10 nonnegative integer. The command reads the whole input and never edits it.

<a id="EXP-2"></a>

## EXP-2 — Reject invalid input without replacing a report

Malformed CSV, missing/wrong columns, a duplicate or empty item name, an invalid quantity or no data rows rejects the export. Exit code is 2. Stderr identifies the error and its 1-based physical input line when a line can be identified; the header is line 1. No report is created or changed.

This rule applies to every input row even when `--below` would exclude that row. The exact explanatory sentence is not a stable protocol; exit code, line reference and preserved output are.

<a id="EXP-3"></a>

## EXP-3 — Publish one complete report

For valid input, exit code 0 means OUTPUT contains the complete selected report. Rows are ordered by item name using case-sensitive lexical order. The Markdown format is shown below. A rendering or prepublication write failure returns code 1 and leaves the previous report unchanged. The command reports a useful error and any retained temporary output needed for diagnosis.

The supported case is one writer on a local filesystem supporting same-directory replacement. Multiple writers, network filesystems and power-loss recovery are outside this example's selected scope. A later requirement can extend those guarantees; the current implementation must not claim them.

<a id="EXP-4"></a>

## EXP-4 — Keep the operation local

Export reads INPUT and writes OUTPUT plus its temporary publication file. It sends no data to a service and does not change the stock source. The caller chooses the output destination and owns any retained report or failed temporary output.

<a id="EXP-5"></a>

## EXP-5 — Select low stock explicitly

Optional `--below N` includes only rows whose quantity is strictly less than N. N is a base-10 nonnegative integer. Invalid N rejects with code 2 without changing OUTPUT. Without the option, every valid row is included. If no row matches, write exactly a `# Stock report` heading, a blank line and `No items match.` with a final newline. This is a successful export.

## Examples and check routes

Use the [sample CSV](../samples/stock.csv). It has Adapter 3, Cable 12 and Clamp 0.

| Case | Expected consequence | Clause / intended native check |
| --- | --- | --- |
| No filter | Adapter, Cable, Clamp appear in that order, with 3, 12, 0 | EXP-1/3; `test_full_report` |
| `--below 5` | Adapter and Clamp appear; Cable does not | EXP-5; `test_below_five` |
| `--below 3` | Only Clamp appears; Adapter equals the threshold | EXP-5; `test_threshold_is_exclusive` |
| `--below 0` | Successful report says `No items match.` | EXP-5; `test_empty_selection` |
| `--below -1` | Code 2; existing output unchanged | EXP-5; `test_invalid_threshold_preserves_report` |
| A row says `Cable,many`, with `--below 5` | Code 2, offending line identified; existing report unchanged | EXP-2/5; `test_invalid_row_cannot_be_filtered_away` |
| Publication temporary-file write fails | Code 1; previous report unchanged | EXP-3; `test_staging_failure_preserves_report` |

The exact full report for the unfiltered sample is:

```markdown
# Stock report

| Item | Quantity |
| --- | ---: |
| Adapter | 3 |
| Cable | 12 |
| Clamp | 0 |
```

These expectations are maintained here. [Development guidance](development.md#checks) explains how to exercise them through the public CLI; it does not maintain a second scenario list. The earlier [invalid-input incident](../history/bug-07/record.md) explains why output preservation matters. Its original record has not been revised to claim filter coverage.
