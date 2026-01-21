"""Pydantic schemas for API requests/responses."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


# ==================== Auth Schemas ====================
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


class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


# ==================== Backtest Schemas ====================
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


# ==================== Trading Schemas ====================
class BuyStockRequest(BaseModel):
    symbol: str
    quantity: float
    price: Optional[float] = None
    notes: Optional[str] = None

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()

    @validator('quantity')
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class SellStockRequest(BaseModel):
    symbol: str
    quantity: float
    price: Optional[float] = None
    notes: Optional[str] = None

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()

    @validator('quantity')
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class TradeResponse(BaseModel):
    id: int
    symbol: str
    trade_type: str
    quantity: float
    price: float
    total_amount: float
    commission: float
    realized_pnl: Optional[float]
    realized_pnl_pct: Optional[float]
    notes: Optional[str]
    trade_date: str


# ==================== Position Schemas ====================
class PositionResponse(BaseModel):
    id: int
    symbol: str
    company_name: Optional[str]
    quantity: float
    average_cost: float
    current_price: float
    market_value: float
    cost_basis: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    day_change: float
    day_change_pct: float
    sector: Optional[str]
    industry: Optional[str]
    opened_at: str


# ==================== Market Data Schemas ====================
class QuoteResponse(BaseModel):
    symbol: str
    current_price: float
    change: float
    percent_change: float
    high: float
    low: float
    open: float
    previous_close: float
    volume: Optional[int]
    timestamp: str


class CompanyProfileResponse(BaseModel):
    symbol: str
    name: str
    country: Optional[str]
    currency: Optional[str]
    exchange: Optional[str]
    industry: Optional[str]
    sector: Optional[str]
    market_cap: Optional[float]
    logo: Optional[str]
    weburl: Optional[str]


class SearchResult(BaseModel):
    symbol: str
    description: str
    type: Optional[str]
    exchange: Optional[str]


# ==================== Strategy Schemas ====================
class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_type: str  # 'momentum', 'mean_reversion', 'value', 'custom'
    parameters: Dict[str, Any] = Field(default_factory=dict)
    symbols: Optional[List[str]] = Field(default_factory=list)
    is_active: bool = True


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    symbols: Optional[List[str]] = None
    is_active: Optional[bool] = None


class StrategyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    strategy_type: str
    parameters: Dict[str, Any]
    symbols: List[str]
    is_active: bool
    created_at: str
    updated_at: str


# ==================== Watchlist Schemas ====================
class WatchlistCreate(BaseModel):
    name: str
    description: Optional[str] = None
    symbols: List[str] = Field(default_factory=list)


class WatchlistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WatchlistAddSymbol(BaseModel):
    symbol: str

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


class WatchlistResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    symbols: List[str]
    created_at: str
    updated_at: str


# ==================== Alert Schemas ====================
class AlertCreate(BaseModel):
    symbol: str
    alert_type: str  # 'price_above', 'price_below', 'volume_spike', 'percent_change'
    threshold_value: float
    message: Optional[str] = None
    is_active: bool = True

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


class AlertUpdate(BaseModel):
    threshold_value: Optional[float] = None
    message: Optional[str] = None
    is_active: Optional[bool] = None


class AlertResponse(BaseModel):
    id: int
    symbol: str
    alert_type: str
    threshold_value: float
    current_value: Optional[float]
    message: Optional[str]
    is_active: bool
    triggered_at: Optional[str]
    created_at: str


# ==================== Portfolio Schemas ====================
class PortfolioMetrics(BaseModel):
    total_value: float
    cash: float
    invested: float
    market_value: float
    unrealized_pnl: float
    total_return: float
    total_return_percent: float
    daily_return: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    beta: float
    alpha: float
    win_rate: float
    total_trades: int


class PortfolioSnapshot(BaseModel):
    timestamp: str
    total_value: float
    cash: float
    invested: float
    total_return: float
    total_return_percent: float


# ==================== Market Data Request ====================
class HistoricalDataRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    interval: str = "1d"  # 1d, 1h, 15m, etc.

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


# ==================== Optimization Schemas ====================
class OptimizationRequest(BaseModel):
    symbols: List[str]
    start_date: str
    end_date: str
    optimization_method: str = "max_sharpe"  # max_sharpe, min_volatility, max_return
    constraints: Optional[Dict[str, Any]] = Field(default_factory=dict)


class OptimizationResponse(BaseModel):
    weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
