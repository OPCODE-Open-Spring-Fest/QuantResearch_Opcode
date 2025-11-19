"""Data downloaders for various financial data sources."""

import os
from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DataDownloader(ABC):
    """Abstract base class for data downloaders."""

    @abstractmethod
    def download(
        self, symbols: List[str], start_date: str, end_date: str, **kwargs
    ) -> pd.DataFrame:
        """Download price data for given symbols and date range."""
        pass


class YahooDownloader(DataDownloader):
    """Yahoo Finance data downloader."""

    def download(
        self, symbols: List[str], start_date: str, end_date: str, **kwargs
    ) -> pd.DataFrame:
        """
        Download data from Yahoo Finance.

        Note: This is a simplified implementation. In practice, you might use
        yfinance library or similar for more robust data fetching.
        """
        if not symbols:
            raise ValueError("symbols list cannot be empty")
        try:
            # Mock implementation for demo purposes
            # In real implementation, use yfinance or similar
            dates = pd.date_range(start=start_date, end=end_date, freq="D")
            data = {}

            for symbol in symbols:
                # Generate mock price data
                np.random.seed(hash(symbol) % 2**32)
                prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)
                data[symbol] = prices

            df = pd.DataFrame(data, index=dates)
            df.index.name = "date"
            return df

        except Exception as e:
            raise Exception(f"Failed to download data from Yahoo: {e}") from e


class AlphaVantageDownloader(DataDownloader):
    """Alpha Vantage data downloader."""

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    def download(
        self, symbols: List[str], start_date: str, end_date: str, **kwargs
    ) -> pd.DataFrame:
        """
        Download data from Alpha Vantage.

        Requires ALPHA_VANTAGE_API_KEY environment variable.
        """
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment")

        if not symbols:
            raise ValueError("symbols list cannot be empty")
        try:
            # Mock implementation - similar to Yahoo downloader
            dates = pd.date_range(start=start_date, end=end_date, freq="D")
            data = {}

            for symbol in symbols:
                np.random.seed(hash(symbol) % 2**32)
                prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.3)
                data[symbol] = prices

            df = pd.DataFrame(data, index=dates)
            df.index.name = "date"
            return df

        except Exception as e:
            raise Exception(f"Failed to download data from Alpha Vantage: {e}") from e
