"""Trade history endpoints."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc

from ..auth import get_current_user
from ..db import get_session
from ..models import User, Trade
from ..services.dashboard import DashboardService
from ..services.finnhub import FinnhubService
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/trades", tags=["trades"])


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
    created_at: str


def get_finnhub_service() -> FinnhubService:
    """Dependency to get Finnhub service."""
    api_key = os.getenv("FINNHUB_API_KEY", "test_key")
    return FinnhubService(api_key)


def get_dashboard_service(
    finnhub: FinnhubService = Depends(get_finnhub_service)
) -> DashboardService:
    """Dependency to get Dashboard service."""
    return DashboardService(finnhub)


@router.get("/", response_model=List[TradeResponse])
async def get_trades(
    limit: int = Query(default=50, le=500),
    symbol: Optional[str] = None,
    trade_type: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    """Get trade history for the current user."""
    try:
        trades = await dashboard_service.get_recent_trades(
            db, current_user.id, limit
        )
        
        # Apply filters
        if symbol:
            trades = [t for t in trades if t['symbol'] == symbol.upper()]
        if trade_type:
            trades = [t for t in trades if t['trade_type'] == trade_type.lower()]
        
        return trades
    except Exception as e:
        logger.error(f"Error fetching trades: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch trades: {str(e)}"
        )


@router.get("/stats")
async def get_trade_stats(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get trade statistics."""
    try:
        # Get all trades
        result = await db.execute(
            select(Trade).where(
                Trade.user_id == current_user.id
            ).order_by(desc(Trade.trade_date))
        )
        all_trades = result.scalars().all()
        
        # Calculate stats
        total_trades = len(all_trades)
        buy_trades = [t for t in all_trades if t.trade_type == "buy"]
        sell_trades = [t for t in all_trades if t.trade_type == "sell"]
        
        total_bought = sum(t.total_amount for t in buy_trades)
        total_sold = sum(t.total_amount for t in sell_trades)
        total_commissions = sum(t.commission for t in all_trades)
        
        # Realized P&L
        realized_trades = [t for t in sell_trades if t.realized_pnl is not None]
        total_realized_pnl = sum(t.realized_pnl for t in realized_trades)
        winning_trades = [t for t in realized_trades if t.realized_pnl > 0]
        losing_trades = [t for t in realized_trades if t.realized_pnl < 0]
        
        win_rate = (len(winning_trades) / len(realized_trades) * 100) if realized_trades else 0
        
        # Average trade size
        avg_trade_size = (total_bought + total_sold) / (2 * total_trades) if total_trades > 0 else 0
        
        # Best and worst trades
        best_trade = max(realized_trades, key=lambda t: t.realized_pnl) if realized_trades else None
        worst_trade = min(realized_trades, key=lambda t: t.realized_pnl) if realized_trades else None
        
        return {
            "total_trades": total_trades,
            "buy_trades": len(buy_trades),
            "sell_trades": len(sell_trades),
            "total_bought": round(total_bought, 2),
            "total_sold": round(total_sold, 2),
            "total_commissions": round(total_commissions, 2),
            "total_realized_pnl": round(total_realized_pnl, 2),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate": round(win_rate, 2),
            "avg_trade_size": round(avg_trade_size, 2),
            "best_trade": {
                "symbol": best_trade.symbol,
                "pnl": round(best_trade.realized_pnl, 2),
                "date": best_trade.trade_date.isoformat()
            } if best_trade else None,
            "worst_trade": {
                "symbol": worst_trade.symbol,
                "pnl": round(worst_trade.realized_pnl, 2),
                "date": worst_trade.trade_date.isoformat()
            } if worst_trade else None
        }
    except Exception as e:
        logger.error(f"Error calculating trade stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate trade stats: {str(e)}"
        )


@router.get("/{trade_id}")
async def get_trade(
    trade_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific trade by ID."""
    try:
        result = await db.execute(
            select(Trade).where(
                and_(
                    Trade.id == trade_id,
                    Trade.user_id == current_user.id
                )
            )
        )
        trade = result.scalar_one_or_none()
        
        if not trade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trade not found"
            )
        
        return {
            "id": trade.id,
            "symbol": trade.symbol,
            "trade_type": trade.trade_type,
            "quantity": trade.quantity,
            "price": round(trade.price, 2),
            "total_amount": round(trade.total_amount, 2),
            "commission": round(trade.commission, 2),
            "realized_pnl": round(trade.realized_pnl, 2) if trade.realized_pnl else None,
            "realized_pnl_pct": round(trade.realized_pnl_pct, 2) if trade.realized_pnl_pct else None,
            "notes": trade.notes,
            "trade_date": trade.trade_date.isoformat(),
            "created_at": trade.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching trade {trade_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch trade: {str(e)}"
        )
