---
name: distill-source
description: Read a user-provided paper, article, docs page, GitHub repo, or skill file and extract what should be adapted to the current repo - mechanisms, assumptions, invariants, failure modes - into a repo-fit adaptation brief before any code/doc/skill change. Use when the user points at a paper/article/docs page/GitHub skill file/source link and asks what to adapt to this repo/setup; this is source-to-codebase distillation, not ML knowledge distillation. Not for already-completed research write-ups (use integrate-research) or broad multi-source/multi-agent research (use prepare-dynamic-workflow).
---

# distill-source

Take one already-available external source - a paper, article, docs page, GitHub repo, or
skill/`SKILL.md` file the user points at, pastes, or attaches - and work out what, if anything,
this repo should adapt from it, before touching any code, doc, task, or skill. Not a scraper, not a
capture pipeline, not a memory system, and not ML knowledge distillation.

**Usage:**
```
/distill-source <url-or-path>
/distill-source https://arxiv.org/abs/xxxx.xxxxx
/distill-source ~/Downloads/some-skill/SKILL.md "focus on the retry logic"
/distill-source https://github.com/org/repo/blob/main/docs/design.md
```

## Composition role

- **Driver** for its own scope: parsing the source, reading target-repo context, and producing the
  adaptation brief. Owns that workflow end to end.
- **Helper** for everything downstream. It recommends a routing (chat-only, inbox item, task, ADR,
  skill-lifecycle proposal) but never executes that durable write itself - it names the target and
  stops. The receiving skill's own protocol governs the actual write.
- Defers to stricter **protocols** already in the stack: task/inbox/ADR creation belongs to
  `harness-add-tasks` / `harness-add-inbox` / `harness-adr` in a Harness-tracked repo;
  `skill-lifecycle`'s add/change/merge/deprecate gates decide whether a distilled idea becomes a
  durable skill. This skill never bypasses those gates.

## When the source is not yet readable

This skill only runs on an already-available source (pasted, linked, or attached). If the source is
a Telegram channel/post or an X post/thread that first needs a bounded local capture, that capture
is a separate, prior step: use the `source-capture` tool (`tools/source-capture/` and its workflow-contract doc, in a
Personal-OS-managed repo) to produce a packet, then run this
skill on that packet's `distill-source-input.md` as the already-available source. Do not scrape,
crawl, poll, or otherwise expand this skill into a capture pipeline - if `source-capture` is not
available, ask before improvising a capture method.

## Workflow

1. **Parse the source and target.** Extract the source pointer (URL, file path, or pasted text)
   and the target repo (current repo unless the user names another). If the source or the scope of
   "what to adapt" is genuinely ambiguous, ask one focused question with AskUserQuestion rather than
   guessing.
2. **Read the source**, respecting access gates (see Stop and ask below):
   - URL: fetch with WebFetch.
   - Local file/attachment: Read it directly.
   - Never install or copy a third-party skill file verbatim - read it to extract the mechanism,
     not to reuse the file.
3. **Read only relevant target-repo context**: `CLAUDE.md`/`AGENTS.md`, `README.md`, project docs,
   and existing skills/tasks/ADRs that already cover the same territory. Use Glob/Grep to find
   candidates by topic term, then read only the matched files - do not read whole trees.
4. **Extract, don't summarize**: transferable mechanisms, load-bearing assumptions, invariants,
   workflows, failure modes, evaluation/validation ideas, and what is explicitly not transferable
   (different stack, license, scale, threat model).
5. **Produce the repo-fit adaptation brief** (template below) before proposing or making any
   implementation change.
6. **Decide retention and routing** using the rules below.

## Retention rules

Save a durable artifact only when the distillation is actionable (names a concrete next step),
reusable (will be referenced again, not a one-off curiosity), decision-shaping (changes what the
repo does next), or likely to become a task/ADR/skill/doc change. Otherwise answer in chat only, or
route a short inbox item - do not create a durable file for a "neat but not actionable" read.

A saved artifact is a **reviewed adaptation brief**, not a raw capture and not durable memory by
itself: it records the extraction and the fit judgment, not the source's full text, and it does not
by itself promote anything into tasks, ADRs, skills, or code - that is always a separate, reviewed
step.

Default save location in a generic repo: `research/distillations/YYYYMMDD-<source-slug>.md`,
matching this repo's `research/prompts/` (`research-prompt`) and `research/findings/`
(`integrate-research`) sibling conventions. In a Harness-tracked repo, prefer routing through
`harness-add-inbox` / `harness-add-tasks` / `harness-adr` instead of a bare file when the target is
that Harness project.

## Output template

```markdown
# Distillation: <source title>

**Source:** <url/path, author/repo, date read>
**Target repo:** <repo/path>

## Thesis
<one paragraph: what the source claims or does>

## Transferable Mechanisms
- ...

## Non-Transferable Assumptions
- ...

## Fit To This Repo
<directly usable / adaptable with changes / incompatible / unknown, per element>

## Proposed Changes
- ...

## Risks / Failure Modes
- ...

## Validation Plan
- ...

## Open Questions
- ...

## Routing
<chat-only | inbox item | task | ADR | skill-lifecycle proposal - and why>
```

Always output either the rendered brief (chat-only routing) or the saved file's path plus a short
summary of the brief - never just "done."

## Composes with (do not duplicate)

- `source-capture` (`tools/source-capture/`) - run first, not by this skill, when the source is a
  Telegram or X source needing a bounded local packet before distillation (see "When the source is
  not yet readable" above).
- `ask-oracle` / `research-prompt` - hand off when the source needs an external deep-research
  consult beyond what is already provided.
- `prepare-dynamic-workflow` - hand off when there are many sources, or the extraction itself needs
  multi-agent fan-out.
- `integrate-research` - use instead of this skill when the input is already a completed research
  report/output, not a raw external source.
- `skill-lifecycle` - run before folding a distilled idea into a durable skill; this skill's
  Routing section proposes, `skill-lifecycle` decides add/merge/deprecate.
- `harness-add-inbox` / `harness-add-tasks` / `harness-adr` - own the actual write when the target
  is a Harness-tracked project; this skill hands off rather than writing task/ADR files itself.

## Guardrails (S-12 boundary)

- No scraper, background monitor, scheduler, or broad capture API client - the source is already in
  hand (pasted, linked, or attached) when this skill runs.
- No raw-source warehouse: do not persist the full source text as a durable artifact; the brief
  cites and quotes only what supports the extraction.
- No credential flow: never fetch a source that requires auth/login without asking first.
- No automatic promotion: a distillation brief is a proposal. Absorbing it into memory, Harness
  tasks/ADRs, or repo code/docs is always a separate, reviewed action.
- Never install a third-party skill file verbatim; extract its mechanism and re-author it for this
  repo's conventions.

## Stop and ask

- Before fetching a private or authenticated source.
- Before creating a persistent raw-source archive.
- Before installing a third-party external skill verbatim.
- Before changing code/docs/tasks based on a distillation without review.
- Before promoting a distilled idea into global skills/practices automatically.
