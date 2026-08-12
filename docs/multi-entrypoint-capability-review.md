# Multi-Entrypoint Capability Review

Open this reference when two or more entrypoints reach the same durable behavior, or when a proposed web, API, bot, worker, job, cron, CLI, script, MCP, desktop, or mobile entrypoint may create another behavior path.

Skip it when the change stays behind one existing interface, entrypoints share only a product-free primitive, or the project already has one proven behavior path and the new work does not change it. This is a conditional architecture lens, not a project template or a reason to add layers.

## Objective

Prevent locally correct entrypoint changes from creating divergent business decisions, lifecycle rules, authorization, persistence, provider calls, or user-visible state. Preserve the project's existing vocabulary and architecture when they already make ownership clear.

## Responsibility Map

Map responsibilities onto the project's current names; do not require these labels or folders.

| Responsibility | Owns | Does not independently own |
|---|---|---|
| Inbound adapter | Transport parsing, authentication context, boundary payload validation, and response formatting | Durable authorization, lifecycle, reconciliation, or a second copy of product behavior |
| Capability / use case / application seam | The user or operator workflow shared by entrypoints | Concrete transport objects or scattered provider-specific calls |
| Domain policy or model | Durable invariants, authority, lifecycle, calculations, and reconciliation when those rules form a real module | Framework glue, transport formatting, or a miscellaneous service bucket |
| Contract | Schemas that cross a real public, process, deployable, or asynchronous boundary | Speculative internal types promoted only for architectural symmetry |
| Platform / infrastructure adapter | Concrete database, queue, filesystem, SDK, provider, auth, and telemetry interaction behind an earned seam | Business decisions that must stay consistent across entrypoints |
| Shared primitive | Product-free utilities or visual primitives with one reason to change | Similar-looking behavior with different meaning, authority, or lifecycle |

One adapter remains a hypothetical seam. Add a port or platform abstraction only when real substitution, repeated infrastructure access, or authority-sensitive containment earns it. When a local stand-in suffices, keep the seam internal rather than introducing a port for testing alone.

## Review Method

1. **Name one behavior.** Use product or operator language and state the observable outcome. Do not review the entire repository under a generic label such as services, API, or utilities.
2. **Map every entrypoint and bypass.** Find routes, handlers, jobs, consumers, cron, scripts, tools, clients, tests, direct writes, and direct provider calls that can reach the behavior. Distinguish authoritative paths from read-only views and operational repair paths.
3. **Identify truth and authority.** Name the authoritative local or external state, who may initiate and authorize changes, the invariant and lifecycle owner, and how user-visible status explains provenance, staleness, missing data, and degraded operation.
4. **Trace the current behavior path.** Find the existing command, query, use case, application service, module interface, or other seam. Report divergent validation, authorization, state transitions, provider calls, or status interpretation rather than assuming several files imply several implementations.
5. **Check effect and recovery semantics when relevant.** Identify the transaction or commit boundary and its owner, idempotency key or replay behavior, duplicate/concurrent invocation behavior, retry and timeout ownership, cancellation, partial failure, external/local reconciliation, and the condition that restores safe state. Open `docs/whole-system-review.md` when these concerns cross components or shared substrates; do not duplicate that analysis here.
6. **Judge the existing seam.** Prefer reusing or deepening a working interface. A new abstraction must concentrate real behavior or failure knowledge; a forwarding wrapper, renamed folder, or interface around one stable call does not qualify.
7. **Choose one vertical correction.** Thin one adapter, route one bypass through the authoritative seam, move one durable rule to its owner, isolate one concrete dependency, or split a fake-shared component and duplicate intentionally when owners or reasons to change differ. Keep unrelated legacy paths intact and visible rather than starting a horizontal migration.
8. **Prove the assembled behavior.** Test the consequence through the shared public seam, prove each changed entrypoint is wired to it, and use a targeted search or structural trace to account for remaining bypasses. Add failure/recovery proof only in proportion to the credible risk.

## Conditional Capability Contract

Use a short project-local capability contract only when implementation depends on resolving more than one entrypoint, durable state, authority, lifecycle, reconciliation, a public or asynchronous boundary, or user-visible stale/degraded behavior. For ordinary contained changes, record that no contract is needed.

When needed, resolve the contract through `grill-with-docs`. If implementation depends on the result, capture it durably in project documentation or through `harness-record` before implementing; do not leave it only in chat. Include only fields that affect implementation or acceptance:

- capability and observable outcome;
- current and planned entrypoints, including repair or administrative paths;
- owner, source of truth, and authorization authority;
- public command/query/use-case seam in the project's vocabulary;
- invariants, lifecycle, transaction/idempotency, retry, reconciliation, and degraded behavior that apply;
- real public/process/async contracts and concrete infrastructure dependencies;
- consequence-level tests, adapter wiring proof, remaining bypasses, risks, and non-goals.

Do not create a contract merely to restate code, make a folder tree look complete, or speculate about future consumers.

## Finding Completion

For an affected architecture candidate, make the existing `architecture-review` fields carry this evidence:

- **Problem:** entrypoints, current shared path, and concrete divergence or bypass.
- **Proposed shape:** authoritative owner and the smallest vertical correction, using existing project names.
- **Risk:** migration, compatibility, concurrent-effect, retry, or recovery risk that the correction introduces or leaves.
- **Verification:** shared-seam consequence proof, changed-adapter wiring, and remaining-bypass accounting.

A valid result may be `no capability-boundary delta`: the existing architecture already gives every entrypoint one authoritative behavior path and sufficient proof.

## Guardrails

- Do not prescribe `app/`, `capabilities/`, `domain/`, `contracts/`, `platform/`, or `shared/` directories.
- Do not create empty layers, global folder migrations, speculative packages, hypothetical ports, or a service split without an operational reason.
- Do not move authentication context and transport validation into the core, and do not leave durable authorization duplicated across adapters.
- Do not infer shared meaning from similar code or visual shape; compare owner, authority, lifecycle, and reason to change.
- Do not create a new architecture or capability-contract skill for this lens. `architecture-review` remains the owner.

## Provenance

This reference adapts the multi-entrypoint ownership, product-language capability, thin-adapter, local-first adoption, bypass-accounting, degraded-state, and conditional capability-contract ideas from Dmitrii Malakhov's *Capability Core + Adapters*, https://github.com/malakhov-dmitrii/capability-core-adapters, inspected at commit `19efb7d6eab9927b01c650154b315e1211bab901` under the MIT License. The transaction, idempotency, concurrency, retry, cancellation, reconciliation, recovery, progressive-disclosure, and existing-skill ownership constraints are repository-specific additions; the source is a design proposal and anecdotal practice report, not empirical proof of a universal architecture.
