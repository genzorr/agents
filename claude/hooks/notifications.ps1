<#
.SYNOPSIS
    Desktop notifier for Claude Code hook events on Windows.
.DESCRIPTION
    Windows counterpart to notifications.sh, which cannot serve here: the `bash` on
    PATH is WSL, so it reaches neither Windows paths nor the Windows notification
    APIs. The installer materializes both notifiers in every Claude home and wires
    this one into settings.json only on a native Windows host, through an explicit
    powershell.exe invocation. On POSIX the file stays installed but unreferenced.
.PARAMETER Message
    Notification body. Claude Code passes the event wording from hooks.json.
.PARAMETER Title
    Notification title. Defaults to "Claude Code".
.EXAMPLE
    notifications.ps1 "Response complete"
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)][string]$Message = 'Claude Code notification',
    [Parameter(Position = 1)][string]$Title = 'Claude Code'
)

# A notifier must never fail the event that triggered it, so every path below ends in a
# swallowed error and exit 0. Stop turns the WinRT and WinForms non-terminating errors
# into catchable ones instead of letting them print and continue.
$ErrorActionPreference = 'Stop'

# Toasts are addressed to a registered AppUserModelID; an unregistered one is
# accepted and then silently dropped. Windows PowerShell's own Start Menu AUMID is
# present on every stock install, which avoids registering an identity of our own.
$AppId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'

function Show-Toast {
    param([string]$Title, [string]$Message)

    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null

    $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
        [Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $nodes = $xml.GetElementsByTagName('text')
    $nodes.Item(0).AppendChild($xml.CreateTextNode($Title)) | Out-Null
    $nodes.Item(1).AppendChild($xml.CreateTextNode($Message)) | Out-Null

    # New-Object, not ::new(): the WinRT projection exposes the activation factory to
    # the former on Windows PowerShell 5.1, where this path is expected to run.
    $toast = New-Object Windows.UI.Notifications.ToastNotification -ArgumentList $xml
    # Ownership passes to the OS here, so the notification outlives this process --
    # the property that lets the hook return immediately instead of blocking the
    # session while a banner is on screen.
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($AppId).Show($toast)
}

function Show-Balloon {
    param([string]$Title, [string]$Message)

    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $icon = New-Object System.Windows.Forms.NotifyIcon
    try {
        $icon.Icon = [System.Drawing.SystemIcons]::Information
        $icon.Visible = $true
        $icon.ShowBalloonTip(5000, $Title, $Message, [System.Windows.Forms.ToolTipIcon]::Info)
        # Unlike a toast, a balloon belongs to this process: disposing immediately
        # would cancel it, so give the shell a moment to pick it up.
        Start-Sleep -Milliseconds 400
    } finally {
        $icon.Dispose()
    }
}

try {
    Show-Toast -Title $Title -Message $Message
} catch {
    try {
        Show-Balloon -Title $Title -Message $Message
    } catch {
        # Nothing left to try; stay silent rather than surface noise into the hook.
    }
}

exit 0
