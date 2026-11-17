<a id="project-foundations"></a>
<a id="start-and-maintain-a-project"></a>

# Write and maintain project instructions and docs

Use this guide to structure, write and maintain global and project instructions, skills, behavior specs, architecture, commands and other project documents as a connected whole. It explains what belongs where, how readers find it and how changes stay consistent.

An author uses the relevant pages to leave useful instructions and documents in a project. Subsequent agents follow that project's entry to its specs, architecture and commands; they revisit this guide when writing or improving those materials. Essential working instructions stay where contributors encounter them before acting. Copying this collection into AGENTS.md or importing all of it at startup defeats that reading path.

Start with the row that matches what you are writing or improving. These are choices, not a required document set or a sequence to run for every change.

<a id="existing-links"></a>

| Your task | Open next | What you should leave behind |
| --- | --- | --- |
| <a id="start-a-new-project"></a>Start a new project | [Write the first useful documents](project-documents.md#start-with-one-useful-path) | A clear purpose, one useful behavior, a supported way to try it and the constraints that matter |
| <a id="improve-an-existing-project"></a>Improve an existing project | [Repair the reader's path](project-documents.md#improve-an-existing-project) | A usable route through the affected docs, with useful names, contracts and history preserved |
| Write global, project, nested or local instructions | [Context File Authoring](context-file-authoring.md#layers) | Essential working instructions at the right scope, with task-specific routes and supported loading |
| Write or update a reusable skill | [Skill Authoring Principles](skill-authoring-principles.md) | A clear trigger, useful procedure and result, with conditional supporting detail |
| <a id="meaningful-behavior-and-derived-architecture"></a>Write specs and architecture | [Behavior](project-documents.md#write-the-behavior-before-the-design) and [architecture](project-documents.md#write-the-architecture-as-an-explanation) | Predictable outcomes and examples, separate from the design used to meet them |
| <a id="native-commands-own-repeated-preparation"></a>Write setup, check or recovery commands | [Supported commands](project-documents.md#write-commands-people-can-use) | Usable commands, prerequisites and failure guidance at their maintained owner |
| <a id="complete-authorized-work"></a>Describe how the project carries changes and investigations through | [Ordinary work and research](project-work.md) | Appropriate working instructions, checks, decision boundaries and evidence routes |
| <a id="changed-intent-and-affected-knowledge-closeout"></a>Maintain instructions, skills and docs | [Update the affected knowledge](project-maintenance.md#maintain-docs-with-the-change); [changed intent](project-work.md#when-the-intended-result-changes) | Current guidance that agrees with the delivered behavior, with original evidence still available |

If you want to see the result before reading the method, open [Shelf Report](examples/shelf-report/README.md). It is a complete, small fictional document set: purpose, agent entry, behavior, architecture, commands and a connected change. Its commands are illustrative. The [walkthroughs](project-foundations-examples.md) connect the example to ordinary repair and research.

## Tree docs and progressive disclosure

**Tree docs** means organizing current documents under descriptive names so a reader can discover them from a small directory listing. **Progressive disclosure** means reading the entry first, then opening the detail needed for the task. A directory listing shows filenames; it does not load all those files. The [document-writing guide](project-documents.md#find-the-document-before-reading-it) demonstrates both.

Keep essential rules on the route before the action they govern. For example, say that demonstrations use an isolated store beside the command that creates one. Detailed storage recovery can wait until a reader needs to change or recover storage. [Context File Authoring](context-file-authoring.md) explains instruction placement and provider loading; an ordinary link and a startup import do different jobs.

## What belongs to the project

<a id="boundaries-and-owners"></a>

The project owns its requirements, architecture, commands and current guidance. Its existing issue, task or work-record system keeps progress and evidence. The [boundary examples](project-documents.md#projects-repositories-checkouts-and-workspaces) explain how to navigate when those owners span repositories.

Keep each explanation at its maintained owner. A cross-project working default belongs in the applicable global source; a project's constraints and reading routes belong in its entry; detailed behavior and design belong in its docs. [Instruction layers](context-file-authoring.md#layers) explains those choices. A project-documentation task does not automatically include changing shared globals or skills owned elsewhere.

[Gardening](project-gardening.md) is optional maintenance inspection. Its initial mode proposes discovered repairs for discussion before implementation. That rule does not interrupt a repair the user has already asked you to make.

## Take the guide with you

<a id="distribution-and-optional-aids"></a>

This collection needs no private OS, Workbench, installed skills or task product. The [distribution list](project-guide-distribution.md) names the pages and example to keep together. Use ordinary files, a Git checkout or an archive. Agents maintains the shared explanation; projects link to it and keep their own facts locally.

## Use this approach in a repository

Give the other lead access to this entry and its linked collection, then use the prompt below. Replace GUIDE with the accessible path or link and name any wider scope, such as shared global instructions, that you actually want included.

> Here is the approach I think we should use in this repo: GUIDE. Let's use it to keep our instructions, skills and project docs connected, with essential working rules in the right instruction files and task-specific detail where it belongs. Read our current entry and relevant docs, then tell me what already fits, what you would change and which decisions need discussion. Reuse useful structure and names, preserve behavior and important boundaries, and keep original evidence available. Let's discuss the recommendation first, then make the agreed changes and check a representative reader path. Include global instructions or shared skills owned elsewhere only if we explicitly select them.

This prompt starts with discussion; it does not authorize installation or publication. For an implementation already requested, continue under that request's actual scope rather than introducing a new discussion gate.
