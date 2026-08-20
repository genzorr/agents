# Orchestrate Sol Feature — Technical Specification

## Authority And Scope

This specification implements the product contract in `docs/orchestrate-sol-feature-prd.md` under Harness task T-36. The PRD controls product behavior; this document controls the bounded repository change. When they conflict, stop and correct the documents before implementation.

## Source Ownership

Agents owns the new generic personal Codex skill. The installed directory under the user's Codex home is an output and must not be edited in this task.

Add these source paths:

- `codex/skills/orchestrate-sol-feature/SKILL.md`
- `codex/skills/orchestrate-sol-feature/agents/openai.yaml`

Modify only as needed:

- `catalog.json`
- `codex/skills/sol-luna-orchestration/SKILL.md`
- `codex/skills/sol-luna-orchestration/agents/openai.yaml` only if its UI wording becomes inaccurate after the terminology clarification.
- `tests/test_goal_prompt_contracts.py`, or one narrowly named new test module if separation materially improves clarity.
- `docs/orchestrate-sol-feature-prd.md`
- `docs/orchestrate-sol-feature-spec.md`
- Harness-owned records for S-25/T-36 through Harness CLI operations.

Do not add scripts, references, templates, assets, custom agents, configuration files, installer logic, Claude counterparts, or runtime dependencies.

## Initialization

Use the available system `skill-creator` initializer as an authoring tool before replacing its generated placeholders; it is not a repository or installed-skill runtime dependency. Generate only `SKILL.md` and `agents/openai.yaml`; do not request unused resource directories or examples. Use the exact skill directory id and frontmatter name `orchestrate-sol-feature`.

## Skill Metadata

The frontmatter contains only `name` and `description`.

Required name:

```yaml
name: orchestrate-sol-feature
```

The description must make the trigger, topology, and launch-authority boundary discoverable without duplicating body-only procedure:

- It dispatches or reuses an ordinary Sol/high feature task from a long-lived Sol project orchestrator.
- It configures the feature owner to use reusable native Sol/medium subagents through the existing inner orchestration lens.
- It applies only after the operator explicitly invokes `orchestrate-sol-feature` or explicitly requests this exact Sol feature-orchestration topology.
- Invocation authorizes creation or reuse of one resolved feature task but does not authorize unrelated work or broaden project, Git, worktree, external-write, or live-install authority.

The skill is Codex-only because its ordinary tasks, native subagents, model identifiers, and task-control surfaces are Codex-specific.

## UI Metadata

Generate `agents/openai.yaml` with exactly the applicable interface and invocation policy fields, quoted string values, and no invented dependency or branding fields.

Required semantic values:

```yaml
interface:
  display_name: "Orchestrate Sol Feature"
  short_description: "Dispatch Sol/high features with Sol/medium workers"
  default_prompt: "Use $orchestrate-sol-feature to launch or resume this agreed feature from the current project orchestrator."
policy:
  allow_implicit_invocation: false
```

## Composition Role

Declare the new skill's composition role as `helper`. The current project-orchestrator protocol or driver retains program lifecycle, authority, and completion ownership; this skill performs the bounded launch-readiness, dispatch, reuse, and handoff-routing operation the caller requested. If the governing protocol or driver forbids task creation, delegation, or the proposed lifecycle change, stop rather than displace it.

The feature task remains a distinct Codex task and may select its own project workflow driver. When no project workflow driver applies, the complete launch contract is the feature task's driver contract. Inside that task, `sol-luna-orchestration` remains a `lens`; neither the new helper nor the lens may silently take lifecycle authority from a governing protocol or driver.

## Required Terms

Define these terms compactly:

- `Project orchestrator`: the current long-lived Sol task that preserves program context and owns program-level decisions.
- `Feature owner`: the ordinary `gpt-5.6-sol` / `high` task that owns one resolved feature's detailed lifecycle and feature-level acceptance.
- `Worker`: a native `gpt-5.6-sol` / `medium` leaf subagent inside the feature owner.
- `Reviewer`: the inner lens's independent `gpt-5.6-sol` / `high` subagent when its escalation rule fires; a reviewer is not a worker, and the Sol/medium profile constrains workers only.
- `Launch contract`: the distilled authoritative context, scope, state, authority, success, verification, stop, and reporting packet sent to a new or reused feature owner.
- `Reset`: the complete reassignment overlay required before compatible feature-task reuse.
- `Recycle`: ending reuse and selecting a fresh feature owner only on a named material boundary or explicit operator request.

Do not coin additional route taxonomy or introduce a persistent registry.

## Activation And Readiness

On explicit invocation:

