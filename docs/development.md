# Develop and maintain Agents

Work in the task-selected source checkout and read [AGENTS.md](../AGENTS.md). The [installer contract](skill-installer-contract.md) owns catalog and reconciliation behavior. No private record store is needed for public contributions.

## Checks

From the selected source root, run the checks relevant to the change:

```bash
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
bash scripts/test-prune-safety.sh
```

Exercise installer changes against scratch homes before any live installation. Cross-repository ownership checks and optional local work tracking are maintainer checks documented in [AGENTS.md](../AGENTS.md).

The existing CI workflow runs these validators, tests and installer-ownership checks on Python 3.9 and 3.13. It checks the advertised minimum Python version independently of the maintainer's current interpreter. The workflow selects Ubuntu 22.04 because the [published Python builds](https://github.com/actions/python-versions/blob/main/versions-manifest.json) include that version pair there; moving `ubuntu-latest` to 26.04 made Python 3.9 setup fail before tests ran. To check minimum-version compatibility locally with a uv-managed interpreter:

```sh
uv run --python 3.9 --no-project python -m unittest discover -s tests
```

## Local outputs and retention

Installer previews use the explicit home variables in [installation guidance](installation.md#preview-the-selected-provider); scratch packaging checks use ignored `.scratch-home/` (or an explicitly selected scratch home), and unit tests use temporary fixtures. Record substantial attempts under distinct task/attempt subdirectories, keeping the actual host/path and decisive result in the existing work record. Keep review/recovery evidence through its consumer; record remaining owner and release/reassessment condition before proposing removal. Installed homes and their ownership ledgers are operational state, not task scratch; do not move or delete them as artifact cleanup. Small receipts may stay with the issue/PR or local task; bulky logs and bundles stay in the chosen scratch location. No remote storage binding is required by these local checks.

## Diagnosis and recovery

For catalog, missing-source, portability, or traveling-reference failures, run the validators above from this checkout; they report the affected asset/path. For an install conflict, select the actual destination home that reported the conflict, using the relevant home variable, and run its owning installer's native `--dry-run --diff` preview from this source checkout. The preview reads that home's destinations and ownership ledger without changing them. A successful preview has no unresolved conflicts in the inspected home and exits zero; a conflict preserves the destination and reports a non-success result.

Use scratch homes for isolated reproduction and installer verification. An empty scratch home has neither the conflicting destination nor its ownership ledger, so a successful scratch preview does not show that the actual selected home's conflict is resolved.

Current desired assets come from `catalog.json`; each selected home's `.agents-install-state.json` records historical ownership and last-installed signatures. Use [the installer contract](skill-installer-contract.md) to distinguish a modified owned file, an unmanaged destination, and an invalid ledger or adapter. Do not delete or rewrite state to bypass a conflict: it is the evidence prune/uninstall need for safe recovery. There is no force option. Restore a known-good source version and preview reconciliation, or have the operator resolve the conflicting destination explicitly. Live-home mutation still requires operator approval.

Keep symptom, command/environment, decisive evidence, cause or remaining hypotheses, and outcome in the existing project work record. Local maintainers use ignored `docs/harness/` when present; public contributors can use the issue or PR record. Promote only verified reusable conclusions into current guidance, and update that guidance when a command or recovery boundary changes.

## Check guidance and distribution

Follow one representative reader task through the actual entry, behavior/command owner and recovery route. Check that prerequisites and next actions are usable; green links alone cannot establish this. Use existing project validators and meaningful checks, without assertions that merely freeze prose.

For reference changes, inspect the path the consumer resolves: provider-home docs for globals, support files under the skill root for a skill. Verify both clickable links and operative code-formatted dependencies in the literal delivered bundle. The [portable copy set](project-guide-distribution.md) and cataloged support layers are distinct distribution surfaces; one does not prove the other. Preview and exercise the affected normal installers in scratch homes before live adoption under actual authority.
