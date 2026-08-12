# Portable Protocol/Readout Contract

Contract version: **1** (`protocol_readout_contract_version: 1`)

A durable, repo-neutral contract for the portable experimental artifacts
`repos/agents` ships (Protocol, traveling Readout, baseline manifest,
experiment ledger) and how they hand off into a Harness-tracked project. It
defines the shared shape and authority split; it does not implement
`design-experiment`/`review-experiment` or the Harness Runs controller.
T-7 through T-10 (this repo, slice S-3) and Harness T-126 through T-130
(slice S-33) build against this contract instead of inventing per-repo
templates or a second scientific authority.

This contract follows the accepted product decision at
`/tmp/agent-handoffs/os/20260720-readout-area-brief-rd-prd.md`: the durable
chain is `Protocol → execution/artifacts → Readout → Area Brief impact
decision → optional ADR`, and it is not renegotiated here.

## 1. Ownership: Agents versus Harness

- **Agents** (this repo) owns portable prompting/skill behavior: the
  `design-experiment` and `review-experiment` skills, the versioned Protocol,
  baseline-manifest, and experiment-ledger templates, and `goal-prompt`/
  `prototype` composition. These artifacts must be self-contained and install
  with no Personal-OS-only path dependency.
- **Harness** (`repos/harness`, slice S-33) owns the canonical, persisted
  Readout and Area Brief schemas, storage paths, retrieval, and the
  experiment-aware Run-review fields that reference them. Harness is the sole
  place a Readout becomes canonical and mutable.
- Neither side re-implements the other's authority: Agents never persists a
  second canonical scientific record, and Harness never redefines the
  portable Protocol/Readout template shape.

## 2. Frozen Protocol identity

- A Protocol is created once by `design-experiment` and then frozen: its
  `protocol` (stable identifier) and `protocol_sha256` (content hash of the
  frozen fields) never change after freezing.
- `protocol_sha256` covers the question, baseline reference, units, metrics,
  gates, commands, artifacts, abort conditions, deviation policy, and mode
  (`exploratory` | `confirmatory` | `regression`).
- A frozen Protocol has **exactly one identity**. Any content change requires
  a new `protocol`; there is no in-place mutation of a frozen Protocol.
- A **coherent series** is the closed, Protocol-declared run set: the finite
  list of run/commit references the Protocol names as belonging to it. The
  set is closed at Protocol-freeze time (or explicitly amended only by a
  Protocol successor, never by appending to a frozen Protocol).

## 3. Flat portable fields

Both the Protocol and the traveling Readout are **flat** artifacts: field
values are scalars, strings, or flat lists — no nested graphs, no
cross-artifact object references beyond the identity/hash pairs below. This
keeps them installable, diffable, and readable without a schema-aware tool.

Protocol (frozen): `protocol`, `protocol_sha256`, `mode`, `question`,
`baseline_ref`, `units`, `metrics`, `gates`, `commands`, `artifacts`,
`abort_conditions`, `deviation_policy`, `run_set` (closed list), `created_at`.

Traveling Readout (portable, pre-canonicalization): `protocol`,
`protocol_sha256`, `runs` (the closed run set), `execution`, `observations`,
`interpretation`, `scope_and_caveats`, `reuse_do_not_repeat`,
`area_brief_disposition` (`no-change` | `update-area-brief` |
`retract-area-brief`), `adoption_disposition` (`no-adoption` |
`consider-adr` | `update-adr`), `source_artifact`, `source_sha256`,
`status`, `replaces` (optional predecessor id), and `date`. These names map
directly to the canonical Harness Readout fields; no second field vocabulary
is invented for the traveling form.

## 4. Direct write versus one-way import/freeze

- **When Harness is present**, `review-experiment` writes or validates the
  canonical project Readout **directly** at Harness's deterministic path.
  There is no intermediate traveling file to import in this path.
- **If an external traveling Readout artifact is used** (e.g. authored
  outside a Harness-tracked checkout), its only permitted transition into
  Harness is a **one-way validated import/freeze**:
  1. validate `protocol`/`protocol_sha256` against the Harness-known
     Protocol, validate the Readout schema, and compute the artifact's
     `source_sha256`;
  2. freeze the external source (it becomes read-only/historical the moment
     it is imported);
  3. create **one** canonical mutable Readout in Harness, recording
     `source_artifact`/`source_sha256` as a paired provenance reference.
- After import, the canonical Readout is the only mutable scientific record.
  The frozen external source is never re-imported, and Harness never
  maintains two independently-editable Readouts for the same Protocol
  identity.

## 5. Deterministic current-leaf resolution

Given a Protocol identity (`protocol` + `protocol_sha256`) and its closed
run set, resolving "the current Readout" must be deterministic:

- **Zero current leaves** — no canonical Readout exists yet for this
  Protocol identity: direct-write or import/freeze proceeds to create the
  first one.
