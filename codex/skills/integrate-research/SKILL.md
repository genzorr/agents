---
name: integrate-research
description: Process research outputs and integrate relevant findings into project documentation.
---

# Integrate Research

Use when the user provides research output files and wants a findings summary or documentation updates.

## Input

Accept:

- one or more research output paths: PDF, markdown, text, or directories
- optional `--prompt <path>` for the original research prompt
- optional free-text guidance

## Workflow

1. Parse paths, prompt path, and user guidance.
2. Read the research outputs and original prompt if provided.
3. Read project context likely to receive the findings: `AGENTS.md`, `README.md`, `docs/`, `research/`, `drafts/`, ADRs, and relevant specs.
4. When findings could become reusable guidance, a default, or a project-level recommendation, open `docs/claim-discipline.md` before synthesis. Keep source observations, target-project evidence, alternatives, counterevidence, supported conditions, and explicit non-claims visible; select the weakest non-vacuous conclusion supported by that complete record, then determine any recommendation or documentation decision separately.
5. Ask only what is needed:
   - focus areas if the research covers multiple topics
   - summary-only versus updating docs
   - target files if documentation updates are requested
6. Write a findings summary to `research/findings/YYYYMMDD-topic-findings.md`.
7. If the user approved doc updates:
   - list target files and proposed changes
   - apply only approved documentation edits
   - keep source research files unchanged
8. Report the findings file and any updated docs.

## Findings Format

```markdown
# Research Findings: <topic>

**Generated:** YYYY-MM-DD
**Source:** <path>
**Original prompt:** <path or none>
**User guidance:** <guidance or none>

## Executive Summary

- ...

## Detailed Findings

### <area>

**Key insight:** ...

**Implications for project:**
- ...

## Recommendations

### Immediate Actions
1. ...

### Future Considerations
1. ...

## Updated Documentation

- `path` — <what changed>

## References

- ...
```

## Rules

- Keep project-specific implications separate from raw research claims.
- Do not overwrite existing research findings; create a new findings file.
- Documentation updates must be scoped to files the user approved or clearly requested.
- If sources conflict, record the conflict instead of hiding it.
