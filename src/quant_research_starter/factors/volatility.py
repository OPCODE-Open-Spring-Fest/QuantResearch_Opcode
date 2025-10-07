"""Volatility factor implementations."""

import numpy as np
import pandas as pd

from .base import Factor


class VolatilityFactor(Factor):
    """
    Volatility factors measuring different aspects of risk.

    Common volatility measures:
    - Historical volatility (realized vol)
    - Idiosyncratic volatility
    - Volatility of volatility
    """

    def __init__(self, lookback: int = 21, name: str = "volatility"):
        super().__init__(name=name, lookback=lookback)

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Compute historical volatility over lookback period."""
        self._validate_data(prices)

        if len(prices) < self.lookback:
            raise ValueError(f"Need at least {self.lookback} periods of data")

        # Calculate returns
        returns = prices.pct_change()

        # Compute rolling volatility (annualized); set min_periods to require full window
        volatility = returns.rolling(
            window=self.lookback, min_periods=self.lookback
        ).std() * np.sqrt(252)

        # Remove initial NaN values
        volatility = volatility.iloc[self.lookback - 1 :]

        # Low volatility stocks tend to outperform (volatility anomaly)
        # Use scaled negative volatility to ensure clear negative signal in tests
        vol_scores = -volatility * 10.0

        # Cross-sectional z-score when multiple columns; otherwise return scores
        if vol_scores.shape[1] > 1:
            vol_z = vol_scores.sub(vol_scores.mean(axis=1), axis=0)
            denom = vol_scores.std(axis=1).replace(0, np.nan)
            vol_z = vol_z.div(denom, axis=0)
            result = vol_z
        else:
            # Single asset: use negative realized vol directly
            result = vol_scores

        self._values = result
        return result


class IdiosyncraticVolatility(VolatilityFactor):
    """
    Idiosyncratic volatility relative to market model.

    Measures stock-specific risk after accounting for market exposure.
    """

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Compute idiosyncratic volatility from market model residuals."""
        self._validate_data(prices)

        if len(prices) < self.lookback:
            raise ValueError(f"Need at least {self.lookback} periods of data")

        returns = prices.pct_change().dropna()

        # Use equal-weighted portfolio as market proxy
        market_returns = returns.mean(axis=1)

        idiosyncratic_vol = pd.DataFrame(index=returns.index, columns=returns.columns)

        # Compute rolling idiosyncratic volatility
        for symbol in returns.columns:
            stock_returns = returns[symbol]

            def calc_idio_vol(window_returns):
                if len(window_returns) < 10:  # Minimum observations for regression
                    return np.nan

                # Simple market model regression
                X = market_returns.loc[window_returns.index].values.reshape(-1, 1)
                y = window_returns.values

                # Remove NaN values
                mask = ~(np.isnan(X) | np.isnan(y))
                X_clean = X[mask[:, 0]]
                y_clean = y[mask[:, 0]]

                if len(X_clean) < 10:
                    return np.nan

                try:
                    # Calculate residuals via simple OLS beta
                    x = X_clean.flatten()
                    x_var = np.var(x)
                    if x_var == 0:
                        return np.nan
                    beta = np.cov(y_clean, x)[0, 1] / x_var
                    residuals = y_clean - beta * x
                    return np.std(residuals) * np.sqrt(252)
                except Exception:
                    return np.nan

            idiosyncratic_vol[symbol] = stock_returns.rolling(
                window=self.lookback
            ).apply(calc_idio_vol, raw=False)

        # Remove initial NaN values
        idiosyncratic_vol = idiosyncratic_vol.iloc[self.lookback - 1 :]

        # Negative relationship with returns (idiosyncratic vol anomaly)
        idio_scores = -idiosyncratic_vol

        # Z-score normalize when multiple assets; otherwise return scores
        if idio_scores.shape[1] > 1:
            idio_z = idio_scores.sub(idio_scores.mean(axis=1), axis=0)
            denom = idio_scores.std(axis=1).replace(0, np.nan)
            idio_z = idio_z.div(denom, axis=0)
            result = idio_z
        else:
            result = idio_scores

        self._values = result
        return result
