# Reading Discipline

Start at the selected project's entry and applicable instructions. Open a known document directly. If the owner is unclear, inspect a limited filename view of current docs, then open the pages relevant to the task. Descriptive filenames and headings should make that choice possible.

A filename listing is discovery, not a request to load every file. Keep history available for questions that rely on past work, without putting all of it in the starting view. Read enough of the affected document to preserve its conditions, exceptions and connected explanation; a narrow source-code search rule is not a reason to miss a spec's surrounding contract.

Use the runtime's available path and search tools. For large source files, find the relevant symbol before reading its context. Read a whole config, schema or design decision when the task depends on the whole artifact. Reuse already-read content unless it changed.

Use clear, stable names for new docs, symbols and checks. Keep useful existing names and references. Move or rename an existing file when it solves a concrete reader problem, updating its callers and preserving supported historical routes.

## Narrowing Order

For source-code search, use the cheapest tool that can answer the question:

1. `Glob` when you know the file name or path pattern.
2. `Grep(output_mode="files_with_matches")` when you know the content but not the file.
3. `Grep(output_mode="content", path=<single file>)` to find the lines.
4. `Read(offset, limit)` for the code itself.

Keep content-search results bounded; locate relevant lines before reading the surrounding region. Read a file whole when the task requires reasoning across all of it, such as config, schemas, ADRs, or threat models.

When a task hands you a list of large source files, read the acceptance criteria first and let it tell you which regions matter.
