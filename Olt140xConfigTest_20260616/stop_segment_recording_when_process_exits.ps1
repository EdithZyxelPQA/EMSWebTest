param(
    [Parameter(Mandatory=$true)]
    [int]$PidToWatch,

    [Parameter(Mandatory=$true)]
    [string]$StopFile,

    [Parameter(Mandatory=$true)]
    [string]$LogFile
)

"Watching PID $PidToWatch at $(Get-Date)" | Out-File -FilePath $LogFile -Append -Encoding utf8

while ($true) {
    $process = Get-Process -Id $PidToWatch -ErrorAction SilentlyContinue
    if ($null -eq $process) {
        "PID $PidToWatch exited at $(Get-Date). Creating stop file: $StopFile" | Out-File -FilePath $LogFile -Append -Encoding utf8
        "stop requested at $(Get-Date)" | Out-File -FilePath $StopFile -Encoding utf8
        break
    }
    Start-Sleep -Seconds 30
}
