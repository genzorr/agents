---
name: prepare-dynamic-workflow
description: Decide whether a task warrants a Claude Code dynamic workflow, then author or reuse one as a durable artifact for a Claude Code session to run — or produce a copyable handoff prompt backed by a durable WORKFLOW.md. Reach for it on research and investigations, large migrations, repo-wide audits/sweeps, scaled sorting/triage, adversarial verification, and multi-angle planning. Not for small, single-context, single-pass-trustworthy tasks. Do not use for ordinary Codex /goal handoffs.
---

# Prepare Dynamic Workflow

A dynamic workflow is a JavaScript script that orchestrates many subagents at scale. A Claude Code runtime
executes the script in the background; intermediate results live in **script variables**, so the session's
context only holds the final answer.

Codex cannot run workflows itself — the `Workflow` runtime is a Claude Code feature. This skill's job is to
produce the **artifacts a Claude Code session will run**: an authored/reused workflow script and/or a
copyable handoff prompt backed by a durable spec. Never tell a Codex session to run a workflow.

> **Frontmatter note (cross-tree).** The Claude twin (`claude/skills/prepare-dynamic-workflow/SKILL.md`)
> carries `model`/`effort`/`allowed-tools`/`argument-hint`. Codex skills omit those Claude-runtime
> fields by convention — this is deliberate, not drift. Do not add them to this file.

This skill is intentionally separate from `goal-prompt`:

- Use `goal-prompt` for durable Codex `/goal` handoffs or ordinary Claude Code handoffs that read `GOAL.md`.
- Use this skill when a task is workflow-shaped (below), or when the user explicitly asks for Claude Code's
  workflow feature / `ultracode`.
- A task being long-running does not by itself mean it needs a workflow.

## Why workflows exist

A single context window that both plans and executes a long, parallel, or adversarial task degrades in
three specific ways. Workflows counter each by giving every agent its own fresh context and a narrow goal:

- **Agentic laziness** — stopping after partial progress (35 of 50 review items) and declaring done.
- **Self-preferential bias** — trusting your own findings when asked to verify or judge them.
- **Goal drift** — losing edge-case and "don't do X" constraints across compactions.

## When to reach for one

Workflow-shaped work — prefer a workflow when the task is any of:

- **Research / investigation** — fan out across sources/angles, then cross-check (codebase deep-dives,
  Slack/incident mining, web research).
- **Deep verification** — extract every claim in a doc/report and verify each independently.
- **Root-cause analysis** — independent hypotheses from disjoint evidence (logs, files, data), each faced
  with verifiers and refuters. Not just for code (sales dips, pipeline failures, post-mortems).
- **Large migration / refactor** — one isolated agent per call-site/module/failing-test, review, merge.
- **Repo-wide audit / sweep** — many files, each its own clean context.
- **Sorting / triage at scale** — 1000+ items ranked by pairwise comparison, or bucket-ranked in parallel.
- **Taste / exploration** — generate many candidates, judge against a rubric, or run a tournament.
- **Multi-angle planning** — draft a hard plan from several independent angles before committing.

Skip a workflow when the task is small, fits one context window, is single-pass-trustworthy, or "a handful
of edits gets it done." Most ordinary coding does not need a panel of five reviewers. Workflows cost
meaningfully more tokens — match the structure to the task.

## Choose the mode(s)

After confirming the task is workflow-shaped, decide what artifact to produce. Modes compose:

1. **Find / reuse** — check for an existing fit first: the repo's `.claude/workflows/*.js` (project), personal
   `~/.claude/workflows/*.js`, or the bundled `/deep-research`. If one fits, the handoff names it
   (`Run /<name>`) and the input it takes via `args`, instead of authoring a new script.
2. **Author** — write a script for this task, composing the patterns below, as a durable artifact the Claude
   session will run. Discover the work-list inline first, then encode the orchestration over it.
3. **Save** — write a script worth keeping to the repo's `.claude/workflows/<name>.js` so it becomes
   `/<name>` for any Claude Code session, or ship it inside a skill folder referenced from SKILL.md as a
   **template** (adaptable), not a script to run verbatim.
4. **Prompt-only** — produce a copyable handoff prompt + durable `WORKFLOW.md` for the Claude Code session
   to run (see the dedicated section).

If the user did not specify a mode and it is not obvious, ask. Default: find/reuse → author the script as a
durable artifact → prompt-only handoff that points at it.

## Patterns

Composable building blocks. Skeletons are illustrative — schemas (`SCHEMA`) are JSON Schema objects.

- **Classify-and-act** — a classifier agent routes each item to a handler by type; also the basis of model
  routing (research the task, then route to a cheaper/stronger model per call).
