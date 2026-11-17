---
name: review-change
description: Review code changes, diffs, branches, pull requests, implementation work, or documentation-only topics for correctness, regressions, missed edge cases, security, performance, maintainability, consistency, stale references, and missing verification. Use for general code/PR review, post-implementation review, risk-focused review, or a docs-only audit when no diff exists.
---

# Review Change

Review the change as a senior engineer with fresh eyes. Default to read-only review; do not edit code unless the user explicitly asks to fix findings.

For supporting `docs/*.md`, resolve from this installed skill’s directory, or repository-root `docs/` in the source checkout. References use this same lookup for their conditional guides; do not resolve them from the consumer project’s cwd.

## Review modes

These modes apply to code reviews and documentation-only audits. State which mode actually ran.

- **Review:** examine the entire resolved change or documentation topic against the original request and contracts.
- **Repeat review:** start a new independent reviewer agent with a fresh context, who neither implemented the change nor participated in its previous reviews. Give it the original request, contracts, original base/topic/path scope, current target including fixes and new files, and available source evidence; withhold implementation discussion and previous review conclusions until it has formed its own findings. It must review the entire current change against the original base, or the entire original documentation scope. A follow-up to the previous reviewer or a diff of only the latest fixes is not a repeat review. If an independent agent is unavailable or delegation is prohibited, report the repeat review as incomplete rather than substituting self-review.
- **Fix verification:** after every batch of fixes to review findings, verify each finding's original failure scenario and relevant regressions, and establish applicable check evidence before claiming it closed. Record each finding as closed, still present, or unverified with evidence. A new substantive verification request uses a fresh independent reviewer context; clarification of an issued report may retain its context. Reuse still-applicable checks and rerun when relevant inputs changed, evidence conflicts or a required check demands it. Call a focused pass **Fix verification**; it does not replace a requested repeat review. A full repeat review may verify fixes in the same pass, with no compulsory separate preceding verification review. Supply original failure scenarios for that verification after the reviewer forms its whole-change findings; if verification is blocked, leave affected findings unverified.

## Inputs

The user may provide terse context:

```text
review-change <what changed, why, what to focus on, optional PR/branch/path>
```

Infer the rest from the project:

- project conventions: `AGENTS.md`, `CLAUDE.md`, README, package config, tests, CI config, local rules;
- expected behavior: user context, active task/goal if present, specs/docs/tests, PR title/body, nearby code;
- review scope: explicit paths/PR/branch first, then staged/unstaged diff, then current branch against upstream/main.

If the request is explicitly a documentation-only audit, read and follow [references/docs-only-audit.md](references/docs-only-audit.md) instead of this code-review workflow. That route is read-only, does not require a code diff, and reports findings in chat by default.

For a code or change review, if there is no discoverable diff, PR, branch comparison, or path scope, ask one concise question for the review target.

## Workflow

1. Resolve review target:
   - explicit PR URL/number, branch, commit range, path list, or user-provided diff;
   - otherwise current working tree diff;
   - otherwise current branch compared to merge base with the default upstream/base branch.
   Record the original base and current revision, or identify the working-tree snapshot including untracked files; for a documentation audit, record the topic and document scope. Retain this scope for repeat reviews. Bind findings to the examined version and disclose changes made after that version.
2. Read project instructions and the smallest set of files needed to understand the change.
3. Inspect the diff first, then read full surrounding files for changed behavior.
4. Identify intended behavior and risk areas from the user's argument. If the user names focus areas, prioritize them without ignoring obvious high-severity issues elsewhere.
5. Run cheap, relevant read-only checks when practical, such as existing tests/lint for touched areas. Do not run destructive, slow, or environment-mutating commands unless the user asked.
6. When the diff changes integration topology, a shared substrate, cross-component coordination/control, or recovery behavior, read `docs/whole-system-review.md` using the supporting-document lookup above and apply its optional lens. Skip it for contained local changes.
7. Follow the Review Checklist route below for the affected behavior and reader tasks.
8. Produce findings first, ordered by severity. If no issues are found, say so clearly and mention any verification gaps.

## Optional Deep Review

Repeat review requires the independent pass defined above. Additional independent passes for an initial or deep review are optional; use them only when the user explicitly asks for multi-agent, deep, parallel, or adversarial review and the runtime supports it.

Recommended independent lenses:

- correctness and edge cases;
- security, privacy, and data handling;
- performance, scalability, and resource use;
- simplicity, maintainability, and over-engineering;
- product/UX behavior when UI or user workflow changed.

The main agent must adjudicate reviewer output. Do not blindly relay or apply every finding. Keep only concrete, reproducible, task-relevant issues.

## Review Checklist

For code/change review, read [review checks](references/review-checks.md) and check the requirements that apply to the change. Inspect intended behavior, actual outcomes, error/recovery paths, independent expectations and affected current guidance, including pages outside the diff. For documentation, follow a representative reader task; working links alone cannot establish usability or complete portable references.

## Finding Dispositions

Bind each finding to evidence and a concrete failure scenario, and distinguish introduced defects from pre-existing issues. An inherited issue is not automatically in scope; explain why it affects the requested outcome. Keep a meaningful disposition in the existing review/task record (for Workbench, a separate scoped report owns review subjects/findings; the task records acceptance against retained report/evidence versions): **fixed** with verification evidence, **dismissed** with an evidence-based reason answering the scenario, **authorized deferral** naming the actual decision-maker and retained obligation, or **unresolved**. A proposed fix or passing unrelated check does not close a finding.

Disputed findings return to the actual acceptor under the supplied mandate. Required defects remain acceptance blockers unless an authorized amendment or waiver changes that gate; deferral alone is not acceptance. When independent closure confirmation is required, the executor cannot dismiss or self-verify away that requirement. Fix verification reports closed, still present or unverified consistently with these dispositions.

Repeated defects can justify preventive improvements under actual accepted scope, including an explicitly granted bounded improvement/amendment mandate; otherwise propose them to the user or an empowered orchestrator. Recurrence or a review role grants no authority to edit rules, skills or checks. Carry consequential changes, their authority and original/revised basis into the reviewed target and final handoff; ordinary repairs already within scope continue.

## What Not To Flag

- Personal style preferences not backed by project conventions.
- Missing features that were not requested.
- Theoretical risks without a concrete failure scenario.
- Refactors that are merely different, not clearly safer or simpler.
- Low-value churn in unrelated files.

## Output

Read [reporting](references/reporting.md) when returning findings or a clean result. Say which review mode ran, who reviewed it, whether the context was fresh, what was examined or left unchecked, which checks ran or were reused, and what happened to each finding. A clean fix verification cannot become a whole-change PASS. Preserve every unresolved required defect and material gap; no count or length cap removes them.
