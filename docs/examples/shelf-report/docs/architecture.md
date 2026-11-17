# How export works

Shelf Report has one path: read and validate the complete CSV, select rows, render the complete report, then publish it. The CLI passes arguments into that path and translates outcomes to the exit codes in [the export spec](export-stock-report.md).

## Responsibilities

| Part | Owns | Does not need to know |
| --- | --- | --- |
| CLI | Arguments, input/output selection, exit status and user-facing errors | Temporary publication filenames |
| CSV reader and validator | File structure, names and quantities; complete validated rows or a located error | Filtering and report destination |
| Row selection | Optional strict quantity threshold over valid rows | CSV parsing and disk writes |
| Renderer | Stable Markdown and item ordering | Output replacement and error recovery |
| Publisher | Temporary write and destination replacement | The meaning of stock quantities |

Validate before filtering. Otherwise a bad row could disappear from a filtered report and escape EXP-2. The selection function receives validated rows; it cannot decide to ignore parsing errors.

Render before replacing the destination. The publisher writes a temporary file beside OUTPUT, closes the completed file and replaces OUTPUT only when that preparation succeeds. EXP-2 requires preservation on invalid input; EXP-3 extends it to rendering and prepublication write failures. Same-directory staging is the chosen mechanism, not an extra user requirement.

## One failure path

An input row contains `Cable,many`. Validation returns the input line and error. No row selection, rendering or publication occurs, so an existing report survives. A renderer exception also prevents publication. If temporary-file writing fails, the publisher reports code 1 through the CLI and retains useful diagnostics without treating a partial file as a completed report.

The caller keeps the prior report and can correct the input or destination problem. [Development and operation](development.md#diagnose-an-export) owns the diagnostic steps. Power-loss durability and concurrent writers would need additional design and evidence; they are outside the selected single-writer contract.

## Why the design changed in version 2

Version 1 sent validated rows straight to rendering. Version 2 adds row selection between those two responsibilities. The [change record](../history/change-12-low-stock.md) preserves the decision and affected docs. The original validation and publication promises remain the same, so the change does not justify replacing their checks with filter-only tests.
