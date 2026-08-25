# Orchestrate Feature — Technical Specification

## Authority And Scope

This specification implements, hardens, and generalizes the product contract in `docs/orchestrate-feature-prd.md`. T-36 owns the initial outer skill, T-38 owns callback delivery and fork discipline, T-39 owns generic naming, role profiles, inner-lens extraction, compatibility, and migration, T-41 owns operator-only reviewer activation, and T-42 owns feature-owner delegation. The PRD controls product behavior; this document controls the bounded repository change. When they conflict, stop and correct the documents before implementation.

## Source Ownership

Canonical Codex-only outer skill after T-39:

- `codex/skills/orchestrate-feature/SKILL.md`
- `codex/skills/orchestrate-feature/agents/openai.yaml`

Canonical Codex-only generic inner lens after T-39:

- `codex/skills/orchestrate-workers/SKILL.md`
- `codex/skills/orchestrate-workers/agents/openai.yaml`
- `codex/skills/orchestrate-workers/references/independent-reviewer-protocol.md`

Remove:

- `codex/skills/orchestrate-sol-feature/`
- `codex/skills/sol-luna-orchestration/`

Modify only as needed:

- `catalog.json`
- `tests/test_goal_prompt_contracts.py`, or one narrowly named new test module if separation materially improves clarity
- `docs/orchestrate-feature-prd.md`
- `docs/orchestrate-feature-spec.md`
- Harness-owned records for S-27/T-39 through Harness CLI operations

Do not add custom agents, runtime controllers, configuration, Claude counterparts, or nonstandard dependencies.

## Initialization And Migration

The outer skill is a rename/generalization of an existing source asset; do not initialize a duplicate skeleton. Initialize the new `orchestrate-workers` skill through the system `skill-creator` initializer with only the `references` resource because this is a genuinely new canonical skill. Generate its UI metadata with the repository's authoring tooling, then replace any placeholder content completely.

Use apply-patch-compatible file moves or deliberate add/delete changes so Git records the outer skill and reviewer protocol as renames when similarity permits. Do not retain the old outer path or the retired preset as a shim or alias.

## Canonical Outer Skill Metadata

Frontmatter contains only `name` and `description`.

```yaml
name: orchestrate-feature
```

The description must state:

- It dispatches or reuses one ordinary profiled feature-owner task from a long-lived project orchestrator.
- It configures the feature owner to use reusable native profiled workers and an independent reviewer only when the operator explicitly requests one through `orchestrate-workers`.
- Defaults are Sol/medium owner and Luna/xhigh workers with feature-owner self-review; an explicitly requested reviewer defaults to Sol/high, and explicit per-feature role overrides are allowed.
- It applies only after explicit invocation of `orchestrate-feature` or an explicit request for this exact topology.
- Invocation authorizes one resolved feature lane but does not mutate the current orchestrator or broaden project/Git/worktree/external-write/live-install authority.

Required UI semantics:

```yaml
interface:
  display_name: "Orchestrate Feature"
  short_description: "Launch feature owners with opt-in review"
  default_prompt: "Use $orchestrate-feature to launch or resume this agreed feature with feature-owner self-review unless I explicitly request an independent reviewer."
policy:
  allow_implicit_invocation: false
```

## Generic Inner Lens Metadata

Frontmatter contains only `name` and `description`.

```yaml
name: orchestrate-workers
```

The description must state:

- It is a generic current-task lens for profiled native implementation workers, optional explicitly requested ordinary implementation tasks, and an independent reviewer only when the operator explicitly requests one for the resolved task.
- It owns decomposition, continuity, context, evidence, optional-review routing, and acceptance without changing the current coordinator's profile or lifecycle driver.
- Defaults are native Luna/xhigh implementation workers with coordinator self-review; an explicitly requested reviewer defaults to native Sol/high. Another exact enabled-role profile requires explicit operator instruction or an operator-authorized launch contract, while the ordinary implementation-task route always requires a separate explicit operator request.
- It applies only after explicit invocation of `orchestrate-workers` or a relayed invocation in an operator-authorized feature launch.

Required UI semantics:

