"""Benchmark script comparing vanilla vs Numba vs Cython implementations."""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from quant_research_starter.backtest.numba_opt import (
    NUMBA_AVAILABLE,
    compute_portfolio_value,
    compute_strategy_returns,
    compute_turnover,
    rank_based_weights,
)
from quant_research_starter.backtest.vectorized import VectorizedBacktest

try:
    from quant_research_starter.backtest.cython_opt import (
        compute_strategy_returns_cython,
        compute_turnover_cython,
    )

    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False


def generate_test_data(n_days: int, n_assets: int, seed: int = 42) -> tuple:
    """Generate synthetic test data."""
    np.random.seed(seed)
    dates = pd.date_range("2020-01-01", periods=n_days, freq="D")
    prices = pd.DataFrame(
        np.random.randn(n_days, n_assets).cumsum(axis=0) + 100,
        index=dates,
        columns=[f"ASSET_{i}" for i in range(n_assets)],
    )
    signals = pd.DataFrame(
        np.random.randn(n_days, n_assets),
        index=dates,
        columns=[f"ASSET_{i}" for i in range(n_assets)],
    )
    return prices, signals


def benchmark_vanilla(prices: pd.DataFrame, signals: pd.DataFrame) -> float:
    """Benchmark vanilla implementation."""
    start = time.perf_counter()
    backtest = VectorizedBacktest(
        prices=prices,
        signals=signals,
        initial_capital=1_000_000,
        transaction_cost=0.001,
    )
    results = backtest.run(weight_scheme="rank")
    elapsed = time.perf_counter() - start
    return elapsed, results


def benchmark_numba(prices: pd.DataFrame, signals: pd.DataFrame) -> float:
    """Benchmark Numba-accelerated implementation."""
    if not NUMBA_AVAILABLE:
        return None, None

    start = time.perf_counter()

    returns_df = prices.pct_change().dropna()
    aligned_signals = signals.loc[returns_df.index]

    returns_arr = returns_df.values
    n_days, n_assets = returns_arr.shape

    weights_list = []
    current_weights = np.zeros(n_assets, dtype=np.float64)
    for date in returns_df.index:
        signal_row = aligned_signals.loc[date].values.astype(np.float64)
        weights = compute_rank_weights_numba(signal_row, 1.0, 0.9, 0.1)
        current_weights = weights.copy()
        weights_list.append(current_weights)

    weights = np.array(weights_list, dtype=np.float64)
    weights_prev = np.vstack([np.zeros((1, n_assets), dtype=np.float64), weights[:-1]])

    turnover = compute_turnover(weights, weights_prev)
    strat_ret = compute_strategy_returns(
        weights_prev, returns_arr.astype(np.float64), turnover, 0.001
    )
    portfolio_value = compute_portfolio_value(strat_ret, 1_000_000.0)

    elapsed = time.perf_counter() - start
    results = {
        "portfolio_value": pd.Series(portfolio_value, index=returns_df.index),
        "returns": pd.Series(
            np.diff(portfolio_value) / portfolio_value[:-1], index=returns_df.index[1:]
        ),
    }
    return elapsed, results


def compute_rank_weights_numba(signals, max_leverage, long_pct, short_pct):
    """Helper to compute rank weights using Numba."""
    return rank_based_weights(signals, max_leverage, long_pct, short_pct)


def benchmark_cython(prices: pd.DataFrame, signals: pd.DataFrame) -> float:
    """Benchmark Cython-accelerated implementation."""
    if not CYTHON_AVAILABLE:
        return None, None

    start = time.perf_counter()

    returns_df = prices.pct_change().dropna()
    aligned_signals = signals.loc[returns_df.index]

    returns_arr = returns_df.values.astype(np.float64)
    n_days, n_assets = returns_arr.shape

    weights_list = []
    current_weights = np.zeros(n_assets, dtype=np.float64)
    for date in returns_df.index:
        signal_row = aligned_signals.loc[date].values.astype(np.float64)
        weights = compute_rank_weights_cython(signal_row, 1.0)
        current_weights = weights
        weights_list.append(current_weights)

    weights = np.array(weights_list, dtype=np.float64)
    weights_prev = np.vstack([np.zeros((1, n_assets), dtype=np.float64), weights[:-1]])

    turnover = compute_turnover_cython(weights, weights_prev)
    strat_ret = compute_strategy_returns_cython(
        weights_prev, returns_arr, turnover, 0.001
    )

    portfolio_value = compute_portfolio_value(strat_ret, 1_000_000)

    elapsed = time.perf_counter() - start
    results = {
        "portfolio_value": pd.Series(portfolio_value, index=returns_df.index),
        "returns": pd.Series(
            np.diff(portfolio_value) / portfolio_value[:-1], index=returns_df.index[1:]
        ),
    }
    return elapsed, results


