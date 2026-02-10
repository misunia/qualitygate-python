# Demo App (System Under Test)

Minimal FastAPI application used as the target for automation tests.

## Run locally

From the repo root:

```bash
pip install -r app/requirements.txt
uvicorn app.main:app --reload
```

Or from the `app/` directory:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://localhost:8000

## Run with Docker Compose

From the repo root:

```bash
docker-compose up --build
```

The app is available at http://localhost:8000 (port 8000 exposed).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Returns `{"status": "ok"}` |
| POST | /api/login | Body: `{"username","password"}` → `{"token": "fake-token"}` |
| GET | /api/todos | Returns list of todos |
| POST | /api/todos | Body: `{"title": "..."}` → 201, created todo with id |
| POST | /api/reset | Clears todos (for test isolation) |

## UI

- **GET /** — Simple HTML page with login form and (after login) todo input and list. All interactive elements use `data-testid` attributes for stable automation selectors.