```yaml
interface:
  display_name: "Orchestrate Workers"
  short_description: "Delegate work with opt-in independent review"
  default_prompt: "Use $orchestrate-workers to delegate this resolved task and keep review with the coordinator unless I explicitly request an independent reviewer."
policy:
  allow_implicit_invocation: false
```

## Composition Roles

- `orchestrate-feature`: helper. The project-orchestrator driver retains program lifecycle, authority, priority, and completion ownership; the helper owns bounded launch readiness, profile/delivery resolution, feature-task dispatch/reuse, and handoff routing.
- `orchestrate-workers`: lens. The current task driver retains lifecycle, success, and acceptance; the lens changes decomposition, delegation, context, evidence, and explicitly requested independent-review routing.
If a governing driver forbids task creation, delegation, or the proposed lifecycle change, stop rather than displacing it.

## Required Terms

Define compactly in the applicable skills:

- `Project orchestrator`: current long-lived task preserving program context and decisions.
- `Feature owner`: ordinary task at the resolved owner profile that owns one feature's detailed lifecycle and feature-level acceptance.
- `Coordinator`: current task applying `orchestrate-workers`; in the outer topology this is the feature owner.
- `Implementation worker`: selected native leaf subagent or separately operator-requested ordinary implementation task at the resolved worker profile.
- `Independent reviewer`: separate native leaf identity at the resolved reviewer profile, disabled unless the operator explicitly requests it for the resolved task.
- `Role profile`: exact route when applicable, model identifier, and effort for one role, plus default/override provenance.
- `Role map`: immutable current-orchestrator profile plus independently resolved feature-owner and worker profiles, reviewer activation, and reviewer profile only when activated.
- `Launch contract`: authoritative context, scope, state, authority, role map, success, verification, stop, and notification packet sent to a feature owner.
- `Notification contract`, `Supervision state`, `Bounded active wait`, `Fork`, `Reset`, and `Recycle`: preserve the reviewed T-38 meanings.

Do not create a profile registry or new route taxonomy beyond the four delivery modes and the inner native/explicit ordinary implementation routes.

## Outer Activation And Readiness

On explicit invocation:

0. Confirm a separate feature owner has material value because the work is multi-phase, context-heavy, has multiple coherent assignments, can progress independently, or the operator explicitly requested this topology. Otherwise recommend contained work and return.
1. Confirm the current session is the project orchestrator rather than a feature owner/child created by this topology. Refuse nested ordinary feature-task creation.
2. Inspect the native current-profile/status surface when exposed. Preserve the current model and effort. If the operator named an orchestrator requirement, validate it as a precondition; mismatch stops rather than mutating the session.
3. Resolve objective, durable authority, start state, scope/shared ownership, operational authority, success, verification, stop gates, fresh-context mode, notification contract, and complete role map.
4. Inspect governing driver, project instructions, saved-project metadata, repository, checkout/worktree policy, and active durable writers. Stop when the driver forbids dispatch.
5. Recover locally answerable gaps and use existing durable authority. Create/update the smallest project-owned task/specification only when needed and allowed; never create an orchestration ledger.
6. Require callback, practical bounded active waiting, another product-validated mechanism/target, or explicitly accepted manual supervision before every new or reused dispatch.
7. Return without task creation for unresolved user-owned/difficult-to-reverse launch choices or an unavailable exact role profile/route/context capability.

Activation applies to one resolved feature. Another feature requires a fresh invocation and fresh role-map resolution.

## Role-Profile Resolution

Default map:

```text
project orchestrator: current task model / current effort (immutable)
feature owner: gpt-5.6-sol / medium
implementation worker: gpt-5.6-luna / xhigh
independent reviewer: disabled; when explicitly requested, gpt-5.6-sol / high
```

Accept only explicit, unambiguous natural-language overrides tied to the current feature. Owner and worker overrides may also come from a durable operator decision governing those roles. Reviewer activation may come only from the current operator invocation or an authoritative operator decision explicitly scoped to the resolved feature; standing or global reviewer preferences never activate review. Resolve each role independently:

