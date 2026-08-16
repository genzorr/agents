# Skill Installer Contract

A durable, repo-neutral contract for how `repos/agents`, `repos/harness`, and `repos/session-harvester` install, update, prune, and uninstall the Codex/Claude assets they own. It defines the shared safety shape; each repository remains the source of truth for the assets physically present in that repository.

## 1. Purpose and ownership

Each repository manages only assets physically present in its own source tree. It never manages, prunes, or removes another repository's assets or a foreign/unknown installed asset such as `codex-primary-runtime`. Agents owns generic personal/global skills, commands, subagents, rules, Codex and Claude global instructions, Claude notification files, and explicitly cataloged traveling documents. Harness owns its `harness-*` assets and coupled Codex stop-gate files. session-harvester owns `skills/harvest-sessions/`.

Agents uses `catalog.json` as the sole desired-state authority. The catalog loader, installer engine, and validators derive identity, platform, sources, source layers, targets, adapters, and traveling documents from that file; the compatibility shell wrappers contain no asset allowlists or copy/prune logic.

## 2. Command surface

| Command | Mutates? | Meaning |
|---|---|---|
| `validate` | no | Validate catalog schema, source/target coverage, frontmatter, portability, traveling references, boundaries, and compatible state shape. |
| `--dry-run` | no | Report planned install, update, prune, uninstall, or adapter actions without creating directories, writing files, changing modes, merging settings, migrating state, or removing files. |
| `--diff` | no | Observational diff surface; implies `--dry-run`. |
| install/update | yes | Materialize current catalog desired state, adopt exact unrecorded outputs, update unchanged recorded outputs, and preserve/report conflicts. |
| `--prune` | yes | Remove only unchanged files recorded as Agents-owned that are absent from current desired state. |
| `--uninstall` | yes | Reconcile every recorded Agents-owned file, including assets removed from the current catalog, then remove state after successful reconciliation. |

Agents exposes the commands through `scripts/install-codex.sh` and `scripts/install-claude.sh`, which resolve the repository, resolve an interpreter through `scripts/lib/python.sh`, and `exec` `scripts/install-assets.py <platform>`. The interpreter is probed by execution rather than by `command -v`, because on Windows `python3` may be a Store alias stub that resolves and then exits without running; the probe also enforces the `requires-python` floor and fails closed with a single diagnostic when no candidate works. The engine is stdlib-only and uses `CODEX_HOME` or `CLAUDE_HOME`, defaulting to the real home only when an operator explicitly approves a live mutation.

On a native Windows host the POSIX wrappers are not a supported entry point: the `bash` on PATH is WSL, so it reaches neither the Windows home nor `powershell.exe`. The supported commands there are `scripts\install-claude.ps1` and `scripts\install-codex.ps1`, which dot-source `scripts\lib\python.ps1`, resolve an interpreter the same way (probing `py -3`, then `python3`, then `python` by execution against the same `requires-python` floor, because the Windows launcher finds a real install even when the alias stub shadows `python3`), forward every engine option unchanged, and propagate the engine's exit code. Both entry points run the same engine with the same platform argument and read the same `CLAUDE_HOME`/`CODEX_HOME` variables, set as `$env:CLAUDE_HOME`/`$env:CODEX_HOME`; the default homes are `%USERPROFILE%\.claude` and `%USERPROFILE%\.codex`. The POSIX wrappers keep their behavior unchanged.

```powershell
$env:CLAUDE_HOME = "$PWD\.scratch-home\claude"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-claude.ps1 --dry-run --diff
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-claude.ps1
$env:CODEX_HOME = "$PWD\.scratch-home\codex"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-codex.ps1 --dry-run --diff
```

## 3. Ownership and prune invariant

`prune` removes a target only when all three conditions hold: the target is recorded in `.agents-install-state.json` as Agents-owned, the target is absent from current catalog desired state, and its current SHA-256 digest and mode equal the last-installed record. A modified recorded target is reported and preserved. An unrecorded exact source match may be adopted during install; uninstall never adopts unrecorded files and removes a recorded file only when its current SHA-256 digest and mode equal the recorded signature. An unrecorded differing destination is an unmanaged conflict and is never overwritten.

