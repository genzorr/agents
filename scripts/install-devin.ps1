#!/usr/bin/env pwsh
# Native-Windows entry point for the Devin engine; the POSIX twin is install-devin.sh.
# Select the home with $env:DEVIN_HOME, and pass engine options through unchanged.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'lib/python.ps1')
$python = Resolve-AgentsPython
& $python.Command @($python.Arguments) -B (Join-Path $PSScriptRoot 'install-assets.py') devin @args
exit $LASTEXITCODE