- An owner override changes only the new feature-owner creation profile.
- A worker override changes only implementation worker route/model/effort passed to the inner lens.
- A reviewer profile instruction activates review and changes only the independent reviewer model/effort passed to the inner lens.
- An orchestrator requirement validates current state and never becomes a mutation request. If the native surface cannot observe an explicit requirement, stop; without an explicit requirement, report the limitation and preserve the current task.
- An omitted model or effort inherits that enabled role's default; it never inherits another role's override. Reviewer controls remain unresolved while review is disabled.
- An override never waives a governing driver/project requirement for a particular role profile; conflict stops at readiness.

Echo the complete map with `disabled`, `default`, or `operator override` provenance before dispatch. Feature-detect exact model, effort, route, and context controls only for enabled roles. If any selected exact value cannot be set or validated, stop. Never silently substitute, normalize to a different profile, raise/lower a selected profile, or claim post-creation readback when only request validation exists. Task size, importance, risk, ambiguity, missing oracles, cross-worker boundaries, agent judgment, reviewer availability, or a generic driver preference never activates review; a driver requirement without explicit operator authorization stops for operator direction.

## New Feature Dispatch

1. Resolve callback identity/action only when callback is selected; otherwise resolve the selected delivery mechanism and target without fabricating an origin route.
2. Use native `create_thread` with fresh context, never a native subagent spawn or `fork_thread`.
3. Select the exact resolved feature-owner model and effort rather than the old hard-coded owner profile.
4. Resolve saved project/environment and exact existing branch/ref or intended working-tree state under user/project policy. Personal OS-managed repos use the existing checkout without explicit worktree authority.
5. Give the task a concise project-and-feature title.
6. Send only the complete Feature Owner Launch Contract. Do not inherit or paste parent history.
7. Treat creation validation as profile provenance, not independent metadata readback. Distinguish pending from ready identity.
8. Retain ready feature identity, host, and latest wait cursor as parent-owned supervision state; perform one bounded `wait_threads` wait/snapshot for immediate completion/failure/attention.
9. Report identity, objective, requested owner profile, worker profile, reviewer activation and enabled profile if any, environment/context, delivery route, wait state, and fallback.

One active durable writer per checkout remains the default. Concurrent work requires disjoint ownership plus one named owner for Git/shared mutable resources, or explicit separate-worktree authority.

## Feature Owner Launch Contract

Include every applicable field whose absence can change behavior or authority:

- `Objective`
- `Durable references`
- `Decisions, assumptions, unknowns, and non-goals`
- `Project, repository, checkout/worktree, branch/ref, and exact starting state`
- `Scope, ownership, interfaces, dependencies, and shared mutable state`
- `Authority` for edits, validation, commit, push, PR, merge, lifecycle, external writes, task creation, and delegation
- `Driver and lens`: project workflow remains driver; explicitly invoke `orchestrate-workers` for this feature under the operator-authorized launch
- `Resolved role map and reviewer request`: immutable orchestrator observation/requirement plus exact owner and worker profiles/provenance; reviewer activation as `disabled` or `operator-requested`; when requested, exact operator-request provenance, acceptance target, and separate reviewer profile/provenance
- `Inner route`: native leaf workers only; ordinary implementation-task route forbidden inside this topology
- `Success criteria and artifacts`
- `Verification and decision-bearing evidence`
- `Stop/ask and reporting gates`
- `Notification and return contract`: selected route-specific target/action, mandatory blocker/gate/terminal events, message shape, extended gates, and fallback
- `Final handoff format`, including the role map actually applied and any readback limitation

The contract states that the feature owner owns integration, self-review, and feature-level acceptance by default; may create only native leaf workers and an explicitly operator-requested native reviewer; cannot delegate authority or create another ordinary task; and treats worker and reviewer reports as evidence rather than acceptance. It binds the owner to delegate coherent execution-depth work—broad investigation, implementation, implementation-depth diagnostics, builds, focused tests, and owned-diff inspection—to configurable native workers when a safe delegation boundary exists. Workers may perform substantial implementation, build, test, diagnostic, and inspection work. The owner retains architecture/risk decisions, assignment contracts, the feature-lane Git/shared-state writer assignment, integrated-state synthesis, integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo decisions, feature acceptance, terminal reporting, and exactly the external-landing authority granted.

