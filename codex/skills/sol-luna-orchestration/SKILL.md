---
name: sol-luna-orchestration
description: Configure Sol-led planning and review with bounded Luna implementation in ordinary Codex threads. Use only when the operator explicitly invokes sol-luna-orchestration or explicitly asks for Sol–Luna orchestration; invocation configures the current task driver and does not itself launch work.
---

# Sol–Luna Orchestration

**Composition role: lens.** The current task skill or workflow remains the driver. The active protocol or driver decides whether an implementation step may be delegated, and this lens never grants Luna authority the driver lacks. This lens changes how implementation is delegated; it does not own task lifecycle, redefine success, or launch Luna merely because it was invoked.

## Configure Only

If invoked without a resolved task and coherent implementation chunk, confirm that the lens is provisionally configured, name the planning and decomposition Sol must finish before delegation, and return without launching Luna. Activation is scoped to the task being configured and does not carry to a later task; a later task requires a fresh explicit invocation, and a provisional configuration requires a fresh invocation after the task is resolved.

## Preconditions

- The originating thread must already be running Sol. Do not change the current thread's model. If the current thread is not Sol, say so and do not silently switch it.
- Preserve the current permissions, approval policy, authorization boundaries, task scope, and no-worktree-without-operator-approval rule.
- Use ordinary Codex threads, not subagents.
- Use stable native thread behavior exposed by the running Codex product. Do not encode experimental RPC names or fabricate unsupported syntax.

## Operating Model

- Sol remains planner, decision-maker, orchestrator, reviewer, and acceptance authority.
- Luna owns one coherent bounded implementation task and its implementation-depth verification: recover authoritative contracts, inspect the full final diff and decision-bearing evidence—the artifacts or observations the delegated claim rests on—with complete coverage of non-interchangeable items and proportional depth, test plausible wrong implementations, trace failure and recovery paths, and report material uncertainty.
- Sol performs a narrow independent gate: challenge load-bearing assumptions, scientific validity when applicable, and release or GPU readiness when applicable; inspect the decision-critical subset—evidence whose observation could change acceptance—directly at proportionate depth and expand only for conflicts, unexplained gaps, or acceptance-critical uncertainty, without redoing Luna's implementation work.
- Luna's report is evidence, not acceptance. Sol accepts work only after inspecting the actual repository state, diff, and proportionate verification evidence.
- Saving Sol tokens must not weaken task definition, verification, authority boundaries, or review quality.

## Delegation Sequence

1. Sol resolves architecture, decomposition, scope, ownership, risks, stop gates, and the completion contract before delegation.
2. Do not delegate every tiny operation. Select a coherent implementation chunk Luna can investigate, implement, validate, and report without taking user-owned decisions.
3. Obtain the originating Sol thread ID from the native current-thread identity or status surface. Do not invent an ID or create a side-channel file, registry, or ledger for it. If the current driver already requires a durable checkpoint, that checkpoint may record the delegated objective and native Luna thread ID; do not create a checkpoint solely for this lens.
4. Before launch, state that the operator's explicit lens invocation requests a Luna worker and name the Luna model choice plus any intentional effort override.
5. Create a new ordinary Codex thread using Luna and send the compact worker contract below. Do not use a subagent and do not change the originating thread's model.
6. After the Luna thread is successfully started, satisfy any existing driver checkpoint requirement and immediately return a concise normal response that identifies the Luna thread and delegated objective. Do not wait, poll, repeatedly check status, or emit no-op progress messages.
7. Luna performs the local investigation required by its bounded task, implements, completes implementation-depth verification, and reports the result to the originating Sol thread ID through the native existing-thread continuation mechanism.
8. Sol reviews the actual changed state and evidence through the narrow independent gate. Inspect the targeted diff, decision-critical evidence, and material risks without repeating Luna's full investigation or routine test execution.
9. If Sol discovers a basic implementation fact Luna should have found, send the immediate correction to the same Luna thread. Classify the lesson as task-specific or reusable: carry a task-specific lesson in that thread's follow-up contract; carry a reusable lesson into later Luna worker contracts and propose a durable update to this skill or the governing project checklist. Do not silently modify durable assets without authority.
10. Send follow-up fixes for the same task to the same Luna thread so it retains context. Start a new Luna thread only for a genuinely separate task.

If the running Codex surface cannot create an ordinary Luna thread, expose the new thread ID, or send a message to the originating Sol thread ID, report the exact missing capability. Do not substitute a subagent, controller, daemon, queue, workflow script, side-channel file, or invented command.

Dispatch is not completion. The driver's task remains open and unaccepted until Sol reviews the returned work. Do not poll, but if the operator asks for status or resumes after an expected report did not arrive, perform one native status or thread-read check on the same Luna thread. Re-send the worker contract to that thread only when the check shows the thread idle or ended with no report delivered. If the check shows work in progress, report that status and do not re-send; otherwise report the stall; never launch a replacement thread silently.

## Compact Luna Worker Contract

