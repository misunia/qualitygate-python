"""Minimal FastAPI demo app - system under test for automation."""

from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Demo API")

# In-memory state (for test isolation use POST /api/reset)
todos: list[dict[str, Any]] = []
_next_id = 1


class LoginBody(BaseModel):
    username: str
    password: str


class TodoCreate(BaseModel):
    title: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/login")
def login(body: LoginBody) -> dict[str, str]:
    return {"token": "fake-token"}


@app.get("/api/todos")
def list_todos() -> list[dict[str, Any]]:
    return todos


@app.post("/api/todos", status_code=201)
def create_todo(body: TodoCreate) -> dict[str, Any]:
    global _next_id
    todo = {"id": _next_id, "title": body.title}
    _next_id += 1
    todos.append(todo)
    return todo


@app.post("/api/reset")
def reset_todos() -> dict[str, str]:
    global todos, _next_id
    todos = []
    _next_id = 1
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return _HTML_PAGE


_HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Todo Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 480px; margin: 2rem auto; padding: 0 1rem; }
    input, button { margin: 0.25rem 0; }
    #todo-section { display: none; }
    #todo-section.visible { display: block; }
    #login-section.hidden { display: none; }
    [data-testid="todo-item"] { margin: 0.5rem 0; padding: 0.5rem; background: #f0f0f0; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Todo Demo</h1>
  <section id="login-section">
    <form id="login-form">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" data-testid="username" required>
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" data-testid="password" required>
      </div>
      <button type="submit" data-testid="login-btn">Login</button>
    </form>
  </section>
  <section id="todo-section">
    <form id="todo-form">
      <input type="text" id="todo-input" data-testid="todo-input" placeholder="New todo" required>
      <button type="submit" data-testid="add-todo-btn">Add</button>
    </form>
    <div data-testid="todo-list"></div>
  </section>
  <script>
    const loginSection = document.getElementById('login-section');
    const todoSection = document.getElementById('todo-section');
    const todoList = document.querySelector('[data-testid="todo-list"]');
    const todoInput = document.querySelector('[data-testid="todo-input"]');

    document.getElementById('login-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.querySelector('[data-testid="username"]').value;
      const password = document.querySelector('[data-testid="password"]').value;
      const r = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!r.ok) return;
      loginSection.classList.add('hidden');
      todoSection.classList.add('visible');
      loadTodos();
    });

    function renderTodos(items) {
      todoList.innerHTML = items.map(t => 
        '<div data-testid="todo-item">' + escapeHtml(t.title) + '</div>'
      ).join('');
    }
    function escapeHtml(s) {
      const div = document.createElement('div');
      div.textContent = s;
      return div.innerHTML;
    }

    async function loadTodos() {
      const r = await fetch('/api/todos');
      const items = await r.json();
      renderTodos(items);
    }

    document.getElementById('todo-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = todoInput.value.trim();
      if (!title) return;
      const r = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      });
      if (r.status !== 201) return;
      todoInput.value = '';
      loadTodos();
    });
  </script>
</body>
</html>
"""
