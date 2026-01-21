"""Portfolio optimization endpoints."""

from __future__ import annotations

import logging
from typing import List, Dict
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..db import get_session
from ..models import User
from ..schemas import OptimizationRequest, OptimizationResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/optimize", tags=["optimization"])


@router.post("/", response_model=OptimizationResponse)
async def optimize_portfolio(
    request: OptimizationRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Optimize portfolio allocation using Modern Portfolio Theory.
    
    Supports:
    - max_sharpe: Maximize Sharpe ratio
    - min_volatility: Minimize portfolio volatility
    - max_return: Maximize expected return
    """
    try:
        import numpy as np
        import pandas as pd
        
        # Mock implementation - in production, fetch real historical data
        # For now, generate random returns for demonstration
        np.random.seed(42)
        
        symbols = request.symbols
        num_assets = len(symbols)
        
        if num_assets < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Need at least 2 symbols for portfolio optimization"
            )
        
        # Generate mock daily returns (in production, fetch from market data API)
        days = 252  # One year of trading days
        returns = np.random.normal(0.001, 0.02, (days, num_assets))
        
        # Calculate statistics
        mean_returns = np.mean(returns, axis=0)
        cov_matrix = np.cov(returns.T)
        
        # Optimization based on method
        if request.optimization_method == "max_sharpe":
            weights = optimize_sharpe_ratio(mean_returns, cov_matrix)
        elif request.optimization_method == "min_volatility":
            weights = optimize_min_volatility(cov_matrix, num_assets)
        elif request.optimization_method == "max_return":
            weights = optimize_max_return(mean_returns, num_assets)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown optimization method: {request.optimization_method}"
            )
        
        # Calculate portfolio metrics
        portfolio_return = np.dot(weights, mean_returns) * 252  # Annualized
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)  # Annualized
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
        
        # Create weights dictionary
        weights_dict = {symbol: float(weight) for symbol, weight in zip(symbols, weights)}
        
        return {
            "weights": weights_dict,
            "expected_return": round(portfolio_return * 100, 2),  # As percentage
            "expected_volatility": round(portfolio_volatility * 100, 2),  # As percentage
            "sharpe_ratio": round(sharpe_ratio, 2)
        }
    except HTTPException:
        raise
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Optimization requires numpy and pandas. Please install dependencies."
        )
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize portfolio: {str(e)}"
        )


def optimize_sharpe_ratio(mean_returns, cov_matrix):
    """Optimize for maximum Sharpe ratio."""
    import numpy as np
    from scipy.optimize import minimize
    
    num_assets = len(mean_returns)
    
    def neg_sharpe(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
    
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]
    
    result = minimize(neg_sharpe, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x if result.success else np.array(initial_guess)


def optimize_min_volatility(cov_matrix, num_assets):
    """Optimize for minimum volatility."""
    import numpy as np
    from scipy.optimize import minimize
    
    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]
    
    result = minimize(portfolio_volatility, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x if result.success else np.array(initial_guess)


def optimize_max_return(mean_returns, num_assets):
    """Optimize for maximum expected return."""
    import numpy as np
    from scipy.optimize import minimize
    
    def neg_return(weights):
        return -np.dot(weights, mean_returns)
    
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]
    
    result = minimize(neg_return, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x if result.success else np.array(initial_guess)


@router.post("/rebalance")
async def suggest_rebalance(
    target_weights: Dict[str, float],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Suggest trades to rebalance portfolio to target weights.
    
    Args:
        target_weights: Dictionary of symbol -> target weight (0-1)
    """
    try:
        from sqlalchemy import select, and_
        from ..models import Position, Portfolio
        from ..services.finnhub import FinnhubService
        import os
        
        # Get current positions
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == current_user.id,
                    Position.status == "open"
                )
            )
        )
        positions = result.scalars().all()
        
        # Get current portfolio value
        portfolio_result = await db.execute(
            select(Portfolio)
            .where(Portfolio.user_id == current_user.id)
            .order_by(Portfolio.timestamp.desc())
            .limit(1)
        )
        portfolio = portfolio_result.scalar_one_or_none()
        
        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No portfolio found"
            )
        
        total_value = portfolio.total_value
        
        # Calculate current weights
        current_weights = {}
        for pos in positions:
            current_weights[pos.symbol] = pos.market_value / total_value if total_value > 0 else 0
        
        # Calculate rebalancing trades
        trades = []
        for symbol, target_weight in target_weights.items():
            current_weight = current_weights.get(symbol, 0)
            weight_diff = target_weight - current_weight
            value_diff = weight_diff * total_value
            
            # Find current position
            current_pos = next((p for p in positions if p.symbol == symbol), None)
            current_price = current_pos.current_price if current_pos else 100  # Default price if no position
            
            shares_to_trade = value_diff / current_price if current_price > 0 else 0
            
            if abs(shares_to_trade) >= 0.01:  # Only suggest if meaningful
                trades.append({
                    "symbol": symbol,
                    "action": "buy" if shares_to_trade > 0 else "sell",
                    "shares": abs(round(shares_to_trade, 2)),
                    "current_weight": round(current_weight * 100, 2),
                    "target_weight": round(target_weight * 100, 2),
                    "estimated_value": abs(round(value_diff, 2))
                })
        
        return {
            "status": "success",
            "total_portfolio_value": round(total_value, 2),
            "trades_needed": len(trades),
            "suggested_trades": trades
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating rebalance: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate rebalance: {str(e)}"
        )
