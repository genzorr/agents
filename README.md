<a id="agents-for-codex-claude-devin-and-pi"></a>

# Agents

Agents maintains reusable project guidance and generic agent assets for Codex, Claude, Devin and Pi. It also owns the tools that install its cataloged assets while preserving modified and foreign files.

## Choose a starting point

| You want to… | Start here |
| --- | --- |
| Structure or improve a project's instructions and documentation | [Project guide](docs/project-foundations.md), or open the [complete small example](docs/examples/shelf-report/README.md) first |
| Write project or global agent instructions | [Context File Authoring](docs/context-file-authoring.md) |
| Find a reusable procedure | [Toolbox by task](docs/toolbox.md) |
| Install, update or remove Agents-owned assets | [Installation](docs/installation.md), then the applicable provider's preview |
| Change this repository | [AGENTS.md](AGENTS.md) and [development guidance](docs/development.md) |
| Inspect possible repository repairs | [Optional gardening](docs/project-gardening.md); discovered repairs are proposed first |

The project guide is ordinary Markdown and needs no installation, private OS or Workbench. Its [distribution list](docs/project-guide-distribution.md) includes the supporting references. Projects keep their actual requirements, architecture, commands and work records.

## Source ownership

Edit generic assets here. Installed copies are derivatives managed by the owning installer. A complete shared skill and a same-name provider skill are not overlaid; provider counterparts can differ in tools, invocation, permissions and model controls.

Harness keeps its runtime-specific assets and parser/CLI. Session Harvester keeps its harvesting skill. BB keeps its runtime-specific instructions and skills. Agents' catalog must not install or remove another owner's assets. The [installer contract](docs/skill-installer-contract.md) owns the detailed behavior.

Local maintainers may use ignored `docs/harness/` when present. Public contributors can use the issue or PR record; private coordination is not needed to understand this repository.

## Install

Read [installation and preview](docs/installation.md#preview-the-selected-provider) before changing a runtime home.

## Update and remove

Use [update and recovery](docs/installation.md#update-prune-or-remove). Preserve managed-state evidence and conflicts; an absent catalog entry is not permission to delete foreign files.

## Project foundations

The [project guide](docs/project-foundations.md) explains how to structure, write and maintain global and project instructions, skills, behavior specs, architecture, commands and other project documents. It teaches what belongs where, how agents find the relevant detail and how changes stay consistent. An author uses the guide to improve a project's own reading routes; subsequent work follows those routes rather than rereading the whole guide. The [complete example](docs/examples/shelf-report/README.md) shows a small connected document set.

To discuss adopting the approach elsewhere, share the guide and its [reusable handoff prompt](docs/project-foundations.md#use-this-approach-in-a-repository).

For optional BB gardening setup, use [its separate guide](docs/project-gardening-bb.md).

## Skills and configuration

Use the [task-based toolbox](docs/toolbox.md). It distinguishes existing procedures from planned consolidation; runtime-specific setup remains at its current owner.

## Development

Use [development guidance](docs/development.md) for checks and source changes.

### Local outputs and retention

[Outputs and retention](docs/development.md#local-outputs-and-retention) owns the actual guidance.

### Diagnosis and recovery

[Diagnosis and recovery](docs/development.md#diagnosis-and-recovery) owns the procedure. These headings retain existing inbound links.
