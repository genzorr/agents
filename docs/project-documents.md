# Write project documents people can use

Suppose you are building a command that turns a stock CSV into a Markdown report. A useful first README might say:

> Shelf Report helps a small workshop see which items need restocking. It reads a local CSV and writes a report. Invalid input must leave the previous report intact. Start with the sample CSV; the command and expected result are below.

That gives the reader a purpose, a first path and a consequential promise. The [complete example](examples/shelf-report/README.md) develops it into connected documents. This page explains how to write yours.

## Start with one useful path

Write the outcome in terms of someone using the project: who does what, with which input, and what should happen. Name an important failure or action that must not occur. Distinguish an agreed need from a proposal. For research, start with the question and the evidence needed to answer it.

For a small project, a README with Purpose, Behavior, Run, Check and Design sections may be enough. Add an agent entry only for relevant instructions and routes. A separate spec becomes useful when several changes need to refer to the same behavior. A separate architecture page becomes useful when someone needs to understand responsibilities or a tradeoff before changing the implementation. A development page earns its place when setup, diagnosis or recovery would crowd out the introduction.

Build and exercise the first useful path as part of an implementation request. Do not create empty directories or pages for capabilities that have no reader yet. A plan-only request can describe the path and its proposed checks without pretending it runs.

## Find the document before reading it

Use descriptive filenames. `export-stock-report.md` tells you more than `phase-2.md` or `notes-new.md`. Preserve an established useful filename when readers already rely on it.

Here is the limited current-document view for the example:

```text
README.md
AGENTS.md
docs/
  export-stock-report.md
  architecture.md
  development.md
```

The record of an earlier failure lives under `history/`; it is intentionally outside this current-document view. It remains reachable from the relevant behavior and change records.

When you do not know where a topic lives, discover filenames first. From a repository root, these are alternatives, not steps you must all run:

```sh
rg --files docs -g '*.md' -g '!docs/harness/**'
tree -L 2 docs
```

Use `tree` only if it is available and the selected root is useful. There is no reason to install it for this method. A file browser works too. `rg --files` lists names recursively under the selected root; on a large repository, select a smaller root such as `docs/export/`. `tree -L 2` limits depth but can still show many entries. Neither command is a content read or a permission to inspect private material.

If names do not answer the question, search the relevant branch for a term, then read the owning section with enough surrounding context to preserve conditions and exceptions. Do not concatenate every file in `docs/` into startup context. Do not truncate an unknown subtree and assume the omitted files are irrelevant.

For example, a change to invalid-input handling opens the README, agent entry, export spec and the validation/publication section of architecture. It opens development guidance to find the check command. It need not start with every past investigation. If the change relies on an earlier result, follow that result to its original evidence before relying on it.

## Give each page a question

| Page or section | Reader's question | Write here |
| --- | --- | --- |
| README | What is this, and where do I start? | Purpose, current usable scope, shortest supported path, links for the next tasks |
| Agent entry | What must I know before acting here? | Important local boundaries, selected checkout/record routes, relevant instructions and check commands |
| Behavior spec | What must happen? | Inputs, visible outcomes, errors, required non-events, quality or scientific commitments and concrete examples |
| Architecture | How does it work, and why this design? | Responsibilities, data/control flow, state ownership, failure behavior and consequential tradeoffs |
| Development/operations | How do I run, change, diagnose or recover it? | Real commands, prerequisites, expected output, safe retry/recovery and output ownership |
| Existing task/result record | What happened in this work? | Request, decisions, source basis, attempts, results, limits and next action |
| Retained source/report | What did the original author or run say? | Original attributable material and its limitations; link later assessments separately |

These are responsibilities, not a required file count. One small development-and-operations page can answer both questions. A large capability can have its own spec and operational page. Avoid maintaining the same detailed procedure in both a README and a runbook; let the README link to the runbook.

## Write the behavior before the design

A behavior clause should let a reader predict a meaningful result. For Shelf Report:

> If any input row has an invalid quantity, the command exits with code 2, identifies the row on stderr and leaves the existing report unchanged.

Then give a case: an existing report, a CSV containing `Adapter,three`, the export command, and the expected error and unchanged bytes. This is more useful than “robust validation.” Derive the expectation from the desired behavior or an independent reference, rather than asking the implementation helper to generate its own expected answer.

Architecture can then explain:

> Parse and validate the entire input before filtering or rendering it. Write the completed report to a temporary file beside the destination, then replace the destination. The publisher owns replacement; the CLI only passes input and reports the outcome.

The first passage is a requirement. The second chooses a way to meet it. Another design can be acceptable if it preserves the required behavior. If an interface, algorithm or data format is externally mandated, identify that source and the reason it is binding.

Use readable clause IDs when tasks, checks or consumers need stable references. The example uses `EXP-1` through `EXP-5`; Workbench already has its own IDs. Preserve an ID when clarifying the same promise, give a new promise a new ID, and never reuse a retired ID for something else. A linked test is a route to evidence, not proof that the clause is fully covered.