- **Fan-out-and-synthesize** (barrier) — split into independent units, run one agent each, then one
  synthesis agent merges. Use when steps benefit from clean, non-cross-contaminating contexts.
  ```js
  phase('Scan')
  const findings = (await parallel(args.files.map(f => () =>
    agent(`Check ${f} for missing auth checks.`, {phase: 'Scan', schema: SCHEMA})))).filter(Boolean)
  phase('Synthesize')                                   // barrier: needs ALL findings at once
  return await agent(`Merge and dedupe: ${JSON.stringify(findings)}`, {schema: SCHEMA})
  ```
- **Adversarial verification** — for each finding, spawn independent skeptics prompted to *refute*; default
  to refuted when unsure. Use `pipeline` so each dimension verifies as its review lands. Give verifiers
  distinct lenses (correctness/security/repro) when a finding can fail several ways.
  ```js
  const results = await pipeline(DIMENSIONS,
    d => agent(d.prompt, {phase: 'Review', schema: SCHEMA}),
    review => parallel(review.findings.map(f => () =>
      agent(`Try to refute "${f.title}". Default refuted=true if uncertain.`, {phase: 'Verify', schema: SCHEMA})
        .then(v => ({...f, verdict: v})))))
  const confirmed = results.flat().filter(Boolean).filter(f => f.verdict?.real)
  ```
- **Generate-and-filter** — generate many candidates, filter by rubric/verification, dedupe, return survivors.
- **Tournament** — N agents attempt the same task from different angles; pairwise judge agents pick a winner
  (comparative judgment beats absolute scoring — use it for sorting/taste).
- **Loop-until-done / -dry** — for unknown-size discovery, keep spawning finders until K consecutive rounds
  surface nothing new. Dedupe against everything *seen*, not just what was confirmed, or it never converges.
  ```js
  const seen = new Set(); let dry = 0
  while (dry < 2) {
    const fresh = (await agent('Find issues not yet reported.', {schema: SCHEMA})).items
      .filter(x => !seen.has(x.key))
    if (!fresh.length) { dry++; continue }
    dry = 0; fresh.forEach(x => seen.add(x.key))        // verify + collect fresh here
  }
  ```
- **Quarantine** (untrusted content) — agents that read public/untrusted input must not take high-privilege
  actions; a separate set of agents acts on what they surface. Essential for triage over support queues.
- **Completeness critic** — a final agent asks "what's missing — a source unread, a claim unverified, a
  modality not run?" Its answers seed the next round.

## Authoring a script

The script runs under Claude Code's `Workflow` runtime. Key rules to encode:

- Start with a pure-literal `export const meta = {name, description, phases}`.
- Primitives: `agent(prompt, opts?)` (opts: `label`, `phase`, `schema`, `model`, `isolation:'worktree'`,
  `agentType`), `parallel(thunks)` (barrier; nulls on failure — `.filter(Boolean)`), `pipeline(items,
  ...stages)`, `phase()`, `log()`, `workflow()`, `args`, `budget`.
- **Default to `pipeline()`.** A `parallel()` barrier is justified only when a stage genuinely needs all of
  the previous stage's results at once (dedup/merge, early-exit on zero, cross-item comparison) — not for a
  flatten/map/filter, which belongs inside a stage.
- Use `schema` to force structured output — validated at the tool layer, so no parsing and the agent retries
  on mismatch.
- Route stages to a cheaper/stronger `model` deliberately; omit when unsure (inherits the session model).
- Use `isolation: 'worktree'` only when agents mutate files in parallel and would conflict (migrations).
- No silent caps: `log()` anything dropped (top-N, no-retry, sampling).
- `Date.now()` / `Math.random()` / argless `new Date()` are unavailable — pass timestamps via `args`; vary
  randomness by index.
- Scale to the ask: "find any bugs" → a few finders, single-vote verify; "thorough audit" → larger pool,
  3–5-vote adversarial pass, synthesis. Honor an explicit token budget via `budget`.
- A saved workflow takes input via the `args` global — design it to parameterize (question, path list,
  config) rather than be edited per run.

## Prompt-only handoff (+ durable WORKFLOW.md)

For autonomous long runs and cross-session handoffs, the deliverable is a copyable prompt plus a durable
spec the Claude Code run reads after compaction. Author both.

Always create or replace a durable workflow spec before writing the prompt:

- Prefer `<project-root>/WORKFLOW.md` for in-project runs; use `/tmp/<topic>-workflow.md` only when the
  project should not be modified or the user wants a temporary handoff.
- `WORKFLOW.md` is the execution contract. Reference any PRD/harness task/design doc/`GOAL.md` as supporting
  context instead of duplicating it; mark a possibly stale `GOAL.md` as background unless the user says it is current.

