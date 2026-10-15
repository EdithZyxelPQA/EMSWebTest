# One-time setup (run in an Administrator PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\Setup_ElevatedTask.ps1
# Registers a scheduled task that runs Run_Elevated.ps1 with highest privileges for the current user.
# Afterwards Start_Elevated.ps1 can be used from a normal PowerShell; no UAC prompt is needed.
#Requires -RunAsAdministrator
param([string]$TaskName = "EMSWeb_GlobalCase_Admin")

$dir = $PSScriptRoot
$user = "$env:USERDOMAIN\$env:USERNAME"
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$dir\Run_Elevated.ps1`"" `
    -WorkingDirectory $dir
# Interactive: runs in the logged-on desktop session, which the browser needs.
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Days 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $TaskName -Action $action -Principal $principal -Settings $settings `
    -Description "Run EMSWeb GlobalCase tests as Administrator (needed by EMS1-7240 LocalMachine\Root CA import)" -Force | Out-Null

Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, @{n = "RunLevel"; e = { $_.Principal.RunLevel } }, @{n = "User"; e = { $_.Principal.UserId } }
