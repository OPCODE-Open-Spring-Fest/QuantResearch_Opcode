"""Tests for risk metrics calculations."""

import numpy as np
import pandas as pd
import pytest

from quant_research_starter.metrics import RiskMetrics


@pytest.fixture
def sample_returns():
    """Create sample return series for testing metrics."""
    dates = pd.date_range("2020-01-01", periods=252, freq="D")  # 1 year of daily data

    # Generate returns with known properties
    np.random.seed(42)
    returns = np.random.normal(0.001, 0.02, len(dates))  # 0.1% daily mean, 2% daily vol

    return pd.Series(returns, index=dates)


@pytest.fixture
def benchmark_returns():
    """Create benchmark returns."""
    dates = pd.date_range("2020-01-01", periods=252, freq="D")
    np.random.seed(43)
    returns = np.random.normal(0.0008, 0.018, len(dates))

    return pd.Series(returns, index=dates)


class TestRiskMetrics:
    """Test risk metrics calculations."""

    def test_basic_metrics(self, sample_returns):
        """Test calculation of basic metrics."""
        metrics_calc = RiskMetrics(sample_returns)
        results = metrics_calc.calculate_all()

        # Check that expected metrics are present
        expected_metrics = [
            "total_return",
            "cagr",
            "volatility",
            "max_drawdown",
            "sharpe_ratio",
            "sortino_ratio",
        ]
        for metric in expected_metrics:
            assert metric in results
            assert isinstance(results[metric], (float, int))

    def test_cagr_calculation(self):
        """Test CAGR calculation with known values."""
        # Create returns that double money in 2 years
        dates = pd.date_range("2020-01-01", "2021-12-31", freq="D")
        n_days = len(dates)

        # Calculate daily return needed to double in 2 years
        total_return = 1.0  # 100% return
        daily_return = (1 + total_return) ** (1 / n_days) - 1

        returns = pd.Series([daily_return] * n_days, index=dates)

        metrics = RiskMetrics(returns)
        results = metrics.calculate_all()

        # Should be close to 100% total return, ~41.4% CAGR for 2 years
        assert abs(results["total_return"] - 1.0) < 0.01  # ~100% total return
        assert abs(results["cagr"] - 0.414) < 0.01  # ~41.4% CAGR

    def test_drawdown_calculation(self):
        """Test drawdown calculation with known pattern."""
        # Create returns that cause a specific drawdown pattern
        dates = pd.date_range("2020-01-01", periods=100, freq="D")

        # Series that goes: 100 -> 150 -> 90 -> 120
        # Drawdown: 0% -> 0% -> 40% -> 20%
        prices = [100, 150, 90, 120]
        # Extend with constant values
        prices.extend([120] * 96)

        returns = pd.Series(np.diff(prices) / prices[:-1], index=dates[:99])

        metrics = RiskMetrics(returns)
        results = metrics.calculate_all()

        # Maximum drawdown should be (150-90)/150 = 40%
        assert abs(results["max_drawdown"] - (-0.4)) < 0.01

    def test_sharpe_ratio(self):
        """Test Sharpe ratio calculation."""
        # Create risk-free returns (zero volatility, positive return)
        dates = pd.date_range("2020-01-01", periods=252, freq="D")
        returns = pd.Series([0.001] * 252, index=dates)  # 0.1% daily return

        metrics = RiskMetrics(returns)
        results = metrics.calculate_all()

        # With zero volatility, Sharpe should be large (infinite in theory)
        # But due to annualization and daily precision, it will be finite but large
        assert results["sharpe_ratio"] > 10

    def test_benchmark_metrics(self, sample_returns, benchmark_returns):
        """Test benchmark-relative metrics."""
        metrics = RiskMetrics(sample_returns, benchmark_returns)
        results = metrics.calculate_all()

        benchmark_metrics = ["alpha", "beta", "tracking_error", "information_ratio"]
        for metric in benchmark_metrics:
            assert metric in results

        # Beta should be around 1 for similar return streams
        assert 0.5 < abs(results["beta"]) < 2.0

    def test_empty_returns(self):
        """Test metrics with empty return series."""
        empty_returns = pd.Series([], dtype=float)
        metrics = RiskMetrics(empty_returns)
        results = metrics.calculate_all()

        # All metrics should be zero or safe defaults
        assert results["total_return"] == 0
        assert results["cagr"] == 0
        assert results["sharpe_ratio"] == 0