- **One current leaf** — exactly one canonical Readout with no successor
  exists: it is the current Readout; direct-write/import targets it for
  clerical edits, or a correction creates its successor (§7).
- **Multiple current leaves** — more than one Readout claims to be the
  current (un-superseded) node for the same Protocol identity: this is a
  contract violation, not an ambiguity to silently resolve. The operation
  fails and requires explicit disambiguation (a missing `replaces` link,
  or two independent corrections, must be fixed before continuing).

## 6. Exact-repeat no-op

If `review-experiment` (direct-write or import) is invoked again with the
same `protocol`/`protocol_sha256`, the same closed `runs`, and content
that hashes identically to the current leaf, the operation is a **no-op**:
it resolves to the existing canonical Readout and creates no new version,
no successor, and no duplicate import record.

## 7. Mismatch rejection and corrections

- **Mismatch rejection**: if `protocol_sha256` does not match the Protocol
  Harness has on record for `protocol`, or an imported artifact's
  `source_sha256` does not match the hash recorded at freeze time, the
  operation is **rejected** outright — never merged, coerced, or silently
  overwritten.
- **Corrections create a successor, never a re-import**: a material
  reinterpretation of a canonical Readout creates a new Readout with a
  `replaces` reference to the predecessor's id (a dated correction).
  Clerical/provenance-only edits may still happen in place with ordinary Git
  history. A correction never re-runs the import/freeze path — the frozen
  external source (if any) stays frozen; the successor is authored directly
  in Harness.
- **One-way successor-only replacement, immutable predecessor**: only the
  successor carries `replaces`, pointing to the predecessor; the predecessor
  never carries a back-reference. A predecessor can have at most one
  successor, and the link is never retargeted or reversed.
  The predecessor remains immutable and retrievable as history — it is
  superseded, never deleted or rewritten — which is what keeps current-leaf
  resolution in §5 deterministic.

## 8. What process success cannot do

Successfully running `design-experiment`, `review-experiment`, a Harness Run,
or the import/freeze transition is **process success only**. On its own it:

- cannot validate the scientific content of a Readout (execution succeeding
  is not the same claim as the interpretation being correct);
- cannot mutate the singleton Area Brief for an area — an Area Brief changes
  only through its own explicit update, driven by a Readout's
  `area_brief_disposition`, never as a side effect of process completion;
  and
- cannot authorize adoption or a default change — only an ADR does that,
  driven by a Readout's `adoption_disposition`, never automatically.

## 9. Boundaries this contract preserves

- **`goal-prompt`** may carry a frozen Protocol's `protocol`/
  `protocol_sha256` and the routing/stop gates for a decision-bearing
  handoff. It restates identity and routing only — it never regenerates or
  duplicates the Protocol's scientific commitments (question, metrics,
  gates, etc.).
- **`prototype`** is feasibility-only. It never produces a confirmatory
  claim, never writes a Readout, and never touches Area Brief or adoption
  authority; escalation to real experiment work routes through
  `design-experiment`.
- **The experiment ledger** is execution/accounting state (what ran, when,
  against which Protocol) — it is never an Evidence ledger, a current-
  knowledge store, or a substitute for the Readout.
- **Legacy `E-*` Evidence lookup** remains historical/searchable only. This
  contract does not restore it to current authority, and nothing here
  triggers new Evidence promotion.
- **ADR adoption/default authority** is exclusive: only an ADR record
  authorizes adoption or a default change; no other artifact in this
  contract (Protocol, Readout, ledger, task Outcome) may do so.

## 10. Field-ownership matrix

| Field / responsibility | Owner |
|---|---|
| Protocol identity, content, freeze | `design-experiment` (Agents) |
| Frozen Protocol reference + routing/stop gates in a handoff | `goal-prompt` (Agents), reference-only |
| Feasibility exploration, no scientific claim | `prototype` (Agents) |
| Execution/accounting of what ran | experiment ledger (Agents) |
| `packet_disposition`, `process_disposition`, immutable digests, Protocol/Readout references | Harness Run review |
| `execution`, `observations`, `interpretation`, `scope_and_caveats`, `reuse_do_not_repeat`, `area_brief_disposition`, `adoption_disposition` | canonical Readout (Harness; authored via `review-experiment` when Harness is present) |
| Current interpretation for an area | Area Brief (Harness), updated only via a Readout's `area_brief_disposition` |
| Historical-only lookup | legacy `E-*` Evidence (Harness) |
| Delivery/accounting link to the Readout, no scientific content | task Outcome (Harness) |
| Adoption / default decision | ADR (Harness), exclusive authority |

## References

- Product decision: `/tmp/agent-handoffs/os/20260720-readout-area-brief-rd-prd.md`
- This repo: slice `S-3`, tasks `T-7`–`T-11`
- Harness: slice `S-33`, task `T-130` (contract-alignment counterpart to this document), and tasks `T-126`–`T-128`
