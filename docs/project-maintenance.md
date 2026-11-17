# Keep project knowledge current

The most useful maintenance happens with a change. If a command, behavior, prerequisite or recovery path changes, update its explanation before handing over the result.

## Maintain docs with the change

Follow the fact to its maintained owner, then inspect the readers that depend on it, including relevant pages outside the code diff. Use this table to decide what needs attention; it is not a request to edit every row.

| Change | Update or check |
| --- | --- |
| Agreed behavior changes | Spec, meaningful examples/checks, affected user commands and consumers |
| Implementation changes but behavior stays | Architecture or diagnosis guidance that describes the changed mechanism; preserve the requirement |
| Command or prerequisite changes | Its operating/development owner, command help/configuration and entry links |
| Instruction scope or loading changes | The applicable [global, project, nested or local entry](context-file-authoring.md#layers), supported wrappers and readers that must encounter its constraints |
| A skill's trigger or procedure changes | Its [invocation and supporting guidance](skill-authoring-principles.md#invocation), affected callers, checks and distributed copies |
| Ownership or source path changes | Current entry/binding and affected callers; preserve historical source references |
| A result is corrected | A new qualification at the record owner and known consumers; keep the original evidence |
| A workaround is no longer needed | Remove it from current guidance; retain why it existed in history when that matters |

In Shelf Report, the [low-stock change](examples/shelf-report/history/change-12-low-stock.md) adds a requirement and an example, explains validate-before-filter in architecture, updates usage and checks, and leaves the [original failed export](examples/shelf-report/history/bug-07/record.md) intact. That is one connected change, not a new document for every stage.

If a page remains accurate, leave it alone. When an affected claim cannot be established or corrected within the task, identify that claim, qualify its use and name the next owner/action. A generic “docs later” note is not enough while the supported instructions remain misleading.

Published source and installed instructions can differ. When the requested change includes installed readers, update through the source owner's supported installer under the applicable authority and check the actual reference locations. Publishing a guide or editing a project entry does not itself update another runtime home.

## Keep current knowledge distinct from work history

Current docs answer what a contributor should use now. Tasks and plans describe work in progress. Results and source reports retain what happened or what an author argued under a named basis. A recent report does not automatically become the current rule.

Put an adopted conclusion in the existing maintained page and link its supporting evidence. Keep the original report unchanged; record accepted, rejected and unresolved recommendations separately. For a historical question, follow the original records. For ordinary operation, the entry should reach current instructions without making the reader reconstruct a chronology.

Preserve source identity, meaningful adverse results, useful partial work and the evidence needed to challenge a conclusion. References to external artifacts do not back up their bytes. Keep their actual locations, owners and retention obligations recoverable in the existing task or artifact metadata.

## Move a page without losing its readers

Before a move, find inbound references in the selected repositories, instruction sources, templates, command help and installer/catalog declarations that actually consume it. Preserve useful headings and explicit anchors. For uninspected or parked consumers, retain the old path as a short redirect with its supported anchors until those consumers can be changed under their own authority.

Update active callers to the new owner so they do not take unnecessary hops. Keep one full explanation; a redirect says where it moved and carries no competing procedure. Do not edit issued reports or copied originals to modernize their historical links. Keep an accessible route to the original source basis instead.

For pending uncommitted work, retain the starting bytes or a recoverable patch before replacement. A Git commit ID alone does not preserve uncommitted/untracked evidence. Do not infer permission to remove files, branches, aliases, outputs or installed assets from a documentation move.

## Check the reader's work

Start from the entry with a representative question and follow only the task's route. Can a reader find the right spec or command, explain a relevant failure, make a small behavior change and update the connected pages without private discussion? Fix the route or explanation where the reader has to guess.

Also check relative links, anchors, command names/prerequisites and retained promises. Use the project's existing check commands where they answer a real question. Static checks establish syntax or reachability; they do not establish that the writing teaches the task, that a provider loaded it, or that a command works on an untested machine.

Reuse adequate check evidence. A documentation-only change does not call for a hardware run, a broad benchmark or a new verification service. A changed command or loader may need its own focused source or runtime check under the corresponding authority.

## Optional gardening

Use [Project Gardening](project-gardening.md) when the request is to inspect for maintenance opportunities rather than make a known change. Pick one relationship, such as “does the documented recovery command still match the supported behavior?” Read existing dispositions so recurrence does not produce duplicate work.

Gardening first returns a repair proposal, a justified no-change result or a clear coverage limit. The user discusses and approves a discovered repair batch before execution. An already-authorized bug fix or documentation rewrite continues under its own request; it does not acquire a new gardening approval gate.

Scheduling is optional and separate. The portable procedure works manually. A schedule does not authorize discovered repairs, installation, publication or cleanup.
