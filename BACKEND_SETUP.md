# Backend Setup and Run Guide

This document explains how to run the production-like backend locally, run migrations, start workers, and test the system.

Prerequisites
- Docker & Docker Compose (for easy local Postgres + Redis)
- Python 3.11 (for local development/testing)

Environment variables (recommended)
- `DATABASE_URL` — e.g. `postgresql+asyncpg://postgres:password@db:5432/qrs`
- `REDIS_URL` — e.g. `redis://redis:6379/0`
- `JWT_SECRET` — strong secret for signing tokens
- `OUTPUT_DIR` — where backtest results are written (default `output/`)

Quick start with Docker Compose
1. Build and start services:

```bash
docker-compose up --build -d
```

2. Run migrations (inside the backend container):

```bash
docker-compose exec backend python scripts/run_migrations.py
```

3. Create a user and obtain a token (example using `curl`):

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}'

curl -X POST http://localhost:8000/api/auth/token -F "username=alice" -F "password=secret"
```

4. Submit a backtest (authenticated):

```bash
curl -X POST http://localhost:8000/api/backtest/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"initial_capital":100000, "weight_scheme":"rank"}'
```

5. Listen for progress via WebSocket (example using `wscat`):

```bash
wscat -c ws://localhost:8000/api/backtest/ws/<JOB_ID>
```

Local development without Docker (optional)
- Set `DATABASE_URL` to a running Postgres server (or use SQLite for testing).
- Install dependencies:

```bash
python -m pip install --upgrade pip
pip install .[dev]
```

- Run migrations:

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/qrs"
python scripts/run_migrations.py
```

- Run the backend (development):

```bash
uvicorn src.quant_research_starter.api.main:app --reload --port 8000
```

Running tests

Unit and integration tests are configured via `pytest`.

```bash
pip install .[dev]
pytest -q
```

CI
- A GitHub Actions workflow is included at `.github/workflows/ci.yml` which runs lint and tests using service containers for PostgreSQL and Redis.

Notes & next steps
- Use a secrets manager to provide `JWT_SECRET` and DB credentials in production.
- Add TLS, logging aggregation, metrics, and autoscaling for real deployments.
