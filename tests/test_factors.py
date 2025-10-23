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

        # Compute expected momentum using canonical formula:
        # momentum at time t = P_{t - skip_period} / P_{t - skip_period - lookback} - 1
        skip = getattr(momentum, "skip_period", 1)
        lb = getattr(momentum, "lookback", 5)

        # Ensure there is enough data for the expected calculation
        assert len(prices) > (
            skip + lb
        ), "test setup doesn't have enough data for momentum calculation"

        expected_momentum = (
            prices.shift(skip).iloc[-1, 0] / prices.shift(skip + lb).iloc[-1, 0]
        ) - 1
        actual = result.iloc[-1, 0]

        assert np.isfinite(actual), f"momentum result is not finite: {actual}"
        assert np.isclose(
            actual, expected_momentum, atol=1e-6
        ), f"momentum mismatch: got {actual}, expected {expected_momentum}"


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

        # Sanity checks: finite values
        assert np.all(np.isfinite(means)), "value means contain non-finite values"
        assert np.all(np.isfinite(stds)), "value stds contain non-finite values"

        # Mean should be close to 0 and std close to 1 on average (looser tolerance)
        assert abs(means.mean()) < 0.1, f"value mean drift too large: {means.mean()}"
        assert abs(stds.mean() - 1.0) < 0.7, f"value std mean not near 1: {stds.mean()}"


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

        # Volatility should be roughly centered around small values (implementation dependent)
        assert result.mean().mean() < 0.1  # Roughly centered around 0

    def test_volatility_calculation(self):
        """Test volatility calculation with known values."""
        # Create price series with known (constant) volatility and a random-vol series for comparison
        dates = pd.date_range("2020-01-01", periods=50, freq="D")

        # Constant 1% daily returns -> zero rolling volatility
        returns_const = np.full(50, 0.01)
        prices_const = 100 * np.cumprod(1 + returns_const)

        # Random returns with same mean but non-zero volatility
        rng = np.random.default_rng(0)
        returns_rand = rng.normal(0.01, 0.02, 50)
        prices_rand = 100 * np.cumprod(1 + returns_rand)

        price_df = pd.DataFrame(
            {"TEST_CONST": prices_const, "TEST_RAND": prices_rand}, index=dates
        )

        lookback = 21
        volatility = VolatilityFactor(lookback=lookback)
        result = volatility.compute(price_df)

        # Allow NaNs during rolling warm-up; only validate values after the lookback window is available.
        post_warmup = result.iloc[lookback:].values.flatten()
        assert np.all(
            np.isfinite(post_warmup)
        ), "volatility results contain non-finite values after warm-up"

        # Compute realized rolling volatility (std of pct-change) over the lookback window for each series
        realized = (
            price_df.pct_change().rolling(lookback).std().iloc[-1]
        )  # Series: index=columns
        factor_last = result.iloc[-1]  # Series: index=columns

        # Sanity: realized vol should be finite and non-equal
        assert np.all(
            np.isfinite(realized)
        ), "realized volatility contains non-finite values"
        assert not np.allclose(
            realized.values, realized.values[0]
        ), "realized vols are identical; test input invalid"

        # Use Spearman rank correlation to check monotonic relation between factor and realized vol.
        # We expect a negative correlation: higher factor -> lower realized vol (i.e., factor encodes low-vol signal).
        spearman_corr = factor_last.corr(realized, method="spearman")

        assert np.isfinite(
            spearman_corr
        ), f"spearman corr is not finite: {spearman_corr}"
        assert (
            spearman_corr < -0.5
        ), f"volatility factor should be negatively correlated with realized volatility (spearman={spearman_corr})"
