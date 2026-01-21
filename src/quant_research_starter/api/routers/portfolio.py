"""Portfolio cash management endpoints."""

from __future__ import annotations

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from ..auth import get_current_user
from ..db import get_session
from ..models import User, Portfolio, Trade

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


class DepositRequest(BaseModel):
    amount: float
    notes: str = None

    @validator('amount')
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v


class WithdrawRequest(BaseModel):
    amount: float
    notes: str = None

    @validator('amount')
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v


@router.post("/deposit")
async def deposit_cash(
    request: DepositRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Deposit cash into portfolio."""
    try:
        # Get latest portfolio snapshot
        result = await db.execute(
            select(Portfolio)
            .where(Portfolio.user_id == current_user.id)
            .order_by(desc(Portfolio.timestamp))
            .limit(1)
        )
        latest_portfolio = result.scalar_one_or_none()
        
        if latest_portfolio:
            new_cash = latest_portfolio.cash + request.amount
            new_total_value = latest_portfolio.total_value + request.amount
        else:
            new_cash = request.amount
            new_total_value = request.amount
        
        # Create new portfolio snapshot
        portfolio = Portfolio(
            user_id=current_user.id,
            total_value=new_total_value,
            cash=new_cash,
            invested=latest_portfolio.invested if latest_portfolio else 0,
            daily_return=0,
            total_return=0,
            total_return_percent=0,
            sharpe_ratio=latest_portfolio.sharpe_ratio if latest_portfolio else 0,
            max_drawdown=latest_portfolio.max_drawdown if latest_portfolio else 0,
            volatility=latest_portfolio.volatility if latest_portfolio else 0,
            beta=latest_portfolio.beta if latest_portfolio else 1.0,
            alpha=latest_portfolio.alpha if latest_portfolio else 0,
            win_rate=latest_portfolio.win_rate if latest_portfolio else 0
        )
        
        db.add(portfolio)
        await db.commit()
        await db.refresh(portfolio)
        
        return {
            "status": "success",
            "message": f"Deposited ${request.amount:,.2f}",
            "new_cash_balance": round(new_cash, 2),
            "total_value": round(new_total_value, 2)
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error depositing cash: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deposit cash: {str(e)}"
        )


@router.post("/withdraw")
async def withdraw_cash(
    request: WithdrawRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Withdraw cash from portfolio."""
    try:
        # Get latest portfolio snapshot
        result = await db.execute(
            select(Portfolio)
            .where(Portfolio.user_id == current_user.id)
            .order_by(desc(Portfolio.timestamp))
            .limit(1)
        )
        latest_portfolio = result.scalar_one_or_none()
        
        if not latest_portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No portfolio found"
            )
        
        if latest_portfolio.cash < request.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient cash. Available: ${latest_portfolio.cash:,.2f}"
            )
        
        new_cash = latest_portfolio.cash - request.amount
        new_total_value = latest_portfolio.total_value - request.amount
        
        # Create new portfolio snapshot
        portfolio = Portfolio(
            user_id=current_user.id,
            total_value=new_total_value,
            cash=new_cash,
            invested=latest_portfolio.invested,
            daily_return=0,
            total_return=latest_portfolio.total_return - request.amount,
            total_return_percent=latest_portfolio.total_return_percent,
            sharpe_ratio=latest_portfolio.sharpe_ratio,
            max_drawdown=latest_portfolio.max_drawdown,
            volatility=latest_portfolio.volatility,
            beta=latest_portfolio.beta,
            alpha=latest_portfolio.alpha,
            win_rate=latest_portfolio.win_rate
        )
        
        db.add(portfolio)
        await db.commit()
        await db.refresh(portfolio)
        
        return {
            "status": "success",
            "message": f"Withdrew ${request.amount:,.2f}",
            "new_cash_balance": round(new_cash, 2),
            "total_value": round(new_total_value, 2)
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error withdrawing cash: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to withdraw cash: {str(e)}"
        )


@router.get("/balance")
async def get_cash_balance(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get current cash balance."""
    try:
        # Get latest portfolio snapshot
        result = await db.execute(
            select(Portfolio)
            .where(Portfolio.user_id == current_user.id)
            .order_by(desc(Portfolio.timestamp))
            .limit(1)
        )
        latest_portfolio = result.scalar_one_or_none()
        
        if not latest_portfolio:
            return {
                "cash": 0,
                "invested": 0,
                "total_value": 0
            }
        
        return {
            "cash": round(latest_portfolio.cash, 2),
            "invested": round(latest_portfolio.invested, 2),
            "total_value": round(latest_portfolio.total_value, 2),
            "timestamp": latest_portfolio.timestamp.isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching cash balance: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch cash balance: {str(e)}"
        )
