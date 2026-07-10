---
name: goal-prompt
description: Create a short copyable prompt for a Codex /goal handoff by default, or a direct Claude Code handoff when explicitly requested, that points to a durable goal spec. Use when the user invokes goal-prompt, /goal-prompt, asks for a prompt that an agent session should use to read a durable goal spec, asks for a long-running autonomous goal, or needs PRD-backed goal setup.
---

# Goal Prompt

Create a short prompt for a target agent session. Default to a Codex session that will run under `/goal`.

> **Cross-tree twin.** `claude/skills/goal-prompt/SKILL.md` is the Claude Code counterpart. The two
> bodies are intentional tree-framed twins (Codex `/goal` set-goal bootstrap vs Claude direct
> prompt), not duplication to extract — keep their section structure in sync when editing either.

For Codex targets, the output is not a normal task prompt like "`/goal do this`". It is a bootstrap prompt that points the target agent to a durable goal spec file, tells it to formulate a compact file-referenced goal, set that goal with the goal tooling, and execute.

For Claude Code targets, the output is a direct task prompt that points the target agent to a durable goal spec file, then tells it to follow that file and execute. Claude Code does not have Codex-style set-goal functionality, so do not instruct the target agent to set a goal or create a meta-prompt for a goal mechanism.

By default the goal spec is a unique per-handoff file at `/tmp/agent-handoffs/<repo>/<YYYYMMDD>-<task-slug>-goal.md` (see Gather step 3). Optimize for compaction resistance by putting the actual instructions in that durable goal spec, not in the generated prompt.

## Input

- Treat all text after `goal-prompt` or `/goal-prompt` as the seed context. The user may provide a rough idea, constraints, copied notes, paths, task IDs, or partial decisions.
- If no seed context is provided, use the current conversation when it clearly contains one.
- If neither the invocation nor the conversation contains enough intent to define a direction, ask one concise question for the missing topic or outcome and stop.
- Ask follow-up questions only when the answer would materially change the project, scope, or success criteria. Ask at most three.
- If the user says the target agent needs a time limit, deadline, timebox, "work until", "do not stop until", or similar persistence constraint, preserve it as a first-class requirement. If the exact duration or wall-clock deadline is missing, ask one concise question for it before writing the prompt.

## Target Agent

- Default target is **Codex `/goal`**.
- If the user explicitly says `for Claude`, `Claude Code`, or otherwise names Claude as the target agent, target **Claude Code** instead.
- For a Claude Code target, produce a direct task prompt. Do not tell Claude to set a goal, use `/goal`, create a meta-prompt, or call goal tooling. Claude should read the goal spec and execute it directly.
- For a Codex target, keep the existing `/goal` bootstrap behavior: tell the target Codex session to set a compact file-referenced goal and execute it.

## Gather

Before writing the prompt, inspect enough local context to make it project-specific. Use already-provided seed context and current conversation details first; gather only what is missing or needs validation.

1. Read applicable `AGENTS.md`, README, and command docs only when they are not already known in the active session or likely to affect the handoff.
2. Find relevant docs, harness tasks, ADRs, plans, or source entry points named by the seed context.
3. Create or update one durable goal spec file before writing the prompt. Default to a unique per-handoff path so concurrent handoffs never collide and no earlier spec is overwritten:
   - **Default:** `/tmp/agent-handoffs/<repo>/<YYYYMMDD>-<task-slug>-goal.md`, where `<repo>` is the target repo/worktree name and `<task-slug>` is a short kebab-case summary of the goal. Create the directory if needed.
   - Only write the goal spec inside the project (for example a committed `docs/.../<topic>-goal.md`) when the user explicitly wants a durable in-repo copy; keep it out of the default handoff path.
4. Before drafting the GOAL file, define a concise `Completion Contract` for every goal, regardless of mode. It must state:
   - **Success exit:** the exact observable conditions that allow the agent to claim the goal is complete, including required verification evidence.
   - **Continue conditions:** signals that mean the agent must keep working instead of stopping after a partial win.
   - **Stop/ask gates:** conditions that require user input before proceeding, such as ambiguous scope, missing credentials/infrastructure, contract-breaking changes, or unsafe broad rewrites.
   - **Blocked exit:** what evidence must be recorded if the agent cannot proceed.
   - **Non-goals/deferred work:** related work that must not be silently folded into success.
