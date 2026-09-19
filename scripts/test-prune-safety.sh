#!/usr/bin/env bash
# Regression test: Agents installers must not prune or uninstall legacy names
# or assets owned by Harness/session-harvester/foreign providers.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

CLAUDE_HOME="$TMP_DIR/claude"
CODEX_HOME="$TMP_DIR/codex"
AGENTS_HOME="$TMP_DIR/agents"
DEVIN_HOME="$TMP_DIR/devin"

touch_skill() {
    local root="$1"
    local name="$2"
    mkdir -p "$root/skills/$name"
    printf 'sentinel\n' > "$root/skills/$name/SKILL.md"
}

require_exists() {
    local path="$1"
    [[ -e "$path" ]] || {
        echo "missing unexpectedly: $path" >&2
        exit 1
    }
}

require_absent() {
    local path="$1"
    [[ ! -e "$path" ]] || {
        echo "still present unexpectedly: $path" >&2
        exit 1
    }
}

touch_skill "$CLAUDE_HOME" dynamic-workflow-prompt
touch_skill "$CLAUDE_HOME" harness-task-start
touch_skill "$CLAUDE_HOME" harvest-sessions
mkdir -p "$CLAUDE_HOME/rules"
printf 'sentinel\n' > "$CLAUDE_HOME/rules/branching-and-prs.md"
printf 'sentinel\n' > "$CLAUDE_HOME/rules/adversarial-review.md"

touch_skill "$CODEX_HOME" dynamic-workflow-prompt
touch_skill "$CODEX_HOME" gpt-pro-context-prompt
touch_skill "$CODEX_HOME" harness-task-start
touch_skill "$CODEX_HOME" harvest-sessions
touch_skill "$CODEX_HOME" codex-primary-runtime
touch_skill "$AGENTS_HOME" foreign-shared
mkdir -p "$DEVIN_HOME"
printf 'sentinel\n' > "$DEVIN_HOME/foreign.txt"

CLAUDE_HOME="$CLAUDE_HOME" bash "$REPO_DIR/scripts/install-claude.sh" --prune >/dev/null
CODEX_HOME="$CODEX_HOME" bash "$REPO_DIR/scripts/install-codex.sh" --prune >/dev/null
AGENTS_HOME="$AGENTS_HOME" bash "$REPO_DIR/scripts/install-agents.sh" --prune >/dev/null
DEVIN_HOME="$DEVIN_HOME" bash "$REPO_DIR/scripts/install-devin.sh" --prune >/dev/null

require_exists "$CLAUDE_HOME/skills/dynamic-workflow-prompt"
require_exists "$CLAUDE_HOME/skills/harness-task-start"
require_exists "$CLAUDE_HOME/skills/harvest-sessions"
require_exists "$CLAUDE_HOME/rules/branching-and-prs.md"
require_exists "$CLAUDE_HOME/rules/adversarial-review.md"
require_exists "$CODEX_HOME/skills/dynamic-workflow-prompt"
require_exists "$CODEX_HOME/skills/gpt-pro-context-prompt"
require_exists "$CODEX_HOME/skills/harness-task-start"
require_exists "$CODEX_HOME/skills/harvest-sessions"
require_exists "$CODEX_HOME/skills/codex-primary-runtime"
require_exists "$AGENTS_HOME/skills/foreign-shared"
require_exists "$DEVIN_HOME/foreign.txt"

CLAUDE_HOME="$CLAUDE_HOME" bash "$REPO_DIR/scripts/install-claude.sh" --uninstall >/dev/null
CODEX_HOME="$CODEX_HOME" bash "$REPO_DIR/scripts/install-codex.sh" --uninstall >/dev/null
AGENTS_HOME="$AGENTS_HOME" bash "$REPO_DIR/scripts/install-agents.sh" --uninstall >/dev/null
DEVIN_HOME="$DEVIN_HOME" bash "$REPO_DIR/scripts/install-devin.sh" --uninstall >/dev/null

require_exists "$CLAUDE_HOME/skills/dynamic-workflow-prompt"
require_exists "$CLAUDE_HOME/skills/harness-task-start"
require_exists "$CLAUDE_HOME/skills/harvest-sessions"
require_exists "$CLAUDE_HOME/rules/branching-and-prs.md"
require_exists "$CLAUDE_HOME/rules/adversarial-review.md"
require_exists "$CODEX_HOME/skills/dynamic-workflow-prompt"
require_exists "$CODEX_HOME/skills/gpt-pro-context-prompt"
require_exists "$CODEX_HOME/skills/harness-task-start"
require_exists "$CODEX_HOME/skills/harvest-sessions"
require_exists "$CODEX_HOME/skills/codex-primary-runtime"
require_exists "$AGENTS_HOME/skills/foreign-shared"
require_exists "$DEVIN_HOME/foreign.txt"
require_absent "$DEVIN_HOME/AGENTS.md"

require_absent "$CLAUDE_HOME/skills/review-change"
require_absent "$CODEX_HOME/skills/review-change"
require_absent "$AGENTS_HOME/skills/babysit-pr"

echo "OK - Agents prune/uninstall leaves legacy, foreign, and other-repo assets untouched"
