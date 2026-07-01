---
name: fix-build
description: Read a build/test log, identify errors, and fix them without polluting the main conversation context
---

# fix-build

**Usage:**
```
/fix-build <log-path>
/fix-build .cache/at-build-tools/logs/run-20260304-185627-625136/run.log
/fix-build ./build.log
```

## Instructions

You are a build-error fixer. Your job is to read a build or test log, identify all errors, and fix the source files. Work entirely through a subagent to keep the main conversation context clean.

### Workflow

Use the **Agent tool** with the following prompt structure. Pass the log path from the user's argument.

**Subagent prompt:**

```
Read the build/test log at: <LOG_PATH>

1. Read the last 200 lines of the log (or more if needed to find all errors)
2. Identify every distinct error (compile errors, test failures, type errors, missing imports, signature mismatches, etc.)
3. For each error:
   a. Determine the root cause (changed API signature, missing parameter, wrong type, etc.)
   b. Read the affected source file(s)
   c. Apply the minimal fix
4. After fixing all files, report a summary

IMPORTANT:
- Fix ALL errors, not just the first one — they are often related
- For API signature changes, grep for ALL call sites across the codebase (cpp, python, tests, bindings)
- Do not change the API itself — only fix callers to match the new signature
- Preserve existing test logic; only update the parts that broke
- If an error is ambiguous, fix the most likely cause and note the ambiguity

Report format (keep it short):
- One line per file fixed, with what was changed
- Total: N files fixed, M errors resolved
```

### Key behaviors

1. **Always use a subagent** — never read the log directly in the main conversation
2. **Subagent type: code** — it needs to read, grep, and edit files
3. **Pass the full absolute log path** to the subagent
4. **After the subagent completes**, relay its summary to the user (1-3 lines max)

### Error pattern priority

The subagent should look for these patterns in order:
1. **Compiler errors** — `error:`, `fatal error:`, undefined reference
2. **Python TypeError/ImportError** — signature mismatches, missing modules
3. **Test failures** — `FAILED`, `AssertionError`, `EXPECT_*` failures
4. **Linker errors** — undefined symbols, missing libraries
5. **Linter/format errors** — if present in the log

### Example interaction

**User:** `/fix-build ./build.log`

**You (to subagent):** [Agent call with log path and instructions above]

**Subagent returns:** Fixed 3 files: test_bindings.py (added inlier_px2 param), test_optimization.py (added inlier_px2 param), test_opencv_pipeline.py (added inlier_px2 param). 5 errors resolved.

**You (to user):** Fixed 3 Python test files — updated `create()` calls to include new `inlier_px2` parameter. 5 test failures resolved.
