# Pro Repository Consultation

Read this reference only after the shared `ask-chatgpt-pro` entrypoint selects the Pro repository consultation route. It owns the GitHub connector workflow, consultation modes, source manifest, artifact policy, and final handoff. Do not apply it to plain external research.

## Goal

Produce a Markdown consult document for ChatGPT Pro, not an answer to the underlying task. Preserve the user's actual stage of work while keeping repository facts, prior reasoning, hypotheses, preferences, and decisions in their correct epistemic roles.

Use GitHub as the primary evidence source. Direct Pro to inspect the named repositories and pinned commits itself. Do not drive ChatGPT Web or create an Oracle context bundle.

## When To Use This Instead Of Ask Oracle

Use this skill when:
- relevant material lives in GitHub repos ChatGPT Pro can access;
- the question benefits from Pro inspecting repo structure, history, branches, PRs, or files directly;
- local changes must be committed and pushed before Pro can evaluate them.

Use `ask-oracle` instead when:
- the essential evidence is not in GitHub or should not be pushed;
- the key evidence is local logs, generated output, private documents, papers, or datasets;
- the user needs a self-contained bundle independent of connector behavior.

## Choose Task Type And Consultation Mode

Classify task type and consultation mode separately.

Task type may be code/change review, debugging, architecture/system review, research/comparison, decision support, execution planning, document/log analysis, or mixed.

Choose exactly one primary mode. Add at most one secondary mode only when it contributes a distinct required output or check that task type and task-specific context cannot express cleanly.

| Mode | Use when |
|---|---|
| **Discover** | Pro should perform a fresh independent audit or orientation pass. |
| **Verify** | The user wants a suspected explanation, proposal, or claim tested. |
| **Refine** | The user already has a synthesis, design, review, or working model that needs critique or improvement. |
| **Decide** | The user needs a choice among credible alternatives. |
| **Execute** | A direction has already been selected and Pro should plan, specify, or review its execution. |

The primary mode owns framing, context authority, stop conditions, and the main Required Output. A secondary mode may add a bounded section after the primary result; it must not contradict, reopen, or relax the primary mode. If the two modes conflict, omit the secondary mode or make the primary mode control explicit. Do not chain more than two modes.

## Shared Context Authority

