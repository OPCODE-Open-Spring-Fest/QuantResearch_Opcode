"""Position management endpoints."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..auth import get_current_user
from ..db import get_session
from ..models import User, Position, Trade, StockQuote, CompanyProfile
from ..services.finnhub import FinnhubService
from ..services.dashboard import DashboardService
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/positions", tags=["positions"])


# Request/Response schemas
class BuyStockRequest(BaseModel):
    symbol: str
    quantity: float
    price: Optional[float] = None  # If None, use current market price


class SellStockRequest(BaseModel):
    symbol: str
    quantity: float
    price: Optional[float] = None  # If None, use current market price


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


def get_finnhub_service() -> FinnhubService:
    """Dependency to get Finnhub service."""
    api_key = os.getenv("FINNHUB_API_KEY", "test_key")
    return FinnhubService(api_key)


def get_dashboard_service(
    finnhub: FinnhubService = Depends(get_finnhub_service)
) -> DashboardService:
    """Dependency to get Dashboard service."""
    return DashboardService(finnhub)


@router.get("/", response_model=List[PositionResponse])
async def get_all_positions(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    """Get all open positions for the current user with live market data."""
    try:
        positions = await dashboard_service.get_positions_with_live_data(db, current_user.id)
        return positions
    except Exception as e:
        logger.error(f"Error fetching positions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch positions: {str(e)}"
        )


@router.get("/{symbol}")
async def get_position(
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    """Get a specific position by symbol."""
    try:
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == current_user.id,
                    Position.symbol == symbol.upper(),
                    Position.status == "open"
                )
            )
        )
        position = result.scalar_one_or_none()
        
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Position for {symbol} not found"
            )
        
        # Update with live data
        await dashboard_service.update_position_prices(db, position)
        
        # Get company profile
        profile = await dashboard_service.finnhub.update_company_profile(db, symbol.upper())
        
        return {
            "id": position.id,
            "symbol": position.symbol,
            "company_name": profile.name if profile else position.company_name,
            "quantity": position.quantity,
            "average_cost": round(position.average_cost, 2),
            "current_price": round(position.current_price, 2),
            "market_value": round(position.market_value, 2),
            "cost_basis": round(position.cost_basis, 2),
            "unrealized_pnl": round(position.unrealized_pnl, 2),
            "unrealized_pnl_pct": round(position.unrealized_pnl_pct, 2),
            "day_change": round(position.day_change, 2),
            "day_change_pct": round(position.day_change_pct, 2),
            "sector": profile.industry if profile else position.sector,
            "industry": profile.finnhub_industry if profile else position.industry,
            "opened_at": position.opened_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching position {symbol}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch position: {str(e)}"
        )


@router.post("/buy")
async def buy_stock(
    request: BuyStockRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Buy stock - create or update position."""
    try:
        symbol = request.symbol.upper()
        
        # Get current market price if not provided
        if request.price is None:
            quote = await finnhub_service.update_cached_quote(db, symbol)
            if not quote:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not fetch price for {symbol}"
                )
            price = quote.current_price
        else:
            price = request.price
        
        # Get company profile
        profile = await finnhub_service.update_company_profile(db, symbol)
        
        # Check if position already exists
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == current_user.id,
                    Position.symbol == symbol,
                    Position.status == "open"
                )
            )
        )
        existing_position = result.scalar_one_or_none()
        
        total_amount = request.quantity * price
        
        if existing_position:
            # Update existing position
            new_quantity = existing_position.quantity + request.quantity
            new_cost_basis = existing_position.cost_basis + total_amount
            new_average_cost = new_cost_basis / new_quantity
            
            existing_position.quantity = new_quantity
            existing_position.cost_basis = new_cost_basis
            existing_position.average_cost = new_average_cost
            existing_position.current_price = price
            existing_position.market_value = new_quantity * price
            existing_position.unrealized_pnl = existing_position.market_value - new_cost_basis
            existing_position.unrealized_pnl_pct = (existing_position.unrealized_pnl / new_cost_basis) * 100 if new_cost_basis > 0 else 0
            existing_position.updated_at = datetime.utcnow()
            
            position = existing_position
        else:
            # Create new position
            position = Position(
                user_id=current_user.id,
                symbol=symbol,
                company_name=profile.name if profile else symbol,
                quantity=request.quantity,
                average_cost=price,
                current_price=price,
                market_value=total_amount,
                cost_basis=total_amount,
                unrealized_pnl=0,
                unrealized_pnl_pct=0,
                day_change=0,
                day_change_pct=0,
                sector=profile.industry if profile else None,
                industry=profile.finnhub_industry if profile else None,
                status="open"
            )
            db.add(position)
        
        # Record trade
        trade = Trade(
            user_id=current_user.id,
            symbol=symbol,
            trade_type="buy",
            quantity=request.quantity,
            price=price,
            total_amount=total_amount,
            commission=0,
            trade_date=datetime.utcnow()
        )
        db.add(trade)
        
        await db.commit()
        await db.refresh(position)
        
        return {
            "status": "success",
            "message": f"Bought {request.quantity} shares of {symbol} at ${price:.2f}",
            "position": {
                "symbol": position.symbol,
                "quantity": position.quantity,
                "average_cost": round(position.average_cost, 2),
                "market_value": round(position.market_value, 2),
                "unrealized_pnl": round(position.unrealized_pnl, 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error buying stock: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to buy stock: {str(e)}"
        )


@router.post("/sell")
async def sell_stock(
    request: SellStockRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Sell stock - reduce or close position."""
    try:
        symbol = request.symbol.upper()
        
        # Get existing position
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == current_user.id,
                    Position.symbol == symbol,
                    Position.status == "open"
                )
            )
        )
        position = result.scalar_one_or_none()
        
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No open position found for {symbol}"
            )
        
        if position.quantity < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot sell {request.quantity} shares. You only have {position.quantity} shares."
            )
        
        # Get current market price if not provided
        if request.price is None:
            quote = await finnhub_service.update_cached_quote(db, symbol)
            if not quote:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not fetch price for {symbol}"
                )
            price = quote.current_price
        else:
            price = request.price
        
        total_amount = request.quantity * price
        
        # Calculate realized P&L
        cost_for_sold_shares = request.quantity * position.average_cost
        realized_pnl = total_amount - cost_for_sold_shares
        realized_pnl_pct = (realized_pnl / cost_for_sold_shares) * 100 if cost_for_sold_shares > 0 else 0
        
        # Update position
        new_quantity = position.quantity - request.quantity
        
        if new_quantity <= 0:
            # Close position
            position.quantity = 0
            position.status = "closed"
            position.closed_at = datetime.utcnow()
            position.market_value = 0
            position.unrealized_pnl = 0
            position.unrealized_pnl_pct = 0
        else:
            # Reduce position
            position.quantity = new_quantity
            position.cost_basis = position.cost_basis - cost_for_sold_shares
            position.current_price = price
            position.market_value = new_quantity * price
            position.unrealized_pnl = position.market_value - position.cost_basis
            position.unrealized_pnl_pct = (position.unrealized_pnl / position.cost_basis) * 100 if position.cost_basis > 0 else 0
        
        position.updated_at = datetime.utcnow()
        
        # Record trade
        trade = Trade(
            user_id=current_user.id,
            symbol=symbol,
            trade_type="sell",
            quantity=request.quantity,
            price=price,
            total_amount=total_amount,
            commission=0,
            realized_pnl=realized_pnl,
            realized_pnl_pct=realized_pnl_pct,
            trade_date=datetime.utcnow()
        )
        db.add(trade)
        
        await db.commit()
        await db.refresh(position)
        
        return {
            "status": "success",
            "message": f"Sold {request.quantity} shares of {symbol} at ${price:.2f}",
            "realized_pnl": round(realized_pnl, 2),
            "realized_pnl_pct": round(realized_pnl_pct, 2),
            "position": {
                "symbol": position.symbol,
                "quantity": position.quantity,
                "status": position.status,
                "market_value": round(position.market_value, 2) if new_quantity > 0 else 0,
                "unrealized_pnl": round(position.unrealized_pnl, 2) if new_quantity > 0 else 0
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error selling stock: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sell stock: {str(e)}"
        )


@router.delete("/{symbol}")
async def close_position(
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Close entire position (sell all shares)."""
    try:
        symbol = symbol.upper()
        
        # Get position
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == current_user.id,
                    Position.symbol == symbol,
                    Position.status == "open"
                )
            )
        )
        position = result.scalar_one_or_none()
        
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No open position found for {symbol}"
            )
        
        # Sell all shares
        sell_request = SellStockRequest(
            symbol=symbol,
            quantity=position.quantity
        )
        
        return await sell_stock(sell_request, db, current_user, finnhub_service)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error closing position {symbol}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to close position: {str(e)}"
        )
