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
        # Use mock data if API key is test_key or empty
        if self.api_key in ("test_key", "", None):
            return self._get_mock_quote(symbol)
        
        try:
            url = f"{self.BASE_URL}/quote"
            params = {"symbol": symbol, "token": self.api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Validate response has data
            if data.get("c") == 0:
                logger.warning(f"No quote data for {symbol}, using mock")
                return self._get_mock_quote(symbol)
            
            return data
        except httpx.HTTPError as e:
            logger.error(f"Finnhub API error for {symbol}: {e}, using mock")
            return self._get_mock_quote(symbol)
        except Exception as e:
            logger.error(f"Unexpected error fetching quote for {symbol}: {e}, using mock")
            return self._get_mock_quote(symbol)
    
    def _get_mock_quote(self, symbol: str) -> dict:
        """Generate mock quote data for testing."""
        import random
        
        # Base prices for common symbols
        base_prices = {
            "AAPL": 178.50,
            "MSFT": 405.30,
            "GOOGL": 142.80,
            "AMZN": 175.20,
            "TSLA": 238.40,
            "META": 520.60,
            "NVDA": 875.30,
            "AMD": 195.80,
        }
        
        base_price = base_prices.get(symbol, 100.00)
        
        # Add some randomness
        variation = random.uniform(-0.05, 0.05)
        current = round(base_price * (1 + variation), 2)
        prev_close = round(base_price, 2)
        change = round(current - prev_close, 2)
        percent_change = round((change / prev_close) * 100, 2)
        
        return {
            "c": current,
            "h": round(current * 1.02, 2),
            "l": round(current * 0.98, 2),
            "o": round(prev_close * 1.001, 2),
            "pc": prev_close,
            "d": change,
            "dp": percent_change
        }
    
    async def get_company_profile(self, symbol: str) -> Optional[dict]:
        """
        Fetch company profile information.
        
        Returns dict with: name, country, currency, exchange, ipo, 
        marketCapitalization, phone, shareOutstanding, ticker, weburl, 
        logo, finnhubIndustry
        """
        # Use mock data if API key is test_key or empty
        if self.api_key in ("test_key", "", None):
            return self._get_mock_profile(symbol)
        
        try:
            url = f"{self.BASE_URL}/stock/profile2"
            params = {"symbol": symbol, "token": self.api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check if valid response
            if not data or not data.get("name"):
                logger.warning(f"No profile data for {symbol}, using mock")
                return self._get_mock_profile(symbol)
            
            return data
        except httpx.HTTPError as e:
            logger.error(f"Finnhub API error for profile {symbol}: {e}, using mock")
            return self._get_mock_profile(symbol)
        except Exception as e:
            logger.error(f"Unexpected error fetching profile for {symbol}: {e}, using mock")
            return self._get_mock_profile(symbol)
    
    def _get_mock_profile(self, symbol: str) -> dict:
        """Generate mock company profile data for testing."""
        companies = {
            "AAPL": {
                "name": "Apple Inc.",
                "country": "US",
                "currency": "USD",
                "exchange": "NASDAQ",
                "finnhubIndustry": "Technology",
                "ipo": "1980-12-12",
                "marketCapitalization": 2800000,
                "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AAPL.png",
                "weburl": "https://www.apple.com/"
            },
            "MSFT": {
                "name": "Microsoft Corporation",
                "country": "US",
                "currency": "USD",
                "exchange": "NASDAQ",
                "finnhubIndustry": "Technology",
                "marketCapitalization": 3000000,
                "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/MSFT.svg",
                "weburl": "https://www.microsoft.com/"
            },
            "GOOGL": {
                "name": "Alphabet Inc.",
                "country": "US",
                "currency": "USD",
                "exchange": "NASDAQ",
                "finnhubIndustry": "Technology",
                "marketCapitalization": 1800000,
                "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/GOOGL.png",
                "weburl": "https://www.google.com/"
            },
        }
        
        # Return company data if available, otherwise generic
        return companies.get(symbol, {
            "name": f"{symbol} Corporation",
            "country": "US",
            "currency": "USD",
            "exchange": "NYSE",
            "finnhubIndustry": "Technology",
            "marketCapitalization": 50000,
            "weburl": f"https://www.{symbol.lower()}.com/"
        })
    
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
    
    async def search_symbols(self, query: str) -> list[dict]:
        """
        Search for stock symbols.
        
        Args:
            query: Search query
        
        Returns:
            List of symbol results
        """
        # Use mock data if test_key
        if self.api_key in ("test_key", "", None):
            return self._mock_search(query)
        
        try:
            url = f"{self.BASE_URL}/search"
            params = {"q": query, "token": self.api_key}
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get("result", [])
        except Exception as e:
            logger.error(f"Error searching symbols: {e}")
            return self._mock_search(query)
    
    def _mock_search(self, query: str) -> list[dict]:
        """Mock symbol search for testing."""
        symbols = [
            {"description": "Apple Inc.", "displaySymbol": "AAPL", "symbol": "AAPL", "type": "Common Stock"},
            {"description": "Microsoft Corporation", "displaySymbol": "MSFT", "symbol": "MSFT", "type": "Common Stock"},
            {"description": "Alphabet Inc.", "displaySymbol": "GOOGL", "symbol": "GOOGL", "type": "Common Stock"},
            {"description": "Amazon.com Inc.", "displaySymbol": "AMZN", "symbol": "AMZN", "type": "Common Stock"},
            {"description": "Tesla Inc.", "displaySymbol": "TSLA", "symbol": "TSLA", "type": "Common Stock"},
            {"description": "Meta Platforms Inc.", "displaySymbol": "META", "symbol": "META", "type": "Common Stock"},
            {"description": "NVIDIA Corporation", "displaySymbol": "NVDA", "symbol": "NVDA", "type": "Common Stock"},
            {"description": "Advanced Micro Devices Inc.", "displaySymbol": "AMD", "symbol": "AMD", "type": "Common Stock"},
        ]
        
        # Filter by query
        query_lower = query.lower()
        return [
            s for s in symbols
            if query_lower in s["symbol"].lower() or query_lower in s["description"].lower()
        ]
