# Skill Authoring Principles

Use this as the craft rubric when creating, reviewing, or slimming repo-managed skills.
`skill-creator` owns the mechanics of making a skill. `skill-lifecycle` owns the policy and
audit gates. This document names the smaller writing decisions that make a skill predictable.

## Core Test

A skill should make the agent follow the same process across runs, even when the outputs differ.
Prefer instructions that change behavior over explanations that merely sound true.

Ask of each line:

- Does this line change what the agent will do?
- Is this information needed every time the skill runs?
- Is this meaning already stated somewhere else?
- Can the agent tell when this step is complete?

## Invocation

Choose invocation deliberately.

- A model-invoked skill pays always-on description cost. Use it only when the agent must discover
  the skill without the user naming it, or when another skill should be able to route to it.
- A user-invoked skill pays human memory cost. Use it when the operator should make the choice
  explicitly and autonomous triggering would add noise.
- If user-invoked skills become hard to remember, prefer one small router skill over many
  overlapping descriptions.

For model-invoked descriptions:

- Front-load the leading term users and project docs already use.
- Include one trigger per real branch, not several synonyms for the same branch.
- Keep body-only identity out of the description. The description is for discovery.

## Composition Roles

Skills compose. Name the role a skill plays when combined with others, so an agent running
several at once knows which one is in charge.

- **Driver** — owns a task or workflow end to end: plans, sequences, and decides when it is
  done. Exactly one skill drives at a time.
- **Router** — selects the right skill or path and hands off. It does not own execution after
  the handoff; the skill it selects becomes the driver.
- **Lens** — adds checks, questions, or quality criteria to whatever the driver is doing. It
  never takes lifecycle ownership and never relaxes a protocol.
- **Helper** — performs one bounded sub-step on request (create a task, critique a diff, run a
  search) and returns. The caller stays the driver.
- **Protocol** — a strict rule set that must hold regardless of what else runs (task-backed
  implementation, ledgers, review gates). It is authoritative; other roles work within it.

Precedence when roles combine: **protocol > driver > router > helper > lens.** Exactly one
skill drives unless a router is actively selecting and handing off. Lenses and helpers compose
freely with the driver, but lens guidance may only add checks or questions — it must not relax
a protocol or take lifecycle ownership. When a lens and a protocol disagree, the protocol wins.

## Orchestration Discipline

When a driver delegates work to other agents (subagents, headless jobs, run packets), it stays
the orchestrator and owns the outcome. This is different from a router: a router owns selection
only until it hands off to the selected driver. Apply this discipline whenever a driver delegates
to a worker agent.

- **Worker output is evidence, not a verdict.** The orchestrator owns acceptance: verify the
  actual result — diff, files changed, checks re-run — never a worker's self-report.
- **Every delegation prompt carries its contract:** objective, scope and ownership, permissions
  (read-only vs. write, commit/lifecycle authority), success criteria, required proof, and
  return format. A prompt missing any of these under-specifies the work.
- **Broad discovery narrows into an exact follow-up.** A scout or survey result is an input to
  a specific next action, not a finish line.
- **Launching is not finishing.** Orchestration is incomplete while a worker is merely running;
  it completes only when the returned work is reviewed, accepted, and integrated.

## Information Hierarchy

Keep the body focused on what the agent must do now.

- Put ordered actions in `SKILL.md`.
- Put definitions, examples, variants, and long checklists in a referenced file when only some
  runs need them.
- Keep related material together. A concept's rule, caveat, and example should be near each other
  so one read loads the whole idea.
- Do not externalize material the agent needs on every run just to reduce line count.

Use a reference pointer that says when to open the file, not just what the file is called.

## Claim breadth

When finite observations are being turned into reusable skill behavior, conditionally open the Agents-owned `docs/claim-discipline.md` reference. First choose the least restrictive behavior that remains correct for the supported cases and required safety/authority boundaries. Then express that behavior as compactly as possible. Textual brevity is an encoding objective, not a generalization objective. Keep the resulting instruction non-vacuous: it needs a real trigger, required behavior, observable output or stop condition, and applicable boundaries.

## Completion Criteria

Every ordered step should end with a clear completion criterion. Good criteria are observable and
demand enough legwork.

Prefer:

- "Done when every modified model has a migration, test, or explicit no-op reason."
- "Done when the generated script passes syntax validation and every captured value has a target."

Avoid:

- "Understand the code."
- "Produce a summary."
- "Make it better."

Weak criteria invite premature completion: the agent moves to the next visible step before the
current one is actually finished. Sharpen the criterion before splitting the skill.

## Proportional Behavior Proof

Match proof to the changed behavior and the claim it must support; do not make every skill edit pay for an evaluation suite.

- **Static contract proof** — use existing deterministic validators for packaging, references, metadata, syntax, exact structural invariants, and other mechanically decidable changes. This supports only those properties.
- **Behavioral conformance proof** — when a change alters invocation, routing, authority, stop conditions, completion behavior, or another semantic contract, exercise the smallest representative cases through the same skill interface callers use. Prefer an observed material failure as a regression case; create a persistent fixture without one only when repeated demonstrated need justifies its upkeep.
- **Outcome proof** — a curated conformance pass does not establish general task improvement, stable triggering, lower rework, or safe additional autonomy. A claim that would change a default or authority boundary belongs in the existing [`design-experiment` → `review-experiment` Protocol/Readout workflow](experiment-protocol-readout-contract.md), with a baseline and decision-relevant evidence.

Do not add a runner, judge, schema, repeated-trial ritual, or standing case corpus until concrete repeated work shows that a shared mechanism would remove more complexity than it adds.

## Leading Terms

Use compact, established terms when they carry real behavior. A good leading term compresses a
larger idea and gives the agent a stable handle for the behavior.

Good terms are already used by the project, by the domain, or by common engineering practice.
Do not coin vocabulary unless the term earns its definition cost.

## Pruning

Keep one source of truth for each meaning.

- Duplication is the same meaning in more than one place. It costs tokens, maintenance, and
  overweights the idea.
- Sediment is old content that remains because removing it feels risky. Prefer the durable record:
  ADR, task outcome, evidence, or canonical board state.
- A no-op is an instruction that does not change model behavior. Delete it instead of polishing it.
- Sprawl is length that is live but hard to use. Fix it with progressive disclosure or a real
  sequence split.

## Attribution

Some vocabulary in this rubric is adapted from Matt Pocock's `writing-great-skills` skill in
`mattpocock/skills`, licensed MIT. Copyright (c) 2026 Matt Pocock.
