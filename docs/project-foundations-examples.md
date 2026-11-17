<a id="project-foundations-examples"></a>

# A complete small project, then a change

[Shelf Report](examples/shelf-report/README.md) is a fictional command-line project for a small workshop. It turns stock counts into a Markdown report. The complete documents describe the selected version 2, which adds a low-stock filter. Commands, incidents and maintainer decisions are illustrative; no application or test run is claimed.

## Open the pages in the order of your question

| Question | Page | What to notice |
| --- | --- | --- |
| What does the tool do? | [README](examples/shelf-report/README.md) | Purpose, a real input/output example and the next reading choices |
| What should an agent read before changing it? | [AGENTS.md](examples/shelf-report/AGENTS.md) | Local constraints and specific routes, without repeating the whole spec |
| What exactly does export promise? | [Export behavior](examples/shelf-report/docs/export-stock-report.md) | Stable requirements, failure/non-events and concrete scenarios |
| Why does validation come before filtering? | [Architecture](examples/shelf-report/docs/architecture.md) | Responsibilities and ordering derived from the behavior |
| How do I run and check it? | [Development and operation](examples/shelf-report/docs/development.md) | Commands, outputs, diagnosis and focused checks |
| What changed, and what remains historical? | [Low-stock change](examples/shelf-report/history/change-12-low-stock.md) | Connected page/check updates and links to original evidence |

For a new project, read the README and the behavior spec, then use [the writing guide](project-documents.md) to write the equivalent for your own project. For a bug fix, start at the affected spec and follow its checks and architecture. You do not need to begin with history.

## One meaningful change

The workshop asks for a report containing items with quantity below a chosen threshold. The change adds `--below N`, with a strict “quantity less than N” comparison. Input validation still applies to the entire file. That last sentence matters: filtering bad rows away would quietly weaken an existing promise.

The current README demonstrates the new command. `EXP-5` owns the new behavior; `EXP-2` still owns invalid-input preservation. Architecture explains validate → select → render → publish. Development guidance checks the threshold boundary and an invalid row that a premature filter could hide. The change record lists those connected updates; it does not copy their complete rules.

The [original v1 contract](examples/shelf-report/history/export-v1.md) and [earlier bug record](examples/shelf-report/history/bug-07/record.md) remain unchanged examples of historical material. The bug record includes its original input and before/after output bytes. Its report predates the filter and therefore supplies no proof for `EXP-5`. A later decision would add a qualification or new result rather than rewrite that record.

## Ordinary repair versus new intent

If invalid input destroys the previous report, repairing validation/publication restores the existing contract. The agent implements, diagnoses and retests within the requested fix; it does not ask for permission after each failure.

If the workshop instead asks to publish valid rows while ignoring invalid ones, that is a different behavior. The maintainer must settle how errors, counts and retries work before dependent implementation. The spec changes explicitly; old all-or-nothing evidence remains evidence for the old contract. [Ordinary work](project-work.md#when-the-intended-result-changes) explains that decision boundary.

## A research project uses the same distinctions

A research area can keep a maintained question and current conclusion beside the source repositories, while the existing experiment records retain the baseline, candidate, input versions, protocol and results. A valid negative result can finish the investigation without selecting the method for the product. The [research section](project-work.md#research-and-experiments) explains this path without adding a second complete document system.

## Compatibility routes

<a id="ordinary-correction-under-an-end-to-end-mandate"></a>

[Ordinary repair](#ordinary-repair-versus-new-intent).

<a id="consequential-intent-change"></a>

[Changed behavior and its connected pages](examples/shelf-report/history/change-12-low-stock.md).

<a id="valid-negative-research-result"></a>

[Research and experiments](project-work.md#research-and-experiments).

<a id="bounded-maintenance-inspection"></a>

[Bounded maintenance inspection and its initial proposal](project-gardening.md).
