---
name: custom-init
description: Set up .claude/ folder for the current project using personal meta-configuration templates
---

# custom-init

**Usage:**
```
/custom-init
```

## Instructions

You are setting up a `.claude/` folder for the current project using templates from `/home/example/configs/claude/`.

### Step 1: Read Meta-Configuration

Read these files to understand the setup process:
1. `/home/example/configs/claude/CLAUDE.md` - Overview and decision trees
2. `/home/example/configs/claude/workflow.md` - Detailed process

### Step 2: Discover Project

Analyze the current project:
- Language(s) and version
- Package manager (pip, conda, poetry, npm, cargo, etc.)
- Test framework and location
- Formatter/linter tools
- Any expensive operations or constraints

Quick discovery commands:
```bash
# Python
ls pyproject.toml requirements.txt setup.py 2>/dev/null
cat pyproject.toml 2>/dev/null | head -30
ls tests/ 2>/dev/null

# C++
cat CMakeLists.txt 2>/dev/null | head -30
ls tests/ test/ 2>/dev/null
```

### Step 3: Ask User

Use AskUserQuestion to clarify:
- Environment activation command (venv, conda, poetry)
- Tool preferences if multiple options exist
- Any specific DO NOT rules or constraints
- Line length preference

### Step 4: Select Templates

Based on project type, read the appropriate example:
- Python: `/home/example/configs/claude/examples/python.md`
- C++: `/home/example/configs/claude/examples/cpp.md`
- pybind11: `/home/example/configs/claude/examples/pybind11.md`

And templates:
- `/home/example/configs/claude/templates/settings-json.md`
- `/home/example/configs/claude/templates/claude-md.md`
- `/home/example/configs/claude/templates/rules.md`

### Step 5: Create Files

Based on project size:
- **< 500 LOC**: CLAUDE.md + settings.json only
- **500-5000 LOC**: + rules/testing.md
- **> 5000 LOC**: + additional rules/ and specs/

### Step 6: Verify

Confirm:
- [ ] Test commands work when copy-pasted
- [ ] Environment activation works
- [ ] DO NOT rules are specific with consequences
- [ ] CLAUDE.md < 200 lines

## Non-Negotiables

1. **CLAUDE_ENV_FILE hook** - Every project with virtual env needs:
```json
"hooks": {
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "echo 'ACTIVATION_CMD' >> \"$CLAUDE_ENV_FILE\""
    }]
  }]
}
```

2. **Default permissions** - Always include:
   - Read, Write, Edit, WebSearch
   - Testing commands (pytest, etc.)
   - Git commands

3. **Testing in quick reference** - Must be in top half of CLAUDE.md

4. **Specific DO NOT rules** - Format: `**DO NOT action** (consequence)`

## Start

Begin by analyzing the current project directory and asking clarifying questions.
