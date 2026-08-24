---
name: text-prune
description: Compress, tighten, deduplicate, consolidate, or remove obsolete material from bounded text while preserving its live information and structure. Use when text pruning is the requested task; do not use merely because another task writes text, for skill lifecycle decisions, or for installed-asset pruning.
---

# Text Prune

Use this skill as the driver when pruning text is the whole request. When another driver or protocol invokes it for a bounded transformation, act as a helper: return the transformed text, ledger, flags, and validation evidence without taking authorization, verification, lifecycle, or completion ownership from the caller.

## Routing and authority

- Handle text supplied by the user or bounded files placed in scope. Edit files only when the request authorizes edits, and follow the repository's source-of-truth, formatting, and verification rules.
- Route decisions to add, change, slim, merge, deprecate, remove, or keep an instruction asset to `skill-lifecycle`. Perform an authorized textual slimming only after that decision; do not make it here.
- Route pruning or uninstalling materialized assets to the owning installer contract. Installed `~/.codex` (runtime-home), `~/.claude` (runtime-home), and other installer-owned runtime copies are outputs: refuse direct edits and redirect to the repository that physically owns the source.
- Keep `doc-audit` audit-only and `review-change` independent. Their findings may be inputs, but this skill does not absorb their authority.

## Workflow

1. Establish the bounded target, audience, authority, output form, edit permission, and mode. Done when every input and permitted output is named.
2. Read the complete bounded input before deleting or consolidating anything. For a document set, identify the canonical owner of each repeated fact or policy. Done when no in-scope section is uninspected.
3. Open only the applicable mode reference, then classify each affected content unit as `KEEP`, `TIGHTEN`, `REMOVE`, `CONSOLIDATE`, or `FLAG`. When apparent repetition may be duplication, sediment, a no-op, or sprawl, use `docs/skill-authoring-principles.md` as the canonical definitions. Done when every contemplated deletion has a classification and uncertain material is `FLAG` rather than guessed away.
4. Produce the smallest clear result that preserves live information and required structure. Do not target a fixed reduction ratio. A no-op is successful when further compression would remove decision-relevant information.
5. Validate the result against the original plus the selected mode's semantic and structural protections. When files change, inspect the surgical diff and run proportionate checks.
6. Return the transformed text or edited paths. Ordinary low-risk prose needs only the result; durable, evidentiary, instruction-bearing, or materially pruned text also needs a compact removal/consolidation ledger and unresolved flags.

## Modes

- Plain prose: open [references/plain-prose.md](references/plain-prose.md) for messages, essays, emails, proposals, or general explanation.
- Evidence-bearing report: open [references/evidence-bearing-report.md](references/evidence-bearing-report.md) for research, reviews, audits, incident summaries, experiment readouts, or decision documents.
- Durable documentation: open [references/durable-documentation.md](references/durable-documentation.md) for README, architecture, operational, policy, ADR-adjacent, or linked documentation.
- Instructions and prompts: open [references/instructions-and-prompts.md](references/instructions-and-prompts.md) for AGENTS.md, CLAUDE.md, rules, skills, workflows, handoffs, or prompts.
- Code comments and docstrings: open [references/code-comments-and-docstrings.md](references/code-comments-and-docstrings.md) for comments, embedded API documentation, directives, annotations, or docstrings. Do not edit executable behavior.

## Output claim

Describe the result as information-preserving under the stated checks, never as unconditionally lossless. For each durable or high-risk removal or consolidation, record the affected location or content unit, classification, reason, retained authority or replacement when applicable, affected consumer when one changed, and any validation limitation. Leave `FLAG` content unchanged until the user or owning authority resolves it. The normal diff is additional review evidence, not a substitute for the ledger when the ledger is required.