The spec defines: objective and non-goals; required references; a P0/P1/P2 board where P0/P1 are
close-blocking; phases (audit, design/invariants, implementation, verification, independent review, final
handoff); hard exit conditions including elapsed-time gates when requested; benchmark/measurement
requirements; commit cadence and branch rules; and stop/ask gates for risky decisions, missing evidence,
destructive changes, or unclear ownership.

Convert broad goals into falsifiable deliverables before writing the board:

- Derive a requirement table: `Requirement | Required artifact/evidence | Completion test | May not be satisfied by`.
- Do not leave close-blocking items as broad verbs ("audit", "improve", "investigate", "make faster")
  unless the item names the concrete artifact, command, metric, or proof that closes it.
- For broad audit/architecture/cleanup objectives, require a durable map/decision artifact as P0 unless the
  user asked for implementation-only work.
- If the user asks for speed/overhead/parity/reliability/correctness/non-interference, make the relevant
  measurement close-blocking. One measured improvement does not close a broader objective.
- Label intentionally-incomplete requirements P2 or non-goal up front; do not hide a primary requirement as
  an `ACCEPT_WITH_TRADEOFF` caveat.

Add a completion-audit section: the final handoff must include `Requirement | Evidence inspected | Status |
Remaining gap`. P0/P1 statuses may be `done` or `blocked`; `deferred`, `unknown`, `partially done`, and
`not measured` are not closeable. Missing evidence for a primary P0/P1 requirement must produce
`BLOCKED_MISSING_EVIDENCE`, `EXPERIMENT_ONLY`, or continued work.

Strengthen review: require an independent/adversarial review of objective *completeness*, not only
correctness of implemented claims, comparing the original objective and completion audit against the diff,
tests, benchmark artifacts, and docs. If an elapsed-time gate exists and the run is ready to finish before
using ~half of it, require a second-pass self-audit.

Keep workflow instructions focused on execution structure; put domain detail in the durable spec or harness task.

### Handoff prompt output

Return exactly one fenced `text` block, plus an optional one-line lead-in:

```text
You are in <project/repo>.

This is a Claude Code dynamic workflow run.

Read <WORKFLOW.md path> first. WORKFLOW.md, plus the files it references, is the durable source of truth for
this run; do not rely on this prompt after compaction. Treat any referenced GOAL.md as background only
unless WORKFLOW.md explicitly says it is current.

Create and use a dynamic workflow for this run. At minimum, include phases for read-only audit,
implementation planning, implementation, verification, independent/adversarial review, and final handoff.
Keep the workflow updated as work progresses.

Follow the hard exit conditions, stop gates, benchmark/measurement requirements, commit cadence, and
final-accounting rules in the durable spec. Do not stop after one useful fix, one passing smoke test, or one
commit while P0/P1 workflow items remain actionable.

Before final handoff, perform the completion audit required by WORKFLOW.md. Do not mark P0/P1 complete from
intent, partial evidence, or a narrower successful result. If a primary requirement remains unmeasured or
only partially proven, keep working or return a blocked/experimental verdict rather than `ACCEPT`.

If the durable spec is under-specified in a way that would change the work, ask before proceeding. Otherwise
proceed autonomously within the spec.
```

If a reusable script was authored or found, name it in the prompt (`Run /<name>` or "run the script at
<path>") so the target session reuses it instead of re-authoring.

## Output by mode

State what you produced. Codex never runs the workflow — every mode's output is an artifact or handoff a
Claude Code session executes. There is no "run" mode here (that is the Claude twin's; this skill stops at the
artifact).

- **Find / reuse** — name the matching workflow (`/<name>` or the script path) and the `args` input it takes,
  so the handoff says `Run /<name>` for a Claude Code session instead of re-authoring.
- **Author** — the script written as a durable artifact (state its path), plus a one-line note that a Claude
  Code session runs it (via the prompt-only handoff, `Run /<name>`, or the Claude Code `/workflows` view). Do
  not run it from Codex.
- **Save** — the saved path (`.claude/workflows/<name>.js`, or a skill-folder `.js` referenced as a template)
  and the `/<name>` it becomes for a Claude Code session.
- **Prompt-only** — the fenced handoff prompt from the section above, returned after writing `WORKFLOW.md`.

## Rules

- Do not tell a Codex session to use or run Claude Code workflows. The artifacts target a Claude Code session.
- Do not generate a Codex `/goal` bootstrap prompt from this skill.
- Do not invoke this skill for a small, single-context, or single-pass-trustworthy task. The token cost must
  be earned.
- Find/reuse before authoring; do not write a new script when a bundled or repo-saved one fits.
- For a handoff, the final prompt must point primarily to `WORKFLOW.md`, not `GOAL.md`. Do not paste large
  project context into the prompt — put it in the spec or a referenced task/doc.
- Preserve uncertainty as stop gates rather than hiding it in broad autonomy wording.
