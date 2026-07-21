# Experiment Readout

<!-- readout_template_version: 1 -->
<!-- protocol_readout_contract_version: 1 -->
<!-- Traveling, pre-canonicalization form. When a Harness-tracked project is present,
     review-experiment writes or validates the one canonical project Readout directly via
     `harness add-readout` / `harness replace-readout` / `harness retract-readout` — this file
     is not that canonical record. Fill it in only for a standalone or not-yet-Harness-tracked
     review; its only permitted transition into Harness is the one-way validated import/freeze
     in docs/experiment-protocol-readout-contract.md §4. Never edit a filled/frozen instance of
     this file in place after it has been imported — corrections happen in Harness via
     `harness replace-readout`, never by re-importing this source. -->

- protocol: <!-- the frozen Protocol's `protocol` id, copied verbatim -->
- protocol_sha256: <!-- the frozen Protocol's `protocol_sha256`, copied verbatim, never re-derived -->
- status: <!-- active | retracted -->
- replaces: <!-- optional: id of the predecessor Readout this corrects. Successor-only — never set this on a predecessor. -->
- date: <!-- ISO 8601 -->
- source_artifact: <!-- this file's own repo-relative path, once frozen for import. Empty until frozen. -->
- source_sha256: <!-- sha256 of this file's frozen content, computed at import time. Empty until frozen. Both source_artifact and source_sha256 must be present together or both absent. -->

## runs

<!-- The closed run_set entries (or a subset of them) this Readout reviews. Every entry must
     already be a member of the reviewed Protocol's frozen `run_set` — never an appended or
     expanded set. Amending the run set requires a Protocol successor from design-experiment,
     never an edit here. -->

-

## execution

<!-- valid | invalid | partial. Did the run(s) execute as the Protocol specified? Independent
     of whether the scientific claim in `gates` held — a valid execution can still fail its
     gates, and an invalid execution cannot support any interpretation regardless of the numbers. -->

## observations

<!-- Measured facts against the Protocol's `metrics`, with artifact references (paths the
     Protocol's `commands` already produced). Report what was measured, not what it means. -->

## interpretation

<!-- What the observations mean against the Protocol's `gates` and `baseline_ref`. -->

## scope_and_caveats

<!-- Limits of what this Readout's result generalizes to: sample size, environment, confounds,
     anything a later reader must not over-extend. -->

## reuse_do_not_repeat

<!-- What future work should reuse from this run, and what it must not repeat (a known dead
     end, an invalid setup, a wasted variant). -->

## area_brief_disposition

<!-- no-change | update-area-brief | retract-area-brief.
     Never mutates the Area Brief itself — only records which disposition a human/agent must
     later apply via Harness's own explicit Area Brief update (`harness add-area-brief`). -->

## adoption_disposition

<!-- no-adoption | consider-adr | update-adr.
     - update-adr requires naming the `adr` id it updates (below).
     - no-adoption forbids naming an adr.
     - consider-adr may optionally name a candidate adr without committing to it.
     Never itself authorizes adoption or a default change — only an ADR does that. -->

- adr: <!-- ADR id; required iff adoption_disposition is update-adr, forbidden iff no-adoption -->

<!--
Direct provenance, no duplication: the protocol/protocol_sha256 pair above is this Readout's
only link to the frozen Protocol document, and is also the provenance link to that Protocol's
own baseline_ref, commands, and artifacts fields — they live inside the one document that pair
identifies. Open the Protocol and its baseline-manifest directly rather than copying their
content here.
-->
