# Code Comments and Docstrings Mode

Preserve rationale, invariants, public contracts, units, edge conditions, safety notes, licenses, generated markers, suppression directives, tool-consumed syntax, and examples executed by doctest or another runner. Remove comments that only restate the code and investigation history that belongs in a commit or durable record.

Edit no executable behavior. Treat annotations, formatter or linter controls, doctest prompts, documentation directives, and generated-code markers as machine-consumed until verified otherwise. When files change, inspect the diff and run proportionate syntax, documentation, or test validation; a prose-only reading cannot prove that tool-consumed content survived.

Follow the active repository's code-comment policy. In Agents, `codex/AGENTS.md` and `claude/rules/code-comments.md` are the semantic sources for their respective platform guidance, not traveling skill dependencies.
