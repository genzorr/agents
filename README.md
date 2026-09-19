# Agents for Codex, Claude, and Devin

Reusable skills, commands, subagents, global instructions, configuration, and notification hooks for Codex, Claude Code, and Devin CLI. The installers copy cataloged assets into independent shared or provider homes and preserve modified or unmanaged files.

## Install

Requires Python 3.9 or newer. The installer uses the Python standard library; no Python packages are required.

Review the [Codex instructions](codex/AGENTS.md), [Claude instructions](claude/CLAUDE.md), [Devin instructions](devin/AGENTS.md), [Devin defaults](devin/config.json), and [asset catalog](catalog.json) before installing. These are opinionated workflows and global defaults. Some skills require separately installed tools or services; see each skill's `SKILL.md` for its requirements.

Portable skills have one managed runtime location at `~/.agents/skills`, which Codex and Devin discover natively. Claude receives managed copies under `~/.claude/skills`; its current documented discovery paths do not include the global shared directory. Provider-specific skills remain complete, unique assets under their provider home and are never overlaid on a same-name shared skill.

From a local checkout, preview the changes first:

```bash
bash scripts/install-codex.sh --dry-run --diff
bash scripts/install-claude.sh --dry-run --diff
bash scripts/install-agents.sh --dry-run --diff
bash scripts/install-devin.sh --dry-run --diff
```

Then run the installer for the platform you use:

```bash
bash scripts/install-agents.sh
bash scripts/install-codex.sh
bash scripts/install-devin.sh
# Claude does not consume ~/.agents/skills, so its provider installer includes managed skill copies:
bash scripts/install-claude.sh
```

The default destinations are `~/.agents`, `~/.codex`, `~/.claude`, and `${XDG_CONFIG_HOME:-~/.config}/devin` (or `%APPDATA%\devin` on Windows). Set `AGENTS_HOME`, `CODEX_HOME`, `CLAUDE_HOME`, or installer-specific `DEVIN_HOME` to use another directory. The shared installer is deliberately independent: provider install, prune, and uninstall commands never mutate `~/.agents`, so Codex and Devin can be installed or removed in either order without competing for shared state. For an isolated trial:

```bash
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh
AGENTS_HOME="$PWD/.scratch-home/agents" bash scripts/install-agents.sh
DEVIN_HOME="$PWD/.scratch-home/devin" bash scripts/install-devin.sh
```

On native Windows, use the PowerShell entry points:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1 --dry-run --diff
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1
# For Claude, use scripts\install-claude.ps1 instead.
# The shared and Devin twins are scripts\install-agents.ps1 and scripts\install-devin.ps1.
```

Set `$env:AGENTS_HOME`, `$env:CODEX_HOME`, `$env:CLAUDE_HOME`, or `$env:DEVIN_HOME` to override the corresponding Windows destination.

When migrating an existing Codex installation, install the shared surface first, verify it, then preview and run `install-codex.sh --prune`. The explicit prune removes only unchanged shared-skill copies recorded as Agents-owned in the Codex state; modified or foreign copies remain conflicts and are preserved. This order avoids duplicate same-name discovery while retaining rollback evidence.

## Update and remove

Re-run the installer after updating your checkout. Install is copy-based and idempotent. Edit source files in this repository rather than installed copies; locally modified destinations are reported as conflicts and preserved.

`--dry-run` and `--diff` are read-only. `--prune` removes unchanged, previously managed files no longer in that home's catalog. `--uninstall` removes unchanged managed assets and reconciles managed Claude hook settings or Devin config values. Both preserve modified and foreign files. Preview either operation before applying it:

```bash
bash scripts/install-codex.sh --uninstall --dry-run --diff
```

The Claude installer merges its notification hooks while preserving unrelated settings. See the [installer contract](docs/skill-installer-contract.md) for conflict handling and recovery.

## Skills and configuration

Browse the [shared skills](shared/skills/), [Codex skills](codex/skills/), and [Claude skills](claude/skills/). Same-name provider skills can intentionally differ. A catalog entry is shared only when its complete installed behavior is provider-neutral; tool names, frontmatter, permissions, invocation, model behavior, and runtime metadata are reasons to retain complete provider twins.

The Devin installer copies a complete [Devin-specific global instruction layer](devin/AGENTS.md) to `AGENTS.md` in the Devin home (by default `~/.config/devin/AGENTS.md`); it is a provider twin, not a symlink or forced copy of the Codex or Claude source. Project `AGENTS.md` files remain the repository-specific instruction surface. The installer also leaf-merges [safe defaults](devin/config.json) into `config.json`: standard `AGENTS.md` project rules stay enabled, and foreign-tool imports are disabled to avoid duplicate rules, skills, hooks, and MCP configuration. Unrelated strict-JSON settings, including an operator-selected model or permission mode, are preserved. A differing unmanaged value, a modified managed value, invalid JSON, or JSON-with-comments is preserved as a conflict rather than reformatted or overwritten. Authentication and credentials are never managed. Model and permission selection belong to the invoking workflow rather than this global interoperability config.

Optional [Codex permission profiles](scripts/install-codex-permissions.py) and [Claude auto-mode settings](docs/claude-auto-mode.md) have separate setup paths and are not applied by the asset installer. The Codex installer validates its complete prospective config in an isolated temporary `CODEX_HOME` before writing, and `--dry-run` validates without creating a destination or backup.

```bash
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-thread-bridge
CODEX_HOME="$HOME/.codex" python3 scripts/install-codex-permissions.py --configure-app-defaults
```

`--configure-thread-bridge` patches the existing bridge server's created-task defaults and approval mode. `--configure-app-defaults` is a separate opt-in that patches only `apps._default`; neither option changes unrelated app, tool, or MCP settings. See the [bridge and permission configuration contract](docs/codex-thread-bridge.md).

## Development

Read [AGENTS.md](AGENTS.md) before changing the repository. Validate source changes with:

```bash
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
bash scripts/test-prune-safety.sh
```

Exercise installer changes against scratch homes before any live installation. Cross-repository ownership checks and optional local work tracking are maintainer checks documented in [AGENTS.md](AGENTS.md).
