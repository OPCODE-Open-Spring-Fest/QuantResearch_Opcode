"""Simple script to setup dashboard - creates tables and seeds data."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, text
from src.quant_research_starter.api.db import AsyncSessionLocal, engine, Base
from src.quant_research_starter.api.models import User, Position, Trade
from src.quant_research_starter.api.auth import get_password_hash


async def setup_dashboard():
    """Setup dashboard tables and sample data."""
    
    print("Step 1: Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created")
    
    # Show created tables
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            ORDER BY tablename
        """))
        tables = result.fetchall()
        print("\nDatabase tables:")
        for table in tables:
            print(f"  - {table[0]}")
    
    print("\nStep 2: Creating demo user and sample data...")
    async with AsyncSessionLocal() as db:
        # Check if demo user exists
        result = await db.execute(select(User).where(User.username == "demo"))
        demo_user = result.scalar_one_or_none()
        
        if not demo_user:
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
        
        # Create sample positions
        result = await db.execute(
            select(Position).where(Position.user_id == demo_user.id)
        )
        existing_positions = result.scalars().all()
        
        if not existing_positions:
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
                current_price = pos_data["average_cost"] * 1.12
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
        else:
            print(f"✓ {len(existing_positions)} positions already exist")
        
        # Create sample trades
        result = await db.execute(
            select(Trade).where(Trade.user_id == demo_user.id)
        )
        existing_trades = result.scalars().all()
        
        if not existing_trades:
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
                trade = Trade(
                    user_id=demo_user.id,
                    symbol=trade_data["symbol"],
                    trade_type=trade_data["trade_type"],
                    quantity=trade_data["quantity"],
                    price=trade_data["price"],
                    total_amount=trade_data["quantity"] * trade_data["price"],
                    commission=0,
                    realized_pnl=trade_data.get("realized_pnl"),
                    realized_pnl_pct=trade_data.get("realized_pnl_pct"),
                    trade_date=trade_data["trade_date"]
                )
                db.add(trade)
            
            await db.commit()
            print(f"✓ Created {len(sample_trades)} trades")
        else:
            print(f"✓ {len(existing_trades)} trades already exist")
    
    await engine.dispose()
    
    print("\n" + "=" * 60)
    print("✅ Dashboard setup completed successfully!")
    print("=" * 60)
    print(f"\n📊 Demo Login Credentials:")
    print(f"   Username: demo")
    print(f"   Password: demo123")
    print(f"\n🚀 Start the backend:")
    print(f"   cd src/quant_research_starter")
    print(f"   uvicorn api.main:app --reload --host 127.0.0.1 --port 8000")
    print(f"\n📡 Test Dashboard APIs:")
    print(f"   http://localhost:8000/docs")
    print(f"   http://localhost:8000/api/dashboard/overview")
    print(f"   http://localhost:8000/api/dashboard/positions")
    print(f"   http://localhost:8000/api/dashboard/trades")


if __name__ == "__main__":
    print("=" * 60)
    print("Dashboard Setup Script")
    print("=" * 60)
    print()
    
    asyncio.run(setup_dashboard())
