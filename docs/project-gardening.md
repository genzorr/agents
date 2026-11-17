# Project gardening

Gardening checks a bounded part of an existing project for useful repairs. Start in **inspect and propose** mode: return a concrete repair batch for the user to discuss before implementing it. You can use this procedure manually; no scheduler, installed skill or Workbench is required.

For a known change already requested by the user, use [ordinary work](project-work.md). Its implementation, diagnosis and relevant retesting continue within that request. Gardening's proposal rule applies to newly discovered maintenance work.

## Select the inspection

Pick a question with a consequence. Examples include whether a setup command still works with its documented prerequisites, whether a recovery instruction preserves the data it promises to preserve, or whether current docs still describe an agreed behavior after a code change.

Name the selected checkout and working files, affected documents/contracts, the existing issue or task that will receive the result, and any previous proposal or disposition. Bound the paths and available effort to that question. Read applicable instructions and preserve pending work. Use the selected record owner's supported route; do not initialize a second history to record the inspection.

A manual request can be as short as: “Inspect the exporter recovery instructions against the selected command/help and focused offline check. Use the existing maintenance issue and its last disposition. Propose repairs only; return a useful no-change or coverage limit if that is what the evidence supports.” Replace the generic references with actual project paths and commands.

## Initial mode: inspect and propose

1. Read the affected current docs, relevant code/configuration and prior result. Distinguish a bug, factual drift, a proposed behavior change, accurate history and an unsupported claim.
2. Use relevant cheap checks within the inspection's permissions. Native help, existing validators and focused offline checks may be sufficient. Live services, private inputs, installation, expensive runs and cleanup require their own authority. A prompt's effort budget is not an enforced resource limit.
3. Compare the finding with the prior disposition by owner, relationship and consequence. If the evidence and premises still hold, link the existing proposal, deferral, rejection or no-change result. Record what you rechecked. A new date or unrelated commit is not a new finding. Revisit it when relevant behavior, evidence, authority or a stated reconsideration condition changes.
4. Return the result at the existing record owner, identifying the examined bytes, evidence, exclusions and next owner/action. A passing check does not establish complete coverage.

Return one of these useful outcomes:

| Outcome | Include |
| --- | --- |
| Proposed repair | Concrete problem and consequence, agreed basis, affected owners/readers, bounded edits, preservation needs and relevant checks |
| No change | Why the selected relationship is coherent and what evidence supports that conclusion |
| Partial or blocked inspection | What was established, what remains unexamined and the next observation or access needed |

Separate repairs that restore agreed behavior from proposals that change it. Do not create one finding per file or a new findings ledger. Keep existing record fields or ordinary prose.

Inspection includes retaining its result when the request permits record updates. It does not include executing the discovered source repairs. Present the batch for user discussion and approval. A recurring schedule, reviewer agreement or green check does not approve it.

## Approved execution

Use the actual approved batch and its limits. Recheck it against current working files and other people's changes. Implement, diagnose, repair and retest within that scope; do not ask for the same approval again after each failure.

Update affected current guidance and reader routes, preserve history, and obtain the review the project requires. A larger repair or changed promise returns to the responsible decision-maker. Installation, publication, merge and destructive actions still need whatever authority applies to them; approval of source edits does not silently include those effects.

Record the delivered bytes, checks and limits, remaining obligations and next action. Keep assessment, integration and operational adoption distinct when the project does.

Source edits and record updates can succeed separately. If interrupted, retain the changed bytes or patch, source basis, completed effects and uncertain operations at the existing task-owned location. Before retrying a record update with an uncertain response, inspect whether it landed. Use the tool's revision/receipt or idempotency rules; do not replay source effects or append duplicate records blindly. Report uncertainty that cannot be resolved.

## Handing this to an automation-setup agent

Provide the same source selection, inspection question, existing record owner, previous-disposition route and proposal-only limits. Name who receives the result and who can approve a repair batch.

The setup agent must inspect the actual scheduler and environment before proposing configuration: working directory, source/instruction availability, permissions, schedule/timezone, result delivery and pause/change controls. Separate settings the scheduler enforces from preferences in a prompt. Start with inspection/proposals; unattended recurrence does not grant repair or merge permission.

No live job, supported BB configuration or scheduler interface is established by this portable page. The existing optional BB integration has its own owner and setup evidence. Manual gardening remains available without it.
