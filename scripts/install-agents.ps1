#!/usr/bin/env pwsh
# Native-Windows entry point for the shared Agents engine; the POSIX twin is install-agents.sh.
# Select the home with $env:AGENTS_HOME, and pass engine options through unchanged.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'lib/python.ps1')
$python = Resolve-AgentsPython
& $python.Command @($python.Arguments) -B (Join-Path $PSScriptRoot 'install-assets.py') agents @args
exit $LASTEXITCODE
