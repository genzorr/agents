# Working on Shelf Report

This repository owns the local CSV-to-Markdown exporter and its current docs. It is a fictional documentation example; command names illustrate the intended project interface.

Before changing export behavior, read [the export spec](./docs/export-stock-report.md), including invalid-input preservation. Read [architecture](./docs/architecture.md) for responsibilities and publication order, then [development guidance](./docs/development.md) for the affected checks. Use disposable input/output directories for checks; preserve user-supplied files.

Keep the supported default export unchanged when adding options. A behavior change updates the affected spec examples, commands and checks together. Keep original investigation inputs/results in their existing issue or history entry; do not rewrite them to match the new behavior.

Complete the requested local implementation and relevant diagnosis/retesting. Return a choice when it changes an agreed promise or needs an effect outside the request. There is no installation, network service or hardware operation hidden in the export path.

This example uses repository history files for its two fictional records. A real project should use its existing record system rather than add this directory merely to match the example.
