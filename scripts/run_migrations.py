"""Run Alembic migrations programmatically using env DATABASE_URL.

Usage:
    python scripts/run_migrations.py
"""
import os

from alembic import command
from alembic.config import Config

here = os.path.dirname(__file__)
alembic_cfg = Config(os.path.join(here, "..", "alembic.ini"))

# Allow overriding DB URL via env
db_url = os.getenv("DATABASE_URL")
if db_url:
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)

command.upgrade(alembic_cfg, "head")

print("Migrations applied")
