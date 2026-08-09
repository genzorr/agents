---
name: integrate-research
description: Process deep research outputs and integrate findings into project documentation
---

# integrate-research

Process deep research outputs (PDFs, markdown) and integrate findings into project documentation. Generates a summary of relevant findings and optionally updates project docs.

**Usage:**
```
/integrate-research <path-to-research-output>
/integrate-research output.pdf
/integrate-research output.pdf --prompt research/prompts/topic.md
/integrate-research output.pdf "focus on method X, skip Y for now"
/integrate-research output.pdf --prompt research/prompts/topic.md "additional context here"
/integrate-research results/*.pdf "summarize all, prioritize implementation aspects"
```

## Instructions

You are a research integration assistant. Your goal is to process deep research outputs and help integrate findings into project documentation.

### Argument Parsing

**Required:**
- `<path>` - Path to research output file(s) (PDF or markdown)

**Optional:**
- `--prompt <path>` - Path to the original research prompt that generated this output
- Free text (not starting with `--`) - User's additional context, thoughts, or guidance

**Examples:**
```
# Just the research output
/integrate-research research-results/loop-closure.pdf

# With original prompt for context
/integrate-research research-results/loop-closure.pdf --prompt research/prompts/20260124-loop-closure.md

# With user guidance
/integrate-research research-results/loop-closure.pdf "focus on KISS-Matcher, we decided to skip VPR"

# Full invocation
/integrate-research research-results/loop-closure.pdf --prompt research/prompts/20260124-loop-closure.md "prioritize coarse alignment methods, fine alignment is already decided"
```

### Workflow

```
1. Parse arguments
   ├── Extract file path(s)
   ├── Extract --prompt path (if provided)
   └── Extract user context/thoughts (remaining text)

2. Read inputs
   ├── Research output(s) - Read PDF/markdown files
   ├── Original prompt (if --prompt provided)
   └── Project context - .claude/CLAUDE.md, relevant docs

3. Ask clarifying questions (AskUserQuestion)
   ├── "Which research areas should I focus on?"
   ├── "What's the integration goal?" [Summary only / Update docs]
   └── "Any specific doc files to update?"

4. Generate findings summary
   └── Save to research/findings/YYYYMMDD-topic-findings.md

5. If updating docs:
   ├── Identify doc files to update
   ├── Show list, ask confirmation
   ├── For each file: propose changes (summary), ask approval
   └── Apply approved changes

6. Output summary of actions taken
```

### Step 1: Parse Arguments

Parse the invocation to extract:
- **File paths**: Anything ending in `.pdf`, `.md`, or a directory path
- **Prompt flag**: `--prompt <path>` extracts the path after `--prompt`
- **User context**: Any remaining text that isn't a file path or flag

### Step 2: Read Inputs

**Research outputs:**
- Use Read tool for PDFs and markdown
- If multiple files, read all and synthesize

**Original prompt (if provided):**
- Provides context on what questions the research was answering
- Helps identify which findings are most relevant

**Project context:**
- Read `.claude/CLAUDE.md` for project overview
- Check `.claude/specs/`, `docs/`, `drafts/` for relevant docs
- Understand what documentation exists that might need updating

When findings could become reusable guidance, a default, or a project-level recommendation, open `docs/claim-discipline.md` before synthesis. Keep source observations, target-project evidence, alternatives, counterevidence, supported conditions, and explicit non-claims visible; select the weakest non-vacuous conclusion supported by that complete record, then determine any recommendation or documentation decision separately.

### Step 3: Ask Clarifying Questions

Use AskUserQuestion to gather user input. Ask 1-3 questions based on what's unclear:

- **Focus areas** (if the research covers multiple topics) — which areas to prioritize.
- **Integration goal** — summary only (recommended) vs summary + update docs.
- **Files to update** (only if "update docs" selected) — which documentation to update.

When you reach this step, open `reference.md` (skill-local) and use its AskUserQuestion option templates for each question.

### Step 4: Generate Findings Summary

Always create a findings document at `research/findings/YYYYMMDD-topic-findings.md` (even when
no docs will be updated), following the **Findings document structure** in `reference.md`.

### Step 5: Update Documentation (if requested)

**Scope: Documentation only**
- `.claude/` - Specs, architecture, rules (NOT research/)
- `research/` - Architecture design, research findings
- `docs/` - Project documentation
- `drafts/` - Design specs, proposals

**DO NOT modify:**
- Source code (`src/`, `tests/`)
- Configuration files (`conf/`)
- Build files

**Update process:**

1. **Identify relevant docs:**
   - Search for docs related to research topic
   - Use Grep to find files mentioning key terms
   - Check files referenced in the research prompt

2. **Show proposed updates:** list each file and the specific changes you intend, then ask
   confirmation before applying (see `reference.md` for an example).

3. **Ask for approval** (AskUserQuestion): offer "all updates" / "review each" / "skip updates"
   (see `reference.md` for the option template).

4. **Apply approved changes:**
   - Use Edit tool for modifications
   - Use Write tool only if creating new doc sections
   - After each file, briefly note what was changed

### Step 6: Output Summary

After completion, output a summary containing:

- **Findings saved to:** the findings file path.
- **Documentation updated:** the list of changed docs with what changed (omit if summary-only).
- **Key findings:** a short numbered list.

See `reference.md` for example output blocks (with and without doc updates).

### Guidelines

**When generating findings:**
- Focus on findings relevant to THIS project
- Filter out generic information not applicable here
- Connect findings to specific project components/decisions
- Be concrete about implications

**When updating docs:**
- Preserve existing structure and style
- Add new information, don't rewrite entire sections
- Use the same terminology as existing docs
- Link to findings document for details

**User context takes priority:**
- If user says "focus on X", prioritize X
- If user says "skip Y", don't include Y in summary
- User guidance overrides prompt-based priorities

For anti-patterns and notes, see `reference.md`.
