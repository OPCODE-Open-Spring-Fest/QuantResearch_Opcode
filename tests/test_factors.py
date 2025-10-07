"""Tests for factor implementations."""

import numpy as np
import pandas as pd
import pytest

from quant_research_starter.factors import (
    MomentumFactor,
    SizeFactor,
    ValueFactor,
    VolatilityFactor,
)


@pytest.fixture
def sample_prices():
    """Create sample price data for testing."""
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    symbols = ["AAPL", "GOOGL", "MSFT"]

    # Generate realistic price series
    np.random.seed(42)
    data = {}
    for symbol in symbols:
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = 100 * np.cumprod(1 + returns)
        data[symbol] = prices

    return pd.DataFrame(data, index=dates)


class TestMomentumFactor:
    """Test momentum factor calculations."""

    def test_momentum_basic(self, sample_prices):
        """Test basic momentum calculation."""
        momentum = MomentumFactor(lookback=21)
        result = momentum.compute(sample_prices)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert set(result.columns) == set(sample_prices.columns)

        # Momentum should be between reasonable bounds
        assert result.abs().max().max() < 10  # Not crazy values

    def test_momentum_lookback_too_long(self, sample_prices):
        """Test momentum with insufficient data."""
        momentum = MomentumFactor(lookback=200)  # More than available data

        with pytest.raises(ValueError):
            momentum.compute(sample_prices)

    def test_momentum_values(self):
        """Test momentum calculation with known values."""
        # Create simple price series
        dates = pd.date_range("2020-01-01", periods=30, freq="D")
        prices = pd.DataFrame(
            {"TEST": [100, 101, 102, 103, 104, 105] + [100] * 24}, index=dates
        )

        momentum = MomentumFactor(lookback=5, skip_period=1)
        result = momentum.compute(prices)

        # Price goes from 100 to 105 over 5 days -> 5% momentum
        expected_momentum = (105 / 100) - 1
        assert abs(result.iloc[-1, 0] - expected_momentum) < 1e-10


class TestValueFactor:
    """Test value factor calculations."""

    def test_value_basic(self, sample_prices):
        """Test basic value factor calculation."""
        value = ValueFactor()
        result = value.compute(sample_prices)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert set(result.columns) == set(sample_prices.columns)

        # Value scores should be z-scored (mean ~0, std ~1)
        means = result.mean(axis=1)
        stds = result.std(axis=1)
        assert abs(means.mean()) < 0.1
        assert abs(stds.mean() - 1.0) < 0.5


class TestSizeFactor:
    """Test size factor calculations."""

    def test_size_basic(self, sample_prices):
        """Test basic size factor calculation."""
        size = SizeFactor()
        result = size.compute(sample_prices)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

        # Size factor should be negative of log prices (normalized)
        log_prices = np.log(sample_prices)
        size_scores = -log_prices
        size_z = size_scores.sub(size_scores.mean(axis=1), axis=0)
        size_z = size_z.div(size_scores.std(axis=1), axis=0)

        # Should match our calculation (allowing for numerical precision)
        pd.testing.assert_frame_equal(result, size_z, check_exact=False)


class TestVolatilityFactor:
    """Test volatility factor calculations."""

    def test_volatility_basic(self, sample_prices):
        """Test basic volatility calculation."""
        volatility = VolatilityFactor(lookback=21)
        result = volatility.compute(sample_prices)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

        # Volatility should be negative (low vol -> high returns)
        assert result.mean().mean() < 0.1  # Roughly centered around 0

    def test_volatility_calculation(self):
        """Test volatility calculation with known values."""
        # Create price series with known volatility
        dates = pd.date_range("2020-01-01", periods=50, freq="D")
        returns = np.full(50, 0.01)  # Constant 1% daily returns
        prices = 100 * np.cumprod(1 + returns)

        price_df = pd.DataFrame({"TEST": prices}, index=dates)

        volatility = VolatilityFactor(lookback=21)
        result = volatility.compute(price_df)

        # Constant returns -> zero volatility -> large negative score
        assert result.iloc[-1, 0] < -1  # Strong low-vol signal
