"""Base factor class and utilities."""

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class Factor(ABC):
    """Abstract base class for factors."""

    def __init__(self, name: str, lookback: int = 21):
        self.name = name
        self.lookback = lookback
        self._values: Optional[pd.DataFrame] = None

    @abstractmethod
    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Compute factor values from price data."""
        pass

    def get_values(self) -> pd.DataFrame:
        """Get computed factor values."""
        if self._values is None:
            raise ValueError("Factor values not computed yet. Call compute() first.")
        return self._values

    def _validate_data(self, prices: pd.DataFrame) -> None:
        """Validate input price data."""
        if prices.empty:
            raise ValueError("Price dataframe is empty")
        if len(prices) < self.lookback:
            raise ValueError(f"Need at least {self.lookback} periods of data")
