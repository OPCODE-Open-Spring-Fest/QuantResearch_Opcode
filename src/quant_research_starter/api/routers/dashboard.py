"""Dashboard API endpoints."""

import logging
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..auth import get_current_user
from ..models import User
from ..services.finnhub import FinnhubService
from ..services.dashboard import DashboardService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def get_finnhub_service() -> FinnhubService:
    """Dependency to get Finnhub service."""
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="FINNHUB_API_KEY not configured"
        )
    return FinnhubService(api_key)


def get_dashboard_service(
    finnhub: FinnhubService = Depends(get_finnhub_service)
) -> DashboardService:
    """Dependency to get Dashboard service."""
    return DashboardService(finnhub)


@router.get("/overview")
async def get_portfolio_overview(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get comprehensive portfolio overview with all metrics.
    
    Returns:
        - total_value: Total portfolio value (cash + investments)
        - cash: Available cash
        - invested: Total invested amount
        - market_value: Current market value of positions
        - unrealized_pnl: Unrealized profit/loss
        - total_return: Total return in dollars
        - total_return_percent: Total return percentage
        - sharpe_ratio: Risk-adjusted return metric
        - max_drawdown: Maximum drawdown percentage
        - volatility: Portfolio volatility
        - beta: Market correlation
        - alpha: Excess return over market
        - win_rate: Percentage of winning trades
        - total_trades: Total number of trades
    """
    try:
        metrics = await dashboard_service.calculate_portfolio_metrics(
            db, current_user.id
        )
        
        # Save snapshot
        await dashboard_service.save_portfolio_snapshot(
            db, current_user.id, metrics
        )
        
        return {
            "status": "success",
            "data": metrics
        }
    except Exception as e:
        logger.error(f"Error calculating portfolio metrics: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate portfolio metrics: {str(e)}"
        )


@router.get("/positions")
async def get_positions(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get all open positions with live market data.
    
    Returns:
        List of positions with:
        - symbol, company_name, quantity
        - average_cost, current_price
        - market_value, cost_basis
        - unrealized_pnl, unrealized_pnl_pct
        - day_change, day_change_pct
        - sector, industry, logo
    """
    try:
        positions = await dashboard_service.get_positions_with_live_data(
            db, current_user.id
        )
        
        return {
            "status": "success",
            "data": positions,
            "count": len(positions)
        }
    except Exception as e:
        logger.error(f"Error fetching positions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch positions: {str(e)}"
        )


@router.get("/trades")
async def get_trades(
    limit: int = 50,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get recent trade history.
    
    Args:
        limit: Maximum number of trades to return (default 50)
    
    Returns:
        List of trades with:
        - symbol, trade_type (buy/sell)
        - quantity, price, total_amount
        - commission
        - realized_pnl, realized_pnl_pct (for sells)
        - trade_date, notes
    """
    try:
        trades = await dashboard_service.get_recent_trades(
            db, current_user.id, limit
        )
        
        return {
            "status": "success",
            "data": trades,
            "count": len(trades)
        }
    except Exception as e:
        logger.error(f"Error fetching trades: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch trades: {str(e)}"
        )


@router.get("/quote/{symbol}")
async def get_stock_quote(
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """
    Get live stock quote for a symbol.
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns:
        Live quote data:
        - current_price, change, percent_change
        - high, low, open, previous_close
        - volume, timestamp
    """
    try:
        quote = await finnhub_service.update_cached_quote(db, symbol.upper())
        
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quote not found for symbol: {symbol}"
            )
        
        return {
            "status": "success",
            "data": {
                "symbol": quote.symbol,
                "current_price": round(quote.current_price, 2),
                "change": round(quote.change, 2),
                "percent_change": round(quote.percent_change, 2),
                "high": round(quote.high, 2),
                "low": round(quote.low, 2),
                "open": round(quote.open, 2),
                "previous_close": round(quote.previous_close, 2),
                "volume": quote.volume,
                "timestamp": quote.updated_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch quote: {str(e)}"
        )


@router.get("/profile/{symbol}")
async def get_company_profile(
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """
    Get company profile information.
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
    
    Returns:
        Company profile:
        - name, country, currency, exchange
        - industry, sector, market_cap
        - ipo, logo, phone, weburl
    """
    try:
        profile = await finnhub_service.update_company_profile(db, symbol.upper())
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found for symbol: {symbol}"
            )
        
        return {
            "status": "success",
            "data": {
                "symbol": profile.symbol,
                "name": profile.name,
                "country": profile.country,
                "currency": profile.currency,
                "exchange": profile.exchange,
                "industry": profile.industry,
                "sector": profile.sector,
                "market_cap": profile.market_cap,
                "ipo": profile.ipo.isoformat() if profile.ipo else None,
                "logo": profile.logo,
                "phone": profile.phone,
                "weburl": profile.weburl,
                "finnhub_industry": profile.finnhub_industry
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching profile for {symbol}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch profile: {str(e)}"
        )


@router.get("/performance")
async def get_performance_history(
    days: int = 30,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get historical portfolio performance.
    
    Args:
        days: Number of days of history (default 30)
    
    Returns:
        Time series of portfolio values and metrics
    """
    from datetime import datetime, timedelta
    from sqlalchemy import select, and_
    from ..models import Portfolio
    
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            select(Portfolio).where(
                and_(
                    Portfolio.user_id == current_user.id,
                    Portfolio.timestamp >= cutoff
                )
            ).order_by(Portfolio.timestamp)
        )
        snapshots = result.scalars().all()
        
        performance_data = [
            {
                "timestamp": s.timestamp.isoformat(),
                "total_value": round(s.total_value, 2),
                "cash": round(s.cash, 2),
                "invested": round(s.invested, 2),
                "total_return": round(s.total_return, 2),
                "total_return_percent": round(s.total_return_percent, 2),
                "sharpe_ratio": round(s.sharpe_ratio, 2),
                "volatility": round(s.volatility, 2)
            }
            for s in snapshots
        ]
        
        return {
            "status": "success",
            "data": performance_data,
            "count": len(performance_data)
        }
    except Exception as e:
        logger.error(f"Error fetching performance history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch performance history: {str(e)}"
        )
