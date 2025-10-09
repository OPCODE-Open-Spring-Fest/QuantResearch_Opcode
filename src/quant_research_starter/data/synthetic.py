"""Synthetic financial data generator for testing and demos."""

import numpy as np
import pandas as pd


class SyntheticDataGenerator:
    """Generate synthetic price data for testing and demonstrations."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)

    def generate_price_data(
        self,
        n_symbols: int = 10,
        days: int = 1000,
        start_date: str = "2020-01-01",
        initial_price: float = 100.0,
        volatility: float = 0.02,
        drift: float = 0.0005,
        correlation: bool = True,
    ) -> pd.DataFrame:
        """
        Generate synthetic price data with optional correlation structure.

        Args:
            n_symbols: Number of symbols to generate
            days: Number of trading days
            start_date: Start date for the series
            initial_price: Starting price for all symbols
            volatility: Daily return volatility
            drift: Daily drift term
            correlation: Whether to add correlation structure

        Returns:
            DataFrame with synthetic price data
        """
        dates = pd.date_range(start=start_date, periods=days, freq="D")
        symbols = [f"SYMBOL_{i:02d}" for i in range(n_symbols)]

        if correlation:
            try:
                returns = self._generate_correlated_returns(
                    n_symbols, days, volatility, drift
                )
            except Exception:
                # Fallback to uncorrelated if correlation matrix is not PD
                returns = np.random.normal(drift, volatility, (days, n_symbols))
        else:
            returns = np.random.normal(drift, volatility, (days, n_symbols))

        # Convert returns to prices
        prices = initial_price * np.cumprod(1 + returns, axis=0)

        df = pd.DataFrame(prices, index=dates, columns=symbols)
        df.index.name = "date"

        return df

    def _generate_correlated_returns(
        self, n_symbols: int, days: int, volatility: float, drift: float
    ) -> np.ndarray:
        """Generate correlated returns using Cholesky decomposition."""
        # Create a reasonable correlation matrix
        base_corr = 0.3
        corr_matrix = np.full((n_symbols, n_symbols), base_corr)
        np.fill_diagonal(corr_matrix, 1.0)

        # Add some sector-like structure
        for i in range(0, n_symbols, 3):
            if i + 2 < n_symbols:
                corr_matrix[i : i + 3, i : i + 3] = 0.7

        # Ensure positive definiteness (add small jitter on diagonal)
        jitter = 1e-6
        corr_matrix_jittered = corr_matrix.copy()
        np.fill_diagonal(corr_matrix_jittered, 1.0 + jitter)

        # Generate correlated returns
        try:
            L = np.linalg.cholesky(corr_matrix_jittered)
        except np.linalg.LinAlgError:
            # As a final fallback, use identity (no correlation)
            L = np.eye(n_symbols)
        uncorrelated_returns = np.random.normal(drift, volatility, (days, n_symbols))
        correlated_returns = uncorrelated_returns @ L.T

        return correlated_returns