5. Select the applicable goal mode or compatible mode combination before drafting the GOAL file. Standard Mode usually stands alone; Research, Timeboxed, and Long-Run modes may be combined when the work needs all of their sections.
   - **Standard Goal Mode**: implement, verify, or continue a known task with a known task order. Keep the GOAL file short and task-directed.
   - **Research Goal Mode**: investigate an uncertain mechanism, compare candidates, diagnose a metric/regression, run benchmarks, decide whether a hypothesis works, or let the agent choose the next attempt after seeing evidence. Add the research-loop sections described below.
   - **Timeboxed Goal Mode**: preserve the deadline/timebox and add primary-work/fallback rules. If the timeboxed work is uncertain or benchmark-driven, combine this with Research Goal Mode.
   - **Long-Run Goal Mode**: run a broad autonomous task for many hours or avoid premature closure. Strong signals include "overnight", "6-8 hours", "xhigh/max", "do not stop early", "hard exit conditions", "improve speed by X", "broad audit", "rewrite/refactor", or "large autonomous run". Combine this mode with Research or Timeboxed Mode when evidence or elapsed time controls success.
6. Decide whether the goal needs a PRD or PRD-like durable spec. Create or update one when the work is product-shaped, architecture-shaped, benchmark-policy-shaped, multi-hour, spans several modules, has ambiguous success criteria, or should survive multiple goal runs.
   - The PRD is the durable **what/why/success contract**: problem, users, goals/non-goals, definitions, constraints, acceptance model, risks, and round-specific completion contract.
   - The goal spec is the **execution routing contract**: branch, task order, references, mode, verification, stop gates, and final handoff requirements.
   - Harness tasks are the **tracked units of work**.
   - Put the PRD under an existing project docs area when obvious, such as `docs/.../<topic>-prd.md`; otherwise use `/tmp/<topic>-prd.md`, label it temporary in the goal spec, and require final accounting to say whether it should be promoted into the repo.
   - Do not create a PRD for tiny fixes, mechanical edits, exact one-off commands, or ordinary task continuations where the harness task already contains enough durable context.
7. If the current project uses harness, check `harness status` or `harness snapshot` when useful. Make the GOAL file a concise routing index that points to concrete harness references supplied by the user or already active:
   - active or named slice file
   - active or named task file(s)
   - any named spec/result docs
   - task order, deadline, verification, stop gates, and transition instructions
   Do not invent harness tasks or slices. If a harness handoff does not have enough durable context, warn the current user that the target agent needs a harness task/spec first, or ask whether to create one.
8. If the current project does not use harness, make the GOAL file the durable working spec: objective, context, constraints, success criteria, verification, durable references, stop gates, and any deadline.
9. For Research Goal Mode, include a `Hypothesis Loop And Exit Conditions` section in the GOAL file. It must define:
   - the real problem being solved, not only the first suspected mechanism;
   - prior evidence and required references the agent must read before choosing candidates;
   - the loop: hypothesis -> smallest implementation or diagnostic -> benchmark/measurement -> accept/reject/inconclusive -> next hypothesis;
   - a concrete minimum effort bar, usually at least 3 serious hypotheses or implementation attempts unless the user gives a different number, a candidate passes promotion gates earlier, or a stop gate blocks work;
   - candidate gates with exact metric thresholds, required artifacts, and any replication rule such as N=1 before N=3;
   - the continuation rule: after every negative, partial, or promising result, formulate the next evidence-derived hypothesis and continue until a listed exit condition is met;
   - the rejection rule: reject a family only after the minimum effort bar is met and the attempted candidates fail gates;
   - stop/ask gates for missing benchmark evidence, unavailable infrastructure, contract-breaking changes, broad rewrites, exhausted nontrivial hypotheses, or user-judgment decisions;
   - the defaults policy: do not change defaults unless replicated evidence passes gates and the task explicitly recommends promotion.