For each shared mutable resource, name exactly one writer at a time—the owner or one worker—within already-granted authority, serialize every other writer including the owner, and evaluate the resulting evidence. Substantial direct owner execution requires a no-boundary reason in the in-task plan or dispatch preamble and the existing final handoff `decisions/divergence`; do not create a new file, ledger, side channel, or notification event for that rationale. Trivial integration glue, narrow corrections, decision-critical inspection, and work without a coherent delegation boundary remain allowed. Assignments need not be distinct workers: sequential assignments to one compatible worker are valid, while parallel workers require genuinely non-overlapping ownership lanes.

## Feature-Task And Subagent Continuity

Feature-owner reuse requires an exact known idle identity plus compatible feature, project, repository/checkout/branch, trust, authority, role, feature-owner model/effort, inner-lens contract, and acceptance boundary. A different owner profile requires a new task; do not override an existing task on follow-up.

Before reuse, inspect current state and revalidate all role profiles and delivery fields. Never send a reset or concurrent assignment to a running feature owner. Send an idle compatible owner a full reset with prior disposition, allowed carry-over facts, invalidated scope/authority/decisions/assumptions/evidence/claims, and complete new objective, interfaces, success, verification, stop, notification, role-map, context, and return contracts. Old origin identity, callback action, wait cursor, event set, or profiles never carry implicitly.

The generic inner lens keys worker/reviewer reuse by exact role, project, checkout, trust, authority, ownership, route, model, and effort. A profile change triggers a fresh identity under existing recycle rules. Reuse compatible idle identities with assignment resets; do not recycle for elapsed time, compaction, assignment count, or ordinary correction. Keep worker and reviewer identities separate.

## Generic Inner Lens Contract

Keep the generic behavioral body in `orchestrate-workers`, preserving and generalizing:

- Driver/lens separation and current-coordinator profile preservation.
- One coherent worker by default; parallel workers only for independent ownership lanes and dependency-free frontier.
- Shared-checkout ownership, one Git/shared-state owner, and no worktree without operator approval.
- No parent turns for new workers; exceptional bounded inherited-turn slice for one named undistillable fact; full-history prohibition.
- Dispatch preamble, compact worker contract, worker verification/evidence rules, leaf-only topology, dependency routing, classification, assignment reset, reuse/recycle, and acceptance boundary.
- Sparse blocker/final return to the current coordinator through native subagent results or exact callback for the separately requested ordinary task route.
- Independent review disabled by default and activated only by an explicit operator request for the resolved task; no task characteristic, evidence gap, driver preference, or agent judgment supplies authorization.
- Fresh reviewer context without history exception, separate reviewer identity, and generic reviewer protocol.

Defaults for direct `orchestrate-workers` invocation are native Luna/xhigh implementation workers and coordinator self-review. An explicitly requested reviewer defaults to native Sol/high. Another worker profile may come from explicit operator instruction or an operator-authorized launch contract; a reviewer profile is resolved only after explicit operator activation, including profile wording or a launch contract carrying the originating operator request. The ordinary implementation-task route always requires a separate explicit operator request; a launch contract does not authorize that route by itself. Before each enabled-role dispatch, state the actual route, model, effort, context mode, and whether each value is default or override. Do not resolve or validate reviewer controls while disabled. Stop when an enabled exact profile cannot be set/validated.

The current coordinator may use any product-exposed profile; the lens preserves it and does not infer that coordinator and workers/reviewer must share a model. The enabled reviewer profile constrains only the independent reviewer. Activation and independence remain behavioral contracts, not claims derived from a model name.

The optional ordinary implementation-task route remains available only on a separate explicit operator request. It uses the resolved worker profile and requires the exact originating coordinator `threadId` and `hostId` when required plus the explicit native `send_message_to_thread` action. An accepted blocker/terminal send establishes delivery; rejection or unavailability remains local delivery failure. The route returns immediately without polling and never changes reviewer routing. `orchestrate-feature` forbids this inner route because its owner is already an ordinary task.

Keep the reviewer protocol at `orchestrate-workers/references/independent-reviewer-protocol.md` and load it only after explicit operator activation; preserve fresh context, read-only default, acceptance target, findings-first report, correction loop, and non-implementation boundary.

## Delivery And Completion

Preserve the reviewed T-38 route matrix in `orchestrate-feature`:

