# Source Distillation Contract

Use this contract when `distill-source` must turn one external source into a repo-fit adaptation
brief. It defines completeness, critical extraction, placement, and negative decisions. The skill
remains proposal-only: this contract never authorizes code, task, ADR, rule, skill, or policy changes.

## 1. Declare Scope Before Reading

A completeness claim is meaningful only against an explicit source map.

Record:

- source identity, canonical pointer, publication/version/date when available, and date read;
- requested focus and target repository or repositories;
- every in-scope structural unit that can be identified before extraction: chapters, pages in the
  declared document set, appendices, examples, guides, repository paths, or other constituent units;
- intentionally excluded units and why they are out of scope;
- access, rendering, or tooling limitations that may hide content.

Use a coverage ledger:

| Unit | In scope | Read | Accounted for in brief | Notes / limitation |
|---|---|---|---|---|
| `<section or file>` | yes/no | yes/no | yes/no | `<reason, omission, or link>` |

Do not call a distillation **complete** while any in-scope unit is unread or unaccounted for. Use one
of these explicit states:

- **complete** — every declared in-scope unit was read and accounted for;
- **bounded-complete** — every unit in a deliberately narrower declared scope was read and accounted
  for; omitted units are named;
- **partial** — one or more in-scope units could not be read or incorporated; name the gap and do not
  infer what the missing unit says.

Discovering a new structural unit of the declared source updates the source map before the verdict.
An independently linked document does not enter scope automatically; name it and ask before a
material widening of the source family or target set.

## 2. Escalate Large Single Sources Deliberately

`distill-source` normally owns one source in one context. Hand preparation to
`prepare-dynamic-workflow` when a *single* source is independently sectioned and any of these hold:

- the user requires complete coverage and the source is too large for reliable one-pass accounting;
- independent section passes or adversarial completeness checks materially reduce omission risk;
- the source must be mapped across several repositories with different authority boundaries; or
- the source contains many claims that need separate verification before synthesis.

The workflow returns one source map, section findings, a completeness critic, and one synthesized
adaptation brief. It does not change the proposal-only promotion boundary. Do not escalate merely
because a source is long when it can still be read and accounted for reliably in one context.

## 3. Extract Mechanisms, Not Just Recommendations

For each material mechanism or claim, capture:

- **Objective** — what failure, cost, or decision the source is trying to improve.
- **Mechanism** — the behavior, structure, or process that produces the effect.
- **Assumptions** — scale, stack, threat model, ownership, lifecycle, or environment it relies on.
- **Invariant** — what must remain true for the mechanism to work.
- **Tension / counterforce** — which other principle pushes back and why.
- **Conflict rule** — how the source resolves that tension, if it does.
- **Failure or misuse risk** — how literal, excessive, or misplaced adoption can backfire.
- **Evidence / lineage quality** — primary evidence, established practice, synthesis, anecdote, or
  unsupported assertion; record material uncertainty or conflict.
- **Transfer boundary** — what is explicitly non-transferable to the target setup.

Preserve source tensions instead of flattening them into a one-sided recommendation. A memorable
slogan without its stated exception or conflict rule is an incomplete extraction.

## 4. Map Existing Coverage Before Proposing Delta

Read only target-repository context relevant to the extracted mechanisms, but inspect enough to find
existing owners and avoid duplicate authority. Use this matrix for every material mechanism:

| Source mechanism | Existing owner / surface | Coverage | Gap | Delta | Enforcement layer | Risk | Validation | Route |
|---|---|---|---|---|---|---|---|---|
| `<mechanism>` | `<file, skill, ADR, interface, task, or none>` | `full / partial / none / conflicting` | `<specific missing behavior>` | `keep / reject / defer / change / add` | `<layer below>` | `<main failure mode>` | `<observable proof>` | `<owner/protocol>` |

A source idea that is already covered should normally produce **keep**, not a synonym, parallel rule,
or new skill. Partial coverage must name the exact missing behavior rather than restating the full
idea. Conflicting coverage must preserve both authorities and route the conflict for decision instead
of silently choosing one.

### Enforcement layers

Choose the lowest durable layer that reliably changes behavior:

1. no change or chat-only explanation;
2. name, type, schema, assertion, or configuration;
3. local interface, module boundary, or authoritative state owner;
4. test, executable check, lint, or validation fixture;
5. project instruction, ADR, runbook, or policy;
6. reusable skill/reference or global instruction;
7. Harness task/run/review contract;
8. new runtime or coordination mechanism — only when lower layers cannot own the invariant.

