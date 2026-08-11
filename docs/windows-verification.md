# Windows verification report

State of the `windows` branch as verified on a real Windows host. Update it when the
branch takes a new upstream merge or gains a platform guard; a claim here without a
command behind it is worse than no claim.

## Host

| | |
|---|---|
| OS | Windows 11, build 10.0.26200 |
| Python | 3.14.3 |
| git | 2.53.0.windows.1 |
| MSYS bash | GNU bash 5.2.37, `x86_64-pc-msys` (Git for Windows) |
| Shell for `.ps1` | Windows PowerShell 5.1.26100; no `pwsh` installed |

`bash` on this host's PATH is `C:\Windows\System32\bash.exe` — the WSL launcher, not the
MSYS bash above. Everything that runs a shell wrapper resolves the MSYS one explicitly.

## Result

| Check | Command | Result |
|---|---|---|
| Test suite | `python -m pytest tests/ -q` | **127 passed, 12 skipped, 0 failed** |
| Catalog | `python scripts/validate_catalog.py` | OK, 1 warning |
| Skill frontmatter | `python scripts/validate_skills.py` | OK, 5 warnings |
| Prune safety | `bash scripts/test-prune-safety.sh` | OK |
| Cross-repo consistency | `python scripts/check_cross_repo_consistency.py` | 2 errors — see below |
| Lint | `python -m ruff check .` | 3 errors — see below |

The suite failed 55 before the two test commits on this branch.

## Not green, and why

**Cross-repo consistency** reports `repo not found` for `claude-headless` and
`session-harvester`. The check expects sibling repositories that are not cloned on this
host. It is an environment gap, not a branch defect, and it reproduces on `main`.

**`ruff`** reports three `F841` (unused locals) in `scripts/validate_skills.py` and
`tests/test_installer_engine.py`. All three are present on the parent commit — verified by
running `ruff` against `git show <parent>:<file>` — and are left alone rather than fixed
as drive-by work.

## Defect classes found and fixed

**Path separators against a catalog.** `_physical_asset_paths` built keys with
`str(path.relative_to(repo))`, which uses the native separator, while catalog source paths
are always forward-slashed. On Windows every comparison missed and the validator reported
the entire tree as uncatalogued. The same defect existed in the pre-rewrite
`check_disk_coverage`; the installer rewrite moved the logic without it.

**A path substituted into raw JSON.** The home token is replaced in the fragment text
*before* it is parsed, so the value must survive as JSON, not merely as a shell word. A
Windows home is backslash-separated and produced invalid `\escape` sequences, failing the
whole install. The same hazard exists on POSIX for any path holding a backslash or quote.

**`python3` assumed present.** The wrappers exec it unconditionally. Windows ships no
`python3`; the name resolves to a Microsoft Store alias stub that sits on PATH — so
`command -v python3` *succeeds* and the install then dies with an advert and a nonzero
exit. Interpreters are now probed by execution.

**A POSIX-only hook command wired on Windows.** Hook lists in `settings.json` merge by
appending, so the shell notifier's invocation would land beside a working PowerShell one
and fire a broken hook on every event. Resolved upstream by the per-host adapter: one
catalog entry declares a `posix-script`, a `windows-script`, and one fragment; both are
materialized in every home and only the host's form is wired.

**Test harness assumptions (54 tests).** The suite invoked `bash <native path>` with a
colon-joined `PATH` naming `/usr/bin:/bin`. Backslashes are escapes to bash; `bash` on
PATH is WSL, whose userland is not the profile being installed into; and that PATH shape
is meaningless to a native process. The suite now resolves an MSYS bash by userland,
passes POSIX separators, and builds the search path per platform. One interpreter stub
also embedded `sys.executable` raw, so its backslashes were eaten by the shell running it.

**CRLF checkout (1 test).** A test pins the sha256 of a skill file. Under
`core.autocrlf=true` the checked-out bytes differ from the blob, so the digest never
matched. Fixed with `.gitattributes` (`* text=auto eol=lf`) rather than by weakening the
assertion — the pinned digest is the point of that test.

## The 12 skips

They assert **POSIX-host behavior**, not incidental POSIX assumptions: that the shell
notifier is the one wired into `settings.json`, that the home path is single-quoted, that
mode bits survive an update. On a Windows host the engine correctly does something else,
so a failure there would be a false signal. Each is marked `skipIf(os.name == "nt")` with
that reason in the message, so an operator sees why rather than a red result they cannot
act on.

Coverage for the Windows side of those behaviors is thinner than for POSIX. What exists is
verified by hand below; a Windows-host variant asserting the PowerShell wiring would close
the gap.

## Verified by hand

Installing into a fresh empty `CLAUDE_HOME` with `install-claude.ps1` under PowerShell
5.1, no `pwsh` present:

- both notifiers materialized — `hooks/notifications.ps1` and `hooks/notifications.sh`
- exactly one command per event, all four wired to the `.ps1`
- the rendered command carries a backslash Windows path inside `settings.json`, and the
  file parses as JSON
- `install-codex.ps1` likewise exits 0; `Resolve-AgentsPython` selects `py -3`

Separately confirmed that installing over a home whose hooks were hand-written leaves
**two** commands per event: the merge only appends, and hand-added leaves are outside
recorded adapter state, so nothing reclaims them. Adopting managed hooks means removing
the hand-written block first.

## Compatibility with POSIX

Every guard is either behind `os.name != "nt"` or a no-op elsewhere: `as_posix()` returns
the same string, `shell_search_path` reproduces exactly the previous
`f"{path}:/usr/bin:/bin"`, and the bash resolver returns plain `bash`. `.gitattributes`
changes nothing where files are already LF.

Pulling this branch on Linux triggers a checkout renormalization. The diff should be
empty; `git add --renormalize .` settles it if `git status` disagrees.
