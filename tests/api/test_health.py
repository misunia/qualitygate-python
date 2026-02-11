"""Health endpoint API tests."""

import pytest

from tests.helpers.http_client import get_json


@pytest.mark.smoke
def test_health_returns_ok(base_url: str) -> None:
    """GET /health returns status ok."""
    data = get_json(f"{base_url}/health")
    assert data["status"] == "ok"
