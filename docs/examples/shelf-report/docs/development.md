# Develop and operate Shelf Report

All commands on this page are illustrative. This folder contains a document example, not the `shelf-report` program, its packaging or tests. In a real repository, maintain these commands against its actual launcher and check their output.

## Setup and run

The hypothetical project uses Python 3.12 and uv. From its source root:

```sh
uv sync
uv run shelf-report export samples/stock.csv --output report.md
```

`uv sync` prepares the project environment; `uv run` selects it. Callers need no separate activation instruction. The export reads the sample and creates or replaces `report.md`. Use an output path you own, especially during development. [The README](../README.md#try-the-ordinary-path) shows the filtered result; [the spec](export-stock-report.md) owns exact behavior and exit codes.

## Checks

The illustrative focused command is:

```sh
uv run pytest tests/test_export_cli.py
```

The suite would invoke the public CLI in isolated temporary directories, using the cases in [the spec](export-stock-report.md#examples-and-check-routes). Expected Markdown comes from those independently written fixtures, not the production renderer. For preservation cases, retain known report bytes, invoke the command with the failing input and compare the output bytes. Check exit status and the relevant stderr information as well.

Changing a private temporary filename should not break the behavior checks. Truncating OUTPUT before validation should break them. Use those distinctions if the suite's value is uncertain; do not add a mandatory mutation test to every change.

A behavior change also checks affected docs and links. Run the actual project's existing broader suite when shared code or a concrete remaining risk requires it; this example does not invent an all-project release gate.

## Diagnose an export

Start with the command, selected input/output paths and exit status. Keep user input intact.

- Code 2: correct the input or threshold identified by the error. Verify that the previous report remains unchanged before rerunning.
- Code 1: inspect the reported rendering or destination failure. Check the supported parent directory and available space. Preserve a useful failed temporary file while investigating; do not replace the good report with it.
- Code 0 with an unexpected report: compare the full input, threshold and expected spec example. A filtered report does not mean the source inventory was changed.

Use a small reproduction in an owned temporary directory. Retain the original failure and source/configuration in the existing issue; put a reusable diagnosis fact here only when future users need it. Fix a recurring setup problem in the project command when possible.

## Outputs and history

The caller owns report files and any useful failed output. Keep decisive inputs, before/after results and source basis with the existing work record or a referenced retained artifact. A closed issue grants no permission to remove someone else's data.

For this fictional collection, [bug 07](../history/bug-07/record.md) demonstrates retained original bytes and [change 12](../history/change-12-low-stock.md) demonstrates how a later feature links them without rewriting them. These are teaching artifacts, not runtime qualification.
