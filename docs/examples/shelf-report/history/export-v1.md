# Export behavior v1 — retained original

Fictional original contract. Kept here to demonstrate a historical basis; use [the current export spec](../docs/export-stock-report.md) for current work.

The exporter reads the complete stock CSV and includes every valid item in its Markdown output. Invalid input exits with code 2, identifies the error and leaves an existing report unchanged. Valid output is ordered by item name. A rendering or prepublication write error exits with code 1 and preserves the previous report. Export operates locally and never edits its source input.

There is no filtering option in this version. The current EXP-1 through EXP-4 preserve these promises with more explicit wording. Later filtering decisions do not change what this original said.
