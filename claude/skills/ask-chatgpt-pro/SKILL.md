---
name: ask-chatgpt-pro
description: Prepare a manual ChatGPT Pro consult for a hard codebase question using ChatGPT's GitHub connector instead of a bundled context pack. Use when the user wants Pro to inspect one or more GitHub repos, branches, commits, PRs, or named files directly; especially when local changes must be committed and pushed so Pro can see them.
---

# Ask ChatGPT Pro

Use this when ChatGPT Pro should answer a hard or complex question by reading GitHub repositories directly through its GitHub connector/plugin.

This skill produces a GitHub-visible state and a copyable prompt. It does not drive ChatGPT Web, and it does not create an Oracle context bundle.

## When To Use This Instead Of Ask Oracle

Use this skill when:
- the relevant material lives in GitHub repos ChatGPT Pro can access;
- the question benefits from Pro inspecting repo structure, history, branches, PRs, or files directly;
- local changes must be committed and pushed before Pro can evaluate them.

Use `ask-oracle` instead when:
- the context is not in GitHub or should not be pushed;
- the key evidence is local logs, generated output, private documents, papers, or datasets;
- the user needs a self-contained bundle independent of connector behavior.

## Workflow

1. Clarify the exact question and output requested.
   Done when the prompt can state the decision, review, diagnosis, plan, or critique Pro should produce.
2. Identify the GitHub repos and refs Pro must inspect.
   Use `gh repo view owner/repo` or `git remote -v` to verify repo names when needed.
   Done when each repo has an `owner/name`, branch/PR/commit if relevant, and target paths or search terms.
3. Check whether local changes are part of the evidence.
   Run `git status --short`, inspect the diff, and decide whether the unpushed state matters.
   Done when the prompt either points to already-visible refs or names the local changes that must become visible.
4. If local changes must be visible, commit them and push a branch before writing the final prompt.
   Respect repo stop/ask gates for commits, branch creation, and remote pushes. If policy requires approval, ask before pushing.
   Done when `git rev-parse HEAD` names the commit Pro should inspect and `git status --short` has no relevant uncommitted evidence.
5. Capture recent validation only when it matters.
   Include commands and concise results, not full logs unless the logs are in GitHub or attached elsewhere.
   Done when Pro can distinguish verified facts from unchecked assumptions.
6. Write the ChatGPT Pro handoff prompt to a Markdown file.
   Prefer `/tmp/chatgpt-pro-<topic>.md` unless the user requests a repo artifact.
   Done when the file includes the template sections below and is ready to paste into ChatGPT Pro.
7. Return the prompt path and the GitHub refs Pro should open.
   Do not paste the whole prompt unless the user asks.

## Handoff Prompt Requirements

The prompt must tell ChatGPT Pro to use its GitHub connector/plugin to inspect the named repos and refs. Do not rely on Codex summaries for primary evidence when the source is available in GitHub.

Include:
- exact repo names, for example `genzorr/agents`;
- branch names, PR URLs, or commit SHAs;
- target files, directories, symbols, issue numbers, or search strings;
- the user question and desired output format;
- constraints, non-goals, and any stop conditions;
- known facts, assumptions, and recent validation;
- evidence rules requiring file/path citations and explicit uncertainty.

## Prompt Template

```markdown
# Task

[Hard question for ChatGPT Pro.]

# GitHub Context

Use your GitHub connector/plugin. Inspect these repos and refs directly; do not rely on this prompt as the primary source when GitHub source is available.

- `owner/repo`
  - Ref: `branch-or-commit-or-PR`
  - Start with:
    - `path/to/file`
    - `path/to/directory`
  - Also search for:
    - `symbol_or_error_string`

# Current State

- Relevant commit(s): `sha`
- Relevant branch/PR: `name or URL`
- Validation already run:
  - `command`: `result`
- Known facts:
  - ...
- Assumptions / uncertainty:
  - ...

# Constraints

- Preserve exact names of files, functions, commands, branches, and config keys.
- Separate facts found in GitHub from inferences and recommendations.
- Cite file paths and line ranges where possible.
- Say when evidence is missing instead of guessing.
- Do not propose changes outside the named scope unless they are necessary to answer the task.

# Required Output

Return:
1. Direct answer / recommendation
2. Evidence from GitHub
3. Alternatives or competing interpretations
4. Risks and failure modes
5. Concrete next steps or validation checks
```

## Final Output Rule

Return only:
- the prompt file path;
- the repo refs Pro should inspect;
- any push/commit status that affects whether Pro can see the evidence.

If a push was required but not allowed or failed, state that the prompt is incomplete until the branch is visible on GitHub.
