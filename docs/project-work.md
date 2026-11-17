# Carry useful work through

Use this page when establishing or revising how a project's instructions and documents support implementation, correction and investigation. It explains the working behavior those materials should preserve, with examples of changed intent and evidence. Keep essential instructions at the appropriate global or project entry and use skills for a selected reusable procedure; detailed rules need not be copied into every surface.

Ordinary development starts from the project's existing instructions, affected specs and commands. Open this page when its explanation helps resolve a question; the whole authoring guide is not a prerequisite for every change. The project's actual requirements and permission boundaries still apply, and no particular skill or task system is required.

## Make a behavior change

Start from the result the person needs. Read the affected current behavior and enough implementation to know what changes. Reuse a sufficient spec or plan. Resolve ordinary technical choices from the project; ask only about a choice that changes the intended result or exceeds the work you may do.

For example, adding a low-stock report to [Shelf Report](examples/shelf-report/docs/export-stock-report.md) preserves EXP-2: validate every input row before filtering. A filter cannot hide an invalid row. This is an existing promise to trace through the change; allowing partial acceptance would be a separate explicit behavior amendment. The architecture explains the ordering, and the [change record](examples/shelf-report/history/change-12-low-stock.md) shows the related doc and check updates.

Choose relevant evidence before implementing. Exercise the supported interface with an ordinary case and a failure that could otherwise pass unnoticed. Expected values should come from the requirement, an independent fixture or a justified reference. Preserve exact assertions when exact text, shape or values are themselves a public protocol, safety boundary or compatibility promise.

A small transformation can use a focused check. Shared state, queues, retries, permissions and recovery need a view of the whole affected path, including failure between components. A component passing alone may miss an unsafe retry. Existing adequate checks can be reused; add or broaden them for a changed consequence, conflicting evidence, a remaining risk or a required project gate.

When removing a check, explain what defect it used to detect and what still protects that behavior. A check for a private temporary filename can change with the design; a check that invalid input preserves the last good report still matters. If coverage is uncertain, try a plausible defect or a legitimate implementation variation to see whether the scenario distinguishes them. That is a useful investigation, not a compulsory exercise for every edit.

## Keep going within the request

When asked to build or fix something, carry it through implementation, relevant execution, diagnosis and necessary retesting within the agreed limits. A failed check or progress update does not mean the person must authorize the same work again. Repair the problem, rerun the affected case and continue toward the requested result.

A request for preparation or review ends with that deliverable unless it also authorizes changes. Permission to edit source does not by itself authorize publication, installation, spending money, deleting data, operating hardware or changing a scientific protocol. Reuse authority already given for the exact action and scope. Hold the dependent action when that authority is missing, and continue independent work where useful.

Use progress messages for findings, consequential changes and real blockers. Return a decision with the known facts, your recommended choice and its effect. Do not ask the person to choose routine variable names, approve every page or release each ordinary test run.

## Diagnose rather than repeat blindly

Reproduce the problem through the supported command or a narrower check that preserves the relevant failure. Retain the symptom, source/configuration and useful failed output. Name the plausible causes, then choose the cheapest observation that separates them.

If an export fails, distinguish invalid input, rendering failure and publication failure before changing retry behavior. If a write may already have committed, inspect the actual state or the operation's receipt before retrying. Keep the original request identity where the project requires exact retry.

After fixing the cause, rerun the failed case and affected regressions. If the cause remains unknown, retain the live explanations and the next observation needed. A negative or unresolved investigation can be complete when it answers the assigned question honestly.

## Stay aligned with the intended result

At a useful checkpoint or repeated consequential failure, ask whether the approach still serves the goal. A passing helper test, a tidy repository or a polished report can leave the real user path broken. Inspect that path before adding another mechanism or review round.

Prefer existing project commands, libraries, platform capabilities and supported configuration where they meet the need. Simplify repeated knowledge or unnecessary layers within the requested change. Moving hidden setup into every caller does not simplify the system. A sound no-change decision is useful; there is no reduction quota.

Keep unrelated improvements as proposals at the existing record owner. Do not add a new requirement merely because it would make the implementation easier to assess. When a different approach materially changes the outcome or commitments, follow the decision boundary below.

## When the intended result changes

Distinguish a repair from a new promise. Fixing invalid-input data loss restores Shelf Report's existing behavior. Allowing partial acceptance of invalid batches would change it: downstream readers and retry behavior may depend on all-or-nothing output.

Record the old promise, proposed replacement, reason and deciding person. If the current assignment already authorizes that amendment, proceed within it; otherwise return the consequential choice before dependent implementation. Update the affected spec, design, commands, checks and consumers once the change is agreed.

Keep old results against their original requirements and source basis. Add a later qualification when their use changes. Do not rewrite an old failed attempt or acceptance report to make it appear that it covered the new behavior.

## Research and experiments

A research task starts with a question that the evidence can answer. Use the project's existing protocol and record format. Name the baseline/candidate, data, metric or correctness reference, conditions, resource budget and stopping rule when they affect interpretation. Preserve any frozen dataset, evaluator, analysis plan or scientific commitment.

Suppose an experiment asks whether an incremental index reduces search latency without changing results. A tested candidate can match the correctness oracle and still miss the latency target. Check that the measurement is valid, retain the adverse result and conclude only about that candidate and those conditions. A failed run caused by broken measurement is invalid evidence of method quality. One failed implementation does not reject a whole family of methods.

Separate the observation, its interpretation and a decision to adopt or try something else. Use [Claim Discipline](claim-discipline.md) when a result is becoming a broader claim or reusable rule. Existing scientific review and independent validation requirements remain in force; a concise guide does not waive them.

Before substantial execution, resolve the actual host, input/output destinations, resource ownership and retention responsibilities through project configuration and any explicitly routed local bindings. A missing mount must not silently redirect a large run elsewhere. Preserve useful partial results and original failed attempts. Task completion or an ignored directory grants no cleanup permission.

## Review and finish

Use required independent review at the boundary selected by the project or assignment. Keep ordinary implementation feedback inside the development loop. Batch review around a coherent result; obtain focused help for a named uncertainty. If independent review is required but unavailable, report that gap and hold the dependent readiness claim, while continuing unaffected work. Self-review is not independent review.

The lead assesses the delivered files, relevant checks and intended use. A worker's summary or a review verdict is evidence for that assessment, not a substitute for it. Review, acceptance, merge and operational adoption remain separate where the project distinguishes them. Delegation itself needs the authority and runtime support selected for the task.

Finish at the existing issue, task or report. State what changed, the actual source/working-file basis, checks and limits, where useful evidence and outputs remain, and the next owner/action for unresolved work. Update current documentation with the change using [maintenance guidance](project-maintenance.md). Do not create a second history store or a standing instruction for every completed task.
