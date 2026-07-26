# Whole-System Review

Open this reference only when a change or diagnosis crosses component boundaries in a way that local
correctness cannot settle: integration topology, shared substrates, queues/caches/retries, distributed
state, production controllers, coordinated rollout, or recovery involving several owners.

Skip it for a contained local refactor, pure transformation, documentation change, or reversible edit
whose state, effects, and failures stay behind one existing interface.

This is a **lens**, not a workflow driver. The active architecture, diagnosis, or review skill keeps
lifecycle ownership. When `systemic-diagnosis` is active, it owns claim labeling and causal-loop
mapping; this reference still owns the remaining questions and guardrails, including the section 4
controller and actuator-interaction checks.

## Objective

Check whether locally reasonable parts compose into an unsafe or cognitively expensive whole, while
avoiding speculative distributed-systems machinery. Prefer a local owner and a simple boundary until
evidence shows that a real cross-component invariant or feedback loop cannot be owned there.

## Five Load-Bearing Questions

### 1. What defeats claimed isolation?

Trace the real end-to-end path and name shared dependencies: database, queue, cache, identity system,
filesystem, process pool, network, clock, configuration, deployment unit, rate limit, or human operator.
Look for cycles and correlated failure. Two components are not independent because their APIs differ
if they still fail through the same substrate.

### 2. Can a transient disturbance become self-sustaining?

Run the disturbance forward through retries, backlog, cache invalidation, timeouts, autoscaling,
load shedding, stale state, and recovery. Ask whether the system returns to normal after the original
fault disappears or remains trapped in a degraded state. Name the mechanism that restores it: bounded
retry, draining, reconciliation, reset, rollback, capacity margin, or operator action.

### 3. What invariant spans components, and who owns it?

State the invariant in one sentence. Identify the authority that can enforce it atomically or
serially. If no single component can own it, compare explicit coordination against alternatives such
as redesigning ownership, making operations idempotent/commutative, or accepting a bounded temporary
inconsistency. Coordination is justified only when the invariant is real and the simpler ownership
shapes cannot preserve it.

### 4. Which control loops interact?

List controllers—autoscalers, retries, circuit breakers, queues, schedulers, caches, reconcilers,
human runbooks, or policy agents—and their signals, levers, timescales, and authority. Check for loops
that amplify the same disturbance, fight over one actuator, react to delayed/stale signals, or erase
each other's safety margins.

### 5. What proves the assembled path?

Name one end-to-end probe and, when risk warrants it, one bounded fault exercise. The proof should
cross the real interfaces and observe both service behavior and recovery, not only unit-level success.
Examples include a canary path, replay against a frozen fixture, queue saturation with bounded input,
dependency timeout with cancellation, rollback rehearsal, or a controlled failure-injection test.

## Review Method

1. **Bound the system.** Name entry point, user-visible outcome, participating components, authority,
   and time horizon. Do not model the whole organization when one request path is enough.
2. **Trace one real path.** Include state, effects, retries, deadlines, and cleanup. Prefer evidence
   from code/config/tests/telemetry over an aspirational diagram.
3. **Label claims when needed.** If the active skill has no claim-labeling method, mark load-bearing
   statements `observed/measured`, `inferred`, or `hypothesized`.
4. **Map propagation and recovery.** Record the initiating disturbance, amplification/containment
   edges, credible blast radius, and the condition that returns the system to a safe state.
5. **Test the invariant owner.** Check whether two actors can disagree, interleave, replay, or outlive
   the authority assumed by the design.
6. **Choose the smallest structural delta.** Prefer clarifying ownership, bounding work, removing a
   cycle, or adding one probe over introducing a coordinator, event bus, distributed lock, or global
   model.

## Finding Shape

```markdown
### <whole-system finding>

- Path / components: <real integration path>
- Claim status: <observed/measured | inferred | hypothesized>
- Shared dependency or loop: <what defeats local reasoning>
- Invariant and owner: <one sentence; owner or ownership gap>
- Propagation / blast radius: <credible failure path>
- Recovery condition: <what restores safe operation>
- Minimal delta: <smallest structural change>
- Proof: <end-to-end probe or bounded fault exercise>
- Coordination cost: <new state/coupling/failure modes, or none>
```

## Anti-Overengineering Guardrails

- Do not infer a distributed-systems problem from file count, service count, or architectural fashion.
- Do not add a port, adapter, coordinator, queue, lock, model, or control plane without a concrete
  invariant or failure path it owns.
- Do not require chaos testing for low-risk local work; match fault exercises to credible blast radius.
- Do not replace one hidden dependency with a larger hidden orchestration layer.
- Do not treat a diagram as evidence that the running path matches it.
- If the whole-system pass finds no cross-component failure that local contracts miss, record
  `no additional whole-system delta` and stop.

## Completion

The lens is complete when the reviewer can state whether local contracts are sufficient. If not, the
result names the shared dependency or loop, invariant owner, propagation path, recovery condition,
smallest justified delta, and observable proof. Unproven hypotheses remain tests to run, not accepted
architecture findings.

Adapted from the integration argument in https://shapeofthesystem.com/the-shape-of-the-whole.html.
