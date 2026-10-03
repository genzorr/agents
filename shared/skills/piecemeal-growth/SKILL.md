---
name: piecemeal-growth
description: Apply a piecemeal growth lens to design, implementation, refactoring, or review only when the user names this skill or explicitly requests piecemeal growth, piecemeal mode, or piecemeal mentality as the task approach. Do not activate for concept discussion or ordinary coding requests.
---

# Piecemeal Growth

Use this task-scoped lens alongside the current design, implementation, refactoring, or review workflow; that workflow retains execution, verification, and completion ownership. Apply it to the full requested scope without adding a separate report, gate, or lifecycle.

Ground design choices in present requirements, supported workflows, and credible failures whose likelihood or cost warrants handling. For proposed configuration, concurrency, fallback paths, validation, or abstractions, identify the concrete pressure they address; omit machinery justified only by hypothetical future uses. State load-bearing assumptions in the current work product and make violations produce useful evidence of the unmet contract.

When new requirements or recurring failures expose that pressure, repair the affected design and generalize only as far as the concrete cases require. Local repair may consolidate shared knowledge or reshape a boundary when repeated patches scatter rules across callers or undermine coherent structure. Choose the smallest coherent mechanism that fulfills the whole contract; do not impose a deletion quota or treat anecdotes as proof of general effectiveness.

Keep real contracts, security and durable-data safeguards, boundary enforcement, and scientific, numerical, and reproducibility obligations intact. Useful failures must still perform required cleanup and recovery and preserve evidence needed to diagnose the cause. A narrow implementation must satisfy every requested requirement; simplicity does not excuse reduced scope or weakened verification.
