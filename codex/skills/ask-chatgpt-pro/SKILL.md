---
name: ask-chatgpt-pro
description: Prepare a neutral, mid-sized manual ChatGPT Pro consult document that uses ChatGPT's GitHub connector for an independent codebase review. Use when Pro should inspect one or more GitHub repos, commits, branches, PRs, or named files directly; especially when local changes must be committed and pushed before Pro can see them.
---

# Ask ChatGPT Pro

## Goal

Produce a neutral Markdown consult document for ChatGPT Pro, not an answer to the underlying task.

Use GitHub as the primary source. The document must be concise enough to paste into ChatGPT Pro and must direct Pro to inspect the named repositories and pinned commits itself. Do not drive ChatGPT Web or create an Oracle context bundle.

## When To Use This Instead Of Ask Oracle

Use this skill when:
- relevant material lives in GitHub repos ChatGPT Pro can access;
- the question benefits from Pro inspecting repo structure, history, branches, PRs, or files directly;
- local changes must be committed and pushed before Pro can evaluate them.

Use `ask-oracle` instead when:
- the context is not in GitHub or should not be pushed;
- the key evidence is local logs, generated output, private documents, papers, or datasets;
- the user needs a self-contained bundle independent of connector behavior.

## Workflow

1. State a neutral task, desired output, scope, non-goals, and success criteria. Do not include a suspected cause, preferred solution, reviewer conclusion, or implementation plan unless the user explicitly asks Pro to evaluate it.
2. Identify each GitHub repo and its stable ref. Record `owner/repo`, an exact commit SHA, its branch or PR URL, target paths, symbols, and search strings. For a change review, record both the base and head commits.
3. Check GitHub visibility. Use `gh repo view owner/repo` or `git remote -v` when needed, then run `git status --short` and inspect the relevant diff. If local changes are evidence, commit and push them before preparing the document; respect repo stop/ask gates.
4. Select only the sources needed to answer the task. Include a minimal source manifest and omit generated files, dependency directories, unrelated modules, PR descriptions, review threads, issue commentary, and prior AI reports unless the user explicitly asks for comparison. Retain a durable experiment/result record only when its directly recorded measurements, commands, or artifacts are needed and available at the pinned ref.
5. Verify every named manifest path at its pinned commit before writing the document. Use `git cat-file -e <sha>:<path>` when the commit is available locally, or an equivalent GitHub API/connector lookup. Remove an unresolved path, or state its access limitation and use a search string instead.
6. Include validation only when it materially changes the review. Record concise command results as secondary framing, not proof that overrides GitHub source.
7. Write `/tmp/chatgpt-pro-<topic>.md` unless the user requests a repo artifact. Use the template below.
8. Return the document path, refs to inspect, and any commit/push status affecting Pro's visibility. Do not paste the document unless asked.

## Neutrality And Evidence Rules

- Treat GitHub source at the named commits as primary evidence. A durable experiment/result record is primary only for its directly recorded measurements, commands, artifacts, and provenance; its agent-written interpretations remain secondary framing. Treat the consult document, source selection rationale, validation summaries, and other agent-written text as secondary framing.
- Ask Pro to inspect primary evidence before relying on secondary framing. The document's Current State must contain only ref and visibility facts, not conclusions about the code.
- Do not include information that anchors an independent reviewer: suspected causes, proposed fixes, desired findings, reviewer opinions, PR descriptions, review threads, issue comments, or prior AI analyses.
- If the user explicitly provides a hypothesis, label it `user-provided hypothesis` and ask Pro to test it against the GitHub evidence and competing explanations.
- Preserve exact repositories, commits, PRs, branches, files, symbols, commands, config keys, error strings, and issue numbers.
- Separate primary-evidence facts, secondary framing, assumptions, inferences, and recommendations. State uncertainty, contradictions, stale context, missing access, and missing evidence explicitly.
- Do not invent implementation details or operational constraints such as urgency, budget, runtime, risk, or priority.
- For an audit or independent review, do not request recommendations, next actions, or an implementation plan unless the user explicitly requests decision support or execution planning.
- Require repository, commit/ref, file-path, and line-range citations where possible. Each recommendation must cite primary evidence or be labeled as an inference with confidence and missing evidence.
- Keep the consult read-only: instruct Pro not to create or modify issues, PRs, branches, commits, or repository files.

