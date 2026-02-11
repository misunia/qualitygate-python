"""Todos API tests."""

import pytest

from tests.helpers.http_client import get_json, post_json


@pytest.mark.regression
def test_todos_list_empty_then_create_then_appears(base_url: str) -> None:
    """Ensure list is empty, create a todo, then ensure it appears in the list."""
    list_url = f"{base_url}/api/todos"
    create_url = f"{base_url}/api/todos"

    # List is empty (api_reset runs before each test)
    todos = get_json(list_url)
    assert todos == [], "todos list should be empty at start"

    # Create one todo
    created = post_json(create_url, {"title": "Buy milk"})
    assert "id" in created
    assert created["title"] == "Buy milk"

    # Todo appears in list
    todos = get_json(list_url)
    assert len(todos) == 1
    assert todos[0]["id"] == created["id"]
    assert todos[0]["title"] == "Buy milk"
