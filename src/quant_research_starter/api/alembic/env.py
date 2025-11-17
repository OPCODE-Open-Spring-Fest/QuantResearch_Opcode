from __future__ import with_statement
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging. Some environments (CI or
# trimmed alembic.ini) may not include all logger sections; guard against
# that to avoid stopping migrations with a KeyError.
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except Exception:
        # Fall back to a minimal logging configuration if the ini is missing
        # expected logger sections (e.g. 'logger_sqlalchemy'). This makes
        # migrations resilient when run in different environments.
        import logging

        logging.basicConfig(level=logging.INFO)

target_metadata = None

# Use DATABASE_URL env if provided
db_url = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
if db_url:
    # Only set the option if we have a valid string value. Avoid setting None
    # which causes ConfigParser type errors (option values must be strings).
    config.set_main_option("sqlalchemy.url", str(db_url))


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Determine whether the configured URL uses an async driver. If so,
    # create an AsyncEngine and run the migrations inside an async context
    # while delegating the actual migration steps to a sync callable via
    # `connection.run_sync`. Otherwise, fall back to the classic sync path.
    url = config.get_main_option("sqlalchemy.url")

    def _do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    if url and url.startswith("postgresql+asyncpg"):
        # Async migration path
        from sqlalchemy.ext.asyncio import create_async_engine
        import asyncio

        async_engine = create_async_engine(url, future=True)

        async def run():
            async with async_engine.connect() as connection:
                await connection.run_sync(_do_run_migrations)

        asyncio.run(run())
    else:
        # Sync migration path (classic)
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            _do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
