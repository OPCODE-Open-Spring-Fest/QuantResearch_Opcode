"""Tests for data module."""

import numpy as np
import pandas as pd
import pytest

from quant_research_starter.data import (
    SampleDataLoader,
    SyntheticDataGenerator,
    YahooDownloader,
)


class TestSyntheticDataGenerator:
    """Test synthetic data generation."""

    def test_generate_price_data_basic(self):
        """Test basic price data generation."""
        generator = SyntheticDataGenerator(seed=42)
        prices = generator.generate_price_data(
            n_symbols=5, days=100, start_date="2020-01-01"
        )

        assert isinstance(prices, pd.DataFrame)
        assert len(prices) == 100
        assert prices.shape[1] == 5
        assert prices.index.name == "date"
        assert prices.index[0] == pd.Timestamp("2020-01-01")

    def test_generate_price_data_uncorrelated(self):
        """Test uncorrelated data generation."""
        generator = SyntheticDataGenerator(seed=42)
        prices = generator.generate_price_data(n_symbols=3, days=50, correlation=False)

        # Check that returns have expected properties
        returns = prices.pct_change().dropna()
        assert returns.std().mean() > 0  # Some volatility

    def test_reproducibility(self):
        """Test that same seed produces same data."""
        gen1 = SyntheticDataGenerator(seed=42)
        prices1 = gen1.generate_price_data(n_symbols=3, days=10)

        gen2 = SyntheticDataGenerator(seed=42)
        prices2 = gen2.generate_price_data(n_symbols=3, days=10)

        pd.testing.assert_frame_equal(prices1, prices2)


class TestSampleDataLoader:
    """Test sample data loading."""

    def test_load_sample_prices(self, tmp_path):
        """Test loading sample prices."""
        # Create temporary data directory
        data_dir = tmp_path / "data_sample"
        data_dir.mkdir()

        # Create sample data
        dates = pd.date_range("2020-01-01", periods=10, freq="D")
        symbols = ["AAPL", "GOOGL"]
        data = np.random.randn(10, 2) + 100
        sample_df = pd.DataFrame(data, index=dates, columns=symbols)
        sample_df.index.name = "date"
        sample_df.to_csv(data_dir / "sample_prices.csv")

        # Test loading
        loader = SampleDataLoader()
        loader.data_dir = data_dir
        prices = loader.load_sample_prices()

        assert isinstance(prices, pd.DataFrame)
        assert len(prices) == 10
        assert list(prices.columns) == symbols


class TestYahooDownloader:
    """Test Yahoo downloader (mock implementation)."""

    def test_download_basic(self):
        """Test basic download functionality."""
        downloader = YahooDownloader()
        symbols = ["AAPL", "MSFT"]
        start_date = "2020-01-01"
        end_date = "2020-01-10"

        prices = downloader.download(symbols, start_date, end_date)

        assert isinstance(prices, pd.DataFrame)
        assert len(prices) > 0
        assert set(prices.columns) == set(symbols)

    def test_download_empty_symbols(self):
        """Test download with empty symbols list."""
        downloader = YahooDownloader()

        with pytest.raises(ValueError):
            downloader.download([], "2020-01-01", "2020-01-10")