Do not default to prose when code can make the failure impossible, and do not build machinery when a
small instruction or existing interface is sufficient.

## 5. Make Negative Decisions First-Class

Every brief separates four outcomes:

- **Keep / no change** — existing behavior already covers the mechanism; cite it.
- **Reject** — incompatible, duplicative, unsupported, too costly, or harmful in this setup; state why.
- **Defer** — potentially useful but not justified yet; name the evidence or trigger that would reopen it.
- **Propose** — a concrete delta with owner, layer, risk, and validation.

A brief containing only additions has probably skipped the existing-coverage pass.

## 6. Output Contract

```markdown
# Distillation: <source title>

**Source:** <canonical pointer, version/date, date read>
**Target:** <repo(s)>
**Completeness:** <complete | bounded-complete | partial>

## 1. Source Coverage

<scope statement, coverage ledger, omissions and access limitations>

## 2. Thesis And Objective

<what the source is optimizing and its load-bearing conflict rule>

## 3. Transferable Mechanisms

### <mechanism>

- Objective:
- Mechanism:
- Assumptions:
- Invariant:
- Tension / conflict rule:
- Failure or misuse risk:
- Evidence / lineage quality:
- Transfer boundary:

## 4. Critical Assessment

<strengths, limitations, contradictions, and material uncertainty>

## 5. Existing Coverage And Fit

<required mechanism-to-owner matrix>

## 6. Keep / No-Change Decisions

<what is already correct and should remain untouched>

## 7. Rejected Or Deferred Ideas

<idea, disposition, reason, and reopen trigger for deferrals>

## 8. Proposed Changes

<smallest correct deltas, owner, enforcement layer, and sequencing>

## 9. Validation Plan

<behavior fixtures, tests, review evidence, and failure cases>

## 10. Routing

<chat-only | inbox | task | ADR | skill-lifecycle proposal | other explicit owner>

## 11. Provenance And Lifecycle

<source links, date, what becomes canonical after adoption, and when this brief becomes provenance>
```

A rendered chat brief may be shorter, but it still reports completeness, negative decisions, existing
coverage, proposed delta, validation, and routing.

## 7. Multi-Repository Ownership

When several repositories are involved:

- map each delta to exactly one owning repository or authority;
- use links or handoffs rather than copying the same policy into several places;
- distinguish cross-project governance, reusable agent behavior, project tracking, and concrete
  project implementation;
- preserve project-local truth in the project repository;
- treat a source brief as provenance after its accepted conclusions have durable homes.

Unknown ownership is a finding. Route it for decision rather than choosing the most convenient repo.

## 8. Promotion Boundary

The adaptation brief proposes. It does not:

- create, close, or mutate Harness tasks, slices, inbox items, ADRs, or Evidence;
- edit project docs, code, global rules, or skills;
- install third-party assets;
- archive the raw source as durable memory; or
- treat source authority as higher than accepted local policy.

After review, the receiving workflow performs any approved write under its own authorization and
validation rules.

## 9. Maintainer Behavior Fixtures

These scenarios are for reviewing changes to `distill-source`, not for an ordinary distillation run:

1. **Omitted middle section** — a ten-section source has section six unread. Expected: `partial`, the
   missing unit is explicit, and no complete verdict is allowed.
2. **Already covered** — the target already enforces the mechanism through an interface and test.
   Expected: `keep`; no new rule or skill is proposed.
3. **Conflicting principles** — the source presents locality and single-source-of-truth as counterforces
   with a scope-based tie-break. Expected: both principles and the tie-break survive extraction.
4. **Multi-repo mapping** — governance, reusable agent behavior, project tracking, and code belong to
   different repositories. Expected: one owner per delta and no duplicated authority.
5. **Unsupported attractive idea** — a memorable recommendation has weak evidence and large adoption
   cost. Expected: reject or defer with a reopen trigger, not automatic adoption.
6. **Proposal boundary** — the brief recommends a task and global-rule change. Expected: routing only;
   no durable write occurs inside `distill-source`.

## Completion Gate

The distillation is done when:

- every in-scope source unit is accounted for or the result is explicitly partial;
- every material mechanism has critical extraction and a target-fit row;
- keep, reject, defer, and propose outcomes were considered;
- each proposal names one owner, one enforcement layer, one concrete risk, and observable validation;
- source claims and local implications are clearly separated; and
- the brief ends at a reviewed routing proposal rather than performing promotion.
