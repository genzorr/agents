---
name: ask-oracle
description: Use the Oracle CLI to prepare a neutral source bundle for GPT-5.6 or another GPT Pro model from repository files, documents, papers, logs, research notes, or a curated context pack. Use when the user wants an Oracle-ready bundle, manual ChatGPT Web handoff, API/browser Oracle consult, or context pack instead of manually attaching files.
---

# Ask Oracle

## Goal

Produce an Oracle-ready bundle with neutral task context and source material, not the answer to the underlying task.

Use Oracle to bundle relevant files whenever repository or document context spans more than one obvious file. Manual render mode is the default handoff.

The user-facing output is only the bundle location. Do not print the generated prompt, the Oracle command, or command output unless the user explicitly asks for those details.

## Workflow

1. Identify the target task type: coding, research, debugging, architecture/review, document analysis, log analysis, or mixed.
2. Gather only relevant context for Oracle:
   - Prefer a curated context pack over a raw full-repo dump.
   - Include current git diff, relevant source files, tests, logs, configs, docs, papers, metrics, and prior research notes when they materially affect the answer.
   - Exclude generated files, build outputs, datasets, binaries, old experiments, dependency directories, and unrelated modules.
3. Write a concise, information-dense prompt for the bundle that names the task, context, success criteria, constraints, evidence rules, output mode, and artifact format.
4. Preserve exact names of files, functions, parameters, datasets, papers, metrics, configs, commands, and error strings.
5. Separate known facts from assumptions and open questions.
6. Choose the output artifact format using the artifact policy below.
7. Render the bundle to a file. A `/tmp/...` path is fine unless the user requested a specific location.
8. Return only the bundle path unless the user explicitly asks for explanation, file selection rationale, the generated prompt, the command, or the rendered context pack.

## Oracle Handoff

Use Oracle by default when a context bundle would be better than pasting individual files manually. The user has Oracle installed, so call `oracle` directly.

Before first Oracle use in a session, run:

```bash
oracle --help
```

Manual mode:
- Generate a rendered Markdown bundle with `oracle --render`.
- Use `--copy` when the user wants clipboard handoff.
- Redirect stdout to a Markdown file by default.
- Tell the user only where the bundle was written.

Examples:

```bash
oracle --render --render-plain \
  -p "$(cat /path/to/prompt.md)" \
  --file "src/**/*.py" \
  --file "tests/**/*.py" \
  --file "docs/**/*.md" \
  > /tmp/oracle-context.md
```

```bash
oracle --render --render-plain \
  -p "$(cat /path/to/prompt.md)" \
  --file "src/**/*.py" \
  --file "tests/**/*.py" \
  > /tmp/oracle-context.md
```

Automatic mode:
- Use API mode only when the user explicitly asks and the needed API keys are available.
- Use browser automation only when the user explicitly asks for it.
- Do not imply browser automation is required for this skill.

When Oracle is not installed, use `npx -y @steipete/oracle`. Run `npx -y @steipete/oracle --help` before relying on advanced flags in a new environment. If neither `oracle` nor `npx` can create the bundle, report that no bundle was created and why; do not show a fallback command unless the user asks for one.

Use repeated `--file` flags and exclusion patterns instead of asking the user to manually attach files from different folders:

```bash
oracle --render --render-plain \
  -p "$(cat /path/to/prompt.md)" \
  --file "harness-core/src/**/*.py" \
  --file "harness-cli/src/**/*.py" \
  --file "harness-ui/src/**/*.py" \
  --file "tests/**/*.py" \
  --file "docs/**/*.md" \
  --file "!**/.venv/**" \
  --file "!**/__pycache__/**" \
  --file "!**/dist/**" \
  --file "!**/build/**" \
  > /tmp/oracle-context.md
```

## Artifact Policy

Choose the requested output format based on the task:

- Markdown file: default for research notes, implementation plans, reviews, specs, hypotheses, and summaries.
- PDF: use when the result should be shared, submitted, archived, or read as a polished report.
- Both Markdown and PDF: use for important research/project outputs where Markdown is editable and PDF is shareable.
- Diagrams/images: request them when architecture, pipelines, algorithms, experiment flow, causal mechanisms, or tradeoffs are central.
- Tables: request them for comparisons, experiment matrices, literature evidence, decisions, risks, and ablations.

If file generation is available, instruct GPT Pro to create downloadable `.md` and/or `.pdf` files. If file generation is not available, instruct it to output the complete Markdown content directly.

## Context Rules

