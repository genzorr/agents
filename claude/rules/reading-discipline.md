# Reading Discipline

**Never read a file whole if you only need part of it. Never search for content when file paths suffice.**

## File reads

- **< 150 lines** → read whole.
- **≥ 150 lines** → grep for the symbol first, then `Read(offset, limit)` on the located region.
- **Already read this session** → use context. Do not re-read. Use `offset+limit` for skipped sections.
- **Exceptions** (read whole regardless of size): config files, schemas, ADRs/threat models where the task requires reasoning across the full content.

## Search pipeline

Ripgrep context mode repeats the full absolute path on every line — match lines *and* context lines. One broad content search can cost 5–10× more tokens than necessary. Always follow this pipeline:

```
1. Glob(pattern="**/*.py")                             → files by name/path pattern
   OR
   Grep(output_mode="files_with_matches")              → files by content
2. Grep(output_mode="content", head_limit=30,
        path=<single file>)                            → which lines
3. Read(offset=N, limit=40)                            → the code
```

Rules:
- Use **Glob** when you know the file name or path pattern. Use **Grep `files_with_matches`** when you know the content. Never skip to step 2 from a directory.
- `head_limit` default is 250 — always override to 20–50 for content mode.
- No `-B`/`-A`/`-C` context flags in step 2. If you need surrounding code, use `Read` with `offset+limit`.

## Task inputs

When a task lists large source files, do not read them wholesale. Read the acceptance criteria first, grep for relevant symbols, then read only located sections.
