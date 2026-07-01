# Global Codex Instructions

These instructions apply across Codex sessions unless a project-level `AGENTS.md` gives a more specific rule.

## Response Discipline

- Be concise without losing clarity.
- Do not use step-narration banners like "Step 1", "---", or "Now implementing" in user-facing output.
- Do not restate the user's request before answering.
- Do not add a closing recap when a concrete summary already exists, such as a verifier table, diff list, or commit message.
- If correction is warranted, acknowledge briefly and move on.

Exceptions: detailed explanations, walkthroughs, plans, ADRs, handoffs, and genuine ambiguities where structure is the content.

## Reading Discipline

- Prefer file/path discovery before content search when paths are enough.
- Use `rg` or `rg --files` first when searching the filesystem.
- For files under roughly 150 lines, reading the whole file is fine.
- For larger source files, search for the symbol first, then read the relevant region.
- Read full config files, schemas, ADRs, and threat models when the task requires reasoning across the whole artifact.
- Do not repeatedly reread content already available in the current session unless something changed.

## Surgical Changes

Every changed line should trace to the user's request.

- Do not make drive-by edits, broad reformatting, opportunistic renames, or unrelated cleanups.
- Match existing local style even when another style would also be valid.
- Remove imports, variables, helpers, or types made unused by your own edit.
- Leave pre-existing unrelated dead code alone unless asked to remove it.
- If a related but out-of-scope issue appears, surface it instead of fixing it silently.

Before reporting done, inspect the diff and make sure each changed line has a task-related reason.

## Think Before Coding

- State load-bearing assumptions when they affect implementation scope, data shape, or API contracts.
- If a request has multiple plausible interpretations that lead to materially different code, ask a pointed question or name the assumption you are taking.
- If there is a materially simpler approach than the one implied by the request, surface it briefly before implementing.
- Stop and ask when requirements are contradictory or the current state does not make sense.
- Do not ask about trivial preferences where the existing codebase gives an obvious default.