Write only the requirements needed to settle real behavior. A bug fix restoring an existing promise may need no spec change. An implementation preference does not become a requirement because it is easy to test.

## Write the architecture as an explanation

Start with the few responsibilities that explain a representative path. Follow one input through them, including a relevant failure. Say who owns persistent state and who may change it. Explain a tradeoff when a future maintainer might reasonably choose differently.

Avoid copying the module list into prose. In the example, “validation precedes filtering so bad rows cannot disappear” explains a design decision and its consequence. The actual file or symbol can be named beside that explanation once it exists. Keep deeper interface shapes and recovery procedures at their owning references.

Separate current design from proposed design. A documentation edit can describe a future migration; it cannot make that migration happen. If code and an accepted spec disagree, describe the discrepancy and repair it or obtain the required behavior decision. Do not silently rewrite the promise to match the code.

## Write commands people can use

Document a command where the reader needs it, with its working directory, prerequisites, inputs, outputs and success/failure signals. Say whether it reads, writes, starts a service or consumes a significant resource. Put a real operational boundary before the command that needs it.

The example's [development page](examples/shelf-report/docs/development.md) shows setup, export, checks and diagnosis in one place. Its commands are explicitly fictional. In a real project, obtain commands from its launcher, package configuration, help, tests and operating docs; verify the applicable ones when authorized. If you cannot verify a platform or environment, say exactly what remains unverified.

When every caller must activate the same environment, generate the same prerequisite or remember an ordering rule, make the existing project command handle that preparation where practical. Keep task-specific input paths and resource choices explicit. Repeating shell preparation in prompts and skills gives future users more opportunities to get it wrong.

## Write the agent entry last

Once the project docs exist, write the small entry that routes work to them. Include the boundaries a contributor must encounter before acting even if they have no private globals. A useful route says, “Before changing export behavior, read the export spec; use the development page for the CLI checks.” “Read the docs” leaves the reader to guess.

The author uses this guide to build that project entry; a later contributor uses the entry to do the work. Keep essential local instructions explicit. For example, Shelf Report's entry requires preserving user files and completing the requested implementation, diagnosis and relevant checks. It links the export spec for the behavior and the development page for commands. A contributor can follow that route without reading this authoring collection or having the author's global instructions. Link this guide conditionally for future documentation work instead of copying it into the entry.

Use [Context File Authoring](context-file-authoring.md) when deciding globals, project entries, nested/local files, provider wrappers or imports. It owns provider mechanics. A linked document is opened for a task; a startup import loads with its parent. Moving all the same text into imported files does not create progressive disclosure.

## Improve an existing project

Choose one real reader task first: start the tool, diagnose a failure, change a behavior, or resume work. Follow it from the existing entry. Read the selected checkout's pending changes as well as its committed revision; preserve other people's work.

Identify the actual failure in that path. Perhaps the README links to a completed design proposal, the setup command omits a prerequisite, or three pages give different retry rules. Repair the affected owner and callers together. Reuse useful filenames, IDs, examples and commands. Move a page only when its new location makes a recurring question easier to answer.

A requested broad redesign needs a concrete map of current docs, instructions, source reports, work history and command owners. Limit it to the selected projects and affected readers. It does not require a new tracking system, an inventory of every parked repository, or a repository-wide audit before each ordinary edit. [Maintenance](project-maintenance.md) covers link preservation and checking the resulting reader path.

## Projects, repositories, checkouts and workspaces

| Boundary | Example | Navigation consequence |
| --- | --- | --- |
| Project | The continuing Shelf Report product | Its purpose and requirements remain recognizable across changes |
| Repository | The versioned source and docs | Follow its contributor instructions and history; another nested repo is independent |
| Checkout | The actual branch and working files selected for a change | Read and test these bytes; a clean older clone cannot stand in for pending work |
| Workspace | A chosen context coordinating one or several projects | Its entry names the selected sources and record system; a parent folder alone does not establish that identity |
| Record owner | An issue tracker or existing task store | Keep progress, decisions and evidence there instead of inventing another journal |
| Artifact owner | The place and person/system responsible for output bytes | A task link does not copy, back up or authorize deleting those bytes |

A single repository can cover all these needs. Separate work records become useful when several checkouts must share continuation, provided the selected tool supports that arrangement. Record the real binding in existing setup guidance; do not infer support from a proposed folder tree.

For a larger research area, a short area page might link a maintained question and scientific constraints to two independent source repositories, the selected experiment records and the retained dataset/output locations. Opening the mapper's docs should not require reading the recorder's internals. A shared experiment record names both exact source bases. It does not duplicate both projects' specs or move their data.

Grow by area only when the material needs it. A larger product might have `docs/import/validate-batch.md` (example-only) and `docs/export/publish-report.md` (example-only), each reached from the entry for that task. A short area README is useful when there are real choices to explain. Empty `architecture/`, `decisions/`, `research/` and `operations/` folders add no help by themselves.