## Artifact Policy

Ask ChatGPT Pro for one mid-sized report: target 800–1,200 words excluding citations. Use a Markdown file by default and also request a PDF when file generation is available. If files cannot be generated, require the complete Markdown report in the response.

Use short sections and citations instead of long excerpts, appendices, or a duplicated source manifest. Request a table or diagram only when it materially clarifies comparisons, architecture, workflow, causal mechanism, or tradeoffs.

## Consult Document Template

```markdown
# Task

[Precise neutral task for ChatGPT Pro.]

# GitHub Context

Use your GitHub connector/plugin. Inspect the repositories and pinned refs below directly. Treat GitHub source at these refs as primary evidence; treat this document as secondary framing. Do not inspect PR descriptions, review threads, issue comments, or prior AI reports unless the task explicitly names them as evidence.

Every named path in this source manifest was mechanically verified at its pinned ref before this document was prepared.

## Source Manifest

- `owner/repo`
  - Pinned ref: `full-commit-sha`
  - Branch / PR: `branch-name` or `PR URL`
  - Start with: `path/to/file`, `path/to/directory`
  - Search for: `symbol_or_error_string`
  - Relevance: [why this source is needed]

# Goal

[Concrete result to provide.]

# Success Criteria

A good answer must:
- [criterion 1]
- [criterion 2]
- [criterion 3]

# Current State

- GitHub-visible commit(s): `sha`
- Relevant branch / PR: `name or URL`
- For a change review: base `sha`, head `sha`
- Local-evidence visibility: [already visible / pushed as above / unavailable to the connector]
- Material validation, if any (secondary framing): `command` — `concise result`
- User-provided hypothesis to evaluate, if any (not a fact): [hypothesis]

# Constraints

- Evaluate independently and neutrally; do not assume any hypothesis, cause, or solution is correct.
- Preserve exact technical names. Do not invent facts or unstated operational constraints.
- Separate primary evidence, secondary framing, assumptions, inferences, and recommendations.
- State uncertainty, contradictions, and missing evidence explicitly.
- Do not extend beyond the named scope unless necessary to answer it; identify any necessary scope expansion.
- Do not create or modify GitHub resources.

# Evidence Rules

- Inspect GitHub source at the pinned ref before relying on this document.
- Treat a durable experiment/result record as primary only for its directly recorded measurements, commands, artifacts, and provenance; treat its interpretations as secondary framing.
- Cite repository, commit/ref, file path, and line range where possible.
- If evidence is missing or the connector cannot access a source, say so and do not guess.
- Support each recommendation with primary evidence or label it as an inference with confidence and missing evidence.

# Required Output

For an independent audit or review, return:
1. Unsupported or weakly supported claims
2. Evidence gaps and contradictions
3. Competing interpretations
4. Questions or checks needed before deciding

For decision support or execution planning explicitly requested in the task, return:
1. Executive summary
2. Main analysis
3. Recommendations with citations or explicit inference labels
4. Alternatives, risks, and failure modes
5. Validation plan and next actions

# Artifact Output

Create one downloadable Markdown report of 800–1,200 words, excluding citations. Also create a PDF if file generation is available. If downloadable files are unavailable, output the complete Markdown report directly. Use a table or diagram only when it materially clarifies the result.
```

For coding tasks, name target files, interfaces, current and desired behavior, tests, acceptance criteria, and do-not-change constraints. For debugging tasks, name the exact error, reproduction steps, environment, recent changes, implicated files, prior attempts, and expected versus actual behavior.

## Final Output Rule

Return only:
- the consult document path;
- the GitHub refs Pro should inspect;
- any push/commit status that affects whether Pro can see the evidence.

If a required push was not allowed or failed, state that the document is incomplete until the branch is visible on GitHub.
