# Agents for Codex and Claude

Reusable skills, commands, subagents, global instructions, and notification hooks for Codex and Claude Code. The installers copy cataloged assets into your chosen home directory and preserve modified or unmanaged files.

## Install

Requires Python 3.9 or newer. The installer uses the Python standard library; no Python packages are required.

Review the [Codex instructions](codex/AGENTS.md), [Claude instructions](claude/CLAUDE.md), and [asset catalog](catalog.json) before installing. These are opinionated workflows and global defaults. Some skills require separately installed tools or services; see each skill's `SKILL.md` for its requirements. The commands below install all assets for the selected platform.

From a local checkout, preview the changes first:

```bash
bash scripts/install-codex.sh --dry-run --diff
bash scripts/install-claude.sh --dry-run --diff
```

Then run the installer for the platform you use:

```bash
bash scripts/install-codex.sh
# Or:
bash scripts/install-claude.sh
```

The default destinations are `~/.codex` and `~/.claude`. Set `CODEX_HOME` or `CLAUDE_HOME` to use another directory. For an isolated trial:

```bash
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh
```

On native Windows, use the PowerShell entry points:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1 --dry-run --diff
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1
# For Claude, use scripts\install-claude.ps1 instead.
```

Set `$env:CODEX_HOME` or `$env:CLAUDE_HOME` to override the Windows destinations, which default to `%USERPROFILE%\.codex` and `%USERPROFILE%\.claude`.

## Update and remove

Re-run the installer after updating your checkout. Install is copy-based and idempotent. Edit source files in this repository rather than installed copies; locally modified destinations are reported as conflicts and preserved.

`--dry-run` and `--diff` are read-only. `--prune` removes unchanged, previously managed files no longer in the catalog. `--uninstall` removes unchanged managed assets and reconciles managed Claude hook settings. Both preserve modified and foreign files. Preview either operation before applying it:

```bash
bash scripts/install-codex.sh --uninstall --dry-run --diff
```

Keep `.agents-install-state.json` in the selected home: it records historical ownership needed for safe updates and removal. The Claude installer merges its notification hooks into `settings.json` while preserving unrelated settings. Conflicts return a non-success status and require inspection before retrying. To roll back, check out a known-good source commit and re-run the installer.

See the [installer contract](docs/skill-installer-contract.md) for ownership, conflict handling, and recovery details.

## Repository guide

| Path | Contents |
|---|---|
| [catalog.json](catalog.json) | Desired assets, source layers, install targets, and supporting documents |
| [codex/](codex/) | Codex global instructions and skills |
| [claude/](claude/) | Claude global instructions, skills, commands, subagents, rules, and notification hooks |
| [shared/](shared/) | Source files shared by both platforms |
| [scripts/](scripts/) | Installers and validators |
| [docs/](docs/) | Usage guides and technical contracts |

Same-name Codex and Claude skills are platform counterparts and can intentionally differ. Agents manages only its own cataloged assets and preserves assets installed by other tools.

## Development

Read [AGENTS.md](AGENTS.md) before changing the repository. Validate source changes with:

```bash
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
bash scripts/test-prune-safety.sh
```

Exercise installer changes against scratch homes before any live installation. Cross-repository ownership checks and optional local work tracking are maintainer checks documented in [AGENTS.md](AGENTS.md).

Optional configuration has separate setup instructions: [Codex permission profile installer](scripts/install-codex-permissions.py) and [Claude auto-mode configuration](docs/claude-auto-mode.md). Neither is applied by the generic asset installer; review its policy before use.