0. Confirm a separate feature owner has material value because the work is multi-phase, context-heavy, contains multiple coherent assignments, can progress independently, or the operator explicitly requested this separate-task topology. Otherwise return the contained-work recommendation without dispatch.
1. Confirm the current session is not itself a feature owner or other child created by this topology. A feature owner must refuse nested ordinary-task creation and report the boundary.
2. Consult the native model/status surface when available, confirm the current session is a product-exposed Sol session, preserve its current effort, and never change its model. If the product cannot expose identity, proceed with the stated limitation rather than invent confirmation; stop only when available evidence indicates a non-Sol session.
3. Resolve the feature objective, durable authorities, user decisions, non-goals, target project/repository, exact intended start state, scope ownership, permissions, success criteria, verification, stop gates, and reporting contract.
4. Inspect the governing protocol/driver, target project instructions, and native project metadata before selecting the task environment. Stop if the governing protocol or driver forbids the dispatch.
5. Recover locally answerable gaps. Use an existing durable task, issue, PRD, or specification when sufficient; create or update the smallest appropriate project-owned authority only when the current driver and permission allow it and the feature needs one.
6. If a material user-owned or difficult-to-reverse choice remains, report the launch blocker and return without task creation.

Activation applies to one resolved feature lane. A later unrelated feature requires a fresh explicit invocation.

## New Feature Dispatch

For a new feature owner:

1. Use the native ordinary-task creation surface, not a native subagent spawn.
2. Select the exact product-exposed model `gpt-5.6-sol` and reasoning effort `high`.
3. Resolve the saved project first. Personal OS and repositories it manages use the existing local checkout unless the operator explicitly authorizes a worktree. Other projects obey explicit user and project local/worktree policy and then the native product default when no stricter rule exists.
4. Use an exact intended existing branch/ref or explicitly intended working-tree state. Do not invent a base or branch.
5. Give the task a concise project-and-feature title that distinguishes it from the project orchestrator and sibling feature owners.
6. Send only the complete Feature Owner Launch Contract below; do not inherit or paste the full parent conversation.
7. Handle ready and pending task identities truthfully. Never use a pending client identity where a ready task identity is required or claim an independently unreadable model value was read back.
8. Report the launch identity, objective, route, exact requested model/effort, environment/context mode, and return behavior to the operator.

Before dispatch into an existing checkout, require one active durable writer by default, counting the project orchestrator and feature owners. While the feature owner writes, the orchestrator performs no concurrent durable writes there unless the contract assigns disjoint paths and one named owner for Git state, generated artifacts, build outputs, test databases, ports, devices, formatters, and other shared mutable resources. If active-writer state cannot be recovered from recorded launches and native inspection, treat it as unresolved and serialize or ask; otherwise concurrent writers require disjoint ownership or explicit worktree authority.

The environment assigned during native ordinary-task creation follows the outer operator/project/default policy. The inner lens's no-worktree-without-operator-approval rule governs any additional worktree the feature owner or worker would create after launch, not an already assigned compliant task environment.

Explicit skill invocation is the operator request required for this one ordinary task creation. It is not permission to launch siblings speculatively.

## Feature Owner Launch Contract

Include only applicable fields, but never omit a field whose absence can change behavior or authority:

- `Objective`
- `Durable references`
- `Decisions, assumptions, unknowns, and non-goals`
- `Project, repository, checkout/worktree, branch/ref, and exact starting state`
- `Scope, ownership, interfaces, dependencies, and shared mutable state`
- `Authority` for edits, validation, commit, push, PR, merge, lifecycle, external writes, task creation, and delegation
- `Driver and lens`: applicable project workflow remains driver; when none applies, this launch contract is the driver contract; explicitly invoke `sol-luna-orchestration` for this resolved feature
- `Worker profile`: operator selected native `gpt-5.6-sol` / `medium`; Luna is not authorized unless the operator later changes the profile
- `Success criteria and artifacts`
- `Verification and decision-bearing evidence`
- `Stop/ask and reporting gates`
- `Return route`
- `Final handoff format`

The contract must state that the feature owner may use native leaf subagents only, cannot create another ordinary task, cannot delegate authority, and owns integrated feature-level acceptance.

The contract must also forbid the inner `sol-luna-orchestration` ordinary Luna task/thread route. That route remains available only when the operator separately selects the current-Sol-driver/ordinary-Luna-worker topology; it cannot be combined with this Sol/high feature-owner topology for the same feature.

## Feature-Task Reuse