- Callback default: exact origin plus native `send_message_to_thread`; accepted terminal send establishes delivery.
- Practical bounded active waiting: native attention state for gates/blockers and terminal result for final handoff while attached; observation establishes delivery, timeout does not.
- Product-validated replacement: named mechanism/target with the same event floor.
- Explicit manual supervision: same native attention/terminal events for later inspection, no automatic-delivery claim, unobserved until inspection.

Only required phase gates, genuine actionable blockers, and final classified handoffs are events. Routine progress, unchanged state, and recoverable friction are not. Parent waiting remains bounded and non-durable; do not poll repeatedly.

The final handoff includes outcome, exact repository/branch/commit/checkout/tested state, changed artifacts, verification, criteria, decisions/divergence, blockers/uncertainty, downstream action, continuity, and role profiles actually used. Program-level disposition does not duplicate feature-level review.

## Native Capability And Truthfulness

At invocation, use only exposed native task creation, subagent creation, saved-project/environment, explicit model/effort, context, task identity, callback, inspection, and bounded-wait surfaces. Ordinary tasks remain peers. Native task/subagent creation is non-blocking where documented by the current tool schema.

If exact selected route/model/effort/context/delivery behavior is unavailable, stop or use only the named truthful delivery fallback. Never infer identity from a title, invent side-channel identity, substitute profiles, or promise a watcher. Distinguish request validation and accepted creation/spawn from independent profile readback.

## Catalog And Managed Migration

Catalog changes:

- Replace outer ID `orchestrate-sol-feature` with `orchestrate-feature`, `kind: skill`, Codex-only, owner `agents`, source `codex/skills/orchestrate-feature`, install target `skills/orchestrate-feature`, tags `role:helper` and `domain:orchestration`.
- Add `orchestrate-workers`, `kind: skill`, Codex-only, owner `agents`, source `codex/skills/orchestrate-workers`, install target `skills/orchestrate-workers`, tags `role:lens` and `domain:orchestration`.
- Remove the `sol-luna-orchestration` ID, source path, and install target; no Claude entry exists.

The repository and scratch installed output contain no `orchestrate-sol-feature` source after migration. Reuse `InstallerEngineTest.test_catalog_deleted_asset_prunes_and_uninstall_uses_history` as the public behavior proof that unchanged managed assets removed from the catalog are pruneable; do not duplicate the installer mechanism. Add branch-specific scratch-upgrade evidence: install exact `main` into an isolated Codex home, run the current branch installer with `--prune`, and prove the old managed outer directory is removed, both new canonical assets are present, the retained preset remains, and an injected unmanaged sentinel outside those targets is unchanged. Use a dry-run/diff first, then perform the scratch mutation to prove the postcondition.

## Static And Behavioral Contracts

Focused tests must fail for these regressions:

1. `orchestrate-feature` becomes implicit, loses helper role, or broadens authority.
2. Old `orchestrate-sol-feature` source/catalog/install target remains or the managed prune path leaves it behind.
3. Default behavior drifts from Sol/medium owner, Luna/xhigh worker, feature-owner/coordinator self-review, and reviewer-disabled state; an enabled no-override reviewer drifts from Sol/high.
4. One role override cascades to another role, an omitted field inherits another override, or the current orchestrator is described as mutable.
5. An unavailable exact role profile substitutes silently or creation validation is reported as independent readback.
6. A non-Sol feature owner is routed through a Sol-only inner precondition or generic worker/reviewer lifecycle knowledge is duplicated across the outer and generic skills.
7. Feature-owner/worker/reviewer reuse ignores role-profile compatibility or reuses a worker as independent reviewer.
8. The retired `sol-luna-orchestration` source or catalog entry remains, or an active reference routes users to it.
9. `orchestrate-workers` loses default coordinator self-review, operator-only reviewer activation, disabled-path token avoidance, fresh worker/reviewer context, leaf topology, continuity/reset, evidence, no-substitution, or acceptance boundaries.
10. Any T-38 callback, bounded-wait/fallback, sparse event-floor, fresh feature-task, exceptional-fork, one-writer, or authority contract regresses.
11. The transmitted feature-owner launch contract delegates coherent execution-depth work—broad investigation, implementation, implementation-depth diagnostics, builds, focused tests, and owned-diff inspection—to configurable native workers when a safe delegation boundary exists; workers may own substantial implementation, build, test, diagnostic, and inspection work, and worker model/effort remains resolved from the role map.
12. The feature owner retains architecture/risk decisions, assignment contracts, feature-lane Git/shared-state writer assignment, integrated-state synthesis, integration, integrated-diff/evidence inspection, verification sufficiency, retain-or-redo, acceptance, terminal reporting, and exactly the external-landing authority granted; primarily orchestrating remains active ownership.
13. Each shared mutable resource has exactly one writer at a time within already-granted authority, retained by the owner or one worker; every other writer, including the owner, is serialized and the owner evaluates the resulting evidence.
14. Substantial direct owner execution records a no-boundary reason in the in-task plan or dispatch preamble and existing final handoff `decisions/divergence`, without a new file, ledger, side channel, or notification event; trivial glue, narrow corrections, decision-critical inspection, and work without a coherent delegation boundary remain allowed.
15. The owner uses `orchestrate-workers` to create native leaf implementation workers, never a nested feature owner or ordinary implementation-task route; sequential assignments may reuse one compatible worker, while parallel workers require genuinely non-overlapping ownership lanes and tests do not require a worker count.

