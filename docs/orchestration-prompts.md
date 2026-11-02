# Orchestration prompts

Use these two requests with the project orchestrator: first prepare the change, then start an authorized implementation run. Supply the project/change context and existing agreements. These are future user requests to copy and adapt, not instructions to execute merely by reading this guide. The second request uses the Codex [orchestrate-feature contract](orchestrate-feature-prd.md); actual supported roles, delivery mechanisms and permissions still govern. Unsupported requested controls need resolution, not silent substitution.

The prompts deliberately request fresh Astra/medium scrutiny for origin preparation/checkpoints and optional Astra/high advice. They preserve existing threads and the skill's default owner/team settings unless separately overridden; they do not change generic role defaults. Neither preparation acceptance nor a positive review grants implementation, merge, deployment or adoption authority.

## Prepare the specification and plan

```text
Prepare the change we have been discussing before implementation, using this project's guidance and existing work records.

Inspect the relevant code, specifications and prior decisions. Clarify the actual need and turn it into necessary requirements, concrete examples, important failure cases and meaningful acceptance evidence. Resolve repository facts yourself; bring me consequential product choices with your recommendation. Challenge requirements or mechanisms that add complexity without serving the need.

Update the applicable stable capability spec, or create one at the project's established spec location when needed. Keep current behavior, proposed requirements and suggested implementation choices distinguishable. Reuse one maintained spec rather than making a new file for every task or review round.

Propose an initial delivery plan: outcomes, dependencies and how we will verify correctness and validate usefulness. Use a slice/roadmap and tasks when the scope warrants them and the project supports them. Leave detailed implementation planning for the relevant tasks. Include environment, resource, recovery and stop constraints where they materially affect the work.

I authorize fresh Astra/medium reviewers to challenge the requirements, approach and plan against my actual need and project evidence. Revise until concrete issues are resolved or a genuinely reserved decision is identified; use a new context for each substantive review. An advisor who shaped the design cannot independently certify it. Use a Pro follow-up only if a material unresolved question would benefit from it.

Return the spec, proposed roadmap, review conclusions and remaining decisions with a concise recommendation. State whether the result is a proposal or an agreed contract. Stop before implementing the feature or launching production/costly runs; preparation acceptance alone does not authorize them.
```

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

Requested by the user, genzorr, on 2026-11-03 alongside proportionate orchestration preparation/supervision (OS T-136). The aim is to challenge specs and criteria before wrong-scope implementation and select checkpoints where earlier evidence can avoid costly late discoveries, while keeping settled work light. User CogOS questions motivated the requests; they establish no measured effectiveness or successful run. Fresh Astra/medium wording review identified a conditional independent preparation-review request; the corrected second prompt requires that review, and another fresh Astra/medium reviewer closed the finding without new issues. This guide is the maintained human-facing owner; the issued standalone versions and review bases remain retained work evidence. Static packaging and wording review do not establish observed model behavior or grant live installation/publication authority.
