# Claim Discipline

This is the Agents-owned traveling reference for turning finite observations into reusable, evidence-bounded claims. Open it conditionally when a workflow selects an interpretation, proposes a reusable rule or default, designs or reviews an experiment, distills a source, audits skill breadth, or promotes session observations. It is a method reference, not a new skill or a replacement for the authority that owns the surrounding workflow.

## Contract

Keep three layers separate:

- **Observation:** what happened, under which source, configuration, workload, provider, project, tool, environment, time window, and validity conditions, with provenance and counterevidence.
- **Conclusion:** the weakest non-vacuous proposition supported by the complete relevant evidentiary record, including counterevidence, after considering alternatives and validity limits.
- **Decision:** what to do next, adopt, reject, defer, test, or keep unchanged. A decision may be conservative under uncertainty, but it is not an observation and must not be smuggled into the conclusion as though it were measured truth.

Evidence comes before conclusion selection. Preserve the concrete observations first; do not widen their scope while summarizing them. Confidence belongs to the scoped conclusion, never to an unspoken broader domain.

## Evidence-first claim selection

Use this sequence when a result may become reusable guidance:

1. Preserve the observations and provenance: name the tested units, source/configuration, workload, provider or model, project, environment, time window, measurement validity, and missing or excluded cases.
2. Enumerate materially plausible alternative explanations. An alternative remains live until the intervention and measurements distinguish it or the evidence rules it out.
3. Check the discriminator: the intervention, comparator, and measurements must be capable of distinguishing the relevant hypotheses. If they cannot, report an inconclusive or unresolved result rather than a causal or family-wide conclusion.
4. Separate supported conditions from incidental conditions. Keep a condition when the evidence or the conclusion's validity depends on it; remove incidental details that merely happened to occur in the observed cases.
5. Examine counterevidence, failed gates, invalid execution, missing runs, confounds, and contradictory cases. Explain whether each narrows the conclusion, leaves an alternative live, or invalidates interpretation.
6. Select the weakest non-vacuous conclusion that the evidence forces. Delete clauses, project names, provider names, mechanism assumptions, and universal quantifiers that the evidence does not support; moving a clause to a caveat is preferable to silently treating it as true.
7. State explicit non-claims: name the stronger proposition, family, provider set, project set, task set, environment, or mechanism that this evidence does not establish.
8. Record the downstream decision separately from the conclusion, including the authority that may adopt it and the next discriminator needed for a stronger claim.

## Strong discriminator, weak conclusion

The paired rule is **strong discriminator, weak conclusion**: experiment interventions and measurements must be strong enough to distinguish the relevant hypotheses, while learned claims include only the conditions actually supported by the evidence. A strong test does not license a broad conclusion, and a weak proxy does not become informative because its wording is cautious.

Safety rules, authorization boundaries, privacy constraints, irreversible-action gates, guardrails, and acceptance proof are deliberately strong boundaries. Claim weakening must not remove, dilute, or bypass them; place them at the narrowest reliable layer while preserving their force.

## Non-vacuity and scope

A reusable instruction remains non-vacuous only when it has a real trigger, required behavior, observable output or stop condition, and applicable boundaries. Removing every condition until the result says “be careful” or “use judgment” is vacuous weakening, not generalization. Preserve the smallest actionable trigger and proof obligation that the supported cases require.

Semantic weakness is scope, not textual brevity. A longer conditional rule can be weaker and more general than a short absolute rule when it constrains fewer unrelated cases while remaining actionable. Textual compactness is an encoding objective; it does not determine the claim's generality.

## Common overgeneralization checks

- **Provider-specific evidence:** repeated behavior from Provider-A supports a Provider-A-scoped claim unless independent evidence covers other providers; it does not support a provider-independent rule by default.
- **Several sessions from one project:** repetition across sessions in one project supports a project-scoped pattern unless independent project lineages or a broader design justify promotion; session count is not project diversity.
- **One failed implementation:** a failed implementation rejects that tested implementation under its recorded conditions and gates; it does not establish that the whole mechanism family cannot work without family-covering evidence.
- **Absolute versus scoped claims:** replace “always” or “never” with the narrowest trigger, behavior, and boundary supported by the evidence; keep explicit non-claims for trivial, unavailable, or out-of-scope cases.
- **Vacuous weakening:** reject a shorter rule that loses its trigger, action, observable proof, or boundary. Generality is useful only when the resulting instruction still changes behavior.
- **Inadequate discriminator:** when two credible explanations predict the same measured result under the chosen intervention, keep the result unresolved and design the next test to separate them.

## Reusable claim record

Use the surrounding artifact's existing fields; do not create a hypothesis entity or a numeric weakness field. The following shape is a checklist, not a new schema:

```text
Observation: what happened and where, with provenance and validity.
Supported conditions: conditions the evidence or the conclusion's validity actually depends on.
Alternatives/counterevidence: live explanations, conflicting cases, and validity limits.
Conclusion: the weakest non-vacuous proposition supported by all relevant evidence and counterevidence here.
Explicit non-claims: stronger scopes, families, mechanisms, or defaults not established.
Decision: the separate next action, owner, authority, and discriminator for a stronger claim.
```

## Downstream handoff

Harness should use this reference when an observation becomes an Evidence interpretation, Readout interpretation, Area Brief conclusion, task finding, or Outcome link. Preserve its existing separation of observations, interpretation, scope/caveats, reuse, disposition, and adoption authority; process completion does not validate a conclusion or authorize a default change.

Session-harvester should use this reference at synthesis and promotion, after extraction has preserved session evidence. Candidate rules should carry their tested scope, evidence lineages, alternatives, counterevidence, explicit non-claims, target cases, and guardrail cases. Repeated sessions from one project do not become cross-project guidance automatically, and no candidate becomes an installed rule without the existing routing and adoption authority.

Agents remains the portable authoring and review owner. Harness remains the durable-record owner, and session-harvester remains the session-induction owner. Downstream consumers should link to this path rather than copy a second claim-selection method.

## Boundaries and provenance

Do not turn this method into an automatic rule generator, a self-improvement service, a scalar weakness optimizer, or a new coordination layer. Do not weaken source authority, user authorization, privacy, safety, acceptance, or installer ownership rules. Do not rewrite historical observations to fit a later conclusion; correct current guidance with an explicit scope and preserve the prior artifact as provenance.

This reference adapts the operational principle in Michael Timothy Bennett, “The Optimal Choice of Hypothesis Is the Weakest, Not the Shortest,” https://arxiv.org/pdf/2301.12987v4. The paper's formal result depends on a finite representation and a uniform task distribution; this repository uses the principle as a disciplined selection rule, not as a numerical optimizer or a direct theorem about software engineering or model behavior.