10. For Long-Run Goal Mode, include a `Hard Exit Conditions` section in the GOAL file. It must define:
   - a P0/P1/P2 board requirement before implementation starts;
   - closure rule: all P0/P1 items are done, explicitly blocked, or the elapsed-time gate is reached with a handoff-quality checkpoint;
   - anti-early-exit rule: one useful fix, one passing smoke test, or one good commit is not enough when P0/P1 items remain actionable;
   - continuation rule: if the run finishes far earlier than the timebox and no stop gate is hit, continue through P1 and then P2/stretch work;
   - measurement rule: speed/performance claims require a microbenchmark, local before/after timing, or benchmark evidence for the affected path;
   - benchmark timing rule: remote benchmark timing claims require replication such as `n>=3`; otherwise label timing inconclusive and separate it from behavior parity;
   - commit cadence: commit coherent chunks after relevant verification, unless the user explicitly says not to commit;
   - final accounting: require a P0/P1 board with done/blocked/deferred status, commits, measurements, verification, benchmark paths, and remaining unsafe claims.
11. For timeboxed autonomous research, include a `Primary Work / Fallback Policy` section in the GOAL file. It must set a concrete minimum effort bar before any fallback work, and hygiene fallback is disabled unless the user explicitly allowed it.
12. Add model/effort recommendations to the goal spec when the target run is delegated, long, expensive,
    quality-sensitive, or likely to spawn Claude workers. Keep them recommendations, not hard requirements,
    unless the user explicitly named settings:
   - model = capability: recommend stronger models for ambiguity, unfamiliar domains, subtle bugs,
     architecture, security-sensitive reasoning, and final review; cheaper models for precise mechanical work;
   - effort = thoroughness: recommend higher effort when success depends on reading broadly, trying multiple
     steps, running tests, or double-checking; use default effort when unsure;
   - do not confuse Claude effort with Codex reasoning effort or the Research Goal Mode "minimum effort bar".
13. Keep gathering proportional. Do not re-audit the whole project when the user already supplied enough context. The goal is a strong handoff prompt, not full implementation.

## Output

Return exactly one fenced Markdown block, plus a one-line lead-in if useful. Use `text` as the fence language so the app renders a copy button. Keep the generated prompt brief; do not copy the full contents of the goal spec into it. Substitute the actual goal-spec path into the prompt.

For a Codex `/goal` target, use this bootstrap prompt:

```text
You are in <project/repo>.

Read <goal-spec path, e.g. /tmp/agent-handoffs/<repo>/<YYYYMMDD>-<task-slug>-goal.md> before setting a goal. That file, plus the files it references, is the durable source of truth; do not rely on this prompt after compaction.

Set a compact Codex goal for yourself that references that goal spec, includes any deadline or stop gates from that file, and then execute it. Inspect only the project context needed to follow the goal spec. Before each harness task/slice transition, activate and read the relevant harness item named in the goal spec.

If the goal spec is under-specified in a way that would change the work, ask before setting the goal. Otherwise proceed autonomously, keep work scoped to the goal spec, verify as instructed there, and do not claim success when required evidence is missing. If the goal spec defines a research loop or hard exit conditions, do not stop after one useful fix or one failed candidate; continue until success, research rejection, elapsed-time exit, or a listed stop/ask gate.
```

For a Claude Code target, use this direct prompt:

```text
You are in <project/repo>.

Read <goal-spec path, e.g. /tmp/agent-handoffs/<repo>/<YYYYMMDD>-<task-slug>-goal.md> first. That file, plus the files it references, is the durable source of truth; do not rely on this prompt after compaction.

Follow the goal spec directly, including any deadline or stop gates from that file, and execute it. Inspect only the project context needed to follow the goal spec. Before each harness task/slice transition, activate and read the relevant harness item named in the goal spec.

If the goal spec is under-specified in a way that would change the work, ask before proceeding. Otherwise proceed autonomously, keep work scoped to the goal spec, verify as instructed there, and do not claim success when required evidence is missing. If the goal spec defines a research loop or hard exit conditions, do not stop after one useful fix or one failed candidate; continue until success, research rejection, elapsed-time exit, or a listed stop/ask gate.
```

## Prompt Requirements

