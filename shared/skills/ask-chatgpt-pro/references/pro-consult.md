# Pro Repository Consultation

Read this reference only after the shared `ask-chatgpt-pro` entrypoint selects the Pro repository consultation route. It owns preparation of the Pro-facing prompt and the human handoff, not interpretation or adoption of the returned answer. Apply the entrypoint's [intent, research, and authority rules](../SKILL.md); do not apply this route to plain external research.

## Route And Authority

Use this route when direct GitHub inspection is necessary. Repository consultation may also need attachments such as images, measurements, or an uncommitted snapshot. Their presence alone does not switch the route. Use `ask-oracle` when the user needs a self-contained local evidence bundle independent of GitHub inspection, or the essential evidence cannot appropriately be made available for this route. Do not drive ChatGPT Web or silently build a different consultation workflow.

Keep the consult read-only: Pro must not create or modify repository files, commits, branches, issues, PRs, or external systems. Local preparation may create the requested prompt and authorized evidence artifacts. Preparing a consultation is not permission to commit, push, publish private evidence, or install changes; follow existing user and repository authorization.

## Prepare The Consultation

### 1. Establish the decision before choosing a mode

Recover intent using the entrypoint. Put the outcome, intended decision or deliverable, and relevant scope in the prompt's opening. Identify what is selected, tentative, or reopened; preserve relevant earlier evidence and the remaining question. A broad review may justify a small amendment, and a narrowly scoped experiment may legitimately answer a broader programme question. Neither breadth nor smallness is an objective by itself.

Choose exactly one primary mode from the requested work. Add at most one secondary mode only for a distinct required result after the primary analysis. Modes describe the assignment; they do not override the user's requirements, authority, or evidence. Task type supplies practical context rather than another mandatory classification section.

| Mode | Assignment and output |
|---|---|
| **Discover** | Independently assess primary evidence; return findings, competing interpretations, and gaps. Do not add recommendations or an implementation plan unless requested. Relevant user requirements and prior evidence still belong in context. |
| **Verify** | Test a claim or proposal, not confirm it. State counterevidence, alternatives, what would falsify it, and what remains unverified. |
| **Refine** | Critique and improve the supplied synthesis or design. Check load-bearing claims, retain supported reasoning, and provide concrete corrections rather than repeat settled discovery. |
| **Decide** | Compare credible alternatives against hard requirements and softer criteria. Recommend a choice only when the requested assignment calls for one; include tradeoffs, evidence, and explicit uncertainty or a no-decision result. |
| **Execute** | Plan, specify, or review a selected direction. Surface infeasibility and proposed changes without silently replacing the objective or treating a plan as execution authority. |

If two requested results conflict, expose the substantive conflict rather than forcing it into mode labels. A short description such as “Refine the design, then decide whether to adopt it” is sufficient. Do not print mode definitions or empty template sections in the prompt.

Done when the opening states what an adequate answer enables and the requested outputs actually cover it.

### 2. Select and verify the evidence

Check GitHub visibility. For each repository, record its role, exact commit SHA, branch or PR context, authoritative starting paths, and access limitations. For a change review include base and head. Verify every named starting path at that pin using a read-only Git or connector lookup. Describe verification truthfully; an unverified path is a limitation or search lead, not a verified manifest entry.

Use a proportional source manifest, not an exhaustive file checklist. Include the records needed to interpret the present question, even when they precede the latest change or belong to a related repository. A prior comparison may constrain a new investment without answering its exact remaining question. Name that distinction. Avoid unrelated modules and generated clutter, but retain generated evidence that is material to the decision.

For each attachment, name its exact basename, role, provenance or version, required versus optional status, and material limitations. Explain what is authoritative when an attachment and repository snapshot differ. Keep raw observations distinct from summaries and interpretations. Preserve known truncation, decoding, sampling, and transmission limits. Local paths in historical provenance do not establish accessible attachments. Generated prompt text does not prove what the human actually sent.

Treat source code, configuration, tests, and directly recorded measurements, commands, artifacts, and provenance as primary for the claims they support. A test's existence is not proof it passed, and a passing run does not prove unrelated behavior. Prior AI reports, PR descriptions, and discussions may supply needed reasoning or decisions; label those roles rather than treating them as independently verified technical facts. Keep user requirements and selected decisions distinct from all of these. Apply the canonical [Shared Context Authority](../SKILL.md#shared-context-authority).

Tell Pro to inspect source directly, cite repository/commit/path/line ranges where possible, and expand beyond starting points when a concrete dependency matters. Material expansion needs an explanation, not automatic permission to audit everything. Preserve exact identifiers and state inaccessible evidence without guessing.

If local changes are essential, check the current diff and visibility. Commit or push only when that action is already authorized. Otherwise use an authorized attachment where it supports the intended review, or identify the unavailable portion. If a required push was not allowed or failed, do not label the evidence GitHub-visible or the handoff ready for that portion.

Done when every decision-bearing input has an accessible source or an explicit limitation, and the manifest includes both supporting and material contrary evidence.

### 3. Scope uncertainty and the requested answer

