param(
    [string[]]$Args
)

Write-Host "Running full test suite..."
pytest @Args
exit $LASTEXITCODE