def compute_rank_weights_cython(signals, max_leverage):
    """Helper to compute rank weights (simplified for Cython benchmark)."""
    valid_mask = ~np.isnan(signals)
    valid_signals = signals[valid_mask]
    if len(valid_signals) == 0:
        return np.zeros_like(signals)

    ranks = np.argsort(np.argsort(valid_signals)) + 1
    long_threshold = np.percentile(ranks, 90)
    short_threshold = np.percentile(ranks, 10)

    weights = np.zeros_like(signals)
    valid_idx = 0
    for i in range(len(signals)):
        if valid_mask[i]:
            if ranks[valid_idx] >= long_threshold:
                weights[i] = 1.0
            elif ranks[valid_idx] <= short_threshold:
                weights[i] = -1.0
            valid_idx += 1

    long_count = (weights > 0).sum()
    short_count = (weights < 0).sum()

    if long_count > 0:
        weights[weights > 0] = 1.0 / long_count
    if short_count > 0:
        weights[weights < 0] = -1.0 / short_count

    total_leverage = abs(weights).sum()
    if total_leverage > max_leverage:
        weights *= max_leverage / total_leverage

    return weights


def run_benchmarks():
    """Run benchmarks across different dataset sizes."""
    test_configs = [
        (252, 10, "Small"),
        (1000, 50, "Medium"),
        (2520, 100, "Large"),
    ]

    results = []

    print("=" * 80)
    print("Backtest Performance Benchmarks")
    print("=" * 80)
    print(f"Numba available: {NUMBA_AVAILABLE}")
    print(f"Cython available: {CYTHON_AVAILABLE}")
    print()

    for n_days, n_assets, label in test_configs:
        print(f"\n{label} dataset: {n_days} days, {n_assets} assets")
        print("-" * 80)

        prices, signals = generate_test_data(n_days, n_assets)

        vanilla_time, vanilla_results = benchmark_vanilla(prices, signals)
        print(f"Vanilla:     {vanilla_time:.4f}s")

        if NUMBA_AVAILABLE:
            numba_time, numba_results = benchmark_numba(prices, signals)
            if numba_time:
                speedup = vanilla_time / numba_time
                print(f"Numba:       {numba_time:.4f}s ({speedup:.2f}x speedup)")
                results.append(
                    {
                        "dataset": label,
                        "n_days": n_days,
                        "n_assets": n_assets,
                        "vanilla": vanilla_time,
                        "numba": numba_time,
                        "numba_speedup": speedup,
                    }
                )

        if CYTHON_AVAILABLE:
            cython_time, cython_results = benchmark_cython(prices, signals)
            if cython_time:
                speedup = vanilla_time / cython_time
                print(f"Cython:      {cython_time:.4f}s ({speedup:.2f}x speedup)")
                if results:
                    results[-1]["cython"] = cython_time
                    results[-1]["cython_speedup"] = speedup

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    for r in results:
        print(f"\n{r['dataset']} ({r['n_days']} days, {r['n_assets']} assets):")
        print(f"  Vanilla: {r['vanilla']:.4f}s")
        if "numba" in r:
            print(f"  Numba:   {r['numba']:.4f}s ({r['numba_speedup']:.2f}x)")
        if "cython" in r:
            print(f"  Cython:  {r['cython']:.4f}s ({r['cython_speedup']:.2f}x)")

    return results


if __name__ == "__main__":
    run_benchmarks()
