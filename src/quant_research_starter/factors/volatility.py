"""Volatility factor implementations (vectorized)."""

import numpy as np
import pandas as pd

from .base import Factor


class VolatilityFactor(Factor):
    """Computes historical volatility (annualized)."""

    def __init__(self, lookback: int = 21, name: str = "volatility"):
        super().__init__(name=name, lookback=lookback)

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Compute historical volatility over lookback period."""
        self._validate_data(prices)

        returns = prices.pct_change()

        # Vectorized rolling std (annualized)
        vol = returns.rolling(window=self.lookback, min_periods=self.lookback).std() * np.sqrt(252)
        vol = vol.iloc[self.lookback - 1:]

        # Low-volatility anomaly (invert sign)
        scores = -vol * 10.0

        # Cross-sectional z-score
        if scores.shape[1] > 1:
            z = (scores - scores.mean(axis=1).values[:, None]) / scores.std(axis=1).values[:, None]
            result = pd.DataFrame(z, index=scores.index, columns=scores.columns)
        else:
            result = scores

        self._values = result
        return result


class IdiosyncraticVolatility(VolatilityFactor):
    """Vectorized idiosyncratic volatility relative to market model."""

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Compute idiosyncratic volatility using vectorized regression."""
        self._validate_data(prices)

        returns = prices.pct_change().dropna()
        market = returns.mean(axis=1)

        # Compute beta for each asset using vectorized covariance/variance
        cov_with_mkt = returns.mul(market, axis=0).rolling(window=self.lookback).mean() - (
            returns.rolling(window=self.lookback).mean().mul(market.rolling(window=self.lookback).mean(), axis=0)
        )
        market_var = market.rolling(window=self.lookback).var()
        beta = cov_with_mkt.div(market_var, axis=0)

        # Predicted returns via market model
        predicted = beta.mul(market, axis=0)
        residuals = returns - predicted

        # Rolling residual std (annualized)
        idio_vol = residuals.rolling(window=self.lookback, min_periods=self.lookback).std() * np.sqrt(252)
        idio_vol = idio_vol.iloc[self.lookback - 1:]

        # Invert sign (low-idio-vol performs better)
        scores = -idio_vol

        # Cross-sectional z-score normalization
        if scores.shape[1] > 1:
            z = (scores - scores.mean(axis=1).values[:, None]) / scores.std(axis=1).values[:, None]
            result = pd.DataFrame(z, index=scores.index, columns=scores.columns)
        else:
            result = scores

        self._values = result
        return result
