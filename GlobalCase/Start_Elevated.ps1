# Start GlobalCase tests as Administrator from a normal PowerShell (needs Setup_ElevatedTask.ps1 once).
#   .\Start_Elevated.ps1
#       opens an elevated window running RUN.py (interactive menu)
#   .\Start_Elevated.ps1 GlobalCase.py -m Unicase -k 7240 --cmdopt=192.168.168.87
#       runs that pytest command unattended; log in report\elevated_<time>.log
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PytestArgs)

$TaskName = "EMSWeb_GlobalCase_Admin"
$argsFile = Join-Path $PSScriptRoot "Run_Elevated.args"

if (-not (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue)) {
    Write-Host "Task $TaskName not found. Run Setup_ElevatedTask.ps1 once in an Administrator PowerShell."
    exit 1
}
if ($PytestArgs) {
    # One argument per line, so quoting survives; Run_Elevated.ps1 deletes the file after reading it.
    [IO.File]::WriteAllLines($argsFile, $PytestArgs, (New-Object Text.UTF8Encoding($false)))
}
elseif (Test-Path $argsFile) {
    Remove-Item $argsFile
}
Start-ScheduledTask -TaskName $TaskName
Write-Host "Started $TaskName" $(if ($PytestArgs) { "with: pytest $PytestArgs" } else { "(RUN.py menu)" })
