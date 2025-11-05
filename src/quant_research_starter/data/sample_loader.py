"""Sample data loader for demo purposes."""

from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm


class SampleDataLoader:
    """Loader for sample data included with the package."""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent.parent / "data_sample"

    def load_sample_prices(self) -> pd.DataFrame:
        """Load sample price data from CSV."""
        sample_file = self.data_dir / "sample_prices.csv"

        if sample_file.exists():
            return pd.read_csv(sample_file, index_col=0, parse_dates=True)
        else:
            # Generate sample data if file doesn't exist
            return self._generate_sample_data()

    def _generate_sample_data(self) -> pd.DataFrame:
        """Generate synthetic sample data for demos."""
        dates = pd.date_range(start="2020-01-01", end="2023-12-31", freq="D")
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

        np.random.seed(42)
        data = {}
        with tqdm(total=len(symbols), desc="Generating sample data", unit="symbol") as pbar:
            for symbol in symbols:
                # Generate realistic-looking price series with trends
                returns = np.random.normal(0.0005, 0.02, len(dates))
                prices = 100 * np.cumprod(1 + returns)
                data[symbol] = prices
                pbar.update(1)
                pbar.set_postfix(symbol=symbol, refresh=False)

        df = pd.DataFrame(data, index=dates)
        df.index.name = "date"

        # Save for future use
        self.data_dir.mkdir(exist_ok=True)
        df.to_csv(self.data_dir / "sample_prices.csv")

        return df
