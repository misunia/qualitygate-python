"""Shared pytest fixtures for API tests."""

import os

import pytest

from tests.helpers.http_client import post_json


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for the API; reads env BASE_URL, default http://localhost:8000."""
    return os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.fixture(autouse=True)
def api_reset(base_url: str) -> None:
    """Reset API state before each test by POSTing to /api/reset."""
    post_json(f"{base_url}/api/reset", {})