The state requirement prevents current desired state from becoming historical ownership authority. State entries remain after normal installs when an asset leaves the catalog, so an explicit prune or uninstall can reconcile the historical output. Foreign, Harness-owned, session-harvester-owned, unrecorded, and legacy names remain untouched.

## 4. Scratch-home testing and live gate

Every mutation-capable command must be exercised against isolated scratch homes before a live run. Fresh-home tests must prove that `--dry-run` and `--diff` leave the home path absent, then prove install, second-install idempotence, update, prune, and uninstall behavior.

```bash
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --dry-run --diff
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --prune --dry-run
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh --dry-run --diff
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh --prune --dry-run
```

Running install, update, prune, or uninstall against the real `~/.codex` (runtime-home) or `~/.claude` (runtime-home) requires an explicit operator approval every time. Repository validation and all prescribed verification use scratch homes and must not mutate live global state.

## 5. Platform adapter safety

Codex writes global `AGENTS.md` and Claude writes global `CLAUDE.md` only when the destination is absent, empty, exactly matches the source and can be adopted, is recorded as unchanged, or has the exact platform header plus its managed ownership marker; other global instructions are preserved and reported. Codex permission-profile merging remains in `scripts/install-codex-permissions.py` and is not part of the generic engine.

Claude never overwrites `settings.json` wholesale. It merges the catalog hook fragment while preserving unrelated hook commands, and records the exact Agents commands and script target needed for later reconciliation. Invalid JSON, malformed adapter data, missing prerequisites, and modified historical Agents commands produce an unresolved conflict with non-success status; they do not authorize destructive cleanup. Uninstall removes only exact recorded or safely inferred Agents commands and preserves unrelated settings and hooks. Existing settings mode is preserved, and new settings use normal file-creation mode.

The current repository fragment gates only the merge/update path. A malformed fragment, or one whose command does not invoke the managed notifier, is an unresolved conflict for install and leaves the live adapter's wiring untouched, because a leaf the loader could not re-validate would make the next run reject its own state. Uninstall never reads the fragment, and prune still retires recorded hook leaves that no current fragment can claim, so a broken fragment cannot strand recorded state in a home.

The settings-hooks adapter is per-host. Its catalog entry declares one `posix-script` notifier, one `windows-script` notifier, and one `settings-hooks` fragment; the loader rejects any other shape and requires the two notifier targets to be `<name>.sh` and `<name>.ps1` twins. Both scripts are materialized in every selected home, so a home stays complete across platforms, and exactly one is wired into `settings.json`: the POSIX script under a POSIX `os.name`, the PowerShell script on native Windows, invoked explicitly through `powershell.exe` with a double-quoted native path. The unwired script is an inert installed asset, never referenced from configuration. Fragment text supports exactly one token, `__CLAUDE_NOTIFY__`, which becomes the host-selected notifier invocation rendered JSON-safely so a home containing a backslash or a double quote cannot corrupt the fragment. Adapter history records the wired `script_target` and derives the command form from that recorded target rather than the current host, so a home installed on one platform stays validatable, prunable, and uninstallable from the other. The twin of the recorded target is derived from its name, never read from state, so an installed state file cannot nominate an extra file as adapter-owned.

## 6. Desired catalog and source layers

Each catalog entry declares `id`, `kind`, `platforms`, `owner`, `source`, `install_target`, and optional `handling`, `tags`, and `$comment`. Any other key is rejected rather than ignored, so prose belongs in `$comment` and a new field must earn loader support. A source may be a file or complete directory; directory sources include every nested file, support asset, template, script, metadata file, and source mode. Ordered source-layer objects take `path`, `target`, and `role`, and may give each layer an explicit non-colliding target or an adapter-only role such as Claude settings hooks.

Install targets are relative to the selected platform home and never repeat `~/.codex` (runtime-home) or `~/.claude` (runtime-home). The loader rejects path traversal, absolute paths, missing or escaping sources, symlinked source trees, duplicate ids, duplicate targets, source-layer collisions, invalid platform declarations, incomplete physical coverage, and reserved cross-repository ids.

