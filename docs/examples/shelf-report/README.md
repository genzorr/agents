# Shelf Report

Shelf Report helps a small workshop find items to restock. It reads a local CSV of item names and quantities and writes a Markdown report. Invalid input leaves the last good report intact.

This is a **fictional documentation example**, showing the agreed version 2 behavior. There is no executable application in this folder. Every command below and in the development guide is illustrative; the example history is invented to demonstrate preservation, not a record of work performed for this package.

## Try the ordinary path

After the setup described in [development and operation](./docs/development.md), the illustrative command is:

```sh
uv run shelf-report export samples/stock.csv --output report.md --below 5
```

The [sample input](samples/stock.csv) contains Adapter 3, Cable 12 and Clamp 0. The report contains:

```markdown
# Stock report

| Item | Quantity |
| --- | ---: |
| Adapter | 3 |
| Clamp | 0 |
```

Omit `--below` to include every item. The tool writes the selected report and its temporary publication file; it does not modify the CSV or contact a service. It does not manage inventory or place orders.

## Where to go next

- To change output or error behavior, read [export behavior](./docs/export-stock-report.md).
- To understand validation, filtering and publication, read [architecture](./docs/architecture.md).
- To run checks or diagnose an export, read [development and operation](./docs/development.md).
- Before an agent edits this project, read [AGENTS.md](AGENTS.md).
- To understand the version 2 change, read its [change record](history/change-12-low-stock.md). Routine use does not require this history.

The current docs describe the selected behavior. Native tests would need to establish its implementation; none ran in this documentation example.