Apply the canonical [Shared Context Authority](../SKILL.md#shared-context-authority) from the entrypoint when sorting supplied context. Keep its categories distinct, preserve hard requirements and selected decisions, use preferences as comparison criteria, and label inferences, recommendations, contradictions, and unresolved gaps. Pro-specific evidence and GitHub rules below add repository authority without redefining the shared categories.

## Workflow

1. Read the user's task for requested deliverable formats. Invoking this skill does not request a PDF; preserve an explicit request such as "do provide PDF along with other output" in the consult's Artifact Output instructions.
2. Choose task type, one primary mode, and an optional secondary mode under the rules above. Do not default every consult to Discover merely because independent judgment is useful.
3. For research work, identify the current research stage and the exact decision this consultation should change or leave unresolved. Apply the research-stage contract from the entrypoint; do not substitute a narrower stage because it is easier to fit the current implementation.
4. Classify supplied context using the shared authority model. Preserve useful context instead of deleting it in the name of neutrality.
5. Identify each GitHub repo and stable ref. Record `owner/repo`, an exact commit SHA, its branch or PR URL, and its role in the task. For a change review, record both base and head commits.
6. Check GitHub visibility. Use `gh repo view owner/repo` or `git remote -v` when needed, then inspect `git status --short` and the relevant diff. If local changes are evidence, commit and push them before preparing the document; respect repo stop/ask gates.
7. Build a proportional source manifest. Name authoritative starting paths and add symbols, errors, or search strings only when they materially improve discovery. Do not turn a broad task into an exhaustive file checklist.
8. Select only the sources needed to answer the task. Omit generated files, dependency directories, and unrelated modules. Include PR descriptions, review threads, issue commentary, or prior AI reports only when the user explicitly requests comparison or the selected mode needs that working synthesis; label them secondary framing.
9. Classify missing inputs as blocking, material-but-nonblocking, or deferrable. If an input is blocking, stop before writing the consult, ask one pointed question, and do not apply the Final Output Rule until the user answers. Convert material-but-nonblocking gaps into explicit assumptions or early decision gates. Leave deferrable gaps unresolved when they cannot change the requested result.
10. Verify every named manifest path at its pinned commit before writing the document. Use `git cat-file -e <sha>:<path>` when available locally, or an equivalent GitHub API/connector lookup. Remove unresolved paths or state the access limitation and use a search string instead.
11. Include validation only when it materially changes the consultation. Record concise command results as secondary framing, not proof that overrides GitHub source.
12. Choose report depth, sections, tables, and diagrams proportionally using the artifact policy below. Do not force one fixed report shape onto every task.
13. Run the prompt self-review before writing `/tmp/chatgpt-pro-<topic>.md` unless the user requests a repo artifact.
14. When no blocking input remains, write the consult and apply the Final Output Rule.

## Epistemic Neutrality And Evidence Rules

- Treat GitHub source at the named commits as primary evidence. A durable experiment/result record is primary only for directly recorded measurements, commands, artifacts, and provenance; its interpretations remain secondary framing.
- Ask Pro to inspect primary evidence before relying on the consult document. Keep repository/ref/visibility facts separate from conclusions.
- Preserve exact repositories, commits, PRs, branches, files, symbols, commands, config keys, error strings, and issue numbers.
- Separate primary evidence, secondary framing, requirements, selected decisions, preferences, hypotheses, assumptions, inferences, and recommendations. State uncertainty, contradictions, stale context, missing access, and missing evidence explicitly.
- Do not invent implementation details or operational constraints such as urgency, budget, runtime, risk, or priority.
- Require repository, commit/ref, file-path, and line-range citations where possible.
- Ground recommendations in primary evidence and the applicable user requirements, selected decisions, preferences, and decision criteria. Label extrapolations beyond those inputs as inferences with confidence and missing evidence.
- Keep the consult read-only: instruct Pro not to create or modify issues, PRs, branches, commits, or repository files.

## Proportional Source Manifest

For each repository, include:
- repository role in the task;
- exact pinned ref and branch/PR context;
- a small set of authoritative starting paths;
- optional symbols, errors, or search strings when the task is targeted;
- known access or evidence limitations.

Do not require every relevant file to be named in advance. Tell Pro it may expand beyond the starting points when necessary, but it must explain material scope expansion. For broad architecture or research tasks, prefer repository roles and starting areas over long path inventories.

## Missing-Input Policy

- **Blocking:** the consult would be misleading or cannot identify the evidence or decision without the answer. Stop before writing the consult, ask one pointed question, and do not return a document path.
- **Material but nonblocking:** different answers could change part of the result, but a reversible assumption or explicit decision gate is possible. State the assumption and consequence, or ask Pro to resolve it first.
- **Deferrable:** the gap cannot materially change the current requested result. Leave it unresolved and do not interrupt the user.

## Artifact Policy

Always request a downloadable Markdown report. Choose a target range from the task rather than applying one universal cap:

- focused verification or bounded question: about 500–900 words;
- narrow code, PR, or defect review: about 800–1,200 words;
- multi-repository refinement, decision support, or execution planning: about 1,500–3,000 words;
- broad architecture or research synthesis: about 2,500–5,000 words.

These are planning ranges, not quotas. Use a shorter or longer report when the evidence and requested decision require it, and state the chosen target in Artifact Output. Do not pad a small task or compress a broad task until important reasoning disappears.

Instruct Pro to create a PDF only if the user explicitly asks for it in the prompt, such as "do provide PDF along with other output"; otherwise, do not create one. Do not infer a PDF request from invoking this skill, task importance, or file-generation availability. If a requested PDF cannot be generated, require the complete Markdown report in the response.

When a PDF is explicitly requested, tell Pro to create it from the finalized Markdown in one export, keep the layout simple, skip page-by-page visual/CV verification and iterative layout polishing, and perform only a lightweight sanity check that the file exists and is readable. Do not spend tokens describing PDF preparation. If the user does not explicitly request a PDF, do not create one.

Use tables when they materially clarify alternatives, evidence, risks, or ownership. Request a diagram only when it answers a distinct architecture, workflow, dataflow, authority, runtime, or causal question; do not request diagrams as decoration.

## Consult Document Template

Adapt this skeleton. Include only sections that contain useful information.

```markdown
# Task

[Precise task for ChatGPT Pro.]

# Consultation Mode

- Primary mode: [Discover | Verify | Refine | Decide | Execute]
- Secondary mode: [optional; omit when none]
- Task type: [code review | debugging | architecture | research | decision support | execution planning | document/log analysis | mixed]
- Why this mode fits: [one sentence]
- Mode ordering: [when secondary is present, state what it adds after the primary result and why it does not conflict]

# GitHub Context

Use your GitHub connector/plugin. Inspect the repositories and pinned refs below directly. Treat GitHub source at these refs as primary evidence; treat this document as secondary framing except for explicitly labeled user requirements, selected decisions, preferences, and decision criteria. Do not inspect PR descriptions, review threads, issue comments, or prior AI reports unless they are named below as secondary material required by this consultation.

Every named path in this source manifest was mechanically verified at its pinned ref before this document was prepared.

## Source Manifest

- `owner/repo`
  - Role: [why this repository matters]
  - Pinned ref: `full-commit-sha`
  - Branch / PR: `branch-name` or `PR URL`
  - Start with: `path/to/file`, `path/to/directory`
  - Search for, if useful: `symbol_or_error_string`
  - Limitations: [missing access or evidence, or none]

Pro may inspect additional repository paths when necessary to answer the task, but must identify material scope expansion and why it was needed.

# Goal

[Concrete result to provide.]

# Research Stage

[For research work: baseline selection | baseline establishment | faithful reproduction | adaptation | diagnosis | novel improvement. State the decision this consultation should change or leave unresolved and any essential method semantics that must remain intact. Omit for non-research work.]

# Context Authority

## User Requirements And Constraints
- [hard requirement, constraint, non-goal, or acceptance criterion]

## Working Synthesis
- [secondary framing to verify or refine; omit when none]

## User-Provided Hypothesis
- [hypothesis to test, not a fact; omit when none]

## Selected Decisions
- [hard user-owned direction to preserve unless explicitly reopened; omit when none]

## Preferences And Decision Criteria
- [soft preference, priority, or comparison criterion; omit when none]

## Assumptions And Unknowns
- [assumption, consequence if wrong, and blocking/material/deferrable classification]

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

# Mode Instructions

[Insert the primary mode block. When a secondary mode is present, append only its distinct output/check and state that the primary mode controls conflicts.]

# Task-Specific Context

[Include only the applicable task-pattern fields below.]

# Evidence Rules

- Inspect GitHub source at the pinned ref before relying on this document.
- Treat a durable experiment/result record as primary only for directly recorded measurements, commands, artifacts, and provenance; treat interpretations as secondary framing.
- Keep requirements, selected decisions, preferences, hypotheses, assumptions, inferences, and evidence distinct.
- Cite repository, commit/ref, file path, and line range where possible.
- If evidence is missing or inaccessible, say so and do not guess.
- Ground recommendations in primary evidence and the applicable user requirements, selected decisions, preferences, and decision criteria. Label extrapolations beyond those inputs as inferences with confidence and missing evidence.
- Do not create or modify GitHub resources.

# Required Output

[Derive the main sections from the primary mode and task type. Add a secondary-mode section only when it contributes a distinct result.]

# Artifact Output

Create one downloadable Markdown report of approximately [chosen range], excluding citations. Create a PDF only if the user explicitly requests it in the prompt; when requested, create it from the finalized Markdown in one export, keep the layout simple, skip page-by-page visual/CV verification and iterative layout polishing, and perform only a lightweight sanity check that the file exists and is readable. If PDF generation is unavailable, provide the Markdown report. If the user does not explicitly request a PDF, do not create one. Use tables or diagrams only when they materially clarify the result.
```

## Canonical Mode Blocks

### Discover

- Perform a fresh independent assessment from primary evidence.
- Minimize hypotheses, preferred solutions, prior conclusions, desired findings, reviewer opinions, and prior analyses unless they are themselves the explicit object of review.
- Return the strongest findings, unsupported claims, evidence gaps, contradictions, competing interpretations, and checks needed before deciding.
- Do not request recommendations, next actions, or an implementation plan unless the user explicitly asks for them.

### Verify

- Include the labeled hypothesis or proposal once and test it rather than trying to confirm it.
- Identify credible competing explanations and the evidence that discriminates among them.
- State what would falsify the hypothesis, what remains unverified, and the confidence justified by the available evidence.

### Refine

- Treat the working synthesis as secondary framing, not source truth.
- Verify the load-bearing claims that could change the conclusion; do not repeat settled discovery without new evidence.
- Return corrections, missing dimensions, stronger formulations, unresolved disagreements, and the improved synthesis.

### Decide

- Preserve hard user requirements separately from soft preferences and decision criteria.
- Compare credible alternatives against those inputs, including tradeoffs, reversibility, failure modes, and evidence gaps.
- Recommend a direction only when requested. Ground it in evidence and the stated user criteria; distinguish value judgments and extrapolations.

### Execute

- Treat selected decisions as constraints unless the user explicitly asks to reopen them.
- Translate the direction into concrete behavior, interfaces, milestones, validation, rollback, and acceptance criteria.
- Surface evidence that makes execution unsafe, infeasible, or inconsistent; do not silently redesign the objective.

## Task-Pattern Fields

- **Code or change review:** exact base/head refs, changed behavior, target interfaces, compatibility commitments, tests, and explicit review scope.
- **Debugging:** exact error, reproduction, environment, expected versus actual behavior, recent changes, implicated paths, and prior attempts.
- **Architecture or system review:** system purpose, runtime/deployment topology, component and process boundaries, communication paths, state/authority ownership, supported variants, quality attributes, and the decision horizon.
- **Research or comparison:** decision to inform, alternatives, source hierarchy, freshness requirements, claims to verify, contradictions, and acceptable unresolved uncertainty.
- **Decision support:** alternatives, hard constraints, soft preferences, decision criteria, reversibility, deadline if supplied, and what evidence would change the choice.
- **Execution planning:** selected direction, target behavior, non-goals, compatibility, sequencing, migration/rollback, verification, and completion criteria.
- **Document or log analysis:** exact artifacts, provenance, time range, known gaps, questions to answer, and what claims the material can and cannot support.

## Prompt Self-Review

Before writing the consult, check:

- Did I choose the correct primary mode, or did I default to Discover mechanically?
- Is a secondary mode genuinely necessary, bounded, ordered after the primary result, and non-conflicting?
- Did I accidentally present a hypothesis, synthesis, preference, or selected decision as repository fact?
- Did I distinguish selected decisions from softer preferences and decision criteria?
- For research work, did I preserve the user's stage, essential method semantics, and decision instead of substituting a smaller or more novel task?
- Could the requested deliverable succeed while missing the user's intended outcome?
- Did I delete useful constraints or decision history in the name of neutrality?
- Am I asking Pro to redo work already completed without identifying a reason or new evidence?
- Does any repeated requirement anchor the answer more strongly than the user intended?
- Is the source manifest proportional, with starting points rather than an exhaustive checklist?
- Did I classify missing inputs before asking the user or inventing an assumption?
- Does the requested output match the breadth, consequence, and reversal cost of the task?
- Are tables, diagrams, and artifacts requested only when useful?
- Do the success criteria test answer quality rather than encode the desired conclusion?
- Does the prompt preserve exact names, refs, and access limitations?

## Final Output Rule

Apply this rule only when no blocking input remains and a consult document was produced.

Return only:
- the consult document path;
- the GitHub refs Pro should inspect;
- any push/commit status that affects whether Pro can see the evidence.

If an input is blocking, stop before writing the consult, ask one pointed question, and do not return a document path.

If a required push was not allowed or failed, state that the document is incomplete until the branch is visible on GitHub.
