# integrate-research — output templates & examples

Open this when you reach the step that needs it: the clarifying-question option templates
(Step 3), the findings document structure (Step 4), the doc-update proposal/approval example
(Step 5), or the final summary examples (Step 6). The skill body (`SKILL.md`) holds the argument
parsing, workflow, read/scope steps, mutation guardrails, and output contract.

## Clarifying-question templates (Step 3)

Use AskUserQuestion. Ask 1-3 questions based on what's unclear.

**Question 1: Focus areas** (if research covers multiple topics)
```
header: "Focus"
question: "Which research areas should I prioritize?"
options:
  - label: "All findings"
    description: "Summarize everything relevant to the project"
  - label: "[Area 1 from research]"
    description: "[Brief description]"
  - label: "[Area 2 from research]"
    description: "[Brief description]"
multiSelect: true
```

**Question 2: Integration goal**
```
header: "Goal"
question: "What should I do with these findings?"
options:
  - label: "Summary only (Recommended)"
    description: "Generate findings doc, don't modify other files"
  - label: "Summary + update docs"
    description: "Generate findings and update relevant documentation"
multiSelect: false
```

**Question 3: Files to update** (only if "update docs" selected)
```
header: "Files"
question: "Which documentation should I update?"
options:
  - label: "[file1.md]"
    description: "[Why this file is relevant]"
  - label: "[file2.md]"
    description: "[Why this file is relevant]"
  - label: "All relevant docs"
    description: "Update all docs that relate to this research"
multiSelect: true
```

## Findings document structure (Step 4)

Create a findings document at `research/findings/YYYYMMDD-topic-findings.md`:

```markdown
# Research Findings: [Topic]

**Generated:** YYYY-MM-DD
**Source:** [path to research output]
**Original prompt:** [path to prompt, if provided]
**User guidance:** [user's additional context, if provided]

---

## Executive Summary

[2-5 bullet points of key findings relevant to this project]

---

## Detailed Findings

### [Finding Area 1]

**Key insight:** [One sentence]

**Details:**
- [Relevant point 1]
- [Relevant point 2]

**Implications for project:**
- [How this affects our implementation]

### [Finding Area 2]

[Same structure...]

---

## Recommendations

### Immediate Actions
1. [Action 1]
2. [Action 2]

### Future Considerations
1. [Consideration 1]
2. [Consideration 2]

---

## Updated Documentation

[If docs were updated, list them here]
- `path/to/doc1.md` - [What was changed]
- `path/to/doc2.md` - [What was changed]

[If no docs updated]
No documentation was updated. Findings are captured in this summary.

---

## References

- Source research: [path]
- Original prompt: [path, if provided]
- Related project docs: [list relevant docs read for context]
```

## Doc-update proposal & approval (Step 5)

When showing proposed updates:
```
I found these docs that may need updates:

1. .claude/specs/architecture.md
   - Add section on [new component]
   - Update [existing section] with [new approach]

2. docs/loop-closure.md
   - Update method comparison table
   - Add KISS-Matcher to recommended approaches

Should I proceed with these updates?
```

Approval question (AskUserQuestion):
```
header: "Updates"
question: "Which updates should I apply?"
options:
  - label: "All updates"
    description: "Apply all proposed changes"
  - label: "Review each"
    description: "Ask me about each file individually"
  - label: "Skip updates"
    description: "Keep findings summary only, don't modify docs"
```

## Output summary examples (Step 6)

With doc updates:
```
Research integration complete.

**Findings saved to:** research/findings/20260124-loop-closure-findings.md

**Documentation updated:**
- research/decentralized-architecture/inter-agent-lc.md - Added KISS-Matcher section
- docs/loop-closure.md - Updated method comparison

**Key findings:**
1. KISS-Matcher recommended for coarse alignment (faster than FPFH+RANSAC)
2. Detection-free approach viable for intra-agent closures
3. [...]

Review the findings document for full details.
```

Summary only (no doc updates):
```
Research integration complete.

**Findings saved to:** research/findings/20260124-loop-closure-findings.md

**Key findings:**
1. [Finding 1]
2. [Finding 2]
3. [...]

No documentation was modified. Review findings for recommendations.
```

## Anti-Patterns

**DON'T:**
- Summarize the entire research output verbatim
- Include findings not relevant to the project
- Modify source code (only docs)
- Skip asking clarifying questions
- Make changes without showing what will change first

**DO:**
- Filter for project relevance
- Ask before modifying files
- Show proposed changes before applying
- Respect user's guidance and priorities
- Create clear, actionable findings

## Notes

- This skill processes outputs from deep research tools (Gemini, Claude, ChatGPT)
- The `--prompt` flag helps connect findings to original research questions
- User's free-text guidance is important for prioritization
- Always generate the findings summary, even if no docs are updated
- Findings docs are persistent project knowledge, not ephemeral