Document ownership follows the consumer that resolves the path. A skill-relative `docs/<name>.md` reference is an explicit source layer of that skill at `skills/<skill-id>/docs/<name>.md`, and its operative `docs/*.md` closure travels under the same skill root; a home-root copy does not satisfy that reference. A non-skill home-root consumer uses `kind: traveling_document` with an explicit platform target, as Claude's always-on model rule does for the model-and-effort document. Do not keep an additional home-root copy without a real home-root consumer. Runtime text scanning never decides what is installed. The transition reader accepts the old `.agents-doc-manifest` once, records its paths in historical state with a trusted-baseline marker, and removes the legacy file only after successful migration; an untrusted legacy baseline cannot authorize destructive removal.

## 7. Historical install state

Each selected home may contain `.agents-install-state.json` with `schema_version`, `owner`, `platform`, a path-keyed `files` object, and historical `adapters`. Each file record contains catalog asset id and kind, last-installed SHA-256, mode, explicit owner, and whether its baseline is trusted; adapter records contain exact structural hook-leaf identities and targets needed for safe retry and uninstall. State is historical ownership evidence, not a second desired-state catalog, and malformed or foreign records are rejected before mutation.

One identity migration is supported, because moving a notifier between catalog entries would otherwise leave a valid record that the identity check rejects before install, prune, or uninstall can reconcile it. A record adopts the current catalog identity only when the target is a settings-hooks adapter notifier, the record is intact Agents hook state with a trusted baseline and a non-foreign id, and its recorded signature equals the installed file or the current source byte for byte. Any other identity mismatch, an unprovable baseline, and a foreign id keep failing closed.

Normal install creates missing desired targets, adopts exact existing targets, updates destinations that still match the recorded digest and mode, and preserves/report modified or unmanaged conflicts. State is written atomically only after a mutating reconciliation; unresolved conflicts retain the state needed for retry. Prune removes unchanged stale entries and empty directories only after owned files are removed. Uninstall removes unchanged recorded outputs and adapter fragments, preserves modified outputs, and deletes state only when reconciliation has no unresolved conflict.

## 8. Validation behavior

`scripts/validate_catalog.py` and the installer load the same stdlib catalog module. Validation covers catalog schema and identity, bidirectional source coverage, complete directory expansion, frontmatter name/description identity, safe relative targets, source-layer collisions, explicit traveling references across skills/commands/subagents/rules/global instructions, boundary ownership, and install-state schema compatibility. `scripts/validate_skills.py` retains skill portability checks and invokes the catalog-backed text/reference validation. Cross-tree presence asymmetry is explicit and allowed; exact sharedness is established mechanically by PR B rather than free-text counterpart metadata.

## 9. Idempotency, conflict handling, and rollback

Install is copy-based and idempotent: unchanged source and mode produce no file action; source or mode changes update only unchanged recorded outputs. Conflicts produce a non-success disposition and fail-closed install behavior. Safe prune/uninstall actions may complete while modified stale paths remain recorded and reported for retry.

Rollback is to check out a known-good source commit and re-run the installer against the selected scratch or approved live home. A prior home backup may restore install outputs independently. There is no broad force flag: explicit operator action outside the installer is required for a destination that cannot be proven Agents-owned.

## 10. Per-repository applicability

| Repository | Managed set | Validate | Install | Update | Prune | Uninstall |
|---|---|---|---|---|---|---|
| agents | `catalog.json` assets, explicit traveling documents, and historical state | yes | yes via shared engine | re-run install | yes | yes |
| harness | physically present `harness-*` assets and coupled files | repository-native | yes | re-run install | yes | deferred unless its contract changes |
| session-harvester | `skills/harvest-sessions/` complete directory | repository-native | yes | re-run install | yes within owned directory | yes |

## References

- `catalog.json` — Agents desired-state catalog.
- `scripts/agent_catalog.py` — shared catalog model, validation, and expansion.
- `scripts/install-assets.py` — shared stdlib installer engine.
- `scripts/validate_catalog.py` and `scripts/validate_skills.py` — repository validation surfaces.
- `repos/harness/scripts/install-claude.sh` and `install-codex.sh` — historical source of the platform safety guards preserved here.
