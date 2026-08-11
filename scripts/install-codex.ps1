#!/usr/bin/env pwsh
# Native-Windows entry point for the Codex engine; the POSIX twin is install-codex.sh.
# Select the home with $env:CODEX_HOME, and pass engine options through unchanged.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'lib/python.ps1')
$python = Resolve-AgentsPython
& $python.Command @($python.Arguments) -B (Join-Path $PSScriptRoot 'install-assets.py') codex @args
exit $LASTEXITCODE
