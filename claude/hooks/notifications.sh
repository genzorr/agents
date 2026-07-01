#!/bin/bash
# Generic desktop notifier for Claude Code hook scripts.
# Usage: notifications.sh "<message>" ["<title>"]

# Exit early if running over SSH — no GUI to notify.
if [ -n "$SSH_CONNECTION" ] || [ -n "$SSH_CLIENT" ]; then
    exit 0
fi

MESSAGE="${1:-Claude Code notification}"
TITLE="${2:-Claude Code}"

if [[ "$(uname)" == "Darwin" ]]; then
    alerter \
        --title "$TITLE" \
        --message "$MESSAGE" \
        --app-icon "/Applications/Warp.app/Contents/Resources/AppIcon.icns" \
        --sound default \
        --timeout 5 \
        >/dev/null 2>&1 &
else
    notify-send "$TITLE" "$MESSAGE"
fi

exit 0