- Keep the generated prompt short. For Codex targets it should be a bootstrap pointer to the goal spec; for Claude Code targets it should be a direct task prompt pointing to that file. Neither form should duplicate the goal spec.
- Do not include large pasted seed context, conversation summaries, or project excerpts in the generated prompt. Put necessary details in the GOAL file instead.
- Include concrete local paths, task IDs, docs, commands, or known constraints in the GOAL file, then reference that file from the generated prompt.
- Prefer durable-reference-first prompts. For Codex targets, the compact stored goal should reference the goal spec. For Claude Code targets, the direct prompt should reference the goal spec. In both cases, the goal spec should reference any other durable files the target agent must re-read after compaction.
- Preserve uncertainty explicitly instead of hiding it. Put unresolved questions in the generated prompt as stop gates.
- Prefer autonomous exploration wording over implementation certainty when the seed is exploratory.
- Always write or update a durable goal spec before producing the prompt. Default to the unique `/tmp/agent-handoffs/<repo>/<YYYYMMDD>-<task-slug>-goal.md` path; write an in-repo copy only when the user explicitly asks. Reference that file from the generated prompt and, for Codex targets, from the compact goal. Do not use the long chat prompt as the only durable source for important requirements.
- For PRD-backed goals, write or update the PRD before finalizing the goal spec, and make the goal spec reference it. The generated prompt should still point primarily to the goal spec; do not paste the PRD into the prompt.
- For harness projects, make the GOAL file small: a routing index with user-provided or already active slice/task files, named spec/result docs, task order, deadline, verification, stop gates, and instructions to respect active task state and lifecycle rules.
- For non-harness projects, make the GOAL file complete enough to continue after compaction: context, constraints, success criteria, verification, durable references, stop gates, and deadline.
- **Completion Contract (required in every GOAL file).** Include a concise section that defines success exit, continue conditions, stop/ask gates, blocked exit evidence, and non-goals/deferred work. Do not let "tests pass" alone define success unless the task is purely mechanical and the acceptance criteria are fully covered by those tests.
- **Validation loop (required in the verification section).** Name the *smallest trustworthy validation loop* for the change: the deterministic tests/checks the agent runs, plus an explicit manual-QA step with recorded evidence (steps + observed result) where behavior cannot be proven automatically (UI, interactive, external state). Do not add an independent-review pass as a default global tax. Require a separate fresh-context review only when the user explicitly asks for it or the target project's task/finalization policy mandates it; in Harness repos, reference `/Users/example/dev/os/repos/harness/docs/harness-runs-operator-guide.md` → *Review Independence* for that project-specific gate.
- **Final Handoff (required in every GOAL file).** Include a `Final Handoff` section requiring the implementation agent to leave a **standard review handoff before exiting**, persisted durably (not only in chat) so the generic lifecycle review/finalize skills (`harness-review-work`, `harness-finalize-work`) can consume it. For harness work, the normal implementer handoff is the task's outcome-shaped `# Last Session` block via `harness-task-checkpoint`, even when the implementer believes the acceptance criteria are met. Match that skill's committed contract: use the `# Outcome` sections as labels (What Landed / Verification / Not Landed / Follow-ups / Evidence) plus a Status line and branch/commits, and keep "tests passed" separate from "browser/external state verified". Reserve `harness-task-done` and the terminal `# Outcome` record for `harness-finalize-work` — closure and terminal Outcome stay finalizer-owned unless the operator explicitly tells the implementation agent to close the task. For non-harness work, require an equivalent durable handoff file (objective status, changed files, verification, not-landed, follow-ups). Anchor to the existing `# Outcome` / `# Last Session` shape; do not invent a competing schema.
- **Model/effort recommendations.** When relevant, include a concise `Recommended Runtime` or equivalent
  line in the goal spec. For Codex targets, recommend reasoning effort only when task risk justifies it. For
  Claude targets or Claude workers, recommend model for capability and effort for thoroughness. Avoid hard
  settings unless the user requested them or the delegation mechanism requires them.
