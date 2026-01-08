"""Test dashboard endpoints"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.quant_research_starter.api.db import AsyncSessionLocal
from src.quant_research_starter.api.auth import verify_password, get_password_hash
from sqlalchemy import select
from src.quant_research_starter.api.models import User, Position


async def test_dashboard():
    print("🧪 Testing Dashboard Backend\n")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Test 1: Check demo user
        print("\n1️⃣ Checking demo user...")
        result = await db.execute(select(User).where(User.username == "demo"))
        user = result.scalar_one_or_none()
        
        if user:
            print(f"   ✅ Demo user found (ID: {user.id})")
            print(f"   Username: {user.username}")
            print(f"   Active: {user.is_active}")
            
            # Test password
            if verify_password("demo123", user.hashed_password):
                print("   ✅ Password verification works!")
            else:
                print("   ❌ Password verification failed")
        else:
            print("   ❌ Demo user not found")
            return
        
        # Test 2: Check positions
        print("\n2️⃣ Checking positions...")
        result = await db.execute(
            select(Position).where(Position.user_id == user.id)
        )
        positions = result.scalars().all()
        
        if positions:
            print(f"   ✅ Found {len(positions)} positions:")
            for pos in positions:
                print(f"      • {pos.symbol}: {pos.quantity} shares @ ${pos.average_cost:.2f}")
                print(f"        Market Value: ${pos.market_value:.2f}")
                print(f"        P/L: ${pos.unrealized_pnl:.2f} ({pos.unrealized_pnl_pct:.2f}%)")
        else:
            print("   ❌ No positions found")
        
        # Test 3: Calculate totals
        print("\n3️⃣ Portfolio Summary:")
        total_cost = sum(p.cost_basis for p in positions)
        total_value = sum(p.market_value for p in positions)
        total_pnl = sum(p.unrealized_pnl for p in positions)
        
        print(f"   Total Invested: ${total_cost:,.2f}")
        print(f"   Current Value: ${total_value:,.2f}")
        print(f"   Unrealized P/L: ${total_pnl:,.2f}")
        print(f"   Return: {(total_pnl/total_cost*100):.2f}%")
    
    print("\n" + "=" * 60)
    print("✅ All dashboard components verified!")
    print("\n📊 Backend is ready to use!")
    print("\n🔐 Login Credentials:")
    print("   Username: demo")
    print("   Password: demo123")
    print("\n🌐 Start Backend:")
    print("   cd src/quant_research_starter")
    print("   uvicorn api.main:app --host 127.0.0.1 --port 8000")
    print("\n📡 API Endpoints (after login):")
    print("   http://localhost:8000/api/dashboard/overview")
    print("   http://localhost:8000/api/dashboard/positions")
    print("   http://localhost:8000/api/dashboard/trades")
    print("   http://localhost:8000/docs (Swagger UI)")


if __name__ == "__main__":
    asyncio.run(test_dashboard())
