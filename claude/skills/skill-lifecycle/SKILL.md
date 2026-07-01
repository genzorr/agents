---
name: skill-lifecycle
description: Audit the repo-managed skill catalog and process docs against an overlap/staleness/sediment rubric and propose consolidate/slim/merge/deprecate/remove actions, plus the small/self-contained/composable authoring norm new skills must follow. Use when asked to prune skills, check for skill overlap or bloat, find stale process docs, or decide whether a new skill should exist. Propose-only — it never edits, merges, or deletes a skill.
---

# Skill Lifecycle

The invocable front door to the skill lifecycle policy. It **audits and proposes** — it
never edits, merges, deprecates, or deletes a skill or doc. Whole-skill merge/delete is a
reviewed action gated on operator approval; the bounded execution of accepted proposals is a
separate implementation task.

`docs/harness-skill-lifecycle-policy.md` is the decision policy (defer-to-native ladder; add /
change / merge / deprecate / remove gates; Codex/Claude ownership rules) and
`docs/harness-skill-audit.md` is its audit method (signals, categories, thresholds). This skill
runs that policy on demand and emits proposals — it does not restate the gates; read those docs
for the exact thresholds.

## Authoring norm (small / self-contained / composable / progressively disclosed)

Every new or edited skill must follow this norm; proposals to slim are measured against it.

- **Small — as small as correct.** One responsibility, one clear invocation boundary. Not
  uniformly tiny: keep the guardrails, the verification steps, and anything a fresh agent could
  not infer. Cut filler, restated policy, and duplicated context.
- **Self-contained.** Co-locate what the skill needs, or reference a doc that **travels on
  install** (the installers copy `docs/<name>.md` paths a skill references into the install
  tree). A reference that only resolves from a dev checkout is a packaging bug.
- **Progressively disclosed.** The `description` is always loaded; the `SKILL.md` body loads when
  the skill runs; a referenced file loads only when the model opens it. So when a skill has a short
  always-needed core plus a heavy block needed only sometimes (a large output template, long
  examples), keep the core in `SKILL.md` and move the heavy block to a file the body points to —
  alongside the skill for 1:1 content, a shared `docs/` file only when several skills repeat the
  same material. Keep twins semantically aligned, not file-shape identical: never pad an
  already-lean twin for symmetry. The same shape applies to commands and agent definitions. Full
  convention: `docs/harness-skill-lifecycle-policy.md` §8.
- **Composable.** Reference or hand off to other skills instead of duplicating their logic
  (e.g. delegate diff critique to `/review-change`, task creation to `/harness-add-tasks`). Name
  the skill; do not inline its body.

## What to audit

Scope is the repo-managed instruction surface, not project code:

- `codex/skills/` and `claude/skills/` skill bodies + frontmatter (both trees).
- `claude/commands/`, `claude/agents/`, `claude/rules/`.
- Installed/project instruction docs: `AGENTS.md`, tracked `.claude/CLAUDE.md`, READMEs, and the
  referenced `docs/` guides.

## Overlap / staleness rubric (skills, commands, rules)

Compare by description **and** body, never by name alone. Propose one category per finding:

- **Slim** — body far longer than correct, restates policy that lives in a traveling doc, or
  duplicates a sibling tree's content verbatim → propose extraction + thin reference. (This is
  the common case and the bounded slimming pass executes accepted slim proposals.)
- **Merge** — two surfaces share responsibility and one can absorb the other without losing a
  platform-specific need → name the survivor and the content owner (one owns the concept, the
  other cross-references). Do not merge across trees when the platform framing legitimately
  differs.
- **Change** — a concrete cited defect fixable without redefining the skill: stale repo path,
  hardcoded machine-specific path, mis-firing description, twin-frontmatter drift.
- **Deprecate → remove** — disuse, duplication, or replacement by a model-native mechanism.
  Harness has no per-skill invocation telemetry, so disuse-based deprecate/remove needs operator
  confirmation; never infer it. Removal is never automatic.
- **Keep + watch** — thin or contested evidence. The default when a finding is not strong.

## Process-sediment rubric (docs)

Old process artifacts should not masquerade as current truth (destination over journey): the
durable record — an ADR, Evidence (`E-N`), a task `# Outcome`, or the canonical board (see
`docs/harness-knowledge-homes.md` for where each lives) — is the truth; the artifact that
produced it is provenance. **Flag, do not delete.** Candidates:

- A PRD/design doc whose decisions have shipped and are now captured in a durable record, with no
  skill/doc referencing it as live guidance → propose archive/trim, citing the superseding record.
- Scratch left in the tree: `GOAL.md`, `WORKFLOW.md`, prompts, logs, generated output.
- Superseded run docs under `docs/harness/ops/<run>/` that no live guidance references.

A flag must cite both the artifact and the durable record that now supersedes it. If no durable
record exists, the artifact is not sediment — it is the only copy; propose capture, not removal.

## Should this skill exist at all?

Before proposing a *new* skill, walk the defer-to-native ladder in the policy doc: standing
guidance → AGENTS.md/CLAUDE.md; a doc-shaped one-off → a `GOAL.md`/`WORKFLOW.md`; a discrete
on-demand capability → a skill; explicit invocation / fresh context / fan-out → command /
subagent / workflow. Add a skill only when no lower tier suffices and its responsibility is
distinct from every existing surface in both trees.

## Output: proposals

Audit-only. Emit a ranked proposal list; do not touch any file.

```markdown
## Skill lifecycle proposals

1. <skill/doc> — <slim | merge | change | deprecate | remove | keep+watch | new-skill>
   Evidence: <description+body overlap, line count, stale path, superseding record — be concrete>
   Proposed action: <what to do; for merge name survivor + content owner; for remove name the soak>
   Approval: <"operator approval required" for any merge/remove/deprecate>

Authoring-norm violations:
- <skill> — <restates traveling-doc policy / not self-contained / duplicates sibling tree>
```

Lead with the highest-confidence, highest-payoff findings. State install verification belongs to
whoever executes an accepted proposal (`install-claude.sh`/`install-codex.sh --dry-run --diff` +
`--prune` review), not to this audit.

## Guardrails

- Propose only. Never edit, merge, deprecate, or delete a skill or doc here.
- Any merge/remove/deprecate is gated on operator approval and a reviewed proposal.
- Keep `claude/` and `codex/` parity in view: dual skills must stay name-aligned; flag drift.
- No daemons, schedulers, MCP, UI, telemetry subsystem, or `harness-core`/CLI/Python changes.