- Use **Research Goal Mode** only when success requires experimental evidence and the target agent may need to choose the next attempt after seeing results. Strong signals include words like "hypothesis", "research", "try approaches", "benchmark candidates", "investigate", "diagnose", "accept/reject", "promote defaults", "find what works", or "continue after failures". Do not use Research Goal Mode for fixed implementation tasks, exact benchmark runs, simple bug fixes, or ordinary handoffs.
- In Research Goal Mode, the GOAL file must include `Hypothesis Loop And Exit Conditions` even when no timebox was requested:
  - State the real problem and distinguish it from the first suspected mechanism.
  - Name prior evidence/references to read before implementation.
  - Require a vertical hypothesis cycle: hypothesis -> implementation/diagnostic -> benchmark/measurement -> accept/reject/inconclusive -> next hypothesis.
  - Set a minimum effort bar. Default to at least 3 serious hypotheses or implementation attempts unless the user gives a different number, a candidate passes promotion gates earlier, or a stop gate blocks progress.
  - Treat "3" as a default calibration, not a law: it is enough breadth to avoid over-rejecting a broad idea after one proxy failure, while still bounded enough for one autonomous run. Use 2 for expensive or risky attempts, 4-5 for cheap diagnostics, or 1 only when the user explicitly wants one candidate.
  - Define a serious hypothesis as evidence-derived, mechanistically distinct from prior attempts, implemented or diagnostically tested, benchmarked/measured against gates, and closed with accept/reject/inconclusive evidence. Nearby threshold or weight sweeps do not count unless prior evidence specifically justifies that sweep.
  - Define candidate gates, required artifacts, and replication rules.
  - Require continuation after negative, partial, or promising results until success, research rejection, or a stop/ask gate.
  - Define research rejection narrowly: only after the minimum effort bar is met and attempted candidates fail gates.
  - Preserve stop/ask gates for missing evidence, unavailable infrastructure, contract-breaking changes, broad rewrites, exhausted nontrivial hypotheses, or decisions that need user judgment.
  - State that defaults stay unchanged unless replicated evidence passes gates and the task explicitly recommends promotion.
- For timeboxed autonomous research, the GOAL file must include a `Primary Work / Fallback Policy` section with these defaults unless the user gave different explicit rules:
  - Hygiene or fallback work is disabled unless the user explicitly allowed it for this run.
  - Do not switch away from the primary task/slice until the minimum effort bar is met: at least 3 serious hypotheses or implementation attempts, and at least 75% of the timebox spent on primary work. The attempt count is not permission to switch early.
  - After each partial, negative, or promising result, formulate the next follow-up hypothesis or implementation attempt and run it unless blocked by a listed stop gate.
  - Do not create many microtasks as a substitute for progress; task creation is not progress by itself.
  - For harness work, one task can contain multiple findings, failed attempts, follow-up attempts, and commits. Harness task explosion is not success.
  - If hygiene fallback is explicitly enabled, cap it to the final 25% of the run after the minimum effort bar is met, or require user approval before switching.
- Use **Long-Run Goal Mode** when the target run should last for hours, consume a large model budget, perform broad architecture or benchmark hardening, or avoid the early-exit failure mode. In this mode, the GOAL file must include `Hard Exit Conditions` even when no exact timebox was requested:
  - Require a P0/P1/P2 board before implementation. P0/P1 define close-blocking work; P2/stretch is optional after P0/P1.
  - Define close as all P0/P1 done, explicitly blocked, or elapsed-time gate reached with a handoff-quality checkpoint.
  - State that one useful fix, one passing smoke, or one benchmark is not enough while P0/P1 remains actionable.
  - Preserve autonomy inside the board: the target agent may choose ordering, add measurements, and do architectural work that supports the objective.
  - Require speed/performance claims to be measured. "Should be faster" is not evidence.
  - Require benchmark timing claims to be replicated (`n>=3` by default) or labelled inconclusive.
  - Require coherent commits after verified chunks unless the user says not to commit.
  - Require final accounting: P0/P1 statuses, measurements, commits, verification, benchmark paths, and unsafe/unproven claims.
- Include concise compaction-resistance wording in the generated prompt:
  - "Do not rely on memory of this prompt after compaction."
  - "The goal spec and the files it references are the durable source of truth."
- When the user requested a time limit or persistence-until-deadline behavior, include explicit instructions in the generated prompt:
  - In the generated prompt, say to follow the deadline and stop gates in the GOAL file.
  - Put detailed persistence, continuation, and final-accounting rules in the GOAL file, not the generated prompt.
- Do not write the generated prompt to a file unless the user asks. The durable GOAL file is separate from the generated prompt and should still be written.
- Do not set a goal in the current session; this skill produces the prompt for another target session. Do not mention setting a goal when the target is Claude Code.
