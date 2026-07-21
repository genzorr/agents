# Experiment workflow behavior fixtures

These cases are small contract fixtures for the installed Codex and Claude
skills. They are behavioral review inputs, not executable experiments: no case
runs a command from a Protocol or claims a scientific result.

| Case | Frozen/design expectation | Review/composition expectation | Forbidden side effect |
|---|---|---|---|
| `ml-confirmatory` | `mode: confirmatory`; decision, mechanism/falsifiers, unit/control, representative baseline tier, role-prefixed metrics, practical gates, trial rationale, provenance, and analysis/validity rules map into the unchanged frozen fields | review records execution, observations, interpretation, caveats, reuse/do-not-repeat, and both dispositions; a successful process is not scientific validation | no experiment execution, Area Brief mutation, or ADR/default change |
| `systems-regression` | `mode: regression`; baseline reference, variation sources, guardrail/resource metrics, non-regression gates, environment provenance, and missing-run handling are frozen before execution | review compares the closed run set to the named baseline and preserves invalid/partial execution separately from interpretation | no post-hoc gate or run-set mutation |
| `agent-evaluation-exploratory` | `mode: exploratory`; unknowns and limited claim stage are explicit, metric roles and trial coverage are justified, no confirmatory claim is promised, and the run set is closed | goal handoff carries only Protocol identity/hash and routing; review may record evidence but retains `no-adoption` unless explicitly dispositioned | no silent promotion to confirmatory work, Area Brief, or adoption authority |
| `prototype-escalation` | prototype states one feasibility question and its limits; it does not freeze a Protocol | a promising prototype routes to `design-experiment` for a new frozen Protocol before decision-bearing execution | no Protocol fields, traveling/canonical Readout, or adoption claim inside the prototype |

For every case, both runtime twins must resolve the same field names and
boundaries. When Harness is present, the review handoff targets the one
canonical project Readout; without Harness, the traveling template remains
non-canonical and can only make the validated one-way import/freeze transition.