Send only the minimum sufficient contract:

- **Objective:** the concrete bounded implementation outcome.
- **Durable references:** relevant task, spec, source, and instruction paths; point to files instead of pasting their contents.
- **Scope and ownership:** files or components Luna owns plus explicit non-goals and overlap boundaries.
- **Authority:** local write, validation, commit, push, and external-write permissions exactly as granted by the user and governing project rules.
- **Success criteria:** observable completion conditions and required artifacts.
- **Verification:** authoritative contracts Luna must recover and cite; exact or proportional checks; the expected decision-bearing evidence set, criteria for decision-critical items, proportional inspection depth, and how to report newly discovered evidence or divergence from the expected set; plausible wrong implementations the tests must distinguish; when a reviewed behavior spine applies, proof that its oracle is independent, a semantics-preserving implementation refactor remains green, a plausible production defect turns the spine red, and a detector ledger accounts for deleted or weakened tests; failure and recovery paths to trace; full-diff and evidence inspection audit; and evidence to preserve.
- **Stop/ask gates:** architecture decisions, user-owned choices, unsafe scope expansion, missing authority, unavailable infrastructure, ambiguous or conflicting evidence, or other material ambiguity Luna must escalate instead of guessing.
- **Return route:** the originating Sol thread ID and instruction to report there.
- **Return format:** outcome; changed files or commit; verification; blockers; material uncertainty; when decision-bearing evidence applies, a concise inspection summary naming scope, depth, load-bearing observations that support or weaken acceptance, limitations (including uninspected items and reasons), and any divergence from the expected evidence set.

Do not include builder reasoning, long conversation history, failed-attempt narration, or a request for hidden chain-of-thought; send no routine progress or acknowledgement messages, and send only a blocker or stop/ask escalation or the final handoff through the return route.

## Luna Worker Rules

- Recover and cite the authoritative inherited contracts before implementation; do not substitute an internally consistent interpretation for the governing definition.
- Inspect the entire final diff and the decision-bearing artifacts the delegated claim rests on, including tests and generated or configuration changes, before reporting review-ready.
- Cover each non-interchangeable decision-bearing artifact in the first pass; use sampling only for genuinely interchangeable items, state the sampling basis and limitations, inspect load-bearing items at proportional depth, add newly discovered decision-bearing evidence to the inspection summary, and report divergence from the expected set.
- Do not treat a producer's success signal, metadata, or contract checks as inspection of the decision-bearing artifact; examine the artifact itself when the claim rests on it.
- Run adversarial consequence tests that distinguish plausible wrong implementations, not only happy-path or source-shape checks.
- Reject an implementation-derived oracle: expected behavior must not come from production identifiers, generated keys, internal paths, or source shape unless that exact shape is the documented contract.
- Trace fail-closed, error, retry, and recovery behavior in proportion to the task's failure surface.
- Challenge the implementation and evidence against task nonclaims and report residual uncertainty explicitly.
- Keep changes within the delegated scope and preserve unrelated user work.
- Escalate architecture changes, contract changes, unsafe broad rewrites, missing authority, or materially different interpretations to Sol.
- Never upgrade Luna work to Sol automatically.
- Do not claim success when required evidence is missing or when the acceptance condition is only partially met.
- Report using the return format above; keep any decision-bearing inspection summary concise and omit step-by-step narration and hidden reasoning.

## Sol Token-Efficiency Rules

- Spend Sol tokens on planning, decomposition, architecture and risk decisions, worker contract quality, the narrow independent gate, and acceptance.
- Let Luna own authoritative-contract recovery, broad routine scans, line-by-line implementation, local diagnostics, adversarial verification, full-diff and first-pass evidence inspection, and test execution needed for its bounded task.
- Prefer durable paths and exact symbols over pasted source and long summaries.
- Challenge load-bearing assumptions, scientific validity, and release or GPU readiness as applicable; apply the decision-critical gate defined in the Operating Model at proportionate depth, expanding only for conflicts, unexplained gaps, or acceptance-critical uncertainty, without redoing Luna's implementation-depth verification by default.
- Do not infer oracle independence from a green suite. When a reviewed behavior spine applies and it is practical, use isolated scratch state to confirm a semantics-preserving implementation refactor remains green and a plausible production defect turns the spine red.
- Treat a basic implementation or evidence fact rediscovered by Sol as Luna-handoff feedback: correct the current task, carry reusable lessons into later worker contracts, and propose the appropriate durable checklist update.
- Do not poll or repeat “still working” messages. Luna reports back when it has a result or blocker.

## Parallel Work

Multiple Luna threads are allowed only for genuinely independent tasks with non-overlapping ownership or an explicit coordination boundary. Parallelism does not authorize Git worktrees. If safe isolation requires a worktree, stop and ask the operator.

## Normal Launch Response

After dispatch, return one concise response in this shape:

```text
Launched Luna thread <thread-id> for <bounded objective>. It will implement, validate, and report back to this Sol thread for review.
```
