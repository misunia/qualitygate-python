"""Todo UI tests using Playwright."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
def test_todo_creation_flow(page: Page, base_url: str) -> None:
    """Test login and todo creation flow."""
    # Navigate to the base URL
    page.goto(base_url)

    # Fill login inputs and click login button
    page.locator('[data-testid="username"]').fill("testuser")
    page.locator('[data-testid="password"]').fill("testpass")
    page.locator('[data-testid="login-btn"]').click()

    # Wait for login to complete (wait for todo input to be visible)
    todo_input = page.locator('[data-testid="todo-input"]')
    expect(todo_input).to_be_visible()

    # Fill todo input and click add button
    todo_input.fill("Buy milk")
    page.locator('[data-testid="add-todo-btn"]').click()

    # Assert the todo appears in the todo list
    todo_list = page.locator('[data-testid="todo-list"]')
    expect(todo_list).to_be_visible()

    todo_items = page.locator('[data-testid="todo-item"]')
    expect(todo_items).to_have_count(1)
    expect(todo_items.first).to_contain_text("Buy milk")
