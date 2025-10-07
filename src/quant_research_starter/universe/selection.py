"""Universe selection utilities."""

from typing import Callable, Optional, Set

import pandas as pd


class UniverseSelector:
    """Base class for universe selection rules."""

    def __init__(self, name: str):
        self.name = name

    def select(self, data: pd.DataFrame, date: pd.Timestamp) -> Set[str]:
        """Select universe members for a given date."""
        raise NotImplementedError


class TopNSelector(UniverseSelector):
    """Select top N assets by some criteria."""

    def __init__(
        self, n: int = 50, sort_by: Optional[Callable] = None, name: str = "top_n"
    ):
        super().__init__(name=name)
        self.n = n
        self.sort_by = sort_by or (lambda x: x)

    def select(self, data: pd.DataFrame, date: pd.Timestamp) -> Set[str]:
        """Select top N assets on given date."""
        if date not in data.index:
            # Find nearest available date
            available_dates = data.index[data.index <= date]
            if len(available_dates) == 0:
                return set()
            date = available_dates[-1]

        day_data = data.loc[date]
        valid_data = day_data.dropna()

        if len(valid_data) == 0:
            return set()

        # Sort and select top N
        sorted_assets = valid_data.sort_values(ascending=False)
        selected = sorted_assets.head(self.n)

        return set(selected.index)


class LiquidityFilter(UniverseSelector):
    """Filter assets based on liquidity (trading volume or price)."""

    def __init__(
        self,
        min_price: float = 5.0,
        min_volume: Optional[float] = None,
        name: str = "liquidity_filter",
    ):
        super().__init__(name=name)
        self.min_price = min_price
        self.min_volume = min_volume

    def select(
        self, prices: pd.DataFrame, volumes: pd.DataFrame, date: pd.Timestamp
    ) -> Set[str]:
        """Select liquid assets based on price and volume filters."""
        if date not in prices.index:
            available_dates = prices.index[prices.index <= date]
            if len(available_dates) == 0:
                return set()
            date = available_dates[-1]

        day_prices = prices.loc[date]
        price_ok = day_prices >= self.min_price

        if self.min_volume is not None and volumes is not None:
            day_volumes = volumes.loc[date]
            volume_ok = day_volumes >= self.min_volume
            liquid_assets = price_ok & volume_ok
        else:
            liquid_assets = price_ok

        return set(liquid_assets[liquid_assets].index)
