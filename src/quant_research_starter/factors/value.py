"""Value factor implementations."""

import numpy as np
import pandas as pd

from .base import Factor


class ValueFactor(Factor):
    """
    Value factors based on various valuation ratios.

    Note: This is a simplified implementation. In practice, value factors
    would use fundamental data like:
    - Book to Market (B/M)
    - Earnings to Price (E/P)
    - Cash Flow to Price (CF/P)
    - Dividend Yield
    """

    def __init__(self, name: str = "value"):
        super().__init__(name=name, lookback=1)

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        Compute synthetic value factor.

        In a real implementation, this would use fundamental data.
        Here we create a synthetic value signal that slowly changes over time.
        """
        self._validate_data(prices)

        # Create synthetic value scores that persist but have some noise
        np.random.seed(42)  # For reproducible synthetic data
        n_assets = prices.shape[1]

        # Base value scores (simulate persistent value characteristics)
        base_scores = np.random.normal(0, 1, n_assets)

        # Add some time-varying component (value factors change slowly)
        days = len(prices)
        noise = np.random.normal(0, 0.1, (days, n_assets))
        time_trend = np.linspace(0, 0.5, days).reshape(-1, 1)

        # Combine to create value scores
        value_scores = base_scores + time_trend + noise

        # Create DataFrame
        value_df = pd.DataFrame(
            value_scores, index=prices.index, columns=prices.columns
        )

        # Z-score normalize cross-sectionally each day
        value_z = value_df.sub(value_df.mean(axis=1), axis=0)
        value_z = value_z.div(value_df.std(axis=1), axis=0)

        self._values = value_z
        return value_z