Reuse requires an exact known task identity plus compatible feature, project, repo/checkout, branch, trust, authority, role, model/effort, and acceptance boundary. The current orchestrator task's own recorded accepted launch result is the profile authority; native inspection establishes that exact task's identity, reachability, and current state. A title, summary, or unsupported recollection is untrusted selection context and never sufficient evidence. If launch provenance is unavailable, create a new owner or ask rather than asserting compatibility.

Before reuse, inspect the task's latest status and repository handoff. Do not reuse a running owner for an incompatible concurrent assignment.

Send a full reset containing:

- Prior assignment and disposition.
- Facts allowed to carry over.
- Assumptions, authority, scope, decisions, completion claims, and evidence that must not carry over.
- New objective, durable references, interfaces, ownership, dependencies, success criteria, verification, stop gates, reporting, and return format.

Preserve the existing task's configured model and effort by omitting per-message overrides when the identity remains compatible. If the exact required profile was never established or is incompatible, create a new owner rather than silently changing an existing one.

Recycle only for material repository/checkout/trust/permission change; incompatible model/effort; unrecoverable superseded contract; repeated acceptance-critical miss or stale assumption after correction; hidden unresolved state; unreachable identity; a materially different feature; or explicit operator request. Classify the prior disposition and lost continuity before replacement.

## Feature Owner Internal Delegation

The launch contract explicitly carries the operator's invocation of `sol-luna-orchestration` and alternate worker choice. The feature owner must apply that lens to the current resolved feature and set native workers to `gpt-5.6-sol` / `medium`.

The inner lens owns worker decomposition, contracts, context, continuity, evidence, review, and acceptance rules. The outer skill adds only these requirements: the feature owner remains feature-level planner/integrator/reviewer/acceptance authority; workers use the exact Sol/medium profile; workers are native leaves; the feature owner cannot use the ordinary Luna task/thread route or create another ordinary task; the project orchestrator cannot launch or duplicate the feature's implementation workers; and blockers/final completion follow the outer reporting contract.

## Existing Sol-Luna Clarification

The existing skill already permits another model or effort when the operator explicitly requests it, but several definitions and headings describe every worker as Luna. Make the smallest semantic clarification that allows a selected alternate worker profile without changing defaults:

- Define `Worker` generically as the selected native implementation subagent or the explicitly operator-requested ordinary implementation route, with Luna/xhigh remaining the default profile.
- Rename `Compact Luna Worker Contract` to `Compact Worker Contract` and `Luna Worker Rules` to `Worker Rules`; update every internal reference and exact-heading test that depends on those names. Make report and acceptance wording apply to the selected worker profile rather than asserting Luna identity where the rule is generic.
- Replace the Luna-specific no-upgrade sentence with a profile-generic rule: never raise the selected worker profile's model or effort without an explicit operator request.
- State that an explicit lens invocation relayed in an operator-authorized ordinary-task launch contract satisfies the lens's explicit-invocation requirement for that resolved task; agent-relayed requests without that operator-authorized launch contract do not.
- Preserve the skill name, explicit-only invocation, composition role, Luna/xhigh default routes, ordinary Luna task/thread route, Sol/high reviewer route, model-substitution stop behavior, worker reuse/recycle rules, and reviewer protocol.
- Do not silently make Sol/medium a new default for direct invocations of `sol-luna-orchestration`.

Update existing tests to assert the preserved defaults and the explicit alternate-profile compatibility rather than retaining Luna-only generic terminology.

## Reporting And Completion

The outer skill keeps every launched or reused feature lane accounted for until classified `complete`, `blocked`, `partial`, or `failed`. Launch is not completion.

Immediately after dispatch, record the non-terminal resting state `launched, awaiting handoff`. Make no progress, health, completion, or acceptance claim until a native handoff or inspection provides evidence.

The feature owner sends only a required phase gate, genuine blocker, or final handoff. The final handoff reports:

- Status and outcome.
- Exact repository, branch, commit, checkout/worktree, and tested state.
- Changed files and artifacts.
- Commands and verification results.
- Acceptance criteria and paths covered.
- Material decisions, divergence, blockers, and uncertainty.
- Downstream action and continuity state.

The project orchestrator validates the smallest program-level boundary required for disposition and does not routinely rerun scope-complete current checks. External landing remains subject to existing authority.

Do not poll repeatedly. Use native waiting or inspection only when following a launched task, responding to a handoff, or answering an explicit status request. If the exact originating task identity is unavailable, do not fabricate a return route; retain and report the feature-task identity for later native inspection.

## Required Native Capability Check

T-36's dated Harness finding records that the current Codex task observed native schemas exposing ordinary task creation with explicit `gpt-5.6-sol` / `high`, native subagent creation with explicit `gpt-5.6-sol` / `medium`, saved-project resolution, ready-versus-pending task identity, and native task inspection/waiting. Treat that observation as current implementation evidence, not a permanent runtime guarantee.

