"""
Volatility factor implementations (vectorized, production-ready).

This file contains:
- VolatilityFactor: historical (realized) volatility (annualized) with
  cross-sectional z-score output.
- IdiosyncraticVolatility: volatility of residuals vs an equal-weighted
  market proxy, computed using vectorized operations.

Key improvements included:
- Proper `__init__` usage.
- Min_periods set on rolling operations; trimming of initial rows to avoid
  ambiguous partial-window values.
- Guarding divide-by-zero when computing beta (market variance).
- Consistent handling for single-column (single-asset) DataFrames.
- Preserves DataFrame output shape/columns and sets self._values.
- Uses ddof=0 for rolling std/var to match population estimates (consistent &
  fast).
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Try to import package Factor base; fallback to a minimal stub if unavailable.
try:
    # Adjust this import if your project stores Factor in a different module.
    from .base import Factor  # type: ignore
except Exception:
    try:
        from quant_research_starter.factors.base import Factor  # type: ignore
    except Exception:
        # Minimal Factor stub so this module can be inspected/tested in isolation.
        class Factor:
            def __init__(
                self, name: Optional[str] = None, lookback: Optional[int] = None
            ):
                self.name = name or "factor"
                self.lookback = lookback or 0
                self._values: Optional[pd.DataFrame] = None

            def _validate_data(self, prices: pd.DataFrame) -> None:
                if not isinstance(prices, pd.DataFrame):
                    raise TypeError("prices must be a pandas DataFrame")

            def __repr__(self) -> str:
                return f"<Factor name={self.name} lookback={self.lookback}>"


# Constants
TRADING_DAYS = 252


class VolatilityFactor(Factor):
    """Computes historical (realized) volatility (annualized) and returns cross-sectional
    z-scores. Low-volatility signals are produced by inverting volatility (i.e. low vol -> high score).

    Parameters
    ----------
    lookback : int
        Rolling lookback window (in trading days). Default is 21.
    name : str
        Human-readable name for the factor.
    """

    def __init__(self, lookback: int = 21, name: str = "volatility"):
        # Call base init if available; also keep explicit attributes for safety.
        try:
            super().__init__(name=name, lookback=lookback)  # type: ignore
        except Exception:
            # Base class might have a different signature; set manually.
            self.name = name
            self.lookback = lookback
            self._values = None

        # Ensure sensible types/values
        if not isinstance(lookback, int) or lookback <= 0:
            raise ValueError("lookback must be a positive integer")
        self.lookback = lookback
        self.name = name

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        Compute annualized historical volatility and return z-scored signals.

        Returns
        -------
        pd.DataFrame
            DataFrame of the same columns (assets) with index trimmed so that the
            first row corresponds to the first full lookback window.
        """
        self._validate_data(prices)

        if prices.shape[0] < self.lookback:
            raise ValueError(
                f"Need at least {self.lookback} rows of data to compute volatility"
            )

        # pct change -> returns
        returns = prices.pct_change()

        # rolling std (population, ddof=0) and annualize
        vol = returns.rolling(window=self.lookback, min_periods=self.lookback).std(
            ddof=0
        ) * np.sqrt(TRADING_DAYS)

        # Trim initial rows that don't correspond to a full window
        if self.lookback > 1:
            vol = vol.iloc[self.lookback - 1 :]

        # Invert sign for low-volatility preference and scale for numeric stability
        scores = -vol * 10.0

        # Ensure DataFrame (even for single-column)
        if isinstance(scores, pd.Series):
            scores = scores.to_frame(name=prices.columns[0])

        # Cross-sectional z-score: (v - mean_row) / std_row
        if scores.shape[1] > 1:
            row_mean = scores.mean(axis=1)
            row_std = scores.std(axis=1).replace(0, np.nan)  # avoid divide-by-zero
            # subtract mean and divide -- use broadcasting via .values for speed
            z = (scores.sub(row_mean, axis=0)).div(row_std, axis=0)
            result = pd.DataFrame(z, index=scores.index, columns=scores.columns)
        else:
            # Single asset -> keep the scores DataFrame (no cross-sectional normalization)
            result = scores.copy()

        # Store and return
        self._values = result
        return result


class IdiosyncraticVolatility(VolatilityFactor):
    """Compute idiosyncratic volatility relative to an equal-weighted market proxy.
    Implements a vectorized market-model approach:
        - compute rolling cov(ri, rm) and var(rm)
        - beta = cov / var
        - residuals = ri - beta * rm
        - idio_vol = rolling std(residuals) (annualized)
    Returns negative idio_vol (so low idio-vol -> high score) and z-scores cross-sectionally.
    """

    def __init__(self, lookback: int = 63, name: str = "idiosyncratic_volatility"):
        super().__init__(lookback=lookback, name=name)

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        self._validate_data(prices)

        # require enough rows to compute returns and rolling windows
        if prices.shape[0] < self.lookback + 1:
            raise ValueError(
                f"Need at least {self.lookback + 1} rows of data to compute idiosyncratic volatility"
            )

        # daily returns
        returns = prices.pct_change().dropna()
        if returns.shape[0] < self.lookback:
            raise ValueError(
                f"Need at least {self.lookback} non-NA return rows to compute idio-vol"
            )

        # Market proxy: equal-weighted mean across assets
        market = returns.mean(axis=1)

        # Rolling means for covariance decomposition
        returns_mean = returns.rolling(
            window=self.lookback, min_periods=self.lookback
        ).mean()
        market_mean = market.rolling(
            window=self.lookback, min_periods=self.lookback
        ).mean()

        # Compute cov(ri, rm) via E[ri*rm] - E[ri]*E[rm]
        e_ri_rm = (
            returns.mul(market, axis=0)
            .rolling(window=self.lookback, min_periods=self.lookback)
            .mean()
        )
        cov_with_mkt = e_ri_rm - returns_mean.mul(market_mean, axis=0)

        # market variance (vector) -- guard zeros
        market_var = (
            market.rolling(window=self.lookback, min_periods=self.lookback)
            .var(ddof=0)
            .replace(0, np.nan)
        )

        # Beta: cov / var  (division broadcasted over columns)
        beta = cov_with_mkt.div(market_var, axis=0)

        # Predicted returns: beta * market (broadcasted)
        predicted = beta.mul(market, axis=0)

        # Residuals (vectorized)
        residuals = returns - predicted

        # Rolling std of residuals (annualized)
        idio_vol = residuals.rolling(
            window=self.lookback, min_periods=self.lookback
        ).std(ddof=0) * np.sqrt(TRADING_DAYS)

        # Trim to first full-window row
        if self.lookback > 1:
            idio_vol = idio_vol.iloc[self.lookback - 1 :]

        # Negative idiosyncratic vol => prefer low idio-vol
        scores = -idio_vol

        # Ensure DataFrame shape (in case of single-column)
        if isinstance(scores, pd.Series):
            scores = scores.to_frame(name=prices.columns[0])

        # Cross-sectional z-score normalization if > 1 asset
        if scores.shape[1] > 1:
            row_mean = scores.mean(axis=1)
            row_std = scores.std(axis=1).replace(0, np.nan)
            z = (scores.sub(row_mean, axis=0)).div(row_std, axis=0)
            result = pd.DataFrame(z, index=scores.index, columns=scores.columns)
        else:
            result = scores.copy()

        # Save and return
        self._values = result
        return result
