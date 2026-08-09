# Generic Skill Lifecycle Policy and Audit Method

This traveling policy governs generic personal/global agent assets physically owned by `repos/agents`. It supplies the lifecycle thresholds, audit method, and authoring norm used by the `skill-lifecycle` platform twins. It does not transfer ownership of another repository's assets or authorize edits during an audit.

## Scope and authority

Source ownership follows physical presence. Apply this policy to Agents-owned skills, commands, subagents, rules, global instructions, and their referenced guidance; treat installed `~/.codex` and `~/.claude` content as outputs, not audit sources. The per-repository installer boundary remains defined by `docs/skill-installer-contract.md`.

Harness-owned `harness-*` assets use this policy only as generic background. Harness's lifecycle policy is the stricter project-specific overlay for those assets; it remains scoped to the Harness repository and its protocols. Other repositories retain their own source ownership and any project overlay.

## Defer-to-native ladder

Before proposing a new generic skill, choose the lowest-overhead mechanism that satisfies the recurring need.

| Tier | Mechanism | Use when |
|---|---|---|
| 1 | `AGENTS.md` / `CLAUDE.md` / rule | Always-on standing guidance needs no named invocation or decision logic. |
| 2 | Native Agent Skill | A discrete, reusable on-demand capability needs progressive disclosure. |
| 3 | Command, subagent, or workflow | Explicit invocation, a separate context, or bounded fan-out materially helps. |
| 4 | Bespoke machinery | No lower tier can express the required protocol or behavior. |

Escalate only with evidence that the lower tier failed, such as missed activation, ignored guidance, context blow-up, or a genuinely novel protocol. Defer when an existing native primitive is sufficient, when the work is a doc-shaped one-off better held in `GOAL.md` or `WORKFLOW.md`, or when a new runtime dependency would be the only justification.

## Lifecycle decisions

All decisions are recommendations. Audit workers do not edit skills, create tasks, install assets, deprecate assets, or remove assets.

| Decision | Threshold | Recommended action |
|---|---|---|
| Add | The defer-to-native ladder passes; the responsibility is distinct across both trees and related commands; the standard frontmatter and installation rules can be met. | Propose a bounded implementation task. |
| Change | A cited, concrete defect is fixable without redefining responsibility: stale path/value, machine-specific dependency, mis-firing description, or frontmatter inconsistency. | Name the exact finding and scoped edit. |
| Slim | The body restates traveling guidance, duplicates a sibling, or is longer than the behavior needs. | Propose extraction or deletion while preserving the invocation contract. |
| Merge | Description and body show shared responsibility, and one surface can absorb the other without losing a real platform-specific need. | Name the survivor and the content owner; cross-reference rather than duplicate. Operator approval required. |
| Deprecate | There is evidence of disuse, duplication, or native replacement, but dependents or an experiment make removal premature. | Propose a visible deprecation and soak window. Operator approval required. |
| Remove | A deprecation soak shows no observed use or dependents, or the asset is dead/never installed. | Propose a removal task and installer prune review. Operator approval required. |
| Keep + watch | Evidence is thin, contested, or does not meet another threshold. | Record the uncertainty; do not manufacture a change. |

Never infer disuse from silence: there is no per-skill invocation telemetry. Confident deprecation or removal based on use needs operator confirmation or bounded observed evidence.

## Audit method

Compare descriptions and bodies, never names alone. Audit the owned skill trees, related commands/subagents/rules, tracked instruction files, README guidance, and referenced traveling documents. Do not read private session logs or live installed homes merely to infer use.

Collect these signals for each finding: observed use or references; packet, handoff, or review failures; duplicated responsibility; stale instructions and machine-specific paths; operator friction; frontmatter activation quality; load cost; native replacement; and installation implications. Cite the source for every material signal.

Check twin behavior semantically: same-name Codex and Claude skills are counterparts, not automatically identical files. Presence gaps, metadata differences, or platform-specific framing are defects only when behavior needs both platforms and the difference is unexplained. Never pad a lean twin or merge a legitimate platform distinction for symmetry.

Treat composition-role hazards as `Change`: a driver framed as a lens, a lens taking lifecycle ownership, or two surfaces claiming one driver role. Apply the role precedence in `docs/skill-authoring-principles.md`: `protocol > driver > router > helper > lens`; a lens may add checks but never relax a protocol.

## Claim breadth audit

When a lifecycle finding would turn finite observations into reusable behavior, open `docs/claim-discipline.md` before choosing its scope. Check evidence lineages, tested and incidental conditions, alternatives, counterevidence, target cases, guardrail cases, and explicit non-claims. Thin evidence should produce a narrow rule or `keep + watch`, not a provider-independent, cross-project, family-wide, or global claim; this method never weakens safety, authorization, or acceptance boundaries.

Treat process sediment as a proposal to capture or trim, never an automatic deletion. A candidate needs both the obsolete artifact and a cited durable replacement such as an ADR, Evidence, task outcome, or canonical board. If no durable record exists, propose capture instead of removal.

## Authoring norm

Use `docs/skill-authoring-principles.md` when creating, changing, or slimming an asset. Keep every skill small as correct, self-contained after installation, progressively disclosed, and composable with a clear role. Retain core trigger, boundaries, procedure, output contract, guardrails, and verification; move only genuinely conditional heavy material into an explicit traveling reference.

Use repo-relative `docs/*.md` references for shared material that must travel; the installers copy resolved references into the scratch install home. A hard-coded user-home dependency, including `/Users/alice`, `/home/alice`, or `C:\Users\alice`, is a packaging defect. An illustrative user-home path must be labelled `example-only` on that same line. A portable `~`, `$HOME`, or `${HOME}` location is allowed only when labelled `runtime-home` on that same line; use it only for a real installed-home/cache/runtime location, never to disguise a source dependency.

## Proposal output

```markdown
## Skill lifecycle proposals

1. <asset> — <add | change | slim | merge | deprecate | remove | keep + watch>
   Evidence: <cited descriptions, bodies, paths, line counts, durable records, or observed use>
   Proposed action: <bounded next action; for merge name survivor and content owner>
   Approval: <operator approval required for merge, deprecate, or remove; otherwise none>

Authoring-norm violations:
- <asset> — <not self-contained / duplicated traveling guidance / role hazard / unnecessary load>
```

Lead with the highest-confidence, highest-payoff findings. An accepted implementation, not this audit, owns static validation and scratch-home `install-claude.sh` / `install-codex.sh --dry-run --diff` plus the relevant prune review.
