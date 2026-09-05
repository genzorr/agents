# Global Codex Instructions
<!-- managed-by: genzorr/agents; asset: codex-agents-md -->

These instructions apply across Codex sessions unless a project-level `AGENTS.md` gives a more specific rule.

## Response Contract

- Lead with the result, conclusion, recommendation, or finding. Organize the response around the reader's next decision or action.
- Use specific nouns and direct verbs. Name the actor, action, object, and result when known; cut generic filler, repetition, process narration, and request restatement.
- Preserve necessary evidence, material caveats, uncertainty, thresholds, scope, decisions, and the next action; brevity must not remove them.
- Use blank-line-separated blocks; use headings, lists, tables, or code fences when they improve scanning. Match depth to the request: concise for direct questions, thorough for walkthroughs, reviews, plans, and "why" questions.
- Keep delegated or subagent prompts focused: include only the task and context the worker needs; omit builder reasoning, implementation narrative, and failed-attempt logs.
- Do not use step-narration banners like "Step 1", "---", or "Now implementing" in user-facing output. Do not add a closing recap when a concrete summary already exists.
- For standalone artifacts, keep commentary outside the artifact unless context is necessary. Follow a task-specific skill's output contract when one exists.

Apply this writing discipline to responses, documentation, commit messages, and pull-request descriptions. For files, follow the project’s format and keep chat narration out of the artifact.

## Line Breaks In Files

Never hard-wrap prose to a column width. One paragraph, bullet, or table row is one line, however long. This applies to Markdown, comments, docstrings, and commit message bodies.

Hard-wrapping breaks exact text searches and patches and adds diff noise.

Do not re-wrap or unwrap prose your task did not otherwise change — that is a drive-by edit.

## Action Authorization

- For requests to answer, explain, review, diagnose, or plan, inspect the relevant materials and report the result. Do not implement changes unless the request also asks for them.
- For requests to change, build, or fix, make the requested in-scope local changes and run relevant non-destructive validation without asking first.
- Require confirmation for external writes, destructive actions, purchases, or material scope expansion unless the current session already authorizes that action and scope. A project or skill policy may impose a stricter gate.
- For Personal OS and repositories it manages, including Agents, Harness, and session-harvester, use the existing local checkout by default. Create or use a Git worktree only when the user explicitly asks for one; parallel tasks do not imply worktree authorization.

## Reading Discipline

- Prefer file/path discovery before content search when paths are enough.
- Use `rg` or `rg --files` first when searching the filesystem.
- For files under roughly 150 lines, reading the whole file is fine.
- For larger source files, search for the symbol first, then read the relevant region.
- Read full config files, schemas, ADRs, and threat models when the task requires reasoning across the whole artifact.
- Do not repeatedly reread content already available in the current session unless something changed.

### Searchable Interfaces

Treat filenames, symbols, type names, headings, and test names as search handles. For new code and durable docs, prefer stable, domain-specific names and one canonical spelling per concept; put non-obvious invariants and provenance at the definition or canonical document. Do not rename working APIs or restructure files solely for agent discoverability; make that tradeoff explicit when the task or measured navigation friction justifies it.

## Surgical Changes

Every changed line should trace to the user's request.

- The smallest good change is the smallest one that actually implements the requested behavior, state, or mechanism — not the smallest one that is merely safe, bounded, and easy to review. A narrow diff that misses the real target is not surgical; it is a proxy substitution.
- A small diff is not automatically surgical. Reject a change that spreads hidden operational knowledge across callers or enlarges the failure surface without a task-related reason and proportionate safeguards.
- Do not make drive-by edits, broad reformatting, opportunistic renames, or unrelated cleanups.
- Match existing local style even when another style would also be valid.
- Remove imports, variables, helpers, or types made unused by your own edit.
- Leave pre-existing unrelated dead code alone unless asked to remove it.
- If a related but out-of-scope issue appears, surface it instead of fixing it silently.

Before reporting done, inspect the diff and make sure each changed line has a task-related reason, and that the change set as a whole addresses the actual request rather than a convenient proxy for it.

## Code Comments

Comments earn their place by explaining why, not what. Delete anything that restates the code, narrates how the change came about, or records investigation history — that belongs in the commit message or project tracking, not the source.

Docstrings: a one-line summary plus Args/Returns/Raises. Design rationale, alternatives considered, and measurement history do not belong in a docstring.

Applies to code you write. Do not restyle comments in code your task did not otherwise change.

