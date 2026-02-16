# QualityGate (Python) — QA Automation Framework (API + UI)

![CI](https://github.com/misunia/qualitygate-python/actions/workflows/ci.yml/badge.svg)

A QA Automation portfolio project that demonstrates a production-style test framework in **Python**.

It includes:
- **System Under Test (SUT):** a minimal **FastAPI** demo app running in **Docker Compose**
- **API tests:** `pytest + requests`
- **UI E2E tests:** `pytest-playwright` (Playwright + Chromium)
- **CI pipeline:** GitHub Actions runs the full suite, generates an **HTML report**, and publishes it to **GitHub Pages**

## Live Test Report (GitHub Pages)
https://misunia.github.io/qualitygate-python/

## What this demonstrates
- Clean automation framework structure (**API / UI / helpers** separation)
- **Test isolation** via a reset endpoint + autouse fixture (reduces flakiness)
- **Stable UI automation** using `data-testid` selectors
- Dockerized, reproducible local and CI runs
- CI artifacts + published HTML report for visibility and debugging

## Tech Stack
- Python + pytest
- requests (API tests)
- Playwright + pytest-playwright (UI E2E)
- Docker / Docker Compose (SUT)
- GitHub Actions + GitHub Pages (CI + report publishing)
- pytest-html (HTML report) + JUnit XML

## Project Structure
app/ # FastAPI demo app (SUT)
main.py
Dockerfile
docker-compose.yml # Run the SUT locally/CI
tests/
api/ # API test suite
ui/ # UI E2E suite (Playwright)
helpers/ # Shared helpers (e.g., HTTP client)
.github/workflows/
ci.yml # CI: build SUT, run tests, publish report
reports/ # Generated at runtime (HTML/JUnit) - ignored by git


## Getting Started (Local)

### Prerequisites
- Python 3.11+ (3.12 recommended)
- Docker Desktop (includes docker compose)
- (First time) Playwright browser install

### Install dependencies
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m playwright install chromium
Start the demo app (SUT)
docker compose up --build
Health check:

curl.exe http://localhost:8000/health
Run tests
Run all tests:

.\.venv\Scripts\python -m pytest -q
Run smoke only:

.\.venv\Scripts\python -m pytest -q -m smoke
Run UI tests only:

.\.venv\Scripts\python -m pytest -q tests/ui
Test Configuration
Base URL
Tests read the application URL from BASE_URL.

Default:

http://localhost:8000

Override example:

$env:BASE_URL="http://localhost:8000"
.\.venv\Scripts\python -m pytest -q
Markers
smoke: fast sanity checks (e.g., /health)

regression: broader coverage (API + UI flows)

CI Overview
On each push/PR to main, CI:

Installs dependencies

Installs Playwright + Chromium

Builds and starts SUT via docker compose

Waits for /health

Runs pytest (API + UI)

Generates:

reports/report.html (pytest-html)

reports/junit.xml (JUnit)

Uploads artifacts and publishes the HTML report to GitHub Pages

Troubleshooting
“curl” in PowerShell shows a security warning
In Windows PowerShell, curl can be an alias for Invoke-WebRequest.
Use:

curl.exe http://localhost:8000/health
UI tests failing due to selectors
UI tests rely on data-testid attributes in the demo app UI.
If the UI changes, update:

tests/ui/test_todo_ui.py

Next Improvements
Enable trace/screenshot/video retention on UI failures

Parallel execution (pytest -n auto) and sharding strategy

Flaky test handling strategy (quarantine/retries policy)

Nightly scheduled run + Slack notification on failures
