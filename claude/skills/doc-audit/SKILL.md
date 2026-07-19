---
name: doc-audit
description: Audit documentation for consistency issues, gaps, and stale references around a topic
---

# doc-audit

Audit project documentation for consistency issues, gaps, stale references, and unresolved question mismatches around a specific topic or decision.

**Usage:**
```
/doc-audit <topic or instructions>
/doc-audit loop closure process placement
/doc-audit transport contracts across IPC docs
/doc-audit "pose graph optimization" — only implementation docs
```

## Instructions

You are a documentation auditor. Your goal is to thoroughly search project documentation for a given topic, find all related references, and produce a structured findings report. You do NOT edit any files — audit only.

### Input Handling

Free-form text from the user invocation. Extract:

- **Topic/decision** — what to audit for (e.g. "loop closure process placement", "transport contracts")
- **Seed paths** — any file paths mentioned (optional; you search proactively regardless)
- **Constraints** — any scoping instructions ("only implementation docs", "skip multi-agent", "research/ only")

If the topic is genuinely ambiguous (could mean two unrelated things), ask ONE clarifying question via AskUserQuestion. Otherwise, proceed.

### Workflow

#### Step 1: Understand Scope

1. Use project structure from CLAUDE.md (already in system prompt context) — don't re-read it
2. Parse the user's instructions for topic, seed paths, and constraints
3. Identify initial search keywords from the topic (synonyms, abbreviations, related terms)

#### Step 2: Search

Cast a wide net, then narrow down. **Run multiple Grep calls in parallel** for different keywords to save time.

1. **Keyword grep** — Search the doc tree for topic keywords across all markdown files:
   - Use Grep with `glob: "**/*.md"` for each keyword — launch these in parallel
   - Include synonyms and abbreviations (e.g. "LC" for "loop closure", "IPC" for "inter-process communication")
2. **Cross-reference following** — For the top matched files (prioritize by match density):
   - Read the file and look for references to other files ("see X", "defined in Y", links, "cf.", "refer to")
   - Follow those references and add them to the scan list
   - **Cap at ~30 files** for detailed reading. If more matches exist, prioritize: seed paths first, then files with highest keyword density, then structural matches
3. **Structural search** — Check these specific locations (use Glob to find them):
   - `research/` — architecture design, findings
   - `docs/` — component documentation
   - `drafts/` — specs and proposals
   - `.claude/specs/` — detailed references
   - Any `open-questions.md`, `resolved/` directories, `review/` files
4. **Build file list** — Deduplicate and record every file that touches the topic

If the user asks for progress updates, report: "Found N files referencing [topic]. Scanning for issues..."

#### Step 3: Analyze

Read each file and check for:

- **Inconsistencies** — File A says X, File B says Y about the same thing. A decision was made but some docs still reflect the old state.
- **Gaps** — Topic is mentioned but not explained; a section header exists but content is missing or shallow; a component is referenced but never documented.
- **Stale references** — Points to a file/section that was renamed, moved, or deleted; references a decision as "open" when it was resolved; cites outdated terminology.
- **Unresolved question mismatches** — Marked as open in open-questions but actually resolved elsewhere (or vice versa); resolved/ directory has an answer but the main doc still says "TBD".

For each finding, note:
- File path and approximate line number
- What the issue is
- What it conflicts with (for inconsistencies) or what's missing (for gaps)
- Severity: **high** (actively misleading), **medium** (confusing/incomplete), **low** (cosmetic/minor)

#### Step 4: Ask Output Location

Use AskUserQuestion to ask where to save the findings file.

First, check which doc directories exist (use Glob or ls). Then provide options that actually exist:
- If `research/` exists: suggest `research/audits/YYYYMMDD-topic-slug.md`
- If `docs/` exists: suggest `docs/audits/YYYYMMDD-topic-slug.md`
- Always include a project-root option: `audits/YYYYMMDD-topic-slug.md`
- Let the user specify a custom path via "Other"

#### Step 5: Write Findings

Write the findings file using the format below. Include ALL findings — don't omit low-severity items.

If zero issues were found, still write the report — with a clean summary (all zeros) and the full "Files Scanned" section. This confirms the audit was thorough and the topic is consistent.

### Findings File Format

```markdown
# Documentation Audit: [Topic]

**Date:** YYYY-MM-DD
**Scope:** [what was searched and any constraints applied]
**Files scanned:** N
**Issues found:** N

## Summary

| Category | Count |
|----------|-------|
| Inconsistencies | X |
| Gaps | Y |
| Stale references | Z |
| Unresolved question mismatches | W |

## Inconsistencies

### 1. [Brief title]
- **File:** `path/to/file.md:NN`
- **Issue:** [description of what this file says]
- **Conflicts with:** `path/to/other.md:MM` — [what the other file says]
- **Severity:** high/medium/low

## Gaps

### 1. [Brief title]
- **File:** `path/to/file.md:NN`
- **Issue:** [what's missing or insufficiently documented]
- **Severity:** high/medium/low

## Stale References

### 1. [Brief title]
- **File:** `path/to/file.md:NN`
- **Issue:** [what's stale — renamed, moved, deleted, or outdated]
- **Severity:** high/medium/low

## Unresolved Question Mismatches

### 1. [Brief title]
- **File:** `path/to/file.md:NN`
- **Issue:** [marked open but resolved elsewhere / marked resolved but still open]
- **Severity:** high/medium/low

## Files Scanned

### [Directory 1]
- `path/to/file1.md`
- `path/to/file2.md`

### [Directory 2]
- `path/to/file3.md`
```

Omit any category section that has zero findings (e.g. if no stale references, skip that section entirely). Keep the summary table complete regardless.

### Anti-Patterns

- **DON'T edit any files** — this is an audit, not a fix
- **DON'T propose solutions** — that's for the resolution phase/agent
- **DON'T skip cross-reference following** — thoroughness is the value
- **DON'T include findings unrelated to the audit topic** — stay focused
- **DON'T deep-dive into source code** — but DO read source files briefly when docs make claims about code behavior and you need to verify accuracy
- **DON'T fabricate line numbers** — use approximate line numbers from what you actually read

### Tips

- When grepping, try multiple keyword variants (singular/plural, abbreviations, full terms)
- Open-questions files and resolved/ directories are gold mines for mismatches
- Review/ files often contain decisions that haven't propagated yet
- Cross-references ("see X", "defined in Y") are where inconsistencies hide
- The most valuable findings are high-severity inconsistencies where two docs actively contradict each other
