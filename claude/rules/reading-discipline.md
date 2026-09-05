# Reading Discipline

Read the part you need, not the file. Narrow to paths before searching content.

## Narrowing Order

Reach for the cheapest tool that can answer the question:

1. `Glob` when you know the file name or path pattern.
2. `Grep(output_mode="files_with_matches")` when you know the content but not the file.
3. `Grep(output_mode="content", path=<single file>)` to find the lines.
4. `Read(offset, limit)` for the code itself.

Keep content-search results bounded; locate relevant lines before reading the surrounding region. Read a file whole when the task requires reasoning across all of it, such as config, schemas, ADRs, or threat models.

When a task hands you a list of large source files, read the acceptance criteria first and let it tell you which regions matter.

## Searchable Interfaces

Treat filenames, symbols, type names, headings, and test names as search handles. For new code and durable docs, prefer stable, domain-specific names and one canonical spelling per concept; put non-obvious invariants and provenance at the definition or canonical document. Do not rename working APIs or restructure files solely for agent discoverability; make that tradeoff explicit when the task or measured navigation friction justifies it.
