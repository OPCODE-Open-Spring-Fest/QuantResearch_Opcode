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


class Portfolio(Base):
    """User's portfolio snapshot with performance metrics."""
    __tablename__ = "portfolios"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    total_value = sa.Column(sa.Float, nullable=False)
    cash = sa.Column(sa.Float, nullable=False, default=0)
    invested = sa.Column(sa.Float, nullable=False, default=0)
    daily_return = sa.Column(sa.Float, default=0)
    total_return = sa.Column(sa.Float, default=0)
    total_return_percent = sa.Column(sa.Float, default=0)
    
    # Risk Metrics
    sharpe_ratio = sa.Column(sa.Float, default=0)
    max_drawdown = sa.Column(sa.Float, default=0)
    volatility = sa.Column(sa.Float, default=0)
    beta = sa.Column(sa.Float, default=1.0)
    alpha = sa.Column(sa.Float, default=0)
    win_rate = sa.Column(sa.Float, default=0)
    
    timestamp = sa.Column(sa.DateTime, server_default=func.now(), index=True)
    created_at = sa.Column(sa.DateTime, server_default=func.now())


class Position(Base):
    """Open stock positions."""
    __tablename__ = "positions"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True)
    symbol = sa.Column(sa.String(16), nullable=False, index=True)
    company_name = sa.Column(sa.String(256))
    quantity = sa.Column(sa.Float, nullable=False)
    average_cost = sa.Column(sa.Float, nullable=False)
    current_price = sa.Column(sa.Float, nullable=False)
    market_value = sa.Column(sa.Float, nullable=False)
    cost_basis = sa.Column(sa.Float, nullable=False)
    unrealized_pnl = sa.Column(sa.Float, nullable=False)
    unrealized_pnl_pct = sa.Column(sa.Float, nullable=False)
    day_change = sa.Column(sa.Float, default=0)
    day_change_pct = sa.Column(sa.Float, default=0)
    
    sector = sa.Column(sa.String(128))
    industry = sa.Column(sa.String(128))
    
    status = sa.Column(sa.String(16), default="open", index=True)
    opened_at = sa.Column(sa.DateTime, server_default=func.now())
    closed_at = sa.Column(sa.DateTime, nullable=True)
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())


class Trade(Base):
    """Trade history."""
    __tablename__ = "trades"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True)
    symbol = sa.Column(sa.String(16), nullable=False, index=True)
    trade_type = sa.Column(sa.String(8), nullable=False)  # 'buy' or 'sell'
    quantity = sa.Column(sa.Float, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    total_amount = sa.Column(sa.Float, nullable=False)
    commission = sa.Column(sa.Float, default=0)
    
    realized_pnl = sa.Column(sa.Float, nullable=True)
    realized_pnl_pct = sa.Column(sa.Float, nullable=True)
    
    notes = sa.Column(sa.Text, nullable=True)
    trade_date = sa.Column(sa.DateTime, nullable=False, index=True)
    created_at = sa.Column(sa.DateTime, server_default=func.now())


class StockQuote(Base):
    """Live stock data cache."""
    __tablename__ = "stock_quotes"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    symbol = sa.Column(sa.String(16), unique=True, nullable=False, index=True)
    current_price = sa.Column(sa.Float, nullable=False)
    change = sa.Column(sa.Float, nullable=False)
    percent_change = sa.Column(sa.Float, nullable=False)
    high = sa.Column(sa.Float, nullable=False)
    low = sa.Column(sa.Float, nullable=False)
    open = sa.Column(sa.Float, nullable=False)
    previous_close = sa.Column(sa.Float, nullable=False)
    volume = sa.Column(sa.BigInteger, nullable=True)
    
    timestamp = sa.Column(sa.DateTime, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now(), index=True)


class CompanyProfile(Base):
    """Company information."""
    __tablename__ = "company_profiles"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    symbol = sa.Column(sa.String(16), unique=True, nullable=False, index=True)
    name = sa.Column(sa.String(256), nullable=False)
    country = sa.Column(sa.String(64))
    currency = sa.Column(sa.String(8))
    exchange = sa.Column(sa.String(64))
    industry = sa.Column(sa.String(128))
    sector = sa.Column(sa.String(128))
    market_cap = sa.Column(sa.Float)
    ipo = sa.Column(sa.Date, nullable=True)
    logo = sa.Column(sa.String(512))
    phone = sa.Column(sa.String(32))
    weburl = sa.Column(sa.String(512))
    
    finnhub_industry = sa.Column(sa.String(128))
    
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())


class Strategy(Base):
    """Trading strategy configuration."""
    __tablename__ = "strategies"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True)
    name = sa.Column(sa.String(256), nullable=False)
    description = sa.Column(sa.Text)
    strategy_type = sa.Column(sa.String(64), nullable=False)  # momentum, mean_reversion, value, custom
    parameters = sa.Column(sa.JSON, default={})
    symbols = sa.Column(sa.JSON, default=[])  # List of symbols
    is_active = sa.Column(sa.Boolean, default=True, index=True)
    
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())


class Watchlist(Base):
    """User watchlists for tracking stocks."""
    __tablename__ = "watchlists"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True)
    name = sa.Column(sa.String(256), nullable=False)
    description = sa.Column(sa.Text)
    symbols = sa.Column(sa.JSON, default=[])  # List of symbols
    
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())


class Alert(Base):
    """Price alerts and notifications."""
    __tablename__ = "alerts"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True)
    symbol = sa.Column(sa.String(16), nullable=False, index=True)
    alert_type = sa.Column(sa.String(64), nullable=False)  # price_above, price_below, volume_spike, percent_change
    threshold_value = sa.Column(sa.Float, nullable=False)
    current_value = sa.Column(sa.Float)
    message = sa.Column(sa.Text)
    is_active = sa.Column(sa.Boolean, default=True, index=True)
    triggered_at = sa.Column(sa.DateTime, nullable=True)
    
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())
