# shellcheck shell=bash
# Resolve a working Python interpreter for the installer wrappers.
#
# `python3` cannot simply be assumed. On Windows the name resolves to a Microsoft
# Store alias stub that sits on PATH, satisfies `command -v`, and then exits
# nonzero with an advert instead of running anything -- so the interpreter must be
# probed by execution, not by lookup. The probe also pins the floor from
# pyproject's requires-python, so a Python 2 `python` is rejected here instead of
# failing later on engine syntax.

resolve_python() {
    # Sourcing this file must not leave variables behind in the caller's shell.
    local candidate probe='import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 9) else 1)'
    for candidate in python3 python; do
        if "$candidate" -c "$probe" >/dev/null 2>&1; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done
    echo "error: no working Python 3.9+ on PATH (tried: python3, python)" >&2
    return 1
}