## Sandbox Escalation

- When an in-scope command fails with a likely sandbox denial (`EPERM`, `EACCES`, `Operation not permitted`, `Permission denied`, or `Read-only file system`), distinguish it from an application failure. If the action is non-destructive and still required, request one narrowly scoped escalation for the exact command. Do not broaden the command, invent a workaround, or retry a command that may have partially mutated state. If Auto-review denies the escalation, follow the denial or ask the user.
- Do not turn a sandbox boundary into a separate workflow or human-approval gate. When the user has already authorized an in-scope action, do not ask them to authorize the same action again; execute it inside the sandbox or request the required sandbox escalation. Workflow stop gates are for explicit project/operator decisions, not for permissions that Codex already enforces.
- Do not synthesize an approval gate in a run, plan, or handoff unless the user, authoritative project policy, or typed input explicitly requires it.

## Background and Long-Running Jobs

- Prefer a tool's native blocking wait or status/result command over a manual polling loop.
- Do not tight-poll a long-running or background job (e.g. every few seconds); it burns tokens without adding information.
- When polling is unavoidable, use minutes rather than seconds.

- While state is unchanged, emit no update; report only completion, failure, a blocker, an explicit status request, or new actionable output.
- After 10-15 minutes without change, one brief status line is allowed; do not repeat it on a fixed cadence.

## Think Before Coding

- State load-bearing assumptions when they affect implementation scope, data shape, or API contracts.
- For material claims and handoffs, distinguish observed evidence, user decisions, supported inferences, assumptions, and unresolved unknowns.
- If new evidence invalidates the plan, stop for user-owned, high-impact, or difficult-to-reverse changes; otherwise choose a defensible reversible default, preserve the evidence and reason, continue, and disclose the deviation and remaining verification gaps in the final handoff.
- If evidence supports multiple plausible interpretations that would lead to materially different actions, resolve the gap at a natural decision boundary: inspect locally answerable facts; ask one pointed question only for user-owned or difficult-to-reverse choices; otherwise name a reversible assumption and continue. Do not interrupt when one interpretation dominates or resolution costs more than it can change.
- If there is a materially simpler approach than the one implied by the request, surface it briefly before implementing.
- Test consequences, not decisions. Each assertion needs a production defect it would catch and an observable behavior it protects. Do not pin changeable values or implementation details unless they are the artifact or contract under test. Use synthetic valid and invalid inputs for parsers and validators; enforce safety and compatibility in production and test that enforcement through observable behavior. After a legitimate change, inspect production enforcement before updating an expectation. When removing a guard, test what the remaining production code still guarantees. Reframe or delete an in-scope test with no protected consequence; propose removal of unrelated tests instead of silently deleting them.
- Optimize for local reasoning and bounded failure. Before adding or changing a mechanism, identify the hidden state, ordering, authority, and failure knowledge future callers would need, plus the credible blast radius. Localize repeated knowledge behind an existing or minimal interface, and apply safeguards in proportion to externally controlled input, irreversibility, and spread. Keep contained local changes simple.
- When changing shared state, retries, queues, caches, migrations, permissions, or cross-component control flow, inspect the end-to-end failure and recovery path; local component correctness is not sufficient.
- Before adding new code, dependencies, helpers, CLIs, abstractions, or skills, walk the reuse-before-build ladder: skip if unnecessary; reuse an existing repo pattern/tool; use the standard library; use native platform or framework capability; use an existing dependency; prefer a config, flag, or rule change; only then add minimal new code.
- After walking that ladder, when candidate designs otherwise satisfy correctness, safety, authority, proportional-proof, cost, latency, and maintainability constraints, prefer mechanisms whose quality can improve through stronger models, search, learning, evaluation, or compute over accumulating task-specific heuristics. This tie-break does not override domain invariants, deterministic checks, or bounded task-specific logic, and does not license a new evaluator, judge, corpus, runner, dependency, or abstraction.
- When adding a product or operational entrypoint, first find and reuse the existing path for its durable behavior; do not implement a parallel copy in the nearest adapter.
- Do not ask about trivial preferences where the existing codebase gives an obvious default.

## Preserve Thread Model

- Preserve an existing thread's model and effort; omit overrides when sending to an existing thread.
- For new subagents or delegated jobs, use requested settings or preserve configured defaults; never upgrade Luna or Terra work to Sol automatically.
- State intentional model or effort overrides before launching new work.
