"""
Benchmark script to compare performance of factor computations.

Usage:
    python examples/benchmarks/benchmark_factors.py
"""

import time

import numpy as np
import pandas as pd

from quant_research_starter.factors import (
    BollingerBandsFactor,
    IdiosyncraticVolatility,
    MomentumFactor,
    SizeFactor,
    ValueFactor,
    VolatilityFactor,
)


def generate_synthetic_prices(
    n_assets: int = 500, n_days: int = 252 * 3
) -> pd.DataFrame:
    """Generate synthetic random walk price data for testing."""
    np.random.seed(42)
    returns = np.random.normal(0, 0.01, size=(n_days, n_assets))
    prices = 100 * np.exp(np.cumsum(returns, axis=0))
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq="B")
    tickers = [f"Stock_{i:03d}" for i in range(n_assets)]
    return pd.DataFrame(prices, index=dates, columns=tickers)


def benchmark_factor(factor, prices: pd.DataFrame):
    """Benchmark runtime of a given factor."""
    start = time.time()
    _ = factor.compute(prices)
    end = time.time()
    elapsed = end - start
    print(
        f"{factor.name:<25} | Lookback: {factor.lookback:<5} | Time: {elapsed:.3f} sec"
    )


def main():
    print("Generating synthetic data...")
    prices = generate_synthetic_prices(n_assets=500, n_days=252 * 3)
    print(f"Data shape: {prices.shape}")

    print("\nRunning factor benchmarks...\n")

    factors = [
        MomentumFactor(lookback=63),
        ValueFactor(),
        SizeFactor(),
        VolatilityFactor(lookback=21),
        IdiosyncraticVolatility(lookback=63),
        BollingerBandsFactor(lookback=20),
    ]

    for factor in factors:
        benchmark_factor(factor, prices)


if __name__ == "__main__":
    main()
