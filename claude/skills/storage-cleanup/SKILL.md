---
name: storage-cleanup
description: Inspect disk usage, identify reclaimable caches and generated artifacts, and safely execute an explicitly approved cleanup plan. Use when the user asks to free disk space, investigate what is consuming storage, clean development caches/build outputs, or reduce local storage usage. Inspection is read-only by default; never delete agent session/history data or other protected user state.
disable-model-invocation: true
---

# Storage Cleanup

Diagnose storage pressure and reclaim space without turning “old” or “large” into permission to delete data.

**Composition role:** Driver. Own inspection, candidate classification, the approval boundary, approved cleanup, and verification for this storage-maintenance task.

## Hard Invariants

- **Agent session/history data is protected.** Never delete or propose deleting Codex, Claude, or other agent session history, transcripts, checkpoints, conversation/context stores, resumability state, or audit/history records. Age, completion status, inactivity, or size does not make this data disposable. If the user wants a separate retention-policy discussion, route it outside this skill; this skill does not perform that deletion.
- **Inspection is read-only.** Until the user approves a concrete cleanup plan, do not delete, prune, uninstall, compact, truncate, vacuum, rewrite, or otherwise mutate storage state.
- **Unknown or user-authored data is protected by default.** Do not classify repositories, documents, downloads, datasets, model/checkpoint files, virtual environments, dependency trees, application state, credentials, or other content as disposable merely because it is large or old.
- **No blanket temp-directory cleanup.** Temporary locations may contain live sockets, locks, active job state, unsaved work, or another application's files. Only propose exact temp paths proven to be owned by a completed/disposable workload.
- **No autonomous recurring cleanup.** Do not create cron, launchd, scheduled tasks, login hooks, or background cleaners through this skill. A recurring maintenance mechanism is a separate explicitly requested change.

## Workflow

1. **Establish the target and pressure.** Identify the operating system, relevant filesystem/volume, free space, and whether the user wants diagnosis only or space reclamation. Prefer read-only filesystem and tool-native status commands. Done when the affected volume and current free/used space are known.
2. **Find the real consumers.** Start broad enough to locate the largest directories/files, then narrow by directory rather than recursively inspecting the whole machine without cause. Include hidden development/tooling locations when relevant. Record measured sizes; do not infer reclaimable bytes from reputation or age. Done when the major contributors to the storage problem are accounted for or explicitly inaccessible.
3. **Attribute ownership and semantics.** Determine what created each material candidate and whether it is canonical data, a cache, generated output, a local dependency copy, a container artifact, a log, or unknown state. Prefer tool-native metadata/status commands and current help/documentation when cleanup semantics are uncertain. Done when every proposed candidate has an owner and a consequence of deletion.
4. **Classify candidates conservatively.** Use the categories below. When evidence is insufficient, classify as protected/unknown rather than guessing. Done when every material candidate has exactly one disposition.
5. **Present the cleanup plan and stop.** Show candidate path or tool scope, measured size, classification, reason, deletion consequence, regeneration/redownload cost, proposed exact action, and confidence. Separate estimated reclaimable bytes from merely observed bytes. Ask for explicit approval of the specific candidate(s) or bounded group(s); a general request to “clean up space” is not approval for every discovered deletion. Do not execute cleanup in the same step that first presents the plan unless the user had already explicitly authorized those exact actions.
6. **Execute only the approved subset.** Re-check that the target still exists and that its meaning has not materially changed. Prefer the owning tool's documented cleanup command over broad filesystem deletion. Use the narrowest path/scope possible; avoid force flags, recursive globs, elevated privileges, and global prune commands unless they are necessary, explained, and explicitly approved. Stop if the command would touch unapproved state.
7. **Verify.** Re-measure the filesystem and cleaned scopes, report actual reclaimed space, note anything skipped or failed, and confirm protected categories were untouched. Do not manufacture a success claim from command exit status alone.

## Candidate Classification

- **Reconstructable cache/generated artifact:** Usually reasonable to propose when its owner and regeneration behavior are known, such as compiler/build caches, package-download caches, generated build outputs, or tool caches. Still disclose redownload/rebuild cost and use the native cleaner when available.
- **Conditional local state:** Non-agent logs, Docker images/build cache, dependency directories, environments, simulator/emulator data, IDE/build-system state, downloads, or other regenerable-looking content can be expensive, offline-critical, or still in use. Propose only with evidence about current use and consequence; never auto-delete.
- **Protected/unknown:** Agent session/history state and logs; user-authored files; source repositories; credentials; application databases/state; unique datasets/checkpoints; backups; or anything whose ownership, canonical copy, or recovery path is uncertain. Do not propose deletion through this skill.

## Cleanup Plan Output

Before any deletion, return a compact table or equivalent with:

- candidate path or tool scope;
- measured size;
- classification;
- why it appears reclaimable;
- what breaks or must be rebuilt/redownloaded if removed;
- exact proposed cleanup action;
- estimated reclaimable space and confidence.

Then state the **protected items explicitly excluded**, including agent session/history data when present, and ask for approval of the concrete cleanup subset.

After approved cleanup, report measured before/after free space, actual bytes reclaimed where measurable, actions performed, actions skipped/failed, and any residual large consumers worth reviewing.

## Guardrails

- Do not use modification/access time alone to decide that content is unused.
- Do not treat a duplicate-file detector as permission to delete either copy; ownership and canonicality must be established first.
- Do not empty trash/recycle bins, remove snapshots/backups, uninstall applications, or prune package/container state unless that exact class was included in the approved plan.
- Do not use `sudo` or equivalent elevation for cleanup unless the user explicitly approves the exact elevated action and the ownership/impact is understood.
- Prefer reversible or tool-managed cleanup where available, but do not misrepresent a cache purge as reversible if it requires redownload/rebuild.
- If deletion semantics are ambiguous, stop at the diagnosis/report rather than guessing.
