# Project Gardening with BB Automations

Use this optional companion to hand [Project Gardening](project-gardening.md) to an agent setting up BB automation. The three-document core remains usable manually without BB. This recipe selects an existing environment and creates a paused, proposal-only agent job; it neither approves discovered repairs nor grants merge, installation or publication authority. The user approves a concrete discovered repair batch before execution.

## Read the native scheduler owner

BB's installed `automations` skill and current CLI help own scheduler contracts. Open that skill from the current BB agent session's available-skills location. Follow its `references/creation.md` for creation, `references/updates.md` before changing an existing job, and `references/script-runtime.md` for runtime or script questions.

```sh
bb skill list --project PROJECT_ID --environment ENVIRONMENT_ID --json
bb automation create --help
bb automation update --help
bb automation runs --help
```

The skill inventory identifies `automations`; its reported `filePath` can belong to the BB server rather than the execution host. Use the readable skill location supplied to the current session or read it on its actual host, rather than assume that path is local. Command help remains directly available. This recipe was checked against BB 0.49.0 / Automations 0.1.0 on 2026-11-17; reinspect the installed help after upgrades. Help and read-only discovery were exercised, but no job was created or run and runtime behavior is not qualified here.

## Bind the gardening inputs

Select the actual source checkout/environment and machine, its revision and pending bytes, applicable project instructions and a readable gardening instruction path. Reuse the selected existing environment; a new worktree from an older HEAD can omit accepted pending work. The BB project owns the schedule; the project's existing record owner may be elsewhere.

Name one relationship, its prior disposition, permitted cheap checks, record/output route and continuation owner. Agree the schedule/timezone and the explicit authorized provider, model, effort and permission mode for a **new** agent. Use `bb environment show ENVIRONMENT_ID --json`, `bb provider list --environment ENVIRONMENT_ID --json` and `bb provider models PROVIDER_ID --environment ENVIRONMENT_ID --json` to check the selected context and supported profile. A prompt or permission mode is not an operating-system read-only sandbox.

Before creating anything, inspect existing jobs and likely matches:

```sh
bb automation list --project PROJECT_ID --json
bb automation show AUTOMATION_ID --project PROJECT_ID --json
```

Match the source, relationship, record route, prompt and schedule; names alone do not identify a job. Reuse a suitable job only within actual update authority, using the native update reference. If creation acknowledgement is uncertain, reconcile list/show before another attempt and preserve the ambiguity if the ID cannot be established. Do not create duplicates or substitute a manual-run retry key for creation recovery.

## Prepare a paused new-agent job

Replace every uppercase token below, including those inside the literal prompt, with the actual selected values. The example's Monday 09:00 UTC schedule is illustrative. The creation profile applies to new threads; it is not permission to alter an existing thread's settings. `--prompt` takes literal text: keep shell expansion out of it, and pass longer file content as a literal argument rather than inventing a prompt-file flag.

```sh
bb automation create --project PROJECT_ID --name 'Weekly project gardening' \
  --disabled --cron '0 9 * * 1' --timezone Etc/UTC \
  --environment ENVIRONMENT_ID \
  --provider PROVIDER_ID --model MODEL_ID --reasoning LEVEL_ID \
  --permission-mode MODE \
  --prompt 'Read GUIDE_PATH and applicable project instructions at SOURCE_ROOT. In initial inspect/propose mode, examine RELATIONSHIP using only permitted cheap non-destructive CHECK_COMMANDS. Preserve pending work. Use RECORD_ROUTE and its prior dispositions; retain a proposed batch, useful no-change or partial coverage without duplicate work. Report to CONTINUATION_OWNER. Do not execute discovered repairs, change jobs, install, publish, merge, clean up or delegate.' \
  --json
```

Inspect the saved job with show and retain its ID, source/record bindings and remaining qualification in the existing setup record. Before authorized activation, inspect current runs and other writers: this recipe supplies no cross-job/shared-checkout lock or hard agent budget. Use the native references for overlap and retry guarantees; do not infer them from a schedule or prompt.

## Activate, inspect and continue within authority

After the saved configuration and activation authority are established, the relevant recipe steps are:

```sh
bb automation resume AUTOMATION_ID --project PROJECT_ID --json
bb automation runs AUTOMATION_ID --project PROJECT_ID --limit 10 --json
bb automation pause AUTOMATION_ID --project PROJECT_ID --json
```

Follow the run's associated thread to the retained result at RECORD_ROUTE. Confirm actual scope, evidence, proposed work/no-change/partial coverage and reuse of prior dispositions; a completed run alone proves none of those. A repair approval goes to its actual execution owner, leaving the recurring prompt in proposal mode. Pause future invocation when changing scope or investigating uncertain effects, then inspect active run/thread state; a paused schedule does not establish that ongoing work stopped. Preserve partial evidence and use the native runtime owner for stop/recovery details.

For an authorized manual continuation to an existing execution owner, use a scope-specific message file without settings overrides:

```sh
bb thread tell THREAD_ID --message-file /absolute/path/continuation.md --mode queue --json
```

Inspect queued delivery before resending. Omit model/effort overrides, including presumed matching or null settings; a settings change needs separate authority naming the exact target and values. Scheduled `--target-thread` preservation is not established by the inspected help/references. Verify actual dispatch preservation before enabling that optional route; otherwise use this manual continuation or an independently authorized new-thread job. The ordinary manual gardening route remains available without any schedule.
