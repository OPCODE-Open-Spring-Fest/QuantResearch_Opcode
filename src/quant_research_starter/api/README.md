API backend for QuantResearchStarter

Run the FastAPI app (development):

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:password@db:5432/qrs"
export REDIS_URL="redis://redis:6379/0"
uvicorn src.quant_research_starter.api.main:app --reload --port 8000
```

Run Celery worker:

```bash
celery -A src.quant_research_starter.api.tasks.celery_app.celery_app worker --loglevel=info
```

Notes:
- This scaffold uses Postgres (asyncpg), Redis (Celery broker + pubsub), and JWT auth.
- For production, run workers and web app in separate containers/processes, and use Alembic to manage schema migrations.
