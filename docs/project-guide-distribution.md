# Copy or share the project guide

Agents maintains this collection under `docs/`. Copy these paths together, preserving their relative layout:

```text
project-foundations.md
project-documents.md
project-work.md
project-maintenance.md
project-foundations-examples.md
project-gardening.md
project-guide-distribution.md
context-file-authoring.md
claim-discipline.md
skill-authoring-principles.md
experiment-protocol-readout-contract.md
examples/shelf-report/     all files below this directory
```

Start at [project-foundations.md](project-foundations.md). The authoring reference is needed when writing instruction files; Claim Discipline is conditional on broader claims; the skill reference is needed only when authoring skills. Including these references keeps the collection usable without an installed runtime. It does not mean reading them all at startup. None requires a private OS or a record product.

An ordinary checkout or archive is enough. Identify the source repository/revision and whether pending working files are included. For an uncommitted delivery, retain the files with hashes or a patch against retained starting bytes. An archive of Git HEAD alone omits pending and untracked work.

The worked example contains fictional documents and data, not an executable application. Do not present its illustrative commands or history as verified project behavior. External articles in the references provide attribution and optional technical verification; the portable writing procedure is explained in the collection itself.

`project-gardening-bb.md`, provider global files, installed skills and the Agents installer are separate optional assets. The BB adapter remains with its existing owners; copying this guide does not configure BB or create a recurring job.

A project can link to a selected Agents revision or a retained bundle and keep its own README, specs, architecture and commands in its repository. If contributors need an offline copy, identify it as a versioned derivative and say where updates come from. Do not independently edit the same generic explanation in several projects.

Agents' catalog carries this set under each supported provider home's `docs/`. Existing skills that carry Context File Authoring also receive its linked guide and example under their own `docs/`. These use the existing traveling-document and layered-source declarations; there is no new installer or guide skill. Resolve a reference from its actual consumer: home-relative docs for a global instruction, skill-relative docs for a skill. A copy elsewhere does not satisfy it. Use the existing installer contract and scratch checks when changing that distribution. Source packaging and scratch success do not establish live installation or provider loading.
