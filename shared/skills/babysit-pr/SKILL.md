---
name: babysit-pr
description: Watch a pull request, branch, or current change for CI/check failures; inspect failing logs; fix failures attributable to the branch; rerun relevant checks; and optionally use review-change after non-trivial fixes. Use when the user asks to babysit, monitor, watch, or clean up CI for a PR or branch.
---

# Babysit PR

Keep a PR or branch moving through checks without changing the intended feature. This skill is for CI/check cleanup, not broad feature work.

## Scope

The user may provide:

```text
babysit-pr <PR URL/number, branch, current PR, or failure focus>
```

If no PR is provided, infer the current branch and use the repository's normal PR/CI tooling. Ask one concise question only if there is no branch, PR, or failing check to inspect.

## Workflow

1. Resolve the target PR/branch and base branch.
2. Read project instructions and CI/test commands from repo docs, package config, workflow files, and previous terminal output.
3. Inspect current status:
   - PR checks and failing jobs;
   - recent workflow/run logs;
   - local git status and diff;
   - whether failures are new on this branch or likely base/infra flakes.
4. For each failing check:
   - read the smallest useful log region first, then expand around the failure;
   - identify the root cause before editing;
   - reproduce locally when practical with the narrowest relevant command;
   - fix only failures attributable to this PR/branch.
5. Rerun relevant local checks after each fix batch.
6. If the fix is non-trivial, security-sensitive, touches shared behavior, or changes public interfaces, run `review-change` on the resulting diff before reporting done.
7. If the user asked for active watching, continue in a bounded loop or use the runtime's native automation/watch facility when available. Report the watch cadence and stop condition.

## Tools And Commands

Prefer the project's normal tooling. Common GitHub CLI commands:

```bash
gh pr status
gh pr view <pr> --json number,title,baseRefName,headRefName,url,statusCheckRollup
gh pr checks <pr>
gh run list --branch <branch> --limit 10
gh run view <run-id> --log-failed
gh run watch <run-id>
```

Use provider-specific equivalents when the repository uses GitLab, Buildkite, CircleCI, Jenkins, or another CI system.

## Fix Rules

- Do not rewrite the implementation just to satisfy CI. Preserve the feature intent.
- Do not fix unrelated failures on the base branch unless the user explicitly asks.
- Do not mask failures by deleting tests, weakening assertions, skipping checks, raising timeouts blindly, or suppressing lint without cause.
- Do not push commits, force-push, merge, close, or approve PRs unless the user explicitly requested that action and repo policy permits it.
- Never expose secrets from logs. Summarize secret-related failures without copying sensitive values.
- If a failure is flaky or infrastructure-related, document the evidence and rerun/watch; do not invent a code fix.
- If credentials, permissions, production services, or third-party outages block progress, stop and report the blocker.

## Review-Change Integration

Use `review-change` after fixes when any of these are true:

- more than one file changed;
- behavior changed rather than only metadata/config;
- the fix touches auth, data handling, migrations, public APIs, or shared utilities;
- the failure was subtle or the first fix attempt failed;
- the user asked for review as part of babysitting.

Do not spawn an endless review/fix loop. One review pass after the final fix batch is usually enough unless the user asks for more.

## Output

Keep the final report operational:

```markdown
Target: <PR/branch>
Status: <green | still failing | blocked>

Fixed:
- <file>: <change and failure it addressed>

Checks:
- checks passed
- <failed/skipped/watching check only>: <detail>

Remaining:
- <only unresolved failures or blockers>
```

If no code changes were needed, say what changed in CI status or why the failure was not branch-caused.
List check commands or log output only when a check failed, was skipped, is still
watching, produced a surprising result, or the user explicitly asked for full accounting.
