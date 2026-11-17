# Find support for the task

The [project guide](project-foundations.md) works without installed skills. Use an available skill where its method changes the work; ordinary implementation needs no skill for every phase. The catalog owns actual provider membership.

| Your task | Start here | What it leaves to the project |
| --- | --- | --- |
| Settle an unsettled behavior or plan | [Prepare Change](../codex/skills/prepare-change/SKILL.md) | Actual promises, deciding actor, sufficient examples and continuation authority; settled fixes proceed directly |
| Review a delivered change or docs topic | [Review Change](../codex/skills/review-change/SKILL.md) or its [Claude counterpart](../claude/skills/review-change/SKILL.md) | Whole target versus fix scope, actual independent-review requirement and acceptance |
| Supervise one separate owner | [Codex Orchestrate Feature](../codex/skills/orchestrate-feature/SKILL.md) or [Pi counterpart](../pi/skills/orchestrate-feature/SKILL.md) | Real runtime topology, authority, callback and acceptance contract |
| Use authorized native assistance | [Codex Orchestrate Workers](../codex/skills/orchestrate-workers/SKILL.md) or [Pi counterpart](../pi/skills/orchestrate-workers/SKILL.md) | Existing execution/acceptance owner, scoped delegation and shared resources |

The [request examples](orchestration-prompts.md) distinguish direct work, preparation-only work and a supervised owner. BB's runtime-specific skill stays at BB's maintained source; provider counterparts are complete procedures with real differences, not overlays. A task list neither activates absent tools nor authorizes agent creation.

## Existing procedures and provider configuration

To create or maintain project `AGENTS.md` and provider-specific context, use [Context File Authoring](context-file-authoring.md). It covers inspecting the real project, verified commands, current documentation versus historical records, and maintaining guidance when behavior changes. The separate `codex-project-init` skill is retired in favor of this standalone route. Existing installed copies are reconciled by the normal Codex installer `--prune` ownership checks; modified or foreign copies are preserved for operator review.

Provider global instructions route documentation setup to the project guide and instruction authoring to Context File Authoring. Ordinary code changes follow the project's own spec and command routes. Each provider installer delivers the guide and its conditional reference dependencies under that provider home's `docs/`; skill-relative copies keep their existing separate catalog ownership. The guide is read on demand, without an automatic startup import. For returned research, Codex and Claude retain `integrate-research`; when that skill is unavailable, compare the answer with the original question and current evidence, separate proposals from decisions, and update only authorized owners.

Browse the [shared skills](../shared/skills/), [Codex skills](../codex/skills/), and [Claude skills](../claude/skills/). Same-name provider skills can intentionally differ. A catalog entry is shared only when its complete installed behavior is provider-neutral; tool names, frontmatter, permissions, invocation, model behavior, and runtime metadata are reasons to retain complete provider twins.

Use [replace-orchestrator](../codex/skills/replace-orchestrator/SKILL.md) to transfer a long-running Codex orchestrator role to a fresh chat while preserving active owners and callback continuity.

For unsettled development, optional [prepare-change](../codex/skills/prepare-change/SKILL.md) clarifies the need, necessary agreement and evidence before the next commitment. Reuse sufficient preparation and skip it for small settled changes. The [human usage guide](orchestration-prompts.md) shows direct use, preparation before/during a separate-owner assignment and a supervised `orchestrate-feature` request; these examples change no default owner/team settings.

Invoke `test-audit` explicitly to audit a bounded existing suite and plan preservation, repair, consolidation, or removal. It reports by default and continues one coherent cleanup batch when already authorized; it does not replace TDD, change review, or architecture review. Its [common source](../shared/skills/test-audit/SKILL.md) is installed into the Codex and Claude provider homes, with explicit-only Codex invocation metadata; shared-home and Devin installation are unsupported.

The Devin installer copies a complete [Devin-specific global instruction layer](../devin/AGENTS.md) to `AGENTS.md` in the Devin home (by default `~/.config/devin/AGENTS.md`); it is a provider twin, not a symlink or forced copy of the Codex or Claude source. Project `AGENTS.md` files remain the repository-specific instruction surface. The installer also leaf-merges [safe defaults](../devin/config.json) into `config.json`: standard `AGENTS.md` project rules stay enabled, and foreign-tool imports are disabled to avoid duplicate rules, skills, hooks, and MCP configuration. Unrelated strict-JSON settings, including an operator-selected model or permission mode, are preserved. A differing unmanaged value, a modified managed value, invalid JSON, or JSON-with-comments is preserved as a conflict rather than reformatted or overwritten. Authentication and credentials are never managed. Model and permission selection belong to the invoking workflow rather than this global interoperability config.

Invoke [piecemeal-growth](../shared/skills/piecemeal-growth/SKILL.md) by name or explicitly request “piecemeal growth”, “piecemeal mode”, or “piecemeal mentality” as the approach to design, implementation, refactoring, or review. This task-scoped lens grounds complexity in present requirements and credible failures while preserving the full contract; the current workflow stays in charge. Concept discussion and ordinary coding requests do not activate it. It installs in the shared Agents home for Codex and Devin discovery and as a Claude copy.

Optional [Codex permission profiles](../scripts/install-codex-permissions.py) and [Claude auto-mode settings](claude-auto-mode.md) have separate setup paths and are not applied by the asset installer. The Codex installer validates its complete prospective config in an isolated temporary `CODEX_HOME` before writing, and `--dry-run` validates without creating a destination or backup.

[Pi setup](pi-setup.md) covers catalog assets, optional Linux permissions and native automatic updates. [catalog.json](../catalog.json) defines skill membership; skills own their prerequisites. Harness assets remain with their owning repository. The separate [pi-accounts package](https://github.com/genzorr/pi-accounts#readme) owns accounts and hourly maintenance. See the [permission contract](pi-permissions.md) before relying on enforcement and [legacy migration/recovery](pi-distribution.md) only for earlier layouts. Live changes require operator authorization.

```bash
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-thread-bridge
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-app-defaults
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --approve-codex-app-tools
```

`--configure-thread-bridge` patches the existing bridge server's created-task defaults and approval mode. `--configure-app-defaults` patches only `apps._default`. `--approve-codex-app-tools` approves the bundled Codex App MCP tools that otherwise prompt. Each option preserves unrelated app, tool, and MCP settings. See the [bridge and permission configuration contract](codex-thread-bridge.md).
