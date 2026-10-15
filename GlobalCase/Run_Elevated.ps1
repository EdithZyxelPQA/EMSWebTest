# Started by the EMSWeb_GlobalCase_Admin scheduled task (highest privileges). Do not call directly.
# With Run_Elevated.args present: run pytest with those arguments unattended and log the output.
# Without it: open RUN.py (interactive menu).
Set-Location $PSScriptRoot
$argsFile = Join-Path $PSScriptRoot "Run_Elevated.args"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if (Test-Path $argsFile) {
    $pytestArgs = @(Get-Content $argsFile -Encoding UTF8 | Where-Object { $_ -ne "" })
    Remove-Item $argsFile
    # Show case progress in the log while it runs (pytest otherwise holds output until the case ends).
    $env:PYTHONUNBUFFERED = "1"
    if (-not ($pytestArgs | Where-Object { $_ -match '^(-s|--capture)' })) { $pytestArgs += "-s" }
    New-Item -ItemType Directory -Force (Join-Path $PSScriptRoot "report") | Out-Null
    $log = Join-Path $PSScriptRoot ("report\elevated_{0}.log" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
    "pytest $pytestArgs" | Out-File $log -Encoding utf8
    & py -3.11 -m pytest @pytestArgs 2>&1 | ForEach-Object {
        $line = "$_"
        Write-Host $line
        Add-Content -Path $log -Value $line -Encoding UTF8
    }
    "exit code $LASTEXITCODE" | Add-Content -Path $log -Encoding UTF8
}
else {
    & py -3.11 RUN.py
    Read-Host "RUN.py finished. Press Enter to close"
}
