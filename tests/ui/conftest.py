"""Playwright-specific pytest fixtures and configuration."""

import os
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for the UI; reads env BASE_URL, default http://localhost:8000."""
    return os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="function")
def browser_context(
    browser_context: BrowserContext, request: pytest.FixtureRequest
) -> BrowserContext:
    """Configure browser context with tracing enabled."""
    # Enable trace on first retry or always-on
    # Using always-on for simplicity (can be changed to retry-based if needed)
    browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield browser_context

    # Stop tracing and save on failure
    # Note: Trace is always collected, but only saved on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        trace_dir = Path("test-results/traces")
        trace_dir.mkdir(parents=True, exist_ok=True)
        trace_path = trace_dir / f"{request.node.name}.zip"
        browser_context.tracing.stop(path=str(trace_path))
    else:
        # Stop tracing without saving if test passed
        browser_context.tracing.stop()


@pytest.fixture(scope="function")
def page(page: Page, request: pytest.FixtureRequest) -> Page:
    """Page fixture with screenshot on failure."""
    yield page

    # Save screenshot on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = Path("test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot/trace on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep)
