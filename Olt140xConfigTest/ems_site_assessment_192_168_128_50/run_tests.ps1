param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

& $Python -m pytest --junitxml reports/junit.xml
& $Python tools/generate_report.py reports/junit.xml reports/assessment_report.md reports/assessment_report.html
