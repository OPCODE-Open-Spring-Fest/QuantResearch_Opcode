"""SQLAlchemy models for users and backtest jobs."""
from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy import func
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String(128), unique=True, index=True, nullable=False)
    hashed_password = sa.Column(sa.String(256), nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
    role = sa.Column(sa.String(32), default="user")
    created_at = sa.Column(sa.DateTime, server_default=func.now())


class BacktestJob(Base):
    __tablename__ = "backtest_jobs"

    id = sa.Column(sa.String(64), primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    status = sa.Column(sa.String(32), nullable=False, default="queued")
    params = sa.Column(sa.JSON, nullable=True)
    result_path = sa.Column(sa.String(1024), nullable=True)
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())
