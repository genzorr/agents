---
name: doc-audit
description: Audit project documentation for consistency issues, gaps, stale references, and unresolved-question mismatches around a topic.
---

# Doc Audit

Use when the user asks to audit documentation around a topic or decision. This skill is audit-only unless the user separately asks for edits.

## Workflow

1. Parse the request into:
   - topic or decision
   - seed paths, if any
   - scope constraints, such as `docs/ only`, `skip research/`, or `implementation docs only`
2. If the topic is genuinely ambiguous, ask one pointed question. Otherwise proceed.
3. Search broadly, then narrow:
   - search markdown and reStructuredText files for the topic and synonyms
   - include common doc roots: `docs/`, `research/`, `drafts/`, `.claude/`, `.codex/`, `.agents/`
   - check `open-questions`, `resolved`, `review`, and ADR files when present
   - follow cross-references such as "see", "defined in", links, and "refer to"
4. Cap detailed reading around 30 files unless the user asked for exhaustive coverage. Prioritize seed paths, high match density, and structurally important docs.
5. Classify findings:
   - inconsistencies: two docs contradict each other
   - gaps: mentioned but not explained, shallow sections, missing component docs
   - stale references: renamed, moved, deleted, or outdated references
   - unresolved-question mismatches: marked open but resolved elsewhere, or the reverse
6. Ask where to save the report, suggesting existing locations such as `research/audits/`, `docs/audits/`, or `audits/`.
7. Write the report after the user confirms the location.

## Report Format

```markdown
# Documentation Audit: <topic>

**Date:** YYYY-MM-DD
**Scope:** <what was searched>
**Files scanned:** N
**Issues found:** N

## Summary

| Category | Count |
|----------|-------|
| Inconsistencies | 0 |
| Gaps | 0 |
| Stale references | 0 |
| Unresolved question mismatches | 0 |

## Inconsistencies

### 1. <title>
- **File:** `path:line`
- **Issue:** ...
- **Conflicts with:** `path:line` — ...
- **Severity:** high | medium | low

## Files Scanned

- `path/to/file.md`
```

Omit empty finding sections, but keep the summary table complete.

## Rules

- Do not edit documentation during the audit.
- Do not include unrelated findings.
- Do not fabricate line numbers; use approximate line numbers from files you actually read.
- If zero issues are found, still write the report with a clean summary and files scanned.
