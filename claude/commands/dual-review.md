# Dual Review: Claude + Codex

Review an implementation plan with Codex before presenting it to the user.

You MUST follow this protocol exactly. Do not skip steps.

## Step 1: Draft the Plan

Based on the user's task: $ARGUMENTS

Explore the codebase thoroughly, then draft a detailed implementation plan. Include:
- Files to create/modify with specific changes
- Architecture decisions and rationale
- Potential risks or trade-offs

## Step 2: Send to Codex for Review

Send the plan to Codex using `mcp__codex__codex` with this prompt:

```
You are a senior engineer reviewing an implementation plan. Your job is to find problems, gaps, and suggest improvements.

Review this plan and respond with ONLY a JSON object (no markdown, no code fences):

{
  "verdict": "APPROVED" | "NEEDS_REVISION",
  "issues": [
    {
      "severity": "critical" | "major" | "minor",
      "description": "What's wrong",
      "recommendation": "How to fix it"
    }
  ],
  "suggestions": ["Optional improvement ideas that aren't blocking"]
}

Rules:
- "critical" = will cause bugs, security issues, or data loss. Must be fixed.
- "major" = significant design flaw or missing requirement. Should be fixed.
- "minor" = style, naming, or small improvements. Nice to have.
- Use APPROVED only when there are zero critical or major issues.
- Be specific. Reference file names, function names, line numbers when possible.

THE PLAN:
<insert your drafted plan here>
```

Save the `threadId` from the response for follow-up rounds.

## Step 3: Process the Review

Parse the JSON response from Codex.

**If APPROVED:** Go to Step 5.

**If NEEDS_REVISION:** For each issue, do one of:
- **Accept**: Modify the plan to address the issue. State what you changed.
- **Reject**: Explain why the issue doesn't apply or why your approach is better.

Then send the updated plan back to Codex using `mcp__codex__codex-reply` with the same `threadId`:

```
I've addressed your review. Here are my responses to each issue:

<for each issue, state: ACCEPTED (with change description) or REJECTED (with reasoning)>

UPDATED PLAN:
<insert updated plan>

Please review again. Same JSON format.
```

## Step 4: Iterate (Max 3 Rounds)

Repeat Step 3 up to 3 total rounds. Track the round number.

If after 3 rounds there is still no APPROVED verdict:
- Present the plan with remaining disagreements clearly marked
- Show Codex's position vs your position for each unresolved issue
- Let the user decide

## Step 5: Present Final Result

Present the final plan to the user with two sections:

### Implementation Plan
The agreed-upon plan.

### Review History
A summary of the review process:
- Number of rounds
- Issues raised and how they were resolved (accepted/rejected)
- Any remaining disagreements (if max rounds reached)
- Codex's final verdict

Format the review history as a collapsible details block:
```
<details>
<summary>Codex Review: {verdict} after {N} round(s) — {X} issues raised, {Y} accepted, {Z} rejected</summary>
... full review back-and-forth ...
</details>
```
