---
name: review-experiment
description: Review a completed experiment run against its frozen Protocol and baseline, separating execution validity, observations, interpretation, scope/caveats, and reuse/do-not-repeat from the Area Brief impact and adoption/ADR decisions. Use when the user asks to review an experiment, invokes review-experiment or /review-experiment, wants to write or validate a Readout for a Protocol's closed run set, or needs to hand a completed run off toward an Area Brief update or ADR decision without prejudging it.
---

# Review Experiment

Review a completed run of a frozen Protocol and record the result as a Readout. This skill produces exactly one thing: a Readout that separates process/execution facts from scientific interpretation from downstream disposition. It never runs the experiment, never fabricates observations or interpretation on the user's behalf, never mutates an Area Brief, and never creates or updates an ADR — see Boundaries.

This skill implements the portable Protocol/Readout contract. The full versioned contract (identity/hash rules, direct-write versus one-way import/freeze, current-leaf resolution, exact-repeat no-op, mismatch rejection, successor-only corrections) lives at `docs/experiment-protocol-readout-contract.md` in the `agents` source repo; the rules that govern *this* skill are restated below so the installed skill is self-contained. This skill does not redefine that contract — see `design-experiment`'s twin `SKILL.md` for the Protocol side of the same contract, which this skill reuses rather than re-derives.

## Contract this skill reviews against

A Readout is the one place execution validity, observations, interpretation, scope/caveats, reuse notes, and two independent dispositions are recorded — never conflated with each other or with the Protocol they review:

