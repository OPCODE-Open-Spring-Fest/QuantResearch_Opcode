import pandas as pd
from tqdm import tqdm

from .base import Factor


class BollingerBandsFactor(Factor):
    """
    Compute Bollinger Bands z-score:
    z = (price - rolling_mean) / rolling_std
    """

    def __init__(
        self, name: str = "bollinger_bands", lookback: int = 20, num_std: float = 2.0
    ):
        super().__init__(name=name, lookback=lookback)
        self.num_std = num_std

    def compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        # Validate data
        self._validate_data(prices)
        n_symbols = len(prices.columns)
        with tqdm(total=4, desc=f"Computing {self.name} ({n_symbols} symbols)") as pbar:
            # Rolling statistics
            pbar.set_description("Calculating rolling mean")
            rolling_mean = prices.rolling(self.lookback).mean()
            pbar.update(1)

            pbar.set_description("Calculating rolling standard deviation")
            rolling_std = prices.rolling(self.lookback).std()
            pbar.update(1)

            # Bollinger z-score
            pbar.set_description("Computing z-scores")
            zscore = (prices - rolling_mean) / rolling_std
            pbar.update(1)

            # Save results
            pbar.set_description("Finalizing factor values")
            self._values = zscore
            pbar.update(1)

        return zscore