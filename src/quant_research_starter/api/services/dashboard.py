"""Dashboard service for portfolio analytics and calculations."""

import logging
from datetime import datetime, timedelta
from typing import Optional, List
import statistics

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc

from ..models import Portfolio, Position, Trade, User
from .finnhub import FinnhubService

logger = logging.getLogger(__name__)


class DashboardService:
    """Service for dashboard analytics and portfolio management."""
    
    def __init__(self, finnhub_service: FinnhubService):
        self.finnhub = finnhub_service
    
    async def calculate_portfolio_metrics(
        self,
        db: AsyncSession,
        user_id: int
    ) -> dict:
        """
        Calculate comprehensive portfolio metrics.
        
        Returns:
            dict with total_value, cash, invested, returns, risk metrics
        """
        # Get all open positions
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == user_id,
                    Position.status == "open"
                )
            )
        )
        positions = result.scalars().all()
        
        # Update positions with live prices
        symbols = [p.symbol for p in positions]
        if symbols:
            await self.finnhub.batch_update_quotes(db, symbols)
            
            # Refresh positions to get updated quotes
            await db.refresh_all(positions)
        
        # Calculate totals
        total_market_value = sum(p.market_value for p in positions)
        total_cost_basis = sum(p.cost_basis for p in positions)
        total_unrealized_pnl = sum(p.unrealized_pnl for p in positions)
        
        # Get user's cash (default 100k if no cash field)
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        
        # Assume initial capital of 100k minus invested amount
        total_invested = total_cost_basis
        cash = 100000 - total_invested  # Simplified
        total_value = cash + total_market_value
        
        # Calculate returns
        if total_invested > 0:
            total_return_pct = (total_unrealized_pnl / total_invested) * 100
        else:
            total_return_pct = 0
        
        # Calculate risk metrics from historical portfolios
        risk_metrics = await self._calculate_risk_metrics(db, user_id)
        
        # Get trade statistics
        trade_stats = await self._calculate_trade_stats(db, user_id)
        
        return {
            "total_value": round(total_value, 2),
            "cash": round(cash, 2),
            "invested": round(total_invested, 2),
            "market_value": round(total_market_value, 2),
            "unrealized_pnl": round(total_unrealized_pnl, 2),
            "total_return": round(total_unrealized_pnl, 2),
            "total_return_percent": round(total_return_pct, 2),
            "sharpe_ratio": risk_metrics["sharpe_ratio"],
            "max_drawdown": risk_metrics["max_drawdown"],
            "volatility": risk_metrics["volatility"],
            "beta": risk_metrics["beta"],
            "alpha": risk_metrics["alpha"],
            "win_rate": trade_stats["win_rate"],
            "total_trades": trade_stats["total_trades"],
            "winning_trades": trade_stats["winning_trades"],
            "losing_trades": trade_stats["losing_trades"]
        }
    
    async def update_position_prices(
        self,
        db: AsyncSession,
        position: Position
    ) -> Position:
        """
        Update a position with current market price.
        
        Args:
            db: Database session
            position: Position to update
        
        Returns:
            Updated position
        """
        # Get current quote
        quote = await self.finnhub.update_cached_quote(db, position.symbol)
        
        if quote:
            position.current_price = quote.current_price
            position.market_value = position.quantity * quote.current_price
            position.unrealized_pnl = position.market_value - position.cost_basis
            
            if position.cost_basis > 0:
                position.unrealized_pnl_pct = (position.unrealized_pnl / position.cost_basis) * 100
            
            position.day_change = quote.change * position.quantity
            position.day_change_pct = quote.percent_change
            position.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(position)
        
        return position
    
    async def get_positions_with_live_data(
        self,
        db: AsyncSession,
        user_id: int
    ) -> List[dict]:
        """
        Get all positions with live market data and company info.
        
        Returns:
            List of position dicts with enriched data
        """
        # Get positions
        result = await db.execute(
            select(Position).where(
                and_(
                    Position.user_id == user_id,
                    Position.status == "open"
                )
            ).order_by(desc(Position.market_value))
        )
        positions = result.scalars().all()
        
        enriched_positions = []
        
        for position in positions:
            # Update with live price
            await self.update_position_prices(db, position)
            
            # Get company profile
            profile = await self.finnhub.update_company_profile(db, position.symbol)
            
            enriched_positions.append({
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
                "logo": profile.logo if profile else None,
                "opened_at": position.opened_at.isoformat()
            })
        
        return enriched_positions
    
    async def get_recent_trades(
        self,
        db: AsyncSession,
        user_id: int,
        limit: int = 50
    ) -> List[dict]:
        """
        Get recent trades for a user.
        
        Args:
            db: Database session
            user_id: User ID
            limit: Max trades to return
        
        Returns:
            List of trade dicts
        """
        result = await db.execute(
            select(Trade).where(
                Trade.user_id == user_id
            ).order_by(desc(Trade.trade_date)).limit(limit)
        )
        trades = result.scalars().all()
        
        return [
            {
                "id": trade.id,
                "symbol": trade.symbol,
                "trade_type": trade.trade_type,
                "quantity": trade.quantity,
                "price": round(trade.price, 2),
                "total_amount": round(trade.total_amount, 2),
                "commission": round(trade.commission, 2),
                "realized_pnl": round(trade.realized_pnl, 2) if trade.realized_pnl else None,
                "realized_pnl_pct": round(trade.realized_pnl_pct, 2) if trade.realized_pnl_pct else None,
                "trade_date": trade.trade_date.isoformat(),
                "notes": trade.notes
            }
            for trade in trades
        ]
    
    async def save_portfolio_snapshot(
        self,
        db: AsyncSession,
        user_id: int,
        metrics: dict
    ) -> Portfolio:
        """
        Save current portfolio metrics as a snapshot.
        
        Args:
            db: Database session
            user_id: User ID
            metrics: Portfolio metrics dict
        
        Returns:
            Created Portfolio snapshot
        """
        portfolio = Portfolio(
            user_id=user_id,
            total_value=metrics["total_value"],
            cash=metrics["cash"],
            invested=metrics["invested"],
            daily_return=0,  # Would need previous snapshot to calculate
            total_return=metrics["total_return"],
            total_return_percent=metrics["total_return_percent"],
            sharpe_ratio=metrics["sharpe_ratio"],
            max_drawdown=metrics["max_drawdown"],
            volatility=metrics["volatility"],
            beta=metrics["beta"],
            alpha=metrics["alpha"],
            win_rate=metrics["win_rate"]
        )
        
        db.add(portfolio)
        await db.commit()
        await db.refresh(portfolio)
        
        return portfolio
    
    async def _calculate_risk_metrics(
        self,
        db: AsyncSession,
        user_id: int
    ) -> dict:
        """
        Calculate risk metrics from historical portfolio snapshots.
        
        Returns:
            dict with sharpe_ratio, max_drawdown, volatility, beta, alpha
        """
        # Get historical snapshots (last 30 days)
        result = await db.execute(
            select(Portfolio).where(
                and_(
                    Portfolio.user_id == user_id,
                    Portfolio.timestamp >= datetime.utcnow() - timedelta(days=30)
                )
            ).order_by(Portfolio.timestamp)
        )
        snapshots = result.scalars().all()
        
        if len(snapshots) < 2:
            return {
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "volatility": 0.0,
                "beta": 1.0,
                "alpha": 0.0
            }
        
        # Calculate daily returns
        returns = []
        for i in range(1, len(snapshots)):
            prev_value = snapshots[i-1].total_value
            curr_value = snapshots[i].total_value
            if prev_value > 0:
                daily_return = (curr_value - prev_value) / prev_value
                returns.append(daily_return)
        
        if not returns:
            return {
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "volatility": 0.0,
                "beta": 1.0,
                "alpha": 0.0
            }
        
        # Volatility (annualized standard deviation)
        volatility = statistics.stdev(returns) * (252 ** 0.5) if len(returns) > 1 else 0
        
        # Sharpe Ratio (assuming 0% risk-free rate for simplicity)
        avg_return = statistics.mean(returns)
        sharpe = (avg_return * 252) / volatility if volatility > 0 else 0
        
        # Max Drawdown
        peak = snapshots[0].total_value
        max_dd = 0
        for snapshot in snapshots:
            if snapshot.total_value > peak:
                peak = snapshot.total_value
            dd = (peak - snapshot.total_value) / peak if peak > 0 else 0
            max_dd = max(max_dd, dd)
        
        return {
            "sharpe_ratio": round(sharpe, 2),
            "max_drawdown": round(max_dd * 100, 2),  # As percentage
            "volatility": round(volatility * 100, 2),  # As percentage
            "beta": 1.0,  # Would need market data for true beta
            "alpha": round(avg_return * 252 * 100, 2)  # Annualized return as alpha proxy
        }
    
    async def _calculate_trade_stats(
        self,
        db: AsyncSession,
        user_id: int
    ) -> dict:
        """
        Calculate trade statistics.
        
        Returns:
            dict with win_rate, total_trades, winning_trades, losing_trades
        """
        result = await db.execute(
            select(Trade).where(
                and_(
                    Trade.user_id == user_id,
                    Trade.trade_type == "sell",
                    Trade.realized_pnl.isnot(None)
                )
            )
        )
        closed_trades = result.scalars().all()
        
        if not closed_trades:
            return {
                "win_rate": 0.0,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0
            }
        
        winning = sum(1 for t in closed_trades if t.realized_pnl > 0)
        losing = sum(1 for t in closed_trades if t.realized_pnl <= 0)
        total = len(closed_trades)
        
        win_rate = (winning / total * 100) if total > 0 else 0
        
        return {
            "win_rate": round(win_rate, 2),
            "total_trades": total,
            "winning_trades": winning,
            "losing_trades": losing
        }
