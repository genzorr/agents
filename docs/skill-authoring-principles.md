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

## Information Hierarchy

Keep the body focused on what the agent must do now.

- Put ordered actions in `SKILL.md`.
- Put definitions, examples, variants, and long checklists in a referenced file when only some
  runs need them.
- Keep related material together. A concept's rule, caveat, and example should be near each other
  so one read loads the whole idea.
- Do not externalize material the agent needs on every run just to reduce line count.

Use a reference pointer that says when to open the file, not just what the file is called.

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