Assert both orchestration skills remain Codex-only, UI policies are explicit-only, no scripts/custom agents/Claude layer/controller/watcher/registry is added, and progressive-disclosure ceilings remain focused. Phrase/source assertions are appropriate because these shipped instruction assets are the contract, but tests should section-scope route/profile clauses so contradictory text cannot pass merely by coexisting.

## Validation

Run at minimum:

```text
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" codex/skills/orchestrate-feature
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" codex/skills/orchestrate-workers
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 scripts/check_cross_repo_consistency.py
python3 -m unittest tests.test_goal_prompt_contracts
python3 -m unittest discover -s tests
bash scripts/test-prune-safety.sh
harness check
git diff --check main
```

Exercise scratch homes only:

```text
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --dry-run --diff
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh --dry-run --diff
<install exact main into an isolated codex-upgrade home>
CODEX_HOME="<isolated codex-upgrade home>" bash scripts/install-codex.sh --dry-run --diff --prune
CODEX_HOME="<isolated codex-upgrade home>" bash scripts/install-codex.sh --prune
```

The upgrade fixture must contain the exact base-generated managed state and old outer asset rather than an unmanaged lookalike. Verify the three skill-directory postconditions and unmanaged sentinel directly. If the full suite has a pre-existing failure, reproduce it on exact base and do not weaken unrelated tests.

## Review And Publication

Required T-39 sequence:

1. Codex authors and performs a read-only design review of the amended PRD/spec against T-39, the current catalog/installer, native schemas, and the accepted T-38 contracts. Resolve material design findings before implementation.
2. Use a compatible `gpt-5.6-luna`/xhigh implementation leaf with a complete assignment reset. It may edit/validate only accepted paths and may not commit, push, open/merge a PR, install live, create a worktree, mutate Harness, or delegate.
3. Codex reviews the integrated diff and routes bounded fixes to the same worker.
4. A fresh independent read-only reviewer checks the exact combined branch against T-39 and all retained T-38 criteria. Resolve every material finding and re-review substantive fixes.
5. Close T-39/S-27, commit reviewed checkpoints, push `codex/orchestrate-feature`, and open one pull request into `main` describing both callback hardening and generic-profile migration.

Do not merge or install the live skill in this task.

## Acceptance

T-39 implementation was accepted under its recorded review and publication sequence. The T-41 amendment is acceptable when default coordinator/feature-owner self-review, explicit operator-only reviewer activation, disabled-path non-resolution/non-loading, enabled-reviewer independence, generic profile routing, and retained T-38/T-39 delivery/context/authority contracts pass focused tests and repository validation with no unrelated diff. The T-42 amendment is additionally acceptable when a code feature containing a Docker image build, focused tests, and a shared-host end-to-end test naturally yields coherent worker-owned implementation/build/test assignments (sequentially on one compatible worker unless lanes are genuinely non-overlapping), exactly one named shared-host writer at a time within authority, and owner-owned integration, integrated-diff/evidence inspection, verification-sufficiency judgment, retain-or-redo, and acceptance without creating another feature-owner task.
