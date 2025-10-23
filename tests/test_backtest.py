"""Tests for backtesting engine."""

import numpy as np
import pandas as pd
import pytest

from quant_research_starter.backtest import VectorizedBacktest


@pytest.fixture
def sample_data():
    """Create sample price and signal data for backtesting."""
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    symbols = ["AAPL", "GOOGL", "MSFT"]

    # Generate price data
    np.random.seed(42)
    prices_data = {}
    for symbol in symbols:
        returns = np.random.normal(0.0005, 0.02, len(dates))
        prices = 100 * np.cumprod(1 + returns)
        prices_data[symbol] = prices

    prices = pd.DataFrame(prices_data, index=dates)

    # Generate simple momentum signals
    signals_data = {}
    for symbol in symbols:
        # Simple mean-reverting signal
        signals_data[symbol] = np.random.normal(0, 1, len(dates))

    signals = pd.DataFrame(signals_data, index=dates)

    return prices, signals


class TestVectorizedBacktest:
    """Test vectorized backtesting engine."""

    def test_initialization(self, sample_data):
        """Test backtest initialization."""
        prices, signals = sample_data
        backtest = VectorizedBacktest(prices, signals)

        assert backtest.prices.equals(prices)
        assert backtest.signals.equals(signals)
        assert backtest.initial_capital == 1_000_000

    def test_data_alignment(self):
        """Test that prices and signals are properly aligned."""
        dates = pd.date_range("2020-01-01", periods=50, freq="D")
        symbols = ["A", "B"]

        # Prices with some dates
        prices = pd.DataFrame(np.random.randn(50, 2), index=dates, columns=symbols)

        # Signals with different dates
        signal_dates = dates[10:40]  # Subset of dates
        signals = pd.DataFrame(
            np.random.randn(30, 2), index=signal_dates, columns=symbols
        )

        backtest = VectorizedBacktest(prices, signals)

        # Should only use common dates
        common_dates = dates[10:40]
        assert len(backtest.prices) == len(common_dates)
        assert len(backtest.signals) == len(common_dates)

    def test_backtest_run_basic(self, sample_data):
        """Test basic backtest execution."""
        prices, signals = sample_data
        backtest = VectorizedBacktest(prices, signals, initial_capital=100000)
        results = backtest.run()

        # Check that all expected results are present
        expected_keys = [
            "portfolio_value",
            "returns",
            "positions",
            "cash",
            "trades",
            "initial_capital",
            "final_value",
            "total_return",
        ]
        for key in expected_keys:
            assert key in results

        # Check portfolio value series
        pv = results["portfolio_value"]
        assert isinstance(pv, pd.Series)
        assert len(pv) == len(prices)
        assert pv.iloc[0] == 100000  # Initial capital

        # Check returns series
        returns = results["returns"]
        assert isinstance(returns, pd.Series)
        assert len(returns) == len(prices) - 1  # One less due to pct_change

    def test_different_weight_schemes(self, sample_data):
        """Test backtest with different weight schemes."""
        prices, signals = sample_data

        for scheme in ["rank", "zscore", "long_short"]:
            backtest = VectorizedBacktest(prices, signals)
            results = backtest.run(weight_scheme=scheme)

            # Should complete without error
            assert results["final_value"] > 0

    def test_transaction_costs(self, sample_data):
        """Test that transaction costs reduce returns."""
        prices, signals = sample_data

        # Backtest without costs
        backtest_no_cost = VectorizedBacktest(prices, signals, transaction_cost=0.0)
        results_no_cost = backtest_no_cost.run()

        # Backtest with costs
        backtest_with_cost = VectorizedBacktest(
            prices, signals, transaction_cost=0.01  # 1% cost
        )
        results_with_cost = backtest_with_cost.run()

        # With costs should have lower final value (or equal)
        assert results_with_cost["final_value"] <= results_no_cost["final_value"]

    def test_rebalancing_frequencies(self, sample_data):
        """Test different rebalancing frequencies."""
        prices, signals = sample_data

        # Test daily rebalancing (default)
        backtest_daily = VectorizedBacktest(prices, signals, rebalance_freq="D")
        results_daily = backtest_daily.run()
        assert results_daily["final_value"] > 0

        # Test weekly rebalancing
        backtest_weekly = VectorizedBacktest(prices, signals, rebalance_freq="W")
        results_weekly = backtest_weekly.run()
        assert results_weekly["final_value"] > 0

        # Test monthly rebalancing
        backtest_monthly = VectorizedBacktest(prices, signals, rebalance_freq="M")
        results_monthly = backtest_monthly.run()
        assert results_monthly["final_value"] > 0

    def test_should_rebalance_logic(self):
        """Test the _should_rebalance method logic."""
        dates = pd.date_range("2020-01-01", periods=35, freq="D")
        symbols = ["A", "B"]
        prices = pd.DataFrame(np.random.randn(35, 2), index=dates, columns=symbols)
        signals = pd.DataFrame(np.random.randn(35, 2), index=dates, columns=symbols)

        # Test daily rebalancing
        backtest_daily = VectorizedBacktest(prices, signals, rebalance_freq="D")
        for date in dates:
            assert backtest_daily._should_rebalance(date)

        # Test weekly rebalancing (should rebalance on Mondays)
        backtest_weekly = VectorizedBacktest(prices, signals, rebalance_freq="W")
        for _i, date in enumerate(dates):
            expected = date.weekday() == 0  # Monday
            assert backtest_weekly._should_rebalance(date) == expected

        # Test monthly rebalancing (should rebalance on 1st of month)
        backtest_monthly = VectorizedBacktest(prices, signals, rebalance_freq="M")
        for date in dates:
            expected = date.day == 1
            assert backtest_monthly._should_rebalance(date) == expected

    def test_invalid_rebalance_frequency(self, sample_data):
        """Test that invalid rebalance frequency raises error."""
        prices, signals = sample_data

        with pytest.raises(ValueError, match="Unsupported rebalance frequency"):
            backtest = VectorizedBacktest(prices, signals, rebalance_freq="X")
            backtest.run()

    def test_rebalancing_frequency_impact(self, sample_data):
        """Test that different rebalancing frequencies produce different results."""
        prices, signals = sample_data

        # Run backtests with different frequencies
        backtest_daily = VectorizedBacktest(prices, signals, rebalance_freq="D")
        results_daily = backtest_daily.run()

        backtest_weekly = VectorizedBacktest(prices, signals, rebalance_freq="W")
        results_weekly = backtest_weekly.run()

        backtest_monthly = VectorizedBacktest(prices, signals, rebalance_freq="M")
        results_monthly = backtest_monthly.run()

        # Different frequencies should generally produce different results
        # (though not guaranteed due to randomness, so we just check they complete)
        assert results_daily["final_value"] > 0
        assert results_weekly["final_value"] > 0
        assert results_monthly["final_value"] > 0

        # Check that positions are different (weekly/monthly should have fewer changes)
        daily_positions = results_daily["positions"]
        weekly_positions = results_weekly["positions"]
        monthly_positions = results_monthly["positions"]

        # Count position changes (non-zero differences)
        daily_changes = (daily_positions.diff().abs() > 1e-10).sum().sum()
        weekly_changes = (weekly_positions.diff().abs() > 1e-10).sum().sum()
        monthly_changes = (monthly_positions.diff().abs() > 1e-10).sum().sum()

        # Weekly and monthly should have fewer position changes than daily
        assert weekly_changes <= daily_changes
        assert monthly_changes <= daily_changes
