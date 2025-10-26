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

    def test_rebalance_frequency_daily(self, sample_data):
        """Test daily rebalancing (default behavior)."""
        prices, signals = sample_data
        backtest = VectorizedBacktest(prices, signals, rebalance_freq="D")
        results = backtest.run()

        # Check that backtest runs successfully
        assert results["final_value"] > 0
        assert len(results["portfolio_value"]) == len(prices)

    def test_rebalance_frequency_weekly(self, sample_data):
        """Test weekly rebalancing."""
        prices, signals = sample_data
        backtest = VectorizedBacktest(prices, signals, rebalance_freq="W")
        results = backtest.run()

        # Check that backtest runs successfully
        assert results["final_value"] > 0
        assert len(results["portfolio_value"]) == len(prices)

        # Weekly rebalancing should result in fewer position changes
        # Count the number of times weights change
        positions = results["positions"]
        position_changes = (positions.diff().abs().sum(axis=1) > 0).sum()

        # Should be significantly fewer than daily (100 days)
        # Approximately ~14 weeks in 100 days
        assert position_changes < len(prices) - 1

    def test_rebalance_frequency_monthly(self, sample_data):
        """Test monthly rebalancing."""
        prices, signals = sample_data
        backtest = VectorizedBacktest(prices, signals, rebalance_freq="M")
        results = backtest.run()

        # Check that backtest runs successfully
        assert results["final_value"] > 0
        assert len(results["portfolio_value"]) == len(prices)

        # Monthly rebalancing should result in fewer position changes than weekly
        positions = results["positions"]
        position_changes = (positions.diff().abs().sum(axis=1) > 0).sum()

        # Should be significantly fewer than daily
        # Approximately ~3 months in 100 days
        assert position_changes < len(prices) - 1

    def test_rebalance_frequency_invalid(self, sample_data):
        """Test that invalid rebalance frequency raises error."""
        prices, signals = sample_data
        backtest = VectorizedBacktest(prices, signals, rebalance_freq="X")

        with pytest.raises(ValueError, match="Unsupported rebalance frequency"):
            backtest.run()

    def test_rebalance_reduces_turnover(self, sample_data):
        """Test that less frequent rebalancing reduces turnover."""
        prices, signals = sample_data

        # Daily rebalancing
        backtest_daily = VectorizedBacktest(prices, signals, rebalance_freq="D", transaction_cost=0.001)
        results_daily = backtest_daily.run()

        # Monthly rebalancing
        backtest_monthly = VectorizedBacktest(prices, signals, rebalance_freq="M", transaction_cost=0.001)
        results_monthly = backtest_monthly.run()

        # Count position changes as proxy for turnover
        daily_changes = (results_daily["positions"].diff().abs().sum(axis=1) > 0).sum()
        monthly_changes = (results_monthly["positions"].diff().abs().sum(axis=1) > 0).sum()

        # Monthly should have fewer rebalances
        assert monthly_changes < daily_changes
