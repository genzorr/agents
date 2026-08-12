---
name: goal-prompt
description: Create a compact durable goal handoff for a Codex /goal session by default, or a direct Claude Code handoff when explicitly requested. Use when the user invokes goal-prompt or asks for a resumable, autonomous, research, or PRD-backed agent handoff.
---

# Goal Prompt

Create one short handoff prompt backed by one durable goal spec. Default to Codex `/goal`; target Claude Code only when the user explicitly asks for Claude.

The durable goal spec carries the real instructions and survives compaction. The generated prompt only points the target session to that spec and tells it how to start.

## Input

- Treat text after `goal-prompt` or `/goal-prompt` as seed context. Use the current conversation when it already contains a clear task.
- Ask at most three follow-up questions, and only when an answer would materially change the outcome, scope, success evidence, deadline, or stop gates.
- If the intent is too vague to define a verifiable outcome, ask one concise question and stop.
- Preserve explicit deadlines, timeboxes, persistence requirements, selected decisions, permissions, and non-goals.

## Target

- Default: Codex `/goal` bootstrap.
- Explicit Claude request: direct Claude Code prompt.
- Do not set a goal in the current session. This skill prepares another session's handoff.
- Do not change either session's model or effort. Recommendations may be recorded in the goal spec when justified, but the operator owns actual settings.

## Goal Quality And Completion Contract

Every durable goal spec must contain one integrated `Completion Contract`. Define it before authoring the other sections, and do not create a second goal-quality section that repeats it.

The contract must state:

- **Outcome:** the concrete state, behavior, decision, or artifact that must exist.
- **Evidence:** the observable proof that the outcome is real, including required commands, measurements, artifacts, or reviewed behavior.
- **Success threshold:** a meaningful quantitative threshold when the domain supports one; otherwise a clear binary or reviewed acceptance condition.
- **Boundaries:** the relevant scope, ownership, constraints, and non-goals.
- **Stop/ask gates:** user-owned decisions, missing authority, unsafe expansion, contradictory requirements, unavailable infrastructure, or material ambiguity the target agent must not silently resolve.
- **Continue conditions:** partial wins, inconclusive evidence, or remaining close-blocking work that require continued work.
- **Blocked exit:** the evidence and current state that must be recorded when progress cannot continue.
- **Evaluator integrity:** tests, metrics, and acceptance checks may be changed only when evaluator work is explicitly in scope, independently justified, and paired with replacement proof.

Repair activity-only goals such as “make progress,” “keep investigating,” or “improve X” into verifiable outcomes. If the missing outcome or validator is user-owned, ask instead of inventing it. Do not score goals numerically.

## Author The Durable Goal Spec

1. Read only the applicable project instructions, named tasks, docs, plans, ADRs, and source entry points needed to make the handoff project-specific.
2. Write the spec to a collision-resistant unique path, normally `/tmp/agent-handoffs/<repo>/<YYYYMMDD-HHMMSS>-<task-slug>-<short-id>-goal.md`. Use a new random or UUID-derived short ID for every handoff; never overwrite or reuse an earlier goal spec. For a cross-machine target, use a user-approved shared or in-repo path the target can read; never issue a handoff that points to the authoring machine's inaccessible `/tmp`. Create an in-repo spec only when the user explicitly requests or approves a durable repository artifact.
3. Add the Completion Contract to every spec. Keep a standard small task short and task-directed: objective, durable references, Completion Contract, permissions, the smallest trustworthy validation loop, and final handoff. Add recorded manual QA only when behavior cannot be proven automatically.
4. For Harness projects, use the spec as a routing index to existing task/slice/spec files. Name the task or slice the target must activate and read plus the lifecycle transitions it is authorized to perform; do not invent Harness items. For non-Harness projects, include enough context to resume after compaction.
5. Add `Expected Starting Ref` and `Material Drift Check` when the target may start or resume after the authoring worktree can change: delayed, queued, cross-machine, cross-worktree, or resumable handoffs. Omit them only for an immediate handoff to a target already anchored to the verified same checkout. Capture the exact target with `git rev-parse --show-toplevel`, `git branch --show-current`, and `git rev-parse HEAD`; do not infer it from memory. Treat a current Git `HEAD` that is neither the expected ref nor its descendant as material drift. For non-Git targets, capture a stable version or digest; stop if none can be established. Reference the drift gate from the Completion Contract, permit commits produced by the goal, and stop when a branch/worktree switch, governing-artifact change, or source/config change invalidates the stated assumptions or acceptance criteria. Record the difference and ask the operator; update the expected ref only after an explicit operator decision.
6. Add a PRD only when the work is product-shaped, architecture-shaped, benchmark-policy-shaped, cross-module, or otherwise needs a durable what/why/success contract. Duration alone does not require a PRD. The PRD states the problem, goals, non-goals, and acceptance model; keep it beside the goal spec under the same `<YYYYMMDD-HHMMSS>-<task-slug>-<short-id>` stem with a `-prd.md` suffix unless the user approves an in-repo path, then reference it from the goal spec. Tiny fixes and ordinary continuations do not need one.
7. Add a concise `Recommended Runtime` only when delegation cost, ambiguity, risk, or required thoroughness makes the recommendation useful. Keep it advisory unless the user explicitly requires a setting.
8. Add a `Final Handoff` section and require it to be durable. For Harness work, follow the existing checkpoint/review/finalize ownership and `# Last Session` / `# Outcome` shape. For non-Harness work, require objective status, changed files or commits, verification, not-landed work, blockers, and material uncertainty.