- **Traveling Readout fields:** `protocol`, `protocol_sha256`, `runs` (the closed run set being reviewed), `execution`, `observations`, `interpretation`, `scope_and_caveats`, `reuse_do_not_repeat`, `area_brief_disposition`, `adoption_disposition`, `source_artifact`, `source_sha256`, `status`, `replaces` (optional), `date`. These names map directly to the canonical Harness Readout fields — no second field vocabulary.
- **`execution`** is one of `valid` | `invalid` | `partial` — whether the run(s) executed as the Protocol specified. This is independent of whether the scientific claim held; a perfectly valid execution can still fail its gates, and an invalid execution cannot support any interpretation regardless of what the numbers show.
- **`area_brief_disposition`** is one of `no-change` | `update-area-brief` | `retract-area-brief` — exact contract vocabulary, no synonyms.
- **`adoption_disposition`** is one of `no-adoption` | `consider-adr` | `update-adr` — exact contract vocabulary, no synonyms. ADR pairing/absence rules (as defined by the accepted Harness contract): `update-adr` requires naming the ADR it updates; `no-adoption` forbids naming an ADR; `consider-adr` may optionally name a candidate ADR without committing to it.
- **Direct provenance, no duplication.** The Readout's only link to the frozen Protocol is the `protocol` + `protocol_sha256` pair, copied verbatim — never re-derived. That pair is also the Readout's provenance link to the Protocol's `baseline_ref`, `commands`, and `artifacts`: those are frozen inside the one Protocol document this pair identifies, so linking to the Protocol *is* linking to them. Never copy `commands`, `artifacts`, `gates`, or the baseline's content into the Readout — open the Protocol and baseline-manifest documents directly instead.
- **`source_artifact`/`source_sha256`** are a paired provenance reference used only when this Readout was produced by importing an external traveling artifact; both present or both absent, never one without the other.
- **Deterministic current-leaf resolution, exact-repeat no-op, mismatch rejection, successor-only corrections** all apply exactly as defined in the contract §§5–7: zero current leaves creates the first Readout; one current leaf with identical content is a no-op; one current leaf with different content is rejected (never merged/coerced) — a material correction creates a successor with `replaces` pointing at the predecessor, and the predecessor is never edited, deleted, or given a back-reference; more than one current leaf is a contract violation that fails outright rather than silently resolving.
- **Process success is not scientific validation.** Successfully writing a Readout proves the review process completed — it never proves the interpretation is correct, never mutates the singleton Area Brief (only the Area Brief's own explicit update does, driven by `area_brief_disposition`), and never authorizes adoption or a default change (only an ADR does that, driven by `adoption_disposition`).

## Steps

1. **Locate and re-verify the frozen Protocol.** Open the Protocol document (`design-experiment`'s `templates/protocol.md` instance) this run claims to belong to. Recompute `protocol_sha256` using `design-experiment`'s exact canonicalization recipe (same field order, same `json.dumps(..., separators=(",", ":"))`, same sha256 — do not invent a different recipe) and confirm it matches the value recorded in the Protocol document. If it does not match, stop: the Protocol has drifted or the wrong document was opened, and no Readout can be written against a Protocol identity that cannot be confirmed.
2. **Confirm the run set.** Every run/commit reference this Readout reviews must already be a member of the Protocol's closed `run_set`. Never expand `run_set` here — that requires a Protocol successor from `design-experiment`, not this skill. If actual execution deviated from the Protocol in a way its own `deviation_policy` does not cover, that deviation itself is an `execution: invalid` or `partial` fact to record, not something to paper over.
3. **Open the baseline manifest** the Protocol's `baseline_ref` names, so `observations`/`interpretation` compare against `metrics_at_baseline` and its documented `caveats` rather than an assumed or re-measured baseline.
4. **Gather each Readout field from the user, one at a time**, with the same discipline `design-experiment` uses for Protocol fields: do not accept a field as complete until it is concrete enough that a different reader could reach the same conclusion without asking a follow-up question. Never fill in `observations` or `interpretation` yourself from inference — elicit the actual measured facts and the actual conclusion from the user; this skill structures the review, it does not perform it:
   - `execution` — `valid` | `invalid` | `partial`.
   - `observations` — measured facts against the Protocol's `metrics`, with artifact references (paths the Protocol's `commands` already produced).
   - `interpretation` — what the observations mean against the Protocol's `gates` and the baseline.
   - `scope_and_caveats` — what this result does and does not generalize to.
   - `reuse_do_not_repeat` — what future work should reuse, and what it must not repeat.
   - `area_brief_disposition` — `no-change` | `update-area-brief` | `retract-area-brief`.
   - `adoption_disposition` — `no-adoption` | `consider-adr` | `update-adr`, with the ADR-naming pairing rule above.
5. **Fill in `templates/readout.md`** with the fields above plus `protocol`, `protocol_sha256`, `runs`, `date`, and (if reviewing an already-frozen external artifact) `source_artifact`/`source_sha256`. Treat the filled file as the traveling Readout — self-contained, no Personal-OS-only path.
6. **When a Harness-tracked project is present**, write or validate the one canonical project Readout *directly* — do not stop at the traveling template. Construct the exact `harness` command from the fields gathered above and run it (or present it for the user to run, if the environment calls for that confirmation step first):
   - First Readout for this Protocol identity: `harness add-readout <area> <title> --date <date> --protocol <protocol> --protocol-sha256 <protocol_sha256> --run <run> [--run <run> ...] --execution <execution> --area-brief-disposition <area_brief_disposition> --adoption-disposition <adoption_disposition> [--adr <adr>] [--source-artifact <path> --source-sha256 <hash>] --observations <file-or-> --interpretation <file-or-> --scope-and-caveats <file-or-> --reuse <file-or->`. `harness` itself resolves zero/one/multiple current leaves and exact-repeat no-op/mismatch rejection — do not reimplement that logic here, and do not hand-edit a Harness Readout file directly.
   - Material correction to an existing canonical Readout: `harness replace-readout <old_readout_id> <title> --date <date> --protocol <protocol> --protocol-sha256 <protocol_sha256> --run <run> [...] --execution <execution> --area-brief-disposition <area_brief_disposition> --adoption-disposition <adoption_disposition> [--adr <adr>] --observations ... --interpretation ... --scope-and-caveats ... --reuse ...`. This is a successor, never a re-import — never pass `--source-artifact`/`--source-sha256` here even if the predecessor had them.
   - Retracting a canonical Readout (visible, not deleted): `harness retract-readout <readout_id> --date <date> --reason <reason>`.
   - `area` (the Harness Evidence-area slug) and `title` are Harness-write-time arguments, not portable Readout fields — ask the user which existing Area Brief this belongs to rather than inventing a new area.
   - Harness's canonical Readout also carries one free-text `--disposition` slot (a rationale for the two disposition enums) beyond this contract's field list. When writing directly into Harness, ask the user for that rationale and pass it via `--disposition`; this is a known Harness-side field the portable contract does not yet name — flag it, do not silently invent a matching portable field.
   - Use the id and path returned by Harness (`Created/Reused readout` and `Path`) as the canonical reference. Report those returned values verbatim; do not derive or substitute a title-based path.
   - When reviewing a Harness Runs experiment packet, use that packet's `readout_date` for `--date` and its complete `runs` list for the repeated `--run` arguments. Normalize Harness's returned `Path` to the repository-relative form if it prints an absolute path, then require the returned id/path to exactly match the packet's `readout_destination`; stop on a mismatch rather than merely reporting it. Standalone non-Runs review continues to use its own supplied date/runs and has no packet destination to compare.
7. **When no Harness-tracked project is present**, the traveling Readout from step 5 is the only artifact produced. It is never claimed to be canonical. Its only permitted future transition into Harness is the one-way validated import/freeze in the contract's §4 — a later `harness add-readout` run with `--source-artifact`/`--source-sha256` pointing at this frozen file, once a Harness-tracked project exists.
8. **Report** the Readout's identity (`protocol`, `protocol_sha256`, `runs`), the returned canonical id/path, the outcome of the write/validate step (created / no-op / rejected with reason / successor created), and the recorded `area_brief_disposition`/`adoption_disposition` so the user can take the next explicit step themselves.

## Boundaries

- Never execute the Protocol's `commands` or run the experiment — this skill only reviews an already-completed run.
- Never fabricate or infer `observations`/`interpretation` on the user's behalf. Elicit them; do not decide the science for the user.
- Never expand a Protocol's closed `run_set`. A run outside the declared set needs a Protocol successor from `design-experiment`, not a Readout.
- Never mutate an Area Brief, regardless of the recorded `area_brief_disposition`. That mutation is a separate explicit action (`harness add-area-brief`), run by the user or a different flow — this skill only records the disposition.
- Never create, update, or otherwise authorize an ADR, regardless of the recorded `adoption_disposition`. ADR authority is exclusive and separate (e.g. `harness-adr`) — this skill only records the disposition and, when `update-adr`, the ADR id it must pair with.
- Never promote legacy `E-*` Evidence. That lookup stays historical/searchable only; nothing here restores it to current authority.
- Never implement a second mutable store for Readouts. When Harness is present, the one canonical Readout lives at Harness's own deterministic destination, written/validated only through Harness's own `add-readout`/`replace-readout`/`retract-readout` commands.
- Never re-import a frozen external source, and never give a predecessor Readout a back-reference to its successor — only the successor carries `replaces`.

## Composing with design-experiment

- Reuse the Protocol this reviews via `design-experiment`'s frozen `protocol`/`protocol_sha256`/`baseline_ref` fields verbatim. Never re-derive `protocol_sha256` with a different recipe than the one `design-experiment`'s `SKILL.md` documents.
- If the Protocol itself needs to change (not just this run's interpretation), that is `design-experiment`'s job — this skill reviews an existing frozen Protocol, it does not amend one.

## Templates

- `templates/readout.md` — the traveling Readout (fill in per Steps above; self-contained, no Personal-OS-only path).
