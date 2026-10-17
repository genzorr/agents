# Pi instruction and skill distribution

Pi assets use the existing catalog engine and its `.agents-install-state.json` ownership record. The asset entrypoint is `scripts/install-pi-assets.sh`; the separate `scripts/install-pi.py` owns optional permission setup and explicit retirement of historical account outputs. The standalone [pi-accounts](https://github.com/genzorr/pi-accounts) repository owns account tooling and maintenance. Each installer retains its own ownership boundary. Catalog install, prune and uninstall do not read or modify Pi settings, credentials, accounts, sessions, permission extensions, maintenance units, or the optional setup's ownership record.

## Managed assets and discovery

The operator's usage-selected initial manifest contains nine Pi-home skills plus six independently managed shared-home discoveries. The source selection is finalized for this initial set; live migration and installation require explicit operator authorization.

The Pi home defaults to `~/.pi/agent`; `PI_CODING_AGENT_DIR` selects another home. Supported Linux path spellings include `~`, `~/...`, paths relative to the current directory, and local `file:///...` URLs with percent-encoded spaces. Tilde expansion uses the process home. Symlinks are not followed during normalization. Unsupported remote hosts, encoded slashes, malformed escapes and backslashes in file URLs are rejected. This migration and its native verification target Linux; native Windows and Mac setup have not been qualified.

The catalog installs Pi's own `AGENTS.md`, four home guidance documents, and nine complete skills under `skills/`. It preserves Pi's normal system prompt and does not write `SYSTEM.md`.

| Pi skill | Source reused without transformation |
|---|---|
| `diagnose`, `archify` | Existing complete Codex source directories; Archify retains all renderer resources and MIT license |
| `review-change`, `integrate-research`, `distill-source`, `architecture-review` | Existing complete Codex source layers, including their traveling documents |
| `explain`, `ask-chatgpt-pro` | Existing complete Claude source layers, using shared bodies and references without Codex metadata overlays |
| `surface-unknowns` | Existing shared body with native explicit-only frontmatter; no Codex metadata overlay |

Archify ships its full renderer source and lockfile but no installed `node_modules` or D2 executable. For a scratch qualification, run `npm ci --ignore-scripts` from that scratch home's `skills/archify` directory before rendering and validating. Use the same prerequisite only in an explicitly authorized live skill directory. Without AJV, the native renderer warns and skips schema validation even when CLI validation returns success; do not report that as full validation. A local D2 executable is required for D2 or combined output. See the [qualification limits](pi-assets.md#invocation-and-unsupported-routes) for tested versions and browser coverage.

The home guidance consists of `docs/context-file-authoring.md`, `docs/skill-authoring-principles.md`, `docs/claim-discipline.md`, and the conditional `docs/experiment-protocol-readout-contract.md`. Skill-local guidance stays under the skill that consumes it. `catalog.json` is the exact source and target authority.

Pi natively discovers the separately managed `~/.agents/skills` home. Its six cataloged skills are `design-experiment`, `docker-optimize`, `logging-optimize`, `piecemeal-growth`, `review-experiment`, and `skill-lifecycle`; install/update them through `scripts/install-agents.sh`. The Pi installer does not copy or prune them. Catalog validation rejects an asset declared in both the shared-home and Pi skill sets, because discovery selects complete skills rather than merging overlays. A skill's physical shared source directory does not imply that it belongs in the shared installed home.

`tdd`, `text-prune` and `ask-oracle` are deferred Pi additions; their existing source and other-provider distributions remain intact. Workers, an ordinary Pi session route followed by feature orchestration, and later Impeccable UI integration remain scoped backlog. The four core Harness workflows are user-required and implemented/reviewed separately in their owning repository; they are not supplied or qualified by this Agents manifest. Other skills, plugins, Harness assets and Codex-only orchestration remain outside this distribution. See the [compatibility and deferred-scope assessment](pi-assets.md) for the selected distillation workflow's conditional limits. Cross-references to optional workflows do not promise that those workflows or their external executables are installed. See the [Pi global instructions](../pi/AGENTS.md) for invocation, authorization, source ownership and child boundaries. Project `AGENTS.md` files load through Pi's native context discovery and do not need conversion. Global skills and project resources have different trust requirements; approve only the intended project through Pi's normal trust interaction rather than globally trusting arbitrary repositories.

## Scratch installation and updates

Preview against isolated homes first:

```bash
PI_CODING_AGENT_DIR=/tmp/pi-asset-trial bash scripts/install-pi-assets.sh --dry-run --diff
PI_CODING_AGENT_DIR=/tmp/pi-asset-trial bash scripts/install-pi-assets.sh
PI_CODING_AGENT_DIR=/tmp/pi-asset-trial bash scripts/install-pi-assets.sh
PI_CODING_AGENT_DIR=/tmp/pi-asset-trial bash scripts/install-pi-assets.sh --uninstall --dry-run
PI_CODING_AGENT_DIR=/tmp/pi-asset-trial bash scripts/install-pi-assets.sh --uninstall
```

When reconciling a scratch home installed from the earlier eight-Pi-skill candidate, preview `--prune --dry-run --diff`, then apply `--prune` only against that scratch home. The selected manifest adds `distill-source`, `architecture-review`, `surface-unknowns` and `archify`, and retires the Pi copies of `tdd`, `text-prune` and `ask-oracle`. Unchanged recorded retired files are removed; modified recorded files remain conflicts and foreign content is preserved. Retained modified copies can still be discovered by Pi, so report that unresolved home instead of claiming its discovery set is fifteen. Do not delete shared-home skills or other-provider copies to match the selected Pi manifest.

Updating an unchanged home from the earlier selected six-Pi-skill snapshot adds `architecture-review`, `surface-unknowns` and `archify` without retiring any of those six skills. Preview and apply through the same scratch `--prune` path; additions do not authorize removing foreign files or changing the separately managed shared home. Surface-unknowns remains explicitly invokable but is excluded from the model-facing skill metadata prompt. Its shared-source frontmatter also strengthens Claude enforcement of the existing explicit-only trigger; Codex retains its existing overlay policy.

The existing engine adopts exact source matches, updates unchanged recorded files, and preserves modified or unmanaged files as conflicts. A foreign or mismatched-platform ownership record is rejected. `--diff` implies a read-only dry run and does not create a fresh home. `--prune` removes unchanged stale owned files; `--uninstall` removes unchanged recorded assets. Both preserve foreign files and modified owned files, retaining ownership evidence for unresolved conflicts. For source-version rollback, rerun from a known-good source revision with the same selected home and ownership record.

## Explicit migration of provisional Codex references

The optional migration command exits before accessing homes on unsupported platforms and handles only the known provisional Linux Pi arrangement: `AGENTS.md` symlinked to an explicitly supplied Codex home's `AGENTS.md`, `docs` symlinked to that home's `docs`, and one exact absolute Codex `skills` string in Pi `settings.json`. It compares link text lexically and never reads the Codex destinations. Relative symlink text is supported when it resolves lexically to the exact expected destination. Missing links or entries are allowed. Foreign links/files, malformed settings, duplicate matching entries, and an existing asset ledger cause a conflict before changes.

Close Pi/T3 sessions that could save these settings. For a synthetic trial, create these provisional surfaces in scratch homes and substitute those homes below. After explicit approval for live migration, the concrete commands are:

```bash
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex" --dry-run
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex"
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh --dry-run --diff
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh
AGENTS_HOME="$HOME/.agents" bash scripts/install-agents.sh --dry-run --diff
# Apply a shared-home update only after reviewing that separate preview:
AGENTS_HOME="$HOME/.agents" bash scripts/install-agents.sh
```

Apply these commands only within explicitly authorized live setup. Review the separate shared-home preview because an update can affect other runtimes that discover that home. Start a fresh Pi process to load the installed instructions and skill set, then verify the global/project context and the native skill picker. No OAuth, model inference, account selection or timer changes are part of this migration.

Before detaching anything, migration writes a private `.agents-pi-migration.json` record inside the selected Pi home. It records only the expected home identities, original link text, the removed skill entry's position, and transaction stage. It does not back up credentials or the entire settings file. Successful repeated migration is a no-op. An interrupted migration leaves a prepared record; use the explicit rollback below before retrying. Do not delete or rewrite the record to bypass a conflict.

## Narrow migration rollback

Remove the catalog-owned outputs first; the rollback refuses to overwrite installed instruction files, documentation directories, or foreign replacements:

```bash
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh --uninstall --dry-run
PI_CODING_AGENT_DIR="$HOME/.pi/agent" bash scripts/install-pi-assets.sh --uninstall
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex" --rollback --dry-run
python3 scripts/migrate-pi-assets.py --pi-home "$HOME/.pi/agent" --codex-home "$HOME/.codex" --rollback
```

Rollback restores only the recorded symlinks if their destinations remain absent or already match the original link text. It reinserts only the recorded Codex skills entry and preserves unrelated settings edits, including the optional permission extension, selected model/effort, packages and other skill paths. If `settings.skills` was removed or changed to an invalid shape, rollback stops for explicit resolution. Foreign or modified content causes a conflict and leaves the migration record available for recovery. It never recursively deletes directories or overwrites a foreign ownership record. A partial rollback can be retried: already-restored exact links and the exact skill entry are accepted. After successful restoration, the migration record is removed.

Migration records are written before effects and files are replaced atomically. An ordinary failure can leave a partially detached arrangement with a recoverable record; it does not automatically rerun or invoke the asset installer. Run asset installation, migration and rollback sequentially; concurrent setup invocations are not coordinated. Keep Pi closed while migrating or rolling back. Migration does not coordinate concurrent external settings writers; it rechecks the original settings bytes before replacement and fails if they changed. These are process-failure recovery bounds, not disk-corruption guarantees. If the generic asset installer itself fails before its ownership-state commit, rerun it to adopt unchanged exact outputs before attempting uninstall; preserve conflicts rather than deleting state or forcing removal.
