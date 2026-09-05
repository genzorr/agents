# Documentation-only audit

Use this route when the user asks to audit documentation around a topic or decision and no code diff is in scope. It is read-only, does not require a branch, PR, or implementation diff, and reports findings in chat by default.

Parse the topic or decision, seed paths, and scope constraints such as `docs/ only`, `skip research/`, or `implementation docs only`. If the topic is genuinely ambiguous, ask one pointed question; otherwise proceed with the supplied scope.

Search Markdown and reStructuredText in the relevant documentation roots, including `docs/`, `research/`, `drafts/`, `.claude/`, `.codex/`, and `.agents/` when present. Search topic synonyms, then narrow to seed paths, high-match files, and structurally important documents. Follow material cross-references such as links and “see”, “defined in”, or “refer to” pointers. Bound detailed reading to the topic and requested scope; for exhaustive coverage, inspect every in-scope document and disclose any gaps. Read source code only as needed to verify documentation claims.

Classify only topic-relevant findings as inconsistencies, gaps, stale references, or unresolved-question mismatches. Ground file paths and approximate line numbers in files actually read. When the topic touches `AGENTS.md`, `CLAUDE.md`, platform rules, or skill authoring, read the applicable `docs/context-file-authoring.md` and `docs/skill-authoring-principles.md`; preserve context-file drift checks. When it makes reusable claims or experiment decisions, read `docs/claim-discipline.md` and `docs/experiment-protocol-readout-contract.md` as conditional guidance.

Report findings with severity, evidence, impact, and the relevant cross-reference. State the files scanned and say when no issues were found. Do not ask where to save a report and do not create a findings file unless the user explicitly requests a durable artifact or path.
