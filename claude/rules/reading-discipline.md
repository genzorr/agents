# Reading Discipline

Read the part you need, not the file. Narrow to paths before searching content.

## Tool Costs

These are not guessable from the tool descriptions:

- **Ripgrep context mode repeats the full absolute path on every line** — on match lines *and* on every `-B`/`-A`/`-C` context line. A broad content search can cost 5–10× what the same information costs via `Read(offset, limit)`. Prefer locating the line, then reading the region.
- **`head_limit` defaults to 250.** Override it to 20–50 for content mode.

## Narrowing Order

Reach for the cheapest tool that can answer the question:

1. `Glob` when you know the file name or path pattern.
2. `Grep(output_mode="files_with_matches")` when you know the content but not the file.
3. `Grep(output_mode="content", path=<single file>)` to find the lines.
4. `Read(offset, limit)` for the code itself.

Going straight to a content search across a directory is the expensive mistake. Read a file whole when the task genuinely requires reasoning across all of it — config, schemas, ADRs, threat models.

When a task hands you a list of large source files, read the acceptance criteria first and let it tell you which regions matter.

## Searchable Interfaces

Treat filenames, symbols, type names, headings, and test names as search handles. For new code and durable docs, prefer stable, domain-specific names and one canonical spelling per concept; put non-obvious invariants and provenance at the definition or canonical document. Do not rename working APIs or restructure files solely for agent discoverability; make that tradeoff explicit when the task or measured navigation friction justifies it.
