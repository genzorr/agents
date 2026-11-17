# Report a review


Lead with findings. Report the actual mode, reviewer, target, coverage, and evidence even when there are no findings. Preserve these limits when summarizing delegated results: a clean fix verification must not become a whole-change PASS, and incomplete coverage must remain explicit. Use this format:

```markdown
Findings:
- [P0] Title
  File: path/to/file.ext:123
  Problem: Evidence and what is wrong; introduced or pre-existing.
  Impact: Concrete failure scenario.
  Fix: Minimal direction.
  Disposition: Fixed / dismissed with evidence-based reason / authorized deferral / unresolved; decision-maker and evidence when applicable.

Review coverage:
- Mode and reviewer: review / repeat review / fix verification; reviewer identity and context freshness; distinguish report clarification from a new substantive request.
- Target: original base and examined revision/snapshot, or documentation topic and scope.
- Examined: files and behavior paths actually inspected; omitted scope and remaining gaps.
- Fix verification, when applicable: each original finding, disposition, and supporting evidence.

Open questions:
- ...

Verification:
- Ran in this pass: ...
- Reused evidence: ... with its source/version and limits.
- Not run: ... because ...
```

Severity:

- `P0`: critical correctness, security, data loss, or production outage risk.
- `P1`: likely bug, requirement miss, broken user workflow, or serious maintainability/performance issue.
- `P2`: meaningful issue that should be fixed before merge if time permits.
- `P3`: minor cleanup only when useful and clearly tied to the change.

Rules:

- Reference file and line for each finding whenever possible.
- Prioritize and group findings in a compact summary while preserving every unresolved required defect and material coverage gap in the complete attributable result. Expose blocking overflow and separate optional suggestions from required corrections. Link the complete report when one exists; if the recipient cannot access it, include the decision-bearing information or disclose the access gap. A count or length limit never removes required findings or gaps.
- If the user asks to fix, fix only accepted or clearly valid findings, then complete Fix verification in [the parent skill’s review modes](../SKILL.md#review-modes).
