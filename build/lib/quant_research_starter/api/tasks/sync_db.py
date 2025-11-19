"""Synchronous DB helper for use in Celery workers.

Celery workers are separate processes; using the async engine from `db.py`
in a separate process is inconvenient. This module provides a small sync
SQLAlchemy engine and helper to update job status/result_path.
"""
import os
import sqlalchemy as sa

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/qrs")

# Convert asyncpg URL to sync psycopg2 URL if necessary
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
else:
    SYNC_DATABASE_URL = DATABASE_URL

engine = sa.create_engine(SYNC_DATABASE_URL, future=True)


def update_job_status(job_id: str, status: str, result_path: str | None = None):
    meta = sa.MetaData()
    jobs = sa.Table(
        "backtest_jobs",
        meta,
        sa.Column("id", sa.String(64), primary_key=True),
        autoload_with=engine,
    )

    with engine.begin() as conn:
        stmt = jobs.update().where(jobs.c.id == job_id).values(status=status)
        if result_path is not None:
            stmt = stmt.values(result_path=result_path)
        conn.execute(stmt)