## Task-Triggered Clauses

Do not classify the task into a mode. Start with the core goal spec above and add only clauses required by explicit task facts:

- **Deadline or timebox:** record the exact deadline or duration, what must continue until then, and any permitted fallback. Do not invent fallback work or treat an attempt count as permission to stop early.
- **Evidence-directed exploration:** when the target agent must choose the next attempt from evidence, add the real problem, prior evidence, hypothesis-to-measurement loop, acceptance and rejection rules, required artifacts, and stop gates. Set a calibrated evidence bar before rejecting an approach family and require measurement for performance claims. When the task carries timing or benchmark claims, state a replication requirement, default to repeated runs for remote or noisy benchmarks, and label timing evidence inconclusive until that requirement is met. Add task-specific `Does Not Count` or `Adversarial Failure Modes` only when a credible proxy, premature-closure, evaluator-gaming, fabricated-status, or stale-state risk exists. Do not change project or benchmark defaults or promote a candidate unless the Completion Contract permits promotion and the required evidence passes its threshold.
- **Semantic fidelity:** when the task implements a source or paper, claims a behavior-preserving refactor, or transforms data whose meaning must survive, name the authoritative source or behavior, the semantics and invariants that must be preserved, and any forbidden approximation, proxy, lossy shortcut, or unsupported substitution. When a plausible shortcut could pass ordinary checks, require discriminating proof that would fail for that shortcut, such as a counterexample, differential oracle, round-trip property, or adversarial fixture. Do not add this clause when exact semantic preservation is immaterial to the requested outcome.
- **Multiple checkpoints:** name only the dependency, ownership, or verification checkpoints needed to execute safely. Do not add a P0/P1/P2 board or other long-run ceremony merely because the task may take hours.

## Frozen Experiment Protocol

When the task is governed by a frozen experiment Protocol, carry its path, `protocol`, and `protocol_sha256` plus routing and stop gates. Do not copy, regenerate, or mutate its question, baseline, commands, metrics, artifacts, gates, abort conditions, or deviation policy. Exploratory work remains exploratory until a new Protocol authorizes confirmatory work. Route completed runs through `review-experiment`; this skill does not create a Readout, ADR, or default-promotion authority.

## Output

Return exactly one `text` fenced block, plus a one-line lead-in when useful. Do not paste the goal spec into the prompt.

For Codex `/goal`:

```text
You are in <project/repo>.

Read <goal-spec path> before setting a goal. The goal spec and the files it references are the durable source of truth; do not rely on memory of this prompt after compaction.

Set a compact Codex goal that references the goal spec, preserves any deadline and stop gates from it, and then execute it. Read only the project context needed to follow the spec. Do not claim completion without the required evidence, and continue while its continue conditions remain true.

If the goal spec is materially under-specified, stop and ask before setting the goal. Otherwise work autonomously within its scope and leave the required durable final handoff.
```

For Claude Code:

```text
You are in <project/repo>.

Read <goal-spec path> first. The goal spec and the files it references are the durable source of truth; do not rely on memory of this prompt after compaction.

Follow the goal spec directly, including any deadline and stop gates it defines, and execute it. Read only the project context needed to follow the spec. Do not claim completion without the required evidence, and continue while its continue conditions remain true.

If the goal spec is materially under-specified, stop and ask before proceeding. Otherwise work autonomously within its scope and leave the required durable final handoff.
```

## Output Rules

- Always write the durable goal spec for this handoff before returning the prompt. Update only the spec already created for this same handoff.
- Keep the prompt short and put concrete paths, task IDs, constraints, verification, and task-triggered clauses in the spec.
- Do not duplicate large conversation excerpts or source files in either artifact; point to durable references.
- Preserve unresolved material questions as stop gates rather than hiding them behind assumptions.
- Do not write the generated prompt to a file unless the user asks.
