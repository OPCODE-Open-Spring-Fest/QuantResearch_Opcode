"""Stock quotes and market data endpoints."""

from __future__ import annotations

import logging
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..auth import get_current_user
from ..db import get_session
from ..models import User, StockQuote, CompanyProfile
from ..services.finnhub import FinnhubService
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/stocks", tags=["stocks"])


class QuoteResponse(BaseModel):
    symbol: str
    current_price: float
    change: float
    percent_change: float
    high: float
    low: float
    open: float
    previous_close: float
    volume: Optional[int]
    timestamp: str


class CompanyResponse(BaseModel):
    symbol: str
    name: str
    country: Optional[str]
    currency: Optional[str]
    exchange: Optional[str]
    industry: Optional[str]
    sector: Optional[str]
    market_cap: Optional[float]
    logo: Optional[str]
    weburl: Optional[str]


def get_finnhub_service() -> FinnhubService:
    """Dependency to get Finnhub service."""
    api_key = os.getenv("FINNHUB_API_KEY", "test_key")
    return FinnhubService(api_key)


@router.get("/quote/{symbol}", response_model=QuoteResponse)
async def get_quote(
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Get real-time quote for a symbol."""
    try:
        symbol = symbol.upper()
        
        # Update and get quote from cache
        quote = await finnhub_service.update_cached_quote(db, symbol)
        
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quote not found for {symbol}"
            )
        
        return {
            "symbol": quote.symbol,
            "current_price": round(quote.current_price, 2),
            "change": round(quote.change, 2),
            "percent_change": round(quote.percent_change, 2),
            "high": round(quote.high, 2),
            "low": round(quote.low, 2),
            "open": round(quote.open, 2),
            "previous_close": round(quote.previous_close, 2),
            "volume": quote.volume,
            "timestamp": quote.timestamp.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch quote: {str(e)}"
        )


@router.get("/quotes", response_model=List[QuoteResponse])
async def get_multiple_quotes(
    symbols: str = Query(..., description="Comma-separated list of symbols"),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Get quotes for multiple symbols."""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        
        # Update quotes in batch
        await finnhub_service.batch_update_quotes(db, symbol_list)
        
        # Fetch from database
        result = await db.execute(
            select(StockQuote).where(StockQuote.symbol.in_(symbol_list))
        )
        quotes = result.scalars().all()
        
        return [
            {
                "symbol": quote.symbol,
                "current_price": round(quote.current_price, 2),
                "change": round(quote.change, 2),
                "percent_change": round(quote.percent_change, 2),
                "high": round(quote.high, 2),
                "low": round(quote.low, 2),
                "open": round(quote.open, 2),
                "previous_close": round(quote.previous_close, 2),
                "volume": quote.volume,
                "timestamp": quote.timestamp.isoformat()
            }
            for quote in quotes
        ]
    except Exception as e:
        logger.error(f"Error fetching multiple quotes: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch quotes: {str(e)}"
        )


@router.get("/company/{symbol}", response_model=CompanyResponse)
async def get_company_profile(
    symbol: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Get company profile and information."""
    try:
        symbol = symbol.upper()
        
        # Update and get profile
        profile = await finnhub_service.update_company_profile(db, symbol)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company profile not found for {symbol}"
            )
        
        return {
            "symbol": profile.symbol,
            "name": profile.name,
            "country": profile.country,
            "currency": profile.currency,
            "exchange": profile.exchange,
            "industry": profile.industry,
            "sector": profile.sector,
            "market_cap": profile.market_cap,
            "logo": profile.logo,
            "weburl": profile.weburl
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching company profile for {symbol}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch company profile: {str(e)}"
        )


@router.get("/search")
async def search_stocks(
    query: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    finnhub_service: FinnhubService = Depends(get_finnhub_service)
):
    """Search for stocks by symbol or name."""
    try:
        # Use Finnhub search API
        results = await finnhub_service.search_symbols(query)
        
        return {
            "query": query,
            "results": results[:10]  # Limit to top 10 results
        }
    except Exception as e:
        logger.error(f"Error searching stocks: {e}", exc_info=True)
        # Return empty results on error rather than failing
        return {
            "query": query,
            "results": []
        }


@router.get("/trending")
async def get_trending_stocks(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get trending/popular stocks."""
    # Return a curated list of popular stocks
    popular_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "AMD"]
    
    try:
        result = await db.execute(
            select(StockQuote).where(StockQuote.symbol.in_(popular_symbols))
        )
        quotes = result.scalars().all()
        
        return [
            {
                "symbol": quote.symbol,
                "current_price": round(quote.current_price, 2),
                "change": round(quote.change, 2),
                "percent_change": round(quote.percent_change, 2),
                "volume": quote.volume
            }
            for quote in quotes
        ]
    except Exception as e:
        logger.error(f"Error fetching trending stocks: {e}", exc_info=True)
        return []
