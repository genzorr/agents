---
name: skill-lifecycle
description: Audit repo-managed skills and instruction assets for overlap, staleness, portability, or bloat and propose lifecycle decisions. Use when asked to prune skills, check for skill overlap, review process sediment, or decide whether a new skill should exist. Proposal-only: it never edits, merges, deprecates, or removes an asset.
---

# Skill Lifecycle

This is the driver for a bounded lifecycle audit. It produces evidence-backed proposals; it never mutates assets, creates tasks, installs skills, or treats a worker's audit as an implementation verdict.

1. Identify the repository that physically owns each asset before assessing it. Apply the generic policy and audit method in `docs/skill-lifecycle-policy.md`; open `docs/skill-authoring-principles.md` when judging authoring shape or composition roles. Done when every finding has the correct ownership and authority.
2. For Harness-owned `harness-*` assets, treat the Harness lifecycle policy as the project-specific overlay. Do not extend that overlay to generic assets or move physical ownership across repositories.
3. Compare responsibilities by description and body, collect cited signals, and choose exactly one lifecycle category per finding. Default thin evidence to `keep + watch`; require operator approval for merge, deprecate, or remove proposals.
4. Return the proposal format from `docs/skill-lifecycle-policy.md`. Done when each proposed change names its evidence, bounded action, content owner where relevant, and any required approval.

Do not add telemetry, daemons, schedulers, MCP/UI systems, or Harness CLI/core changes through this audit. Installation verification belongs to the accepted implementation and uses scratch homes only.
