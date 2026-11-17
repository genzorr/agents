# Install and update Agents assets

Use this page for normal shared/provider installation. Run commands from the selected Agents source checkout. Source edits do not update runtime copies. Use the action's existing authority for live changes and use scratch homes for verification. The [installer contract](skill-installer-contract.md) owns reconciliation, state, adapters and recovery details.

## Preview the selected provider

Requires Python 3.9 or newer. The installer uses the Python standard library; no Python packages are required.

Review the [Codex instructions](../codex/AGENTS.md), [Claude instructions](../claude/CLAUDE.md), [Devin instructions](../devin/AGENTS.md), [Devin defaults](../devin/config.json), [Pi instructions](../pi/AGENTS.md), and [asset catalog](../catalog.json) before installing. These are opinionated workflows and global defaults. Some skills require separately installed tools or services; see each skill's `SKILL.md` for its requirements.

Portable skills have one managed runtime location at `~/.agents/skills`, which Codex, Devin and Pi discover natively. Claude receives managed copies under `~/.claude/skills`; its current documented discovery paths do not include the global shared directory. Provider-specific skills remain complete, unique assets under their provider home and are never overlaid on a same-name shared skill. Skills that require another runtime skill remain provider assets until their complete dependency chain is proven portable; for example, `babysit-pr` and `thermo-nuclear-code-quality-review` remain Codex/Claude assets because both require `review-change`.

From a local checkout, preview the changes first:

```bash
bash scripts/install-codex.sh --dry-run --diff
bash scripts/install-claude.sh --dry-run --diff
bash scripts/install-agents.sh --dry-run --diff
bash scripts/install-devin.sh --dry-run --diff
bash scripts/install-pi-assets.sh --dry-run --diff
```

Then run the installer for the platform you use:

```bash
bash scripts/install-agents.sh
bash scripts/install-codex.sh
bash scripts/install-devin.sh
bash scripts/install-pi-assets.sh
# Claude does not consume ~/.agents/skills, so its provider installer includes managed skill copies:
bash scripts/install-claude.sh
```

The default destinations are `~/.agents`, `~/.codex`, `~/.claude`, `${XDG_CONFIG_HOME:-~/.config}/devin` (or `%APPDATA%\devin` on Windows), and `~/.pi/agent`. Set `AGENTS_HOME`, `CODEX_HOME`, `CLAUDE_HOME`, installer-specific `DEVIN_HOME`, or `PI_CODING_AGENT_DIR` to use another directory. The shared installer is deliberately independent: provider install, prune, and uninstall commands never mutate `~/.agents`, so provider homes can be installed or removed in either order without competing for shared state. For an isolated trial:

```bash
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh
AGENTS_HOME="$PWD/.scratch-home/agents" bash scripts/install-agents.sh
DEVIN_HOME="$PWD/.scratch-home/devin" bash scripts/install-devin.sh
PI_CODING_AGENT_DIR="$PWD/.scratch-home/pi" bash scripts/install-pi-assets.sh
```

Pi asset setup uses the POSIX entrypoint; native Windows Pi setup is unsupported. For the other providers on native Windows, use the PowerShell entry points:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1 --dry-run --diff
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1
# For Claude, use scripts\install-claude.ps1 instead.
# The shared and Devin twins are scripts\install-agents.ps1 and scripts\install-devin.ps1.
```

Set `$env:AGENTS_HOME`, `$env:CODEX_HOME`, `$env:CLAUDE_HOME`, or `$env:DEVIN_HOME` to override the corresponding Windows destination.

When migrating an existing Codex installation, install the shared surface first, verify it, then preview and run `install-codex.sh --prune`. The explicit prune removes only unchanged skills that moved to the shared surface; `babysit-pr` and `thermo-nuclear-code-quality-review` remain desired Codex assets and are retained. Modified or foreign copies remain conflicts and are preserved. If an earlier consolidation preview removed either dependent skill from the Codex home, re-run the Codex installer before pruning the shared home so the provider copy is restored before its stale shared copy is removed.

## Update, prune or remove

Re-run the installer after updating your checkout. Install is copy-based and idempotent. Edit source files in this repository rather than installed copies; locally modified destinations are reported as conflicts and preserved.

`--dry-run` and `--diff` are read-only. `--prune` removes unchanged, previously managed files no longer in that home's catalog. `--uninstall` removes unchanged managed assets and reconciles managed Claude hook settings or Devin config values. Both preserve modified and foreign files. Preview either operation before applying it:

```bash
bash scripts/install-codex.sh --uninstall --dry-run --diff
```

The Claude installer merges its notification hooks while preserving unrelated settings. See the [installer contract](skill-installer-contract.md) for conflict handling and recovery.

## Recover a conflict

Use [diagnosis and recovery](development.md#diagnosis-and-recovery). Preserve modified/foreign bytes and the ownership ledger. A preview reports the actual conflict; it does not authorize broad replacement or erase historical ownership.
