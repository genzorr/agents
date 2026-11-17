---
name: orchestrate-feature
description: Launch or resume a separate ordinary feature owner from a long-lived orchestrator, then assess its handoff through validation and disposition. The owner executes and obtains required independent review; it cannot accept or close its feature. Use on explicit invocation or request for this topology.
---

# Orchestrate Feature

**Composition role: helper.** The project workflow stays the driver. An explicit invocation selects one separate ordinary feature owner regardless of task size. Resolve the feature before creating anything; another feature needs another invocation. Only the project orchestrator launches an owner. Native helpers stay leaves; the owner cannot launch another ordinary owner or accept/close its own feature.

## Launch one owner

Read [Prepare and launch](references/feature-contract.md#prepare-and-launch) before launch or reuse. Identify the intended result, selected checkout and working bytes, permitted actions, success criteria, useful checkpoints and supported return route. Reuse adequate preparation. If a choice is unresolved, delegate only the investigation already authorized and continue work that does not depend on its answer. Existing threads retain their settings; creation defaults and explicit overrides apply only at creation.

Write the assignment using the [owner contract](references/feature-contract.md#owner-contract), using the relevant decisions and source references rather than parent history or this outer skill. Say that the requesting orchestrator/user decides acceptance, and specify which assistance and review the user authorized. Preserve scientific, resource, privacy, Git and external-effect limits.

## Work through the return

The owner implements, diagnoses, repairs, retests and updates affected current docs within scope. A progress report or ordinary failure creates no new approval gate. Independent review of the final delivered result remains required unless the user explicitly waives it. If required review cannot run, report that gap and continue other authorized work; do not claim the result is ready for validation. When native help is authorized and useful, the owner uses [Orchestrate Workers](../orchestrate-workers/SKILL.md).

Before sending or receiving a handoff, read [delivery](references/feature-contract.md#owner-messages-and-delivery) and [origin assessment](references/feature-contract.md#orchestrator-receives-and-acts). Read the actual result and evidence, carry out any missing authorized validation, and record what must be corrected, can continue or is accepted. Passing checks, an accepted message and a reviewer verdict cannot show by themselves that the result serves its intended use. Merge/adoption remain with the user.


## Existing links

<a id="prepare-and-launch"></a>

[Continue: prepare and launch](references/feature-contract.md#prepare-and-launch).

<a id="owner-contract"></a>

[Continue: owner contract](references/feature-contract.md#owner-contract).

<a id="owner-messages-and-delivery"></a>

[Continue: owner messages and delivery](references/feature-contract.md#owner-messages-and-delivery).

<a id="orchestrator-receives-and-acts"></a>

[Continue: orchestrator receives and acts](references/feature-contract.md#orchestrator-receives-and-acts).
