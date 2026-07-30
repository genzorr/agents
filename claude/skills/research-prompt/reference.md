# research-prompt — output template & authoring reference

Open this when generating a prompt (step 8 of the skill). It holds the full
prompt template, per-section authoring guidelines, anti-patterns, and a worked
example. The skill body (`SKILL.md`) holds the trigger, input handling, scope
detection, file discovery, and output contract.

## Template Structure

Generate prompts with these sections (adapt as needed):

```markdown
# Research Prompt: [Topic Title]

## Context

[Project background - what are you building/researching?]
[Current state - what exists, what's working]
[Goals - what you're trying to achieve]
[Constraints - technology choices, timeline, team skills]

---

## Problem Statement

[Core challenge in 1-2 sentences]

**Key sub-challenges:**
1. [Challenge 1]
2. [Challenge 2]
3. [Challenge 3]

---

## Decision To Inform

[Concrete decision, action, or downstream use this research will inform.]

---

## What We Already Know

### From Prior Research/Experience
- [Finding 1] - [source/reference]
- [Finding 2] - [source/reference]

### Constraints/Decisions Made
- [Constraint 1] - [rationale]
- [Constraint 2] - [rationale]

See: [references to prior docs if any]

---

## What Needs Research

### 1. [Research Area 1]

[Brief description of the area]

**Options:**

#### A. [Option/Approach A]
- [Key characteristics]
- [Pros/cons if known]

#### B. [Option/Approach B]
- [Key characteristics]
- [Pros/cons if known]

**Questions:**
- [Specific question 1]
- [Specific question 2]

### 2. [Research Area 2]

[Repeat structure...]

---

## Research Questions Summary

### [Category 1]
1. [Question 1]
2. [Question 2]

### [Category 2]
3. [Question 3]
4. [Question 4]

---

## Key Papers/Resources to Review

### [Category 1]
- **[Paper/Resource Name]** ([Venue Year]) - [Brief note] | [Link if available]

### [Category 2]
- **[Paper/Resource Name]** ([Venue Year]) - [Brief note] | [Link if available]

---

## Expected Research Output

### 1. [Deliverable 1]

**Compare:** [What to compare]

**For each scenario:** [How to structure comparison]

### 2. [Deliverable 2]

[Structure...]

---

## Implementation Priorities

**Immediate (for [timeframe/milestone]):**
1. [Priority 1]
2. [Priority 2]

**Research (if pursuing [goal]):**
1. [Priority 1]
2. [Priority 2]

**Future:**
1. [Priority 1]
2. [Priority 2]

---

## Desired Research Format

Please provide:

1. **Summary table:** [What comparisons in table form]
2. **Recommendations:** [What decisions need recommendations]
3. **Trade-offs:** [What trade-offs to analyze]
4. **Implementation roadmap:** [If needed]
5. **Open problems:** [What to flag as needing more research]

---

## References

### Prior Documents
- [Reference to prior research/docs in project]

### Architecture/Design Docs
- [Reference to relevant design docs]

---

## Relevant Project Files

The following project files provide additional context for this research. Pass these to the research model along with this prompt.

### Core Documentation
- `path/to/file.md` - [Brief description of relevance]

### Source Code
- `src/path/to/module.py` - [Brief description of relevance]

### Prior Research
- `research/findings/related-topic.md` - [Brief description of relevance]
- `research/decentralized-architecture/component.md` - [Brief description of relevance]
```

## Section Guidelines

**Context:**
- Keep concise (5-15 lines)
- Focus on what's relevant to the research
- Include technology stack if relevant

**Problem Statement:**
- One clear sentence for core challenge
- 3-5 sub-challenges maximum
- Avoid vague statements

**Decision To Inform:**
- Name the concrete decision, action, or downstream use
- Explain which findings would change that decision

**What We Already Know:**
- Include sources/references
- Distinguish facts from assumptions
- Link to prior research documents

**What Needs Research:**
- 2-5 major research areas
- Each area has options and specific questions
- Questions should be answerable, not rhetorical

**Research Questions Summary:**
- Numbered for easy reference (Q1, Q2...)
- Grouped by category
- Specific and actionable

**Key Papers/Resources:**
- Include venue and year
- Add GitHub links when available
- Brief note on relevance

**Expected Output:**
- Be specific about deliverables
- Include format preferences (tables, lists, etc.)
- Define what "done" looks like
- Prefer primary evidence such as official documentation, source code, papers, standards, filings, and changelogs; use secondary commentary only as supporting context
- Separate verified facts, supported inferences, contradictions, and unresolved uncertainty
- End with one gap review for unanswered questions, contradictions, and consequential single-source claims; use an additional search where it could materially close a gap, otherwise leave it explicitly unresolved

**Implementation Priorities:**
- Three tiers: Immediate, Research, Future
- Realistic scope per tier

**Relevant Project Files:**
- List 5-15 files maximum (most relevant only)
- Group by type: Documentation, Source Code, Prior Research
- Include brief description of why each file is relevant
- Use relative paths from project root
- Only include files that actually exist in the project

## Anti-Patterns

**DON'T:**
- Write vague questions ("How does X work?")
- Include unnecessary background padding
- Ask questions you can answer yourself with a quick search
- Request "everything about X"
- Mix research questions with implementation tasks

**DO:**
- Ask specific, comparative questions
- Provide context for why each question matters
- Include constraints that affect answers
- Reference concrete papers/tools to compare
- Define clear success criteria

## Example Invocation

**User:** `/research-prompt attention mechanisms for long sequences`

**Response:** (After brief clarification)

Creates `research/prompts/20260124-long-sequence-attention.md` with:
- Context about the project (if provided)
- Problem statement: handling sequences > context window
- Research areas: sparse attention, memory mechanisms, efficient transformers
- Specific questions comparing Mamba, Flash Attention, Ring Attention, etc.
- Papers to review with venues and links
- Expected output format (comparison table, recommendations)
- List of relevant project files

**Then outputs to user:**
```
Research prompt saved to: research/prompts/20260124-long-sequence-attention.md

Relevant project files to include:
1. docs/architecture.md - System architecture overview
2. src/models/attention.py - Current attention implementation
3. research/findings/transformer-optimization.md - Prior research on transformers
4. conf/model_config.py - Model configuration schema

Pass the prompt file + these files to your deep research tool.
```

## Notes

- Prompts are meant for AI deep research tools, not for direct implementation
- Include enough context that the research tool can work autonomously
- The more specific the questions, the more useful the research output
- Always include "Desired Research Format" to get actionable output
- The "Relevant Project Files" section in the prompt AND the output list should match
