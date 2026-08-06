# Ask ChatGPT Pro Mode-Aware Conformance Readout

## Scope and claim boundary

**Method:** Single same-agent manual conformance pass against the current `ask-chatgpt-pro` skill contract. Each case was presented as a user request to the skill interface; the resulting consultation classification and generated prompt shape were inspected against the stated contract.

This readout checks representative routing, authority, stop, output, and artifact behavior. It does not establish general model performance, autonomous trigger precision, or stability across models and runs.

**Result:** 10/10 PASS.

## Cases

### `discover-fresh-audit` — PASS

**Request:** Independently audit a pull request for correctness. The user supplies no preferred diagnosis and does not ask for recommendations or an implementation plan.

**Generated prompt shape:**
- Primary mode: Discover
- Task type: code review
- Working synthesis/hypothesis/selected decisions: omitted
- Required output: findings, unsupported claims, contradictions, competing interpretations, and checks
- Recommendations/next actions/implementation plan: explicitly excluded

**Observed:** The consult remained analysis-only and did not invent a solutioning phase.

### `verify-hypothesis` — PASS

**Request:** Review a timeout defect. The user suspects a cache invalidation race and asks Pro to verify it.

**Generated prompt shape:**
- Primary mode: Verify
- User-Provided Hypothesis contains the race hypothesis once
- Required output asks for competing explanations, discriminating evidence, falsification conditions, confidence, and remaining gaps

**Observed:** The hypothesis was neither omitted nor presented as fact.

### `refine-existing-synthesis` — PASS

**Request:** Review and improve an existing architecture synthesis without repeating the full original audit.

**Generated prompt shape:**
- Primary mode: Refine
- Working Synthesis labeled secondary framing
- Required output asks Pro to verify only load-bearing claims, identify corrections and missing dimensions, and return an improved synthesis

**Observed:** The prompt preserved prior reasoning without promoting it to primary evidence or requesting wholesale rediscovery.

### `decide-hard-soft` — PASS

**Request:** Choose between two storage systems. Data must remain in the EU; lower operational complexity is preferred.

**Generated prompt shape:**
- Primary mode: Decide
- User Requirements And Constraints: EU residency as a hard constraint
- Preferences And Decision Criteria: operational simplicity as a soft preference
- Required output compares alternatives and grounds the recommendation in evidence plus both user-owned inputs

**Observed:** The hard constraint was not weakened, and the soft preference was not hardened into an execution constraint.

### `execute-selected-direction` — PASS

**Request:** PostgreSQL has already been selected. Prepare the migration plan.

**Generated prompt shape:**
- Primary mode: Execute
- Selected Decisions: PostgreSQL
- Required output: behavior, sequencing, compatibility, validation, rollback, and acceptance criteria
- Safety/infeasibility escape remains explicit

**Observed:** The consult did not reopen the database choice by default, but still required Pro to report evidence that would make execution unsafe or impossible.

### `blocking-input` — PASS

**Request:** “Review the current PR” with no identifiable repository, PR, branch, or local checkout.

**Generated behavior:** One pointed question requesting the repository/PR target.

**Observed:** No consult document was written and no document path or refs were returned. The Final Output Rule was not applied.

### `material-nonblocking` — PASS

**Request:** Prepare an execution consult where the exact rollout date is unknown but does not change the selected technical direction.

**Generated prompt shape:**
- Consult produced
- Assumptions And Unknowns labels the date as material but nonblocking
- Required output includes an early rollout-date decision gate and describes what sequencing would change

**Observed:** The user was not interrupted unnecessarily, and uncertainty remained visible.

### `broad-architecture` — PASS

**Request:** Review architecture across several repositories and produce a long-term direction.

**Generated prompt shape:**
- Source manifest describes repository roles and a few authoritative starting areas rather than exhaustive file lists
- Pro may expand scope with an explanation
- Artifact target selected from the broad architecture range, approximately 2,500–5,000 words
- Diagrams requested only for distinct architectural questions

**Observed:** The prompt was neither a vague “inspect everything” request nor a prescriptive path checklist.

### `pdf-opt-in` — PASS

**Request A:** Produce a Markdown review; no PDF requested.

**Observed A:** Artifact Output requires Markdown and explicitly says not to create a PDF.

**Request B:** “Do provide PDF along with other output.”

**Observed B:** Artifact Output requests Markdown and PDF, with one export from finalized Markdown, simple layout, no iterative visual polishing, and a lightweight readability check.

### `secondary-mode-composition` — PASS

**Request:** Refine an existing architecture synthesis and, after the refinement, propose an eight-week implementation direction.

**Generated prompt shape:**
- Primary mode: Refine
- Secondary mode: Execute
- Mode ordering states that Refine controls the architectural conclusion; Execute contributes only a bounded work-program section based on the refined direction
- The secondary section may not reopen, contradict, or relax the primary result

**Observed:** The mixed request was represented explicitly without creating two competing prompt drivers.

## Residual limitations

- This was one same-agent pass, not a blinded or repeated evaluation.
- It checks generated prompt semantics, not the quality of ChatGPT Pro’s eventual answer.
- Static repository tests should preserve these contracts, while future observed failures can justify focused regression cases.
