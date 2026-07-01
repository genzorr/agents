---
name: review-change
description: Review code changes, diffs, branches, pull requests, or implementation work for correctness, regressions, missed edge cases, security, performance, maintainability, over-engineering, and missing verification. Use when the user asks for a general code review, PR review, post-implementation review, or risk-focused review of changed code.
---

# Review Change

Review the change as a senior engineer with fresh eyes. Default to read-only review; do not edit code unless the user explicitly asks to fix findings.

## Inputs

The user may provide terse context:

```text
review-change <what changed, why, what to focus on, optional PR/branch/path>
```

Infer the rest from the project:

- project conventions: `AGENTS.md`, `CLAUDE.md`, README, package config, tests, CI config, local rules;
- expected behavior: user context, active task/goal if present, specs/docs/tests, PR title/body, nearby code;
- review scope: explicit paths/PR/branch first, then staged/unstaged diff, then current branch against upstream/main.

If there is no discoverable diff, PR, branch comparison, or path scope, ask one concise question for the review target.

## Workflow

1. Resolve review target:
   - explicit PR URL/number, branch, commit range, path list, or user-provided diff;
   - otherwise current working tree diff;
   - otherwise current branch compared to merge base with the default upstream/base branch.
2. Read project instructions and the smallest set of files needed to understand the change.
3. Inspect the diff first, then read full surrounding files for changed behavior.
4. Identify intended behavior and risk areas from the user's argument. If the user names focus areas, prioritize them without ignoring obvious high-severity issues elsewhere.
5. Run cheap, relevant read-only checks when practical, such as existing tests/lint for touched areas. Do not run destructive, slow, or environment-mutating commands unless the user asked.
6. Review for the checklist below.
7. Produce findings first, ordered by severity. If no issues are found, say so clearly and mention any verification gaps.

## Optional Deep Review

For normal or small diffs, inline review by this agent is the right default. For a **substantial change** — many files, large diffs, public API/data-contract changes, or a run-produced branch — prefer an independent reviewer pass when the runtime supports it (a fresh `code-reviewer` subagent that is not given the implementer's plan/reasoning, or cross-model review), even if the user did not explicitly ask; when such a pass is warranted but unavailable, note the residual risk. In a Harness repo this is Tier 1+ on the review-independence ladder (`docs/harness-ops-operator-guide.md` → *Review Independence*). Also run independent passes whenever the user explicitly asks for multi-agent, deep, parallel, or adversarial review.

Recommended independent lenses:

- correctness and edge cases;
- security, privacy, and data handling;
- performance, scalability, and resource use;
- simplicity, maintainability, and over-engineering;
- product/UX behavior when UI or user workflow changed.

The main agent must adjudicate reviewer output. Do not blindly relay or apply every finding. Keep only concrete, reproducible, task-relevant issues.

## Review Checklist

- **Correctness**: wrong conditions, stale assumptions, broken invariants, off-by-one errors, bad async/order behavior, incorrect state transitions, data loss.
- **Requirements**: mismatch with user request, task acceptance criteria, docs, API contract, or PR intent.
- **Edge cases**: empty/null inputs, boundary sizes, malformed external input, retries, concurrent operations, partial failures.
- **Security and privacy**: authz/authn gaps, secret leakage, injection, path traversal, unsafe deserialization, excessive logging, PII exposure.
- **Performance**: avoidable N+1 queries, unbounded loops, repeated expensive work, cache invalidation, large memory spikes, slow startup/build paths.
- **Interfaces**: breaking API changes, migration gaps, inconsistent names/types, confusing return values, missing compatibility handling.
- **Maintainability**: over-engineering, duplicated logic, unnecessary abstractions, hidden coupling, complex code where a simpler local pattern exists.
- **Verification**: missing or weak tests for risky behavior, tests that do not exercise the changed contract, CI gaps.

## What Not To Flag

- Personal style preferences not backed by project conventions.
- Missing features that were not requested.
- Theoretical risks without a concrete failure scenario.
- Refactors that are merely different, not clearly safer or simpler.
- Low-value churn in unrelated files.

## Output

Lead with findings. Use this format:

```markdown
Findings:
- [P0] Title
  File: path/to/file.ext:123
  Problem: What is wrong.
  Impact: Concrete failure scenario.
  Fix: Minimal direction.

Open questions:
- ...

Verification:
- Ran: ...
- Not run: ... because ...
```

Severity:

- `P0`: critical correctness, security, data loss, or production outage risk.
- `P1`: likely bug, requirement miss, broken user workflow, or serious maintainability/performance issue.
- `P2`: meaningful issue that should be fixed before merge if time permits.
- `P3`: minor cleanup only when useful and clearly tied to the change.

Rules:

- Reference file and line for each finding whenever possible.
- Cap findings at the highest-signal 10 issues.
- If the user asks to fix, fix only accepted or clearly valid findings, then rerun relevant verification.
