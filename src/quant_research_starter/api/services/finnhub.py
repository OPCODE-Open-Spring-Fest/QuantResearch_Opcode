"""Finnhub API service for live market data."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import StockQuote, CompanyProfile

logger = logging.getLogger(__name__)


class FinnhubService:
    """Service for fetching live market data from Finnhub API."""
    
    BASE_URL = "https://finnhub.io/api/v1"
    CACHE_DURATION_SECONDS = 60  # Cache quotes for 1 minute
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
    
    async def get_quote(self, symbol: str) -> Optional[dict]:
        """
        Fetch real-time quote for a symbol.
        
        Returns dict with: c (current), h (high), l (low), o (open), 
        pc (previous close), d (change), dp (percent change)
        """
        try:
            url = f"{self.BASE_URL}/quote"
            params = {"symbol": symbol, "token": self.api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Validate response has data
            if data.get("c") == 0:
                logger.warning(f"No quote data for {symbol}")
                return None
            
            return data
        except httpx.HTTPError as e:
            logger.error(f"Finnhub API error for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching quote for {symbol}: {e}")
            return None
    
    async def get_company_profile(self, symbol: str) -> Optional[dict]:
        """
        Fetch company profile information.
        
        Returns dict with: name, country, currency, exchange, ipo, 
        marketCapitalization, phone, shareOutstanding, ticker, weburl, 
        logo, finnhubIndustry
        """
        try:
            url = f"{self.BASE_URL}/stock/profile2"
            params = {"symbol": symbol, "token": self.api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check if valid response
            if not data or not data.get("name"):
                logger.warning(f"No profile data for {symbol}")
                return None
            
            return data
        except httpx.HTTPError as e:
            logger.error(f"Finnhub API error for profile {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching profile for {symbol}: {e}")
            return None
    
    async def update_cached_quote(
        self, 
        db: AsyncSession, 
        symbol: str,
        force: bool = False
    ) -> Optional[StockQuote]:
        """
        Update cached quote in database.
        
        Args:
            db: Database session
            symbol: Stock symbol
            force: Force update even if cache is fresh
        
        Returns:
            Updated StockQuote or None
        """
        # Check cache first
        if not force:
            result = await db.execute(
                select(StockQuote).where(StockQuote.symbol == symbol)
            )
            cached = result.scalar_one_or_none()
            
            if cached:
                age = datetime.utcnow() - cached.updated_at
                if age.total_seconds() < self.CACHE_DURATION_SECONDS:
                    logger.debug(f"Using cached quote for {symbol}")
                    return cached
        
        # Fetch fresh data
        quote_data = await self.get_quote(symbol)
        if not quote_data:
            return None
        
        # Update or create
        result = await db.execute(
            select(StockQuote).where(StockQuote.symbol == symbol)
        )
        stock_quote = result.scalar_one_or_none()
        
        if stock_quote:
            stock_quote.current_price = quote_data["c"]
            stock_quote.change = quote_data["d"]
            stock_quote.percent_change = quote_data["dp"]
            stock_quote.high = quote_data["h"]
            stock_quote.low = quote_data["l"]
            stock_quote.open = quote_data["o"]
            stock_quote.previous_close = quote_data["pc"]
            stock_quote.updated_at = datetime.utcnow()
        else:
            stock_quote = StockQuote(
                symbol=symbol,
                current_price=quote_data["c"],
                change=quote_data["d"],
                percent_change=quote_data["dp"],
                high=quote_data["h"],
                low=quote_data["l"],
                open=quote_data["o"],
                previous_close=quote_data["pc"]
            )
            db.add(stock_quote)
        
        await db.commit()
        await db.refresh(stock_quote)
        
        logger.info(f"Updated quote for {symbol}: ${quote_data['c']}")
        return stock_quote
    
    async def update_company_profile(
        self, 
        db: AsyncSession, 
        symbol: str
    ) -> Optional[CompanyProfile]:
        """
        Update company profile in database.
        
        Args:
            db: Database session
            symbol: Stock symbol
        
        Returns:
            Updated CompanyProfile or None
        """
        # Check if already exists and is recent (cache for 24 hours)
        result = await db.execute(
            select(CompanyProfile).where(CompanyProfile.symbol == symbol)
        )
        profile = result.scalar_one_or_none()
        
        if profile:
            age = datetime.utcnow() - profile.updated_at
            if age < timedelta(hours=24):
                logger.debug(f"Using cached profile for {symbol}")
                return profile
        
        # Fetch fresh data
        profile_data = await self.get_company_profile(symbol)
        if not profile_data:
            return None
        
        if profile:
            # Update existing
            profile.name = profile_data.get("name", "")
            profile.country = profile_data.get("country")
            profile.currency = profile_data.get("currency")
            profile.exchange = profile_data.get("exchange")
            profile.industry = profile_data.get("finnhubIndustry")
            profile.market_cap = profile_data.get("marketCapitalization")
            profile.logo = profile_data.get("logo")
            profile.phone = profile_data.get("phone")
            profile.weburl = profile_data.get("weburl")
            profile.finnhub_industry = profile_data.get("finnhubIndustry")
            
            # Parse IPO date
            ipo_str = profile_data.get("ipo")
            if ipo_str:
                try:
                    profile.ipo = datetime.strptime(ipo_str, "%Y-%m-%d").date()
                except:
                    pass
            
            profile.updated_at = datetime.utcnow()
        else:
            # Create new
            ipo_date = None
            ipo_str = profile_data.get("ipo")
            if ipo_str:
                try:
                    ipo_date = datetime.strptime(ipo_str, "%Y-%m-%d").date()
                except:
                    pass
            
            profile = CompanyProfile(
                symbol=symbol,
                name=profile_data.get("name", ""),
                country=profile_data.get("country"),
                currency=profile_data.get("currency"),
                exchange=profile_data.get("exchange"),
                industry=profile_data.get("finnhubIndustry"),
                market_cap=profile_data.get("marketCapitalization"),
                ipo=ipo_date,
                logo=profile_data.get("logo"),
                phone=profile_data.get("phone"),
                weburl=profile_data.get("weburl"),
                finnhub_industry=profile_data.get("finnhubIndustry")
            )
            db.add(profile)
        
        await db.commit()
        await db.refresh(profile)
        
        logger.info(f"Updated profile for {symbol}: {profile.name}")
        return profile
    
    async def batch_update_quotes(
        self, 
        db: AsyncSession, 
        symbols: list[str]
    ) -> dict[str, Optional[StockQuote]]:
        """
        Update multiple quotes efficiently with rate limiting.
        
        Args:
            db: Database session
            symbols: List of stock symbols
        
        Returns:
            Dict mapping symbol to StockQuote
        """
        results = {}
        
        for symbol in symbols:
            quote = await self.update_cached_quote(db, symbol)
            results[symbol] = quote
            
            # Rate limiting: 30 API calls/second max
            await asyncio.sleep(0.04)
        
        return results
