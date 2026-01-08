"""Seed script for dashboard demo data."""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from src.quant_research_starter.api.db import AsyncSessionLocal, engine, Base
from src.quant_research_starter.api.models import User, Position, Trade
from src.quant_research_starter.api.auth import get_password_hash


async def seed_dashboard_data():
    """Seed database with sample portfolio data."""
    
    async with AsyncSessionLocal() as db:
        # Check if demo user exists
        result = await db.execute(select(User).where(User.username == "demo"))
        demo_user = result.scalar_one_or_none()
        
        if not demo_user:
            print("Creating demo user...")
            demo_user = User(
                username="demo",
                hashed_password=get_password_hash("demo123"),
                is_active=True,
                role="user"
            )
            db.add(demo_user)
            await db.commit()
            await db.refresh(demo_user)
            print(f"✓ Created demo user (ID: {demo_user.id})")
        else:
            print(f"✓ Demo user exists (ID: {demo_user.id})")
        
        # Check if positions already exist
        result = await db.execute(
            select(Position).where(Position.user_id == demo_user.id)
        )
        existing_positions = result.scalars().all()
        
        if existing_positions:
            print(f"✓ {len(existing_positions)} positions already exist")
        else:
            print("Creating sample positions...")
            
            # Sample portfolio positions
            sample_positions = [
                {
                    "symbol": "AAPL",
                    "company_name": "Apple Inc.",
                    "quantity": 50,
                    "average_cost": 175.50,
                    "sector": "Technology",
                    "industry": "Consumer Electronics"
                },
                {
                    "symbol": "MSFT",
                    "company_name": "Microsoft Corporation",
                    "quantity": 30,
                    "average_cost": 380.25,
                    "sector": "Technology",
                    "industry": "Software"
                },
                {
                    "symbol": "GOOGL",
                    "company_name": "Alphabet Inc.",
                    "quantity": 25,
                    "average_cost": 142.30,
                    "sector": "Technology",
                    "industry": "Internet"
                },
                {
                    "symbol": "TSLA",
                    "company_name": "Tesla Inc.",
                    "quantity": 20,
                    "average_cost": 245.80,
                    "sector": "Consumer Cyclical",
                    "industry": "Auto Manufacturers"
                },
                {
                    "symbol": "NVDA",
                    "company_name": "NVIDIA Corporation",
                    "quantity": 15,
                    "average_cost": 495.60,
                    "sector": "Technology",
                    "industry": "Semiconductors"
                }
            ]
            
            for pos_data in sample_positions:
                # Simulate current price (slightly higher for unrealized gains)
                current_price = pos_data["average_cost"] * 1.12  # 12% gain
                quantity = pos_data["quantity"]
                cost_basis = pos_data["average_cost"] * quantity
                market_value = current_price * quantity
                unrealized_pnl = market_value - cost_basis
                unrealized_pnl_pct = (unrealized_pnl / cost_basis) * 100
                
                position = Position(
                    user_id=demo_user.id,
                    symbol=pos_data["symbol"],
                    company_name=pos_data["company_name"],
                    quantity=quantity,
                    average_cost=pos_data["average_cost"],
                    current_price=current_price,
                    market_value=market_value,
                    cost_basis=cost_basis,
                    unrealized_pnl=unrealized_pnl,
                    unrealized_pnl_pct=unrealized_pnl_pct,
                    day_change=0,
                    day_change_pct=0,
                    sector=pos_data["sector"],
                    industry=pos_data["industry"],
                    status="open",
                    opened_at=datetime.utcnow() - timedelta(days=30)
                )
                db.add(position)
            
            await db.commit()
            print(f"✓ Created {len(sample_positions)} positions")
        
        # Check if trades exist
        result = await db.execute(
            select(Trade).where(Trade.user_id == demo_user.id)
        )
        existing_trades = result.scalars().all()
        
        if existing_trades:
            print(f"✓ {len(existing_trades)} trades already exist")
        else:
            print("Creating sample trades...")
            
            # Sample trade history (buy orders for positions)
            sample_trades = [
                {
                    "symbol": "AAPL",
                    "trade_type": "buy",
                    "quantity": 50,
                    "price": 175.50,
                    "trade_date": datetime.utcnow() - timedelta(days=30)
                },
                {
                    "symbol": "MSFT",
                    "trade_type": "buy",
                    "quantity": 30,
                    "price": 380.25,
                    "trade_date": datetime.utcnow() - timedelta(days=28)
                },
                {
                    "symbol": "GOOGL",
                    "trade_type": "buy",
                    "quantity": 25,
                    "price": 142.30,
                    "trade_date": datetime.utcnow() - timedelta(days=25)
                },
                {
                    "symbol": "TSLA",
                    "trade_type": "buy",
                    "quantity": 20,
                    "price": 245.80,
                    "trade_date": datetime.utcnow() - timedelta(days=20)
                },
                {
                    "symbol": "NVDA",
                    "trade_type": "buy",
                    "quantity": 15,
                    "price": 495.60,
                    "trade_date": datetime.utcnow() - timedelta(days=15)
                },
                # Add a sell trade with profit
                {
                    "symbol": "AMZN",
                    "trade_type": "buy",
                    "quantity": 10,
                    "price": 145.00,
                    "trade_date": datetime.utcnow() - timedelta(days=45)
                },
                {
                    "symbol": "AMZN",
                    "trade_type": "sell",
                    "quantity": 10,
                    "price": 165.00,
                    "realized_pnl": 200.00,
                    "realized_pnl_pct": 13.79,
                    "trade_date": datetime.utcnow() - timedelta(days=10)
                }
            ]
            
            for trade_data in sample_trades:
                total_amount = trade_data["quantity"] * trade_data["price"]
                commission = 0  # Zero commission
                
                trade = Trade(
                    user_id=demo_user.id,
                    symbol=trade_data["symbol"],
                    trade_type=trade_data["trade_type"],
                    quantity=trade_data["quantity"],
                    price=trade_data["price"],
                    total_amount=total_amount,
                    commission=commission,
                    realized_pnl=trade_data.get("realized_pnl"),
                    realized_pnl_pct=trade_data.get("realized_pnl_pct"),
                    trade_date=trade_data["trade_date"],
                    notes=None
                )
                db.add(trade)
            
            await db.commit()
            print(f"✓ Created {len(sample_trades)} trades")
        
        print("\n✅ Dashboard seeding completed!")
        print(f"\nDemo credentials:")
        print(f"  Username: demo")
        print(f"  Password: demo123")


if __name__ == "__main__":
    print("=" * 60)
    print("Dashboard Data Seeder")
    print("=" * 60)
    print()
    
    asyncio.run(seed_dashboard_data())
