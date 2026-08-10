# Learning Design For Technical Explanations

Use these principles to turn source inspection into a mental model the user can operate, not a polished summary they can only recognize.

## Design The Learning Contract

- Name a capability, not a topic: “trace a failed request from handler to retry queue” is testable; “understand the queue” is not.
- Bound depth by novelty, coupling, blast radius, reversibility, and the user's next task. A small local change should not trigger a textbook; a cross-boundary change should not receive a file list.
- Infer expertise from the conversation, vocabulary, and repository work. Offer a skippable beginner layer while keeping the main path concise; instruction that helps a novice can become redundant load for an expert.
- Separate immediate comprehension, near transfer, local calibration, and durable retention. One session can probe the first three only in bounded ways; durable retention requires delayed retrieval. Do not create reminders, schedulers, or background loops unless the user separately asks.

## Build A Causal Mental Model

- Move from purpose to prerequisites, intuition, structure, one concrete dynamic trace, invariants, and consequences. “Intuition before details” does not mean intuition without evidence.
- Use a worked example with small realistic data, then require the learner to explain a step or apply the model to a varied case. The explanation and self-explanation work together.
- Pair important abstractions with source anchors. A mental model should compress code while preserving the facts needed to predict behavior.
- Include a counterexample, failure path, or boundary condition when it sharpens the rule. Avoid exhaustive edge-case catalogs that hide the main mechanism.
- Use headings, signaling, and learner-controlled segments. Remove ornamental anecdotes, repeated prose, and decorative diagrams that compete with the core model.

## Check Understanding

- Prefer retrieval before reveal: ask the user to predict, trace, explain why, compare, or apply. Recognition and rereading can create familiarity without usable recall.
- Use two to five questions proportional to the target. Cover behavior, causality, contracts, failure, tradeoffs, or transfer; avoid trivia and copied phrases.
- Give feedback after the attempt. State the supported answer, the reasoning chain, and the likely misconception. Multiple-choice distractors can teach false information when feedback is absent.
- Use multiple choice only when the user requests it or recognition is the actual task. Balance correct-answer positions, option length, grammar, specificity, and confidence; use plausible misconception-based distractors; avoid “all/none,” joke answers, and fixed answer patterns.
- Ask for confidence only when calibration matters, then compare it with the answer. Do not treat confidence as evidence of understanding.

## Interpret What A Check Establishes

- **Immediate comprehension:** A same-session explanation, prediction, or trace can show that the learner can currently operate the presented model. It does not show that the model will persist.
- **Near transfer:** A varied but structurally similar case can sample whether the learner applies the model beyond the worked example. One successful item is evidence for that item, not broad transfer.
- **Local calibration:** When confidence is collected, compare it with the evidence-backed performance on the same item. This reveals local over- or under-confidence, not general self-knowledge.
- **Durable retention:** Establishing retention requires delayed retrieval under relevant conditions. A quiz, diagram, saved artifact, or confident answer in the current session cannot establish it.

## Use Micro-Worlds Deliberately

A micro-world is a small manipulable environment that makes one hidden mechanism observable. It is not a miniature product or an animated documentation page.

- Start from a question the user cannot answer, such as “which rule is active at this step?” or “how does changing this coordinate alter projection?”
- Expose the relevant state, controls, and transitions; provide step, reset, and side-by-side comparison when useful.
- Let the user form a prediction, change one variable, observe the result, and reconcile the result with the source model.
- Keep the model faithful to named invariants and label every simplification. Link states and transitions back to source paths, equations, or tests.
- Use synthetic, non-sensitive data. Do not execute target code, migrations, network calls, or external side effects unless the user explicitly authorizes that separate action and project policy permits it.
- Grow the world only when a new learning question appears. Stop once the mechanism is inspectable; throwaway code is preferable to a new maintained subsystem.

## Create Shared Spaces Without Creating A Second Source Of Truth

- A shared explanation should be editable, commentable, and anchored to a pinned ref or source version. Record vocabulary, diagrams, decision rationale, known uncertainty, and open questions.
- Treat the artifact as a boundary object for discussion, not proof of consensus or a replacement for code, tests, ADRs, or authoritative docs.
- Separate stable mental models from volatile status. Link to live project state instead of copying it.
- Name an owner and refresh trigger for durable artifacts. Mark stale or ref-mismatched material visibly.
- Require confirmation before writing to Notion, a PR, an issue, a shared drive, or another external destination.

## Evidence Basis And Limits

- Geoffrey Litt's [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html) motivates background-first explainers, intuition, literate diffs, quizzes as a speed regulator, micro-worlds, shared spaces, and understanding for participation.
- Peter Naur's [Programming as Theory Building](https://pages.cs.wisc.edu/~remzi/Naur.pdf) and Margaret-Anne Storey's [cognitive debt essay](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) frame the maintained human theory of a program as a software asset.
- Heinonen et al.'s [systematic review of programmers' mental models](https://arxiv.org/abs/2212.07763) supports treating mental models as organized representations used to explain, predict, interpret, and decide, while warning that acquisition in modern programming settings remains under-specified.
- Roediger and Karpicke's [retrieval-practice experiments](https://doi.org/10.1111/j.1467-9280.2006.01693.x), Chi et al.'s [self-explanation study](https://doi.org/10.1207/s15516709cog1803_3), Kalyuga et al.'s [expertise-reversal review](https://doi.org/10.1207/S15326985EP3801_4), and Mayer and Moreno's [multimedia-learning research](https://doi.org/10.1016/S0959-4752(01)00018-4) motivate retrieval, self-explanation, adaptive scaffolding, signaling, coherence, and segmenting.
- Butler and Roediger's [multiple-choice feedback experiments](https://doi.org/10.3758/MC.36.3.604) motivate immediate corrective feedback and caution about distractor misinformation.
- Noss and Hoyles' [constructionism and microworlds review](https://doi.org/10.1007/978-3-319-02600-8_3) supports manipulable external representations while preserving the tension between teaching specific content and open construction.
- Mathieu et al.'s [shared mental models study](https://doi.org/10.1037/0021-9010.85.2.273) supports the relationship between convergent task/team models, team process, and performance.

Most direct learning evidence comes from educational settings, not professional AI-assisted code review. Evidence about micro-worlds and shared mental models is also context-dependent and does not directly validate this workflow for professional engineering teams. Treat the mechanisms above as evidence-informed design inputs that need task-based forward testing; report same-session checks as probes of immediate comprehension, sampled near transfer, or local calibration, and never as proof of broad transfer or durable retention.
