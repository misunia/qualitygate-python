"""Auth/login API tests."""

import pytest

from tests.helpers.http_client import post_json


@pytest.mark.regression
def test_login_returns_token(base_url: str) -> None:
    """POST /api/login returns token (string not empty)."""
    data = post_json(
        f"{base_url}/api/login",
        {"username": "testuser", "password": "testpass"},
    )
    assert "token" in data
    token = data["token"]
    assert isinstance(token, str), "token must be a string"
    assert len(token) > 0, "token must not be empty"
