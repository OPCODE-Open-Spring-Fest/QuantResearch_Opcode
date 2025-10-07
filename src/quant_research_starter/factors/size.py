"""Size factor implementation."""

import numpy as np
import pandas as pd

from .base import Factor


class SizeFactor(Factor):
    """
    Size factor based on market capitalization.

    Typically uses log market cap to reduce skewness.
    """

    def __init__(self, name: str = "size"):
        super().__init__(name=name, lookback=1)

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        Compute size factor using log prices as proxy for market cap.

        In practice, you would use actual market capitalization data.
        Here we use price levels as a rough proxy.
        """
        self._validate_data(prices)

        # Use log prices as proxy for market cap (simplified)
        # In reality, you'd multiply by shares outstanding
        log_prices = np.log(prices)

        # Size factor is typically negative (small caps outperform)
        # So we use negative log market cap
        size_scores = -log_prices

        # Z-score normalize cross-sectionally
        size_z = size_scores.sub(size_scores.mean(axis=1), axis=0)
        size_z = size_z.div(size_scores.std(axis=1), axis=0)

        self._values = size_z
        return size_z
