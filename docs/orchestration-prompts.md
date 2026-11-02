# Preparing and orchestrating changes

`prepare-change` is an optional method for turning an unsettled development request into a justified next commitment. Use it directly in the current development chat or before/during an authorized owner assignment; it needs no team, Workbench or private OS checkout. It does not launch an owner. `orchestrate-feature` selects the separate-owner topology and owns supervision; using preparation does not select that topology.

| Situation | Useful request |
| --- | --- |
| Broad change, unclear behavior or weak success evidence | Use `$prepare-change` to inspect the actual need, requirements/examples and evidence before committing to implementation. |
| Agreed preparation already supports authorized implementation | Reuse it and proceed within the mandate; do not repeat preparation merely to invoke a skill. Reassess affected work if material evidence changes. |
| Small settled bug fix with a clear reproducer and expected behavior | Fix and verify directly under existing authorization; no preparation spec, slice or review ritual is needed. |
| Existing criteria/examples express the complete behavioral agreement | Keep them; do not create a capability-spec file just to fill a template. |
| Separate owner requested | Invoke `$orchestrate-feature`. Use optional preparation before launch or inside that owner's mandate when a real gap warrants it. |

A necessary shared capability spec belongs at the project's established owner; tasks/roadmaps hold delivery planning. Preparation-only returns the preparation deliverable. An end-to-end request can continue when sufficiently prepared within existing authority; the method grants no additional permissions. `grill-with-docs` remains available for a deliberate plan/design interview and retains its existing callers; it is no prerequisite here. `answer-pro` assesses a returned consultation rather than wrapping generic preparation.

## Prepare a change directly

For an unsettled request, supply the project/change context and existing agreements:

```text
Use $prepare-change for the change we discussed. Inspect the current code/specs and actual need; return necessary requirements/examples, acceptance evidence, an initial outcome plan and remaining consequential decisions. Stop before implementation.
```

Request scoped independent scrutiny explicitly when useful or required, for example: “I authorize fresh Astra/medium reviewers to challenge this preparation and verify substantive corrections.” This is a request-specific profile, not a generic skill default. Without delegation, the method can still prepare and self-review, labeling missing independent coverage honestly; unavailable required review holds only its dependent readiness/action. Unsupported role/delivery controls need resolution rather than silent substitution. To authorize an end-to-end change, say so in the implementation request and carry its real limits; preparation acceptance alone does not grant that authority.

## Start a supervised run

```text
Using the reviewed specification and delivery plan, prepare and start the agreed implementation run within our existing scope, permissions and limits.

First check that the applicable requirements, decisions and guiding documents are coherent enough for the next commitment. Reuse the accepted preparation; do not restart it or add ceremony. Resolve local facts and ordinary technical choices yourself. Raise only material unresolved choices outside your authority, with facts, a recommendation and consequences.

Prepare your supervision alongside the same delivery roadmap. Select checkpoints where earlier evidence could change a consequential decision or prevent material wasted work before a dependent action. For each, state the result/evidence due, the required review or decision, who decides, and what the owner may continue or must wait for. A bounded or settled run may need only final assessment; duration alone does not require extra stages. Reassess when material assumptions, dependencies, evidence, scope or limits change.

I authorize native reviewers, advisors and bounded assistance needed for this assignment. Obtain a fresh Astra/medium independent review of your run preparation. Use fresh Astra/medium reviewers for the independent scrutiny required at selected checkpoints. Seek Astra/high advice when a consequential uncertainty warrants it. Keep an advisor's continuity within one unresolved discussion; start fresh for a new substantive question. Reviewers start fresh for each substantive request, and an advisor who shaped a result cannot independently certify it. Preserve existing threads' settings.

Review the run preparation, resolve concrete findings, then launch or resume a separate owner through $orchestrate-feature using its default owner/team settings unless we already selected overrides. Give the owner its relevant scope, criteria, limits, evidence and return/continuation contract. Keep your assessment responsibilities in the existing work record. Establish an actual supported delivery/observation route; do not assume invisible monitoring.

At agreed checkpoints, inspect the owner's result and decisive evidence, obtain the required scoped scrutiny and validation, then continue within authority, return bounded corrections, seek advice or raise a genuinely reserved blocker. Routine owner checks need no extra approval. Partial review or checkpoint acceptance cannot establish completion of the whole feature, merge, deployment or adoption.

Proceed through authorized work without another routine GO request. Stop only affected work at a real scope, authority, resource or required-evidence boundary; continue independent work. Preserve useful results and recovery context. Finish by assessing the complete promised outcome and reporting what is accepted, what remains unresolved, and where the supporting evidence lives.
```

## Source and rationale

Requested by genzorr on 2026-11-03: T-136 introduced the reviewed preparation/supervision requests; T-137 adds optional `prepare-change` and clear use/skip guidance so ordinary development can reuse the method without adopting a team or mandatory pipeline. The aim is to challenge specs/criteria before wrong-scope implementation and select checkpoints where earlier evidence can prevent costly late discoveries while settled work stays light. User CogOS questions motivated the requests; they establish no measured effectiveness or successful run.

The supervised-run example deliberately requests fresh Astra/medium origin preparation/checkpoint scrutiny and optional Astra/high advice, preserving existing threads and default owner/team settings unless separately overridden. Its earlier conditional independent-preparation-review wording was corrected and independently verified in T-136. These are future user requests to adapt, not instructions to execute by reading the guide; actual supported roles, project permissions and the [orchestration contract](orchestrate-feature-prd.md) govern. This guide is the maintained human-facing owner; earlier issued standalone versions/review bases remain retained work evidence. No installation or publication authority follows.
