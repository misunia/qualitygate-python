param(
    [string]$Path = "."
)

Write-Host "Running Black format on $Path..."
black $Path
exit $LASTEXITCODE