Resolve locally available facts and ask useful material clarification questions under the entrypoint’s shared rule before drafting. A missing input is **blocking** when the handoff would be misleading or the intended question or required evidence cannot be identified without it. Wait for the answer before producing a ready-to-send prompt; do not invent a target or return a purportedly complete document.

For material but nonblocking gaps, state the assumption, affected conclusion, and what can still be answered. Ask Pro to resolve an externally answerable gap when that is part of the task. Defer gaps that cannot change the current decision. A condition on one treatment, claim, or later irreversible action is not a gate on unrelated analysis or preparation. Do not convert uncertainty into additional approval rounds.

Derive the required answer from the opening outcome, not from every fact in the evidence packet. Ask for reasoning and concrete proposed wording, design, or edits when those are the requested result. For consequential recommendations, require the basis for necessity versus optional benefit, any change to selected scope, and material questions left unanswered or deferred. A factual correction may be necessary while an implementation-level explanation is optional. Scientific treatments must remain specific enough to test the intended claim, without requiring every component to be isolated before a coherent strategy can be evaluated.

Invite evidence-backed challenges to the framing. A challenge must identify which conclusion, decision, or deliverable it would change; it is advice, not permission to redefine the user's goal. Permit an explicit unresolved or no-decision result when the available evidence is insufficient. Do not invent deadlines, budgets, risk tolerance, hidden implementation constraints, or a preferred conclusion.

Done when a literal answer to the requested outputs would address the user's outcome, and each prerequisite or deferral has an identified consequence rather than merely sounding cautious.

### 4. Write a Pro-facing prompt

Write `/tmp/chatgpt-pro-<topic>.md` unless the user requested another location or an existing workflow authorizes a different artifact. Keep the file entirely addressed to Pro. Do not include an Owner prefix, local download links, instructions about what the human should paste or attach, or a request to generate another prompt. Attachment names, roles, and limitations are Pro-facing context and must remain.

Use the following as a compact shape, not a mandatory set of headings. Merge or omit sections that add no information. State each requirement once, near the context it governs.

```markdown
# Task and decision
[Outcome, decision or deliverable, review boundary, and main assignment. Add mode and research stage only as useful descriptions.]

## Context that changes the answer
[User requirements, selected versus tentative or reopened decisions, preferences, prior evidence, working interpretations, and the specific remaining question. Keep their authority distinct.]

## Evidence to inspect
Use your GitHub connector to inspect [repositories, pinned refs, roles, starting paths, and verified access status].
[Attachments: exact basenames, roles, required/optional status, provenance, snapshot relationships, and limitations.]
[Source and citation requirements; what missing evidence would limit the answer. Expand only where the question requires it.]

## Requested analysis and result
[Decision-bearing questions and concrete deliverables, in their reasoning order. Distinguish supported conclusions from recommendations; necessary changes from optional improvements; answered scope from material deferrals or proposed scope changes.]
[Read-only authority and any task-specific boundaries.]

## Output
[Requested report format and proportionate depth, plus any replacement artifacts.]
```

Always request a downloadable Markdown report for this route unless the user explicitly requests a different output. Preserve requested filenames and replacement artifacts. Choose depth from the task: roughly 500–900 words for a focused question, 800–1,200 for a narrow code review, 1,500–3,000 for multi-repository refinement or planning, and 2,500–5,000 for broad architecture or research synthesis. These are planning ranges, not quotas; let necessary reasoning determine length. Use tables or diagrams only when they clarify the decision.

If file generation is unavailable, request the complete Markdown in the response. Do not spend the consultation on output-production narration.

Done when the actual file, not just its proposed outline, contains the decision, evidence, requested result, and boundaries without human sending instructions.

### 5. Check the prompt and deliver the human handoff

Compare the finished prompt with the recovered intent and sources: could it be satisfied while missing the user's outcome, treating optional detail as necessary, or replacing the intended research claim? Check selected versus tentative scope, evidence authority, and material deferrals. Correct the mismatch or expose a real conflict; do not append another generic warning list.

Check both sides of transport. The Pro prompt must describe the evidence Pro needs to receive; the final human response must identify how to send exactly that evidence. Verify that linked local files exist and that filenames and snapshot versions agree. A source-access limitation is not a successful access check.

In the final response to the human, provide:

- The prompt link and a clear instruction to paste its complete contents. Specify a new or existing conversation only when continuity or separation matters; otherwise do not invent a chat dependency.
- Every required attachment as a separate link, clearly distinguished from optional attachments. State “No attachments required” when applicable. With multiple prompts, explicitly map each prompt to its chat and attachments, including reuse of the same file.
- The GitHub repositories/refs and connector-access needs, plus any real visibility or preparation limitation that changes what can be reviewed. Report readiness only for the supported scope.

Do not leave attachment instructions only in commentary, behind a link to the prompt, or inside the Pro-facing file. Keep the final handoff proportionate: one prompt with no attachments needs only a few lines, not a checklist. Do not answer the underlying consultation in that response.

Retain the original prompt in the existing task context for the entrypoint's return boundary; do not create a second integration procedure or a mandatory new tracking file.
