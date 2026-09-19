#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=scripts/lib/python.sh
. "$REPO_DIR/scripts/lib/python.sh"
PYTHON="$(resolve_python)" || exit 1
exec "$PYTHON" -B "$REPO_DIR/scripts/install-assets.py" agents "$@"
