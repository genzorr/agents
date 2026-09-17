# Research Goal Alignment Conformance Readout

## Scope and claim boundary

**Method:** Single same-agent manual conformance pass against the updated `ask-chatgpt-pro` and `integrate-research` contracts. Each case was evaluated for the handoff or integration behavior the instructions require.

This readout checks the observed goal-drift failure modes and the intended proportional exceptions. It does not establish general model performance, repeated-run stability, or the quality of an eventual external research report.

**Result:** 3/3 PASS.

## Cases

### `faithful-baseline` — PASS

**Request:** Find a strong literature-backed baseline to adopt, reproduce faithfully, and later improve within an existing research repository.

**Required behavior:** The consultation identifies baseline selection as the current stage and establishment or faithful reproduction as the downstream stage. The decision is which baseline to adopt and what evidence would establish it credibly. The prompt asks for established candidates, essential method components, evaluation semantics, adaptation costs, and evidence needed for a faithful result. It does not require novelty or shrink the task to one loss, hook, or discriminator.

**Observed:** The research-stage contract rejects a narrower novel-mechanism substitute, protects essential components when current hooks are insufficient, and keeps the programme outcome in the success check.

### `explicit-small-scout` — PASS

**Request:** Run a small causal scout to determine whether a named failure is driven by one hypothesized mechanism before committing to a larger experiment.

**Required behavior:** The consultation preserves diagnosis as the primary stage and the bounded discriminator as the requested deliverable. The decision is whether the hypothesis merits a larger test or should be rejected. It does not inflate the scout into baseline establishment or force an unrelated literature sweep.

**Observed:** The contract explicitly keeps causal scouts and small discriminators legitimate when they answer the stated decision without displacing the programme outcome.

### `recommended-pivot` — PASS

**Request:** Integrate a completed report that supplies useful evidence but recommends abandoning the selected baseline for a different method.

**Required behavior:** Integration records supported evidence independently from the recommendation, identifies the proposed changes to the chosen baseline, method semantics, goal, or deliverable, and checks existing decision authority. If the user already delegated this choice and evidence is sufficient, the integrator may decide and record why. Otherwise it preserves the pivot as a proposal and does not turn it into project direction or a worker assignment until the next authorized action depends on resolving it.

**Observed:** The integration contract permits authorized decisions without another approval loop while preventing a report's recommendation from becoming authority by itself.
