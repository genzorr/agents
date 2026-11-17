---
name: prepare-change
description: Prepare a development change when intended behavior, success evidence or approach is unsettled, or consequential work needs reviewed preparation. Reuse sufficient preparation and skip this method for small settled changes; usable directly or within an existing owner assignment.
---


# Prepare Change

**Composition role: helper.** Use this method when a change needs clearer requirements, examples or a plan. Reuse preparation that already answers those questions. A small settled fix can proceed directly. This method does not authorize implementation, delegation or a new approval stage.

<a id="establish-the-need-and-contract"></a>

## Read what the change needs to do

Read how the result will be used, the affected current spec, relevant source and prior decisions. Resolve repository facts and ordinary reversible technical choices yourself. Separate existing promises, proposed behavior and implementation suggestions. A linked spec or filled template alone establishes neither correctness nor usefulness.

Ask the person responsible when a choice would change the intended result or require permission you do not have. Explain the known facts, your recommendation and its consequences. Continue work that does not depend on the answer. For example, adding a filter must preserve an existing promise to validate the whole input; filtering alone is no reason to reopen that promise.

Use the existing spec/task and concrete ordinary, boundary and failure examples to decide how to check the result. Add a capability spec only when the behavior needs a shared written agreement. When a spec needs writing, open `docs/project-documents.md` from the installed skill's directory, or repository-root `docs/` in the source checkout. Its complete example separates requirements from design. Do not resolve supporting docs from the consumer project's cwd.

<a id="plan-and-challenge-proportionately"></a>

## Plan the work and check the risks

Plan the results, dependencies and checks. Include resources, environment, recovery and stop limits where they affect the work. Preserve scientific freezes, privacy, permission for external/destructive actions and the project's review requirements. Use existing project records; this method requires no universal form or new task tree.

Creating an independent reviewer requires explicit permission to delegate that review and supported tools. When review is requested or required and authorized, use a fresh independent context for each substantive request, including correction review; clarification can retain its issued report's context. An advisor who shaped the result cannot certify it. If required review is unavailable, report what is missing. Do not claim that review is complete or take a step that requires it; continue other authorized work. Self-review is not independent review, and optional advice creates no extra approval gate.

## Reassess the approach

When progress reveals a consequential problem or an existing checkpoint calls for it, read [focused approach review](references/approach-review.md). Diagnose an ordinary bug/environment failure before deciding that the architecture or intended outcome is wrong. Continue implementation, repair, retesting and affected-doc maintenance within scope. Ask the person responsible before changing an agreed promise unless the assignment already authorizes that change.

<a id="return-or-continue-under-the-mandate"></a>

## Finish preparation or continue implementation

If asked only to prepare the change, return the proposed change, examples and checks, initial plan, review results or missing coverage, important assumptions/limits and remaining decisions. Say what is proposed versus agreed and who needs to decide what. Keep supporting evidence in the project's existing records, and stop before implementation.

If implementation is already requested and preparation is sufficient, continue implementing, diagnosing failures, fixing them and running relevant checks without asking again for the same work. Revisit the affected plan when assumptions, scope, dependencies or limits change; continue work that does not depend on the unresolved question. The requesting orchestrator/user still decides whether to accept the feature and close its task; the feature owner cannot create nested ordinary owners.
