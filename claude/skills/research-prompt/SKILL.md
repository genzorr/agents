---
name: research-prompt
description: Generate comprehensive research prompts for deep research tools
---

# research-prompt

Generate structured research prompts optimized for AI deep research tools (Claude, Gemini Deep Research, ChatGPT o3-pro, etc.).

**Usage:**
```
/research-prompt <topic>
/research-prompt loop closure for multi-agent SLAM
/research-prompt attention mechanisms in transformers
/research-prompt rust async runtime comparison
```

## Instructions

You are a research prompt generator. Your goal is to create comprehensive, well-structured research prompts that enable AI tools to conduct thorough deep research.

### Input Handling

**Required:**
- Topic or question to research

**Optional (gathered via conversation):**
- Project context (what are you building?)
- Constraints (technologies, timeline, team expertise)
- Prior knowledge (what you already know)
- Specific questions (what needs answering?)
- Output format preferences

**If minimal input provided:**
1. Ask 2-3 clarifying questions to understand scope
2. Infer reasonable context from the topic
3. Generate a general-purpose research prompt

### Scope Detection

**Suggest splitting if the research requires MORE than 3 of:**
- Multiple distinct problem domains (e.g., "ML + distributed systems + security")
- Both deep theory AND detailed implementation
- Comparisons across >5 independent methods/frameworks
- Multiple pipeline stages each needing deep dives
- Cross-cutting concerns (performance, security, scalability, etc.)

**When scope is too large:**
```
This topic covers multiple distinct research areas:
1. [Area 1] - [brief description]
2. [Area 2] - [brief description]
3. [Area 3] - [brief description]

I recommend splitting into focused prompts:
- Prompt A: [specific focus]
- Prompt B: [specific focus]

Which would you like to start with?
```

### Output Location

Save generated prompts to the project's research-prompts directory:
```
research/prompts/YYYYMMDD-topic-slug.md
```

If `research/prompts/` doesn't exist, create it.

If working outside a project, output directly to the user.

### Length Constraints

- **Target:** 250-400 lines
- **Maximum:** 500 lines
- **If exceeding:** Propose 2-4 focused sub-prompts

### Generation Process

1. **Understand the topic** - Ask clarifying questions if needed
2. **Check scope** - Suggest splits if too broad
3. **Gather context** - Project background, constraints, prior work
4. **Search for relevant files** - Find project files related to the topic (see below)
5. **Identify research areas** - Break down into focused questions
6. **Find key resources** - Papers, docs, repos to review
7. **Define deliverables** - What output format is needed?
8. **Write the prompt** - Follow the template, section guidelines, and anti-patterns in `reference.md`
9. **Save to file** - Use proper naming convention
10. **Output file list** - List relevant files to pass to research model

### Relevant File Discovery

**Search the project for files related to the research topic.** These files provide context that should be passed to the deep research model along with the prompt.

**Where to search:**
```
.claude/           # Project instructions, specs, rules
research/          # Architecture design, research findings, prompts
docs/              # Documentation
drafts/            # Specs, proposals, design docs
src/               # Source code (key modules only)
conf/              # Configuration schemas
README.md          # Project overview
```

**What to look for:**
- Prior research documents on related topics
- Architecture/design docs for relevant components
- Spec files describing interfaces or protocols
- Key source files implementing related functionality
- Configuration schemas affecting the research area

**Search strategy:**
1. Use Glob to find docs: `**/*.md`, `**/*.rst`
2. Use Grep to search for topic keywords in docs and code
3. Check `research/` for prior research, findings, and architecture design
4. Check `drafts/` for relevant specs
5. Limit to 5-15 most relevant files

**File relevance criteria:**
- Directly discusses the research topic
- Defines interfaces/APIs the research will affect
- Contains prior decisions or constraints
- Documents related components or systems

### Writing the Prompt

When you reach step 8, open `reference.md` (skill-local) and follow it. It
holds the full output template (Context, Problem Statement, Decision To Inform, What
We Already Know, What Needs Research, Research Questions Summary, Key Papers/
Resources, Expected Output, Implementation Priorities, Desired Research Format,
References, Relevant Project Files), the per-section authoring guidelines,
anti-patterns, and a worked example. Load it only when you are actually writing
the prompt.

### Final Output Format

After saving the prompt file, **always output to the user**:

1. **Path** to the saved prompt file.
2. **Numbered list of relevant project files** — grouped by type (Documentation,
   Source Code, Prior Research), each with a brief relevance note; only include
   files that actually exist.
3. **Instruction** to pass the prompt file + these files to the deep research tool.

```
Research prompt saved to: research/prompts/YYYYMMDD-topic.md

Relevant project files to include:
1. path/to/file1.md - [relevance]
2. path/to/file2.py - [relevance]
...

Pass the prompt file + these files to your deep research tool.
```

If no relevant project files are found, say so instead of listing files:
```
Research prompt saved to: research/prompts/YYYYMMDD-topic.md

No additional project files found relevant to this topic.
```

The "Relevant Project Files" section inside the prompt AND this output list must match.
