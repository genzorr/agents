---
name: zoom-out
description: Explain how an unfamiliar code area fits into the broader system. Use when the user asks to zoom out, asks for a map, or needs higher-level context before changing code.
---

# Zoom Out

Give a higher-level map before proposing changes.

## Workflow

1. Identify the code area, feature, or concept the user is asking about.
2. Read project docs, active harness context if present, and the nearest tests.
3. Trace callers and callees with Grep/Glob before reading large files.
4. Explain the relevant modules, data flow, interfaces, side effects, and verification points.
5. Call out uncertainty and the next file or test that would resolve it.

## Output

```markdown
Map: <one-sentence overview>

Modules:
- <module>: <role and key interface>

Flow:
1. <important step>

Verification:
- <tests/commands that exercise this area>

Open questions:
- <only if material>
```

Do not edit code unless the user also asks for implementation.
