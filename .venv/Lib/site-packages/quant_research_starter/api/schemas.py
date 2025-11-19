"""Pydantic schemas for API requests/responses."""
from __future__ import annotations
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str


class BacktestRequest(BaseModel):
    data_file: Optional[str] = None
    signals_file: Optional[str] = None
    initial_capital: Optional[float] = 1_000_000
    weight_scheme: Optional[str] = "rank"
    rebalance_freq: Optional[str] = "D"


class BacktestStatus(BaseModel):
    job_id: str
    status: str


class BacktestResult(BaseModel):
    metrics: Dict[str, Any]
    portfolioSnapshots: Optional[list] = Field(default_factory=list)
    trades: Optional[list] = Field(default_factory=list)