At invocation, use only capabilities actually exposed by the native surface. If exact ordinary-task model/effort, exact subagent model/effort, required fresh-context control, target project/environment selection, or truthful return/inspection behavior is unavailable, follow the named stop or fallback in this specification and never substitute another profile silently.

## Catalog Entry

Add one `catalog.json` skill entry:

- `id`: `orchestrate-sol-feature`
- `kind`: `skill`
- `platforms`: `codex` only
- `owner`: `agents`
- `source.codex`: `codex/skills/orchestrate-sol-feature`
- `install_target.codex`: `skills/orchestrate-sol-feature`
- Tags include `role:helper` and `domain:orchestration`.

Do not create a Claude catalog entry or traveling-document dependency. The PRD/spec are repository design records, not skill-relative runtime references.

## Static And Behavioral Contracts

Add focused tests that fail for these plausible regressions:

1. The skill becomes implicitly invocable or its description no longer requires explicit invocation.
2. The new skill is added to the Claude tree or catalog.
3. The project orchestrator is allowed to spawn the feature implementation worker directly.
4. The feature owner is not an ordinary Sol/high task or an implementation worker is not native Sol/medium; the separate Sol/high reviewer route remains permitted.
5. The feature owner may create nested ordinary tasks or workers may delegate.
6. Full parent history is inherited or launch authority omits durable references, scope, permissions, verification, stop gates, or reporting.
7. A task is reused by title alone or without a reset contract.
8. Worktree, branch, push, PR, merge, live-install, or external-write authority is silently broadened.
9. Pending/validated model identity is misrepresented as independent readback.
10. Existing `sol-luna-orchestration` loses Luna/xhigh defaults, explicit-only behavior, lens role, worker continuity, or independent-review guardrails.

Also assert the UI policy remains `allow_implicit_invocation: false`; no scripts, references, assets, custom agents, Claude source layer, or traveling dependency is added; one-active-durable-writer, `launched, awaiting handoff`, no-poll, and no-fabricated-return-identity clauses remain present; the existing lens description and default prompt continue to advertise Luna/xhigh as the default; and both skill bodies remain under a focused word-count ceiling consistent with existing progressive-disclosure tests.

Prefer consequence-bearing phrase and section contracts consistent with the repository's existing skill tests. Do not add a general eval runner or persistent prompt corpus.

## Validation

Run at minimum:

```text
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" codex/skills/orchestrate-sol-feature  # runtime-home authoring tool; run when present, otherwise report unavailable
python3 scripts/validate_catalog.py
python3 scripts/validate_skills.py
python3 scripts/check_cross_repo_consistency.py
python3 -m unittest tests.test_goal_prompt_contracts
python3 -m unittest discover -s tests
bash scripts/test-prune-safety.sh
harness check
git diff --check
```

Exercise the catalog through scratch homes only:

```text
CLAUDE_HOME="$PWD/.scratch-home/claude" bash scripts/install-claude.sh --dry-run --diff
CODEX_HOME="$PWD/.scratch-home/codex" bash scripts/install-codex.sh --dry-run --diff
```

If the full suite has a pre-existing failure, reproduce it on the exact base commit and record the bounded comparison. Do not weaken or delete unrelated tests.

## Review And Publication

Required sequence:

1. Read-only Claude Opus/high review of the PRD/spec before skill implementation.
2. Fresh Sol/medium native subagent implementation from the accepted documents, with local edits and validation but no push, PR, merge, live install, or delegation. For T-36, the current Codex task is the feature owner executing an operator-specified implementation workflow, not a long-lived project orchestrator invoking the new product topology.
3. Codex review of the integrated diff and verification evidence.
4. The same Sol/medium subagent applies bounded accepted fixes and reruns affected checks.
5. Fresh read-only Claude Opus/high review of the final branch diff against `main` and the accepted PRD/spec.
6. Resolve every material finding; if final fixes are non-trivial, obtain a focused fresh Claude re-review of the corrected diff.
7. Commit as useful checkpoints, push `codex/orchestrate-sol-feature`, and open a pull request into `main`.

Do not merge the pull request or install the live skill in this task.

## Acceptance

Implementation is acceptable when every T-36 criterion is evidenced, the skill and catalog validators pass, focused tests cover the topology and authority contract, full-suite results are classified, scratch installs show the intended Codex-only asset, Harness and diff checks pass, both requested Claude reviews have no unresolved material finding, and the pull request is open against `main` with no unrelated diff.
