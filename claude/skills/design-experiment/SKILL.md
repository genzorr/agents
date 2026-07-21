---
name: design-experiment
description: Freeze an experiment Protocol (question, baseline, units, metrics, gates, commands, artifacts, abort conditions, deviation policy) before anything runs, and distinguish exploratory, confirmatory, and regression commitments. Use when the user asks to design an experiment, invokes design-experiment or /design-experiment, wants to freeze a Protocol before running or comparing against a baseline, or needs a portable Protocol identity ahead of execution.
---

# Design Experiment

Freeze the scientific contract for one experiment before anything runs. This skill produces exactly one thing: a frozen Protocol, its baseline manifest, and an initialized experiment-ledger entry. It never runs the experiment, never interprets results, never writes a Readout, never changes an Area Brief, and never authorizes adoption — see Boundaries.

This skill implements the portable Protocol contract. The full versioned contract (including the traveling Readout, review-experiment, and Harness handoff) lives at `docs/experiment-protocol-readout-contract.md` in the `agents` source repo; the rules that govern *this* skill are restated below so the installed skill is self-contained.

## Contract this skill freezes

A Protocol is created once and then frozen — never mutated in place:

- **Frozen fields:** `protocol`, `protocol_sha256`, `mode`, `question`, `baseline_ref`, `units`, `metrics`, `gates`, `commands`, `artifacts`, `abort_conditions`, `deviation_policy`, `run_set` (closed list), `created_at`.
- **`protocol_sha256` covers exactly:** `mode`, `question`, `baseline_ref`, `units`, `metrics`, `gates`, `commands`, `artifacts`, `abort_conditions`, `deviation_policy` — in that order. It does **not** cover `protocol`, `run_set`, or `created_at`.
- **One identity, no in-place mutation.** Any change to a frozen field requires a new `protocol` id from a fresh design-experiment run. There is no edit-in-place of a frozen Protocol.
- **`run_set` is closed at freeze time.** It is the finite list of run/commit references this Protocol declares as belonging to it. It may only be amended by a Protocol successor, never by appending to a frozen Protocol.
- All fields are flat — scalars, strings, or flat lists. No nested objects, no cross-artifact graphs.

## Modes

Pick exactly one `mode` and hold the Protocol to it:

- **exploratory** — no confirmatory claim is being made. Gates may be informative rather than pass/fail. Say so explicitly in `deviation_policy` so a later reader cannot mistake this for a confirmatory result.
- **confirmatory** — the Protocol commits to a specific, falsifiable claim against the baseline. `gates` must be exact pass/fail thresholds decided *before* any run, not chosen after seeing data.
- **regression** — the Protocol commits to holding an existing metric steady against `baseline_ref`. `gates` are non-regression thresholds (e.g. "no worse than baseline by X").

If the user's request doesn't make the mode obvious, ask one concise question naming the three options rather than guessing.

## Steps

1. **Determine mode.** exploratory, confirmatory, or regression (see above). This drives how strict `gates` must be.
2. **Gather each frozen field in `templates/protocol.md`**, one at a time. Do not accept a field as complete until it is concrete enough that a different agent could execute `commands` and check `gates` without asking a follow-up question:
   - `question` — the one question this experiment answers.
   - `baseline_ref` — the stable id of a `templates/baseline-manifest.md` instance (create it — see step 5 — before finishing this field).
   - `units` — the unit(s) of measurement/analysis.
   - `metrics` — exact metric names this Protocol reports.
   - `gates` — one exact pass/fail (or non-regression) threshold per metric or decision.
   - `commands` — exact commands that produce the metrics and artifacts. Freeze these; do not run them here.
   - `artifacts` — output paths/files the commands must produce.
   - `abort_conditions` — conditions that stop execution early.
   - `deviation_policy` — what counts as an allowed deviation during execution versus what forces a new Protocol.
3. **Assign `run_set`.** The closed list of run/commit references this Protocol declares as belonging to it. An empty list is valid at freeze time if runs haven't been scheduled yet, but the list itself is still closed — it is not appended to later; a Protocol successor is created instead.
4. **Compute `protocol_sha256`.** Build the canonical object below in this exact key order, serialize with no extra whitespace, and hash it. Run this via a shell tool — do not hand-compute the digest:

   ```
   python3 - <<'PY'
   import hashlib, json

   fields = {
       "mode": "<mode>",
       "question": "<question>",
       "baseline_ref": "<baseline_ref>",
       "units": ["<unit>", "..."],
       "metrics": ["<metric>", "..."],
       "gates": ["<gate>", "..."],
       "commands": ["<command>", "..."],
       "artifacts": ["<artifact>", "..."],
       "abort_conditions": ["<condition>", "..."],
       "deviation_policy": "<deviation_policy>",
   }
   canonical = json.dumps(fields, ensure_ascii=False, separators=(",", ":"))
   print(hashlib.sha256(canonical.encode("utf-8")).hexdigest())
   PY
   ```

   This recipe is fixed on purpose: any agent (Codex or Claude) that fills in the same field values and runs this exact script produces the same `protocol_sha256`, which is what makes the two runtimes' Protocols interoperable.
5. **Assign `protocol`.** Use `<kebab-slug>-<YYYYMMDD>-<first 8 hex chars of protocol_sha256>`. This is a convention, not a contract requirement, but it keeps the id human-readable and guarantees it changes whenever content changes even if a step is skipped.
6. **Write the baseline manifest** from `templates/baseline-manifest.md` (before or alongside step 2's `baseline_ref`, whichever the user has ready first): what the baseline is, its source reference, the metrics measured at baseline, how to reproduce it, and known caveats.
7. **Initialize the experiment ledger** from `templates/experiment-ledger.md`: one row per `run_set` entry (or a single `planned` placeholder row if `run_set` is still empty), recording `protocol` and `protocol_sha256`.
8. **Report the frozen identity** to the user: `protocol`, `protocol_sha256`, `mode`, and the paths of the three artifacts written.

## Boundaries

- Never execute the Protocol's `commands` or run the experiment.
- Never interpret metrics against `gates` or draw a conclusion — that is `review-experiment`'s job, not this skill's.
- Never write or update a Readout, traveling or canonical.
- Never mutate an Area Brief. An Area Brief changes only through a Readout's `area_brief_disposition`, in Harness.
- Never authorize adoption or a default change. Only an ADR does that, driven by a Readout's `adoption_disposition`.
- If a frozen Protocol needs to change, run design-experiment again to produce a new `protocol` id. Never edit a frozen Protocol's fields in place.

## Composing with goal-prompt and prototype

- For a decision-bearing handoff that carries this Protocol into execution, use `goal-prompt` and give it this Protocol's `protocol` id, `protocol_sha256`, and file path. `goal-prompt` restates identity and routing/stop gates only — it must not regenerate or duplicate `question`/`metrics`/`gates`/etc.
- If the real need is feasibility exploration with no confirmatory claim, route to `prototype` instead of freezing a Protocol here. Escalate to design-experiment only once a real experiment — with a baseline and gates — is warranted.

## Templates

- `templates/protocol.md` — the frozen Protocol (fill in, hash, then treat as read-only).
- `templates/baseline-manifest.md` — the baseline the Protocol's `baseline_ref` points at.
- `templates/experiment-ledger.md` — execution/accounting log for runs against this Protocol. Never a Readout or Evidence substitute.
