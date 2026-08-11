# Resolve a working Python interpreter for the native-Windows installer wrappers.
#
# Dot-source this file, then call Resolve-AgentsPython. `python3` cannot simply be
# assumed: on Windows the name usually resolves to a Microsoft Store alias stub that
# sits on PATH, satisfies Get-Command, and then exits nonzero with an advert instead
# of running anything -- so every candidate is probed by execution. The probe pins the
# floor from pyproject's requires-python, so a Python 2 `python` is rejected here
# instead of failing later on engine syntax.

function Resolve-AgentsPython {
    $probe = 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 9) else 1)'
    # `py -3` first: the Windows launcher finds a real install even when the alias
    # stub shadows `python3` on PATH.
    $candidates = @(
        @{ Command = 'py'; Arguments = @('-3') },
        @{ Command = 'python3'; Arguments = @() },
        @{ Command = 'python'; Arguments = @() }
    )
    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Command -ErrorAction SilentlyContinue)) {
            continue
        }
        try {
            & $candidate.Command @($candidate.Arguments) -c $probe *> $null
        } catch {
            continue
        }
        if ($LASTEXITCODE -eq 0) {
            return $candidate
        }
    }
    throw 'no working Python 3.9+ on PATH (tried: py -3, python3, python)'
}
