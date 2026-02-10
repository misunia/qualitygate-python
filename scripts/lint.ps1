param(
    [string]$Path = "."
)

Write-Host "Running Ruff lint on $Path..."
ruff check $Path
exit $LASTEXITCODE

