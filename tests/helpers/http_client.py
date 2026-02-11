"""HTTP helpers for API tests using requests."""

import requests


def get_json(url: str, timeout: int = 5, **kwargs) -> dict | list:
    """GET URL and return JSON; uses timeout=5 and raise_for_status()."""
    resp = requests.get(url, timeout=timeout, **kwargs)
    resp.raise_for_status()
    return resp.json()


def post_json(
    url: str, payload: dict, timeout: int = 5, **kwargs
) -> dict | list:
    """POST JSON payload to URL and return JSON; uses timeout=5 and raise_for_status()."""
    resp = requests.post(url, json=payload, timeout=timeout, **kwargs)
    resp.raise_for_status()
    return resp.json()
