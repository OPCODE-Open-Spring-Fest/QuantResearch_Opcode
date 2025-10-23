import pandas as pd
from .base import Factor


class BollingerBandsFactor(Factor):
    """
    Compute Bollinger Bands z-score:
    z = (price - rolling_mean) / rolling_std
    """

    def __init__(self, name: str = "bollinger_bands", lookback: int = 20, num_std: float = 2.0):
        super().__init__(name=name, lookback=lookback)
        self.num_std = num_std

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        # Validate data
        self._validate_data(prices)

        # Rolling statistics
        rolling_mean = prices.rolling(self.lookback).mean()
        rolling_std = prices.rolling(self.lookback).std()

        # Bollinger z-score
        zscore = (prices - rolling_mean) / rolling_std

        # Save results
        self._values = zscore

        return zscore
