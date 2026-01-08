"""Create dashboard tables migration."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from src.quant_research_starter.api.db import engine, Base
from src.quant_research_starter.api.models import (
    User, BacktestJob, Portfolio, Position, Trade, StockQuote, CompanyProfile
)


async def create_tables():
    """Create all database tables."""
    print("Creating dashboard tables...")
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Dashboard tables created successfully!")
    
    # Show tables
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
    
    await engine.dispose()


if __name__ == "__main__":
    print("=" * 60)
    print("Dashboard Tables Creation")
    print("=" * 60)
    print()
    
    asyncio.run(create_tables())
