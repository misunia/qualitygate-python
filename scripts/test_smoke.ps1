param(
    [string[]]$Args
)

Write-Host "Running smoke test suite..."
pytest -m smoke @Args
exit $LASTEXITCODE