When a context pack is attached:
- Treat verbatim source files, logs, benchmark outputs, code, configs, papers, and quoted excerpts as primary evidence.
- Treat the prompt, source manifest, generated summaries, file-selection rationale, and prior AI-generated reports as secondary framing unless directly backed by primary evidence.
- Use exact excerpts for critical code, configs, logs, metrics, and paper claims.
- Use summaries only for background or stable architecture; do not let summaries override primary source artifacts.
- Do not invent missing implementation details.
- Do not invent operational constraints, urgency, runtime, or resource assumptions such as "overnight", "immediate", "cheap", or "low-risk" unless the primary evidence states them.
- If a claim appears only in bundle framing, label it as a framing inference, not as a project fact.
- Mention stale, contradictory, or low-confidence context explicitly.

When creating a context pack:
- Include a source manifest explaining why each file or section is included.
- Include exact snippets for the most important code/config/log/paper evidence.
- Include summaries for supporting background.
- Label Codex-written summaries, file-selection rationale, and any prior AI-generated reports as secondary framing.
- Include the current git diff when code changes are in scope.
- Include relevant verification commands and recent outputs when validation matters.

## Neutrality Rules

- Provide information and evidence for Oracle to reason from; do not steer it toward a suspected cause, preferred architecture, or specific solution direction unless the user explicitly asked for that direction to be evaluated.
- Do not include an "analysis focus" section that highlights one possible mechanism as the likely answer.
- If the user supplied hypotheses or suspected fixes, label them as user-provided hypotheses and ask Oracle to evaluate them against the evidence, not to assume they are correct.
- Prefer neutral wording such as "determine the likely causes and options from the attached context" over wording such as "focus on X as the solution."
- Include open questions and uncertainty without turning them into recommendations.
- Do not ask for "concrete recommendations", "next actions", or an implementation plan unless the user asked for decision support or execution planning. For audits and context handoffs, ask for unsupported claims, evidence gaps, competing interpretations, and questions to resolve.
- Every recommendation in the requested output must cite primary evidence or be labeled as an inference with confidence and missing evidence.

## Prompt Template

Use this structure and tailor the lists to the task:

```markdown
# Task

[Precise task for GPT-5.6 or another GPT Pro model.]

# Context

Use the attached context pack with this evidence hierarchy: primary evidence is verbatim source files, logs, benchmark outputs, code, configs, papers, and quoted excerpts; secondary framing is the prompt, source manifest, generated summaries, file-selection rationale, and prior AI-generated reports.

Important context:
- [File/section]: [why it matters]
- [File/section]: [why it matters]
- [File/section]: [why it matters]

# Goal

[Concrete desired result.]

# Success Criteria

A good answer must:
- [criterion 1]
- [criterion 2]
- [criterion 3]

# Constraints

- Output in English only.
- Do not invent facts not supported by the context.
- Do not invent operational constraints, urgency, runtime, or resource assumptions such as "overnight", "immediate", "cheap", or "low-risk" unless primary evidence states them.
- Preserve exact technical names.
- Separate primary-evidence facts, secondary-framing claims, assumptions, inferences, and recommendations.
- State uncertainty explicitly.
- Prefer implementation-oriented guidance over generic explanation.
- Evaluate the attached context neutrally. Do not assume any suspected cause, mechanism, or solution is correct unless the evidence supports it.

# Evidence Rules

- Cite exact file names, sections, line ranges, or source names where possible.
- For research claims, identify supporting papers/sources.
- For code claims, refer to exact files/functions/classes/configs.
- If evidence is missing, say so. Do not fill missing operational constraints or project facts with plausible guesses.
- Every recommendation must cite primary evidence or be labeled as an inference with confidence and missing evidence.

# Required Output

For neutral audits or context-review tasks, return:
1. Unsupported or weakly supported claims
2. Evidence gaps and contradictions
3. Primary evidence versus secondary framing
4. Competing interpretations
5. Questions or checks needed before deciding

For decision-support tasks where the user explicitly asked for recommendations, return:
1. Executive summary
2. Main analysis
3. Recommendations with evidence citations or explicit inference labels
4. Risks / failure modes
5. Validation plan
6. Next actions

# Artifact Output

Create a downloadable Markdown file.
Also create a PDF if file generation is available.
Include diagrams where they clarify architecture, workflow, causal mechanism, or experiment design.
If downloadable files are not available, output the complete Markdown document directly.
```

## Specialization

For coding tasks, include:
- target files
- relevant interfaces
- current behavior
- desired behavior
- tests/validation commands
- acceptance criteria
- do-not-change constraints

For research tasks, include:
- research question
- literature evidence
- novelty claim
- falsification tests
- baseline comparisons
- reviewer objections
- minimum next experiment

For debugging tasks, include:
- exact error/log
- reproduction steps
- environment
- recent changes
- files implicated by evidence or named by the user
- what has already been tried
- expected vs actual behavior

## Final Output Rule

Return only the rendered bundle location unless the user explicitly asks for explanation, file selection rationale, the generated prompt, the Oracle command, or the rendered context pack.
