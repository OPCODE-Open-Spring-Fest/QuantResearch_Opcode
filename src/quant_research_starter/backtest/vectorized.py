"""Vectorized backtesting engine."""

from typing import Dict, Optional

import pandas as pd


class VectorizedBacktest:
    """
    Vectorized backtester for quantitative strategies.

    Features:
    - Daily rebalancing with position sizing
    - Transaction costs (fixed and proportional)
    - Portfolio constraints (leverage, concentration)
    - Realistic market dynamics (slippage, execution)
    """

    def __init__(
        self,
        prices: pd.DataFrame,
        signals: pd.DataFrame,
        initial_capital: float = 1_000_000,
        transaction_cost: float = 0.001,  # 10 bps
        max_leverage: float = 1.0,
        min_position_size: float = 0.001,  # 0.1% of portfolio
        rebalance_freq: str = "D",
    ):
        self.prices = prices
        self.signals = signals
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.max_leverage = max_leverage
        self.min_position_size = min_position_size
        self.rebalance_freq = rebalance_freq

        # Align signals with prices
        self._align_data()

        # Results storage
        self.positions: Optional[pd.DataFrame] = None
        self.portfolio_value: Optional[pd.Series] = None
        self.returns: Optional[pd.Series] = None
        self.trades: Optional[pd.DataFrame] = None

    def _align_data(self) -> None:
        """Align price and signal data on common dates."""
        common_dates = self.prices.index.intersection(self.signals.index)
        if len(common_dates) == 0:
            raise ValueError("No common dates between prices and signals")

        self.prices = self.prices.loc[common_dates]
        self.signals = self.signals.loc[common_dates]

    def run(self, weight_scheme: str = "rank") -> Dict:
        """
        Run the backtest.

        Args:
            weight_scheme: How to convert signals to weights
                - "rank": Rank-based weights
                - "zscore": Z-score based weights
                - "long_short": Equal long/short weights
        """
        print("Running backtest...")

        # Vectorized returns-based backtest with configurable rebalancing
        returns_df = self.prices.pct_change().dropna()
        aligned_signals = self.signals.loc[returns_df.index]

        # Track rebalancing
        prev_rebalance_date = None
        current_weights = pd.Series(0.0, index=self.prices.columns)

        # Compute daily weights from signals (rebalance only on rebalance dates)
        weights_list = []
        for date in returns_df.index:
            if self._should_rebalance(date, prev_rebalance_date):
                # Rebalance: compute new target weights
                current_weights = self._calculate_weights(
                    aligned_signals.loc[date], weight_scheme
                )
                prev_rebalance_date = date

            # Append current weights (maintain between rebalances)
            weights_list.append(current_weights)

        weights = pd.DataFrame(
            weights_list, index=returns_df.index, columns=self.prices.columns
        ).fillna(0.0)

        # Previous day weights for PnL calculation
        weights_prev = weights.shift(1).fillna(0.0)

        # Turnover for transaction costs (L1 change / 2)
        turnover = (weights.fillna(0.0) - weights_prev).abs().sum(axis=1) * 0.5
        tc_series = turnover * self.transaction_cost

        # Strategy returns
        strat_ret = (weights_prev * returns_df).sum(axis=1) - tc_series

        # Build portfolio value series
        portfolio_value = (1 + strat_ret).cumprod() * self.initial_capital
        portfolio_value = pd.concat(
            [
                pd.Series(self.initial_capital, index=[self.prices.index[0]]),
                portfolio_value,
            ]
        )
        portfolio_value = portfolio_value.reindex(self.prices.index).ffill()

        # Store results
        self.positions = weights  # interpret as weights positions
        self.cash = None
        self.portfolio_value = portfolio_value
        self.returns = portfolio_value.pct_change().dropna()
        self.trades = pd.DataFrame()

        return self._generate_results()

    def _should_rebalance(
        self, date: pd.Timestamp, prev_rebalance_date: Optional[pd.Timestamp] = None
    ) -> bool:
        """Check if we should rebalance on given date.

        Args:
            date: Current date to check
            prev_rebalance_date: Last rebalance date (None for first rebalance)

        Returns:
            True if should rebalance, False otherwise
        """
        # Always rebalance on first date
        if prev_rebalance_date is None:
            return True

        if self.rebalance_freq == "D":
            # Daily rebalancing
            return True
        elif self.rebalance_freq == "W":
            # Weekly rebalancing - rebalance if week changed
            return (
                date.isocalendar()[1] != prev_rebalance_date.isocalendar()[1]
                or date.year != prev_rebalance_date.year
            )
        elif self.rebalance_freq == "M":
            # Monthly rebalancing - rebalance if month changed
            return (
                date.month != prev_rebalance_date.month
                or date.year != prev_rebalance_date.year
            )
        else:
            raise ValueError(
                f"Unsupported rebalance frequency: {self.rebalance_freq}. "
                f"Supported frequencies: 'D' (daily), 'W' (weekly), 'M' (monthly)"
            )

    def _calculate_weights(self, signals: pd.Series, scheme: str) -> pd.Series:
        """Convert signals to portfolio weights."""
        valid_signals = signals.dropna()

        if len(valid_signals) == 0:
            return pd.Series(0.0, index=signals.index)

        if scheme == "rank":
            # Rank-based weights (long top decile, short bottom decile)
            ranks = valid_signals.rank()
            long_threshold = ranks.quantile(0.9)
            short_threshold = ranks.quantile(0.1)

            weights = pd.Series(0.0, index=valid_signals.index)
            weights[ranks >= long_threshold] = 1.0
            weights[ranks <= short_threshold] = -1.0

            # Normalize to have equal long/short exposure
            long_count = (weights > 0).sum()
            short_count = (weights < 0).sum()

            if long_count > 0:
                weights[weights > 0] = 1.0 / long_count
            if short_count > 0:
                weights[weights < 0] = -1.0 / short_count

            # Apply leverage constraint
            total_leverage = abs(weights).sum()
            if total_leverage > self.max_leverage:
                weights = weights * (self.max_leverage / total_leverage)

        elif scheme == "zscore":
            # Z-score based weights (linear in z-scores)
            weights = valid_signals.copy()

            # Truncate extreme values
            cap_level = 3.0
            weights = weights.clip(-cap_level, cap_level)

            # Normalize to target leverage
            total_abs_weight = abs(weights).sum()
            if total_abs_weight > 0:
                weights = weights * (self.max_leverage / total_abs_weight)

        elif scheme == "long_short":
            # Simple equal long/short
            long_count = (valid_signals > 0).sum()
            short_count = (valid_signals < 0).sum()

            weights = pd.Series(0.0, index=valid_signals.index)
            if long_count > 0:
                weights[valid_signals > 0] = 1.0 / long_count
            if short_count > 0:
                weights[valid_signals < 0] = -1.0 / short_count

        else:
            raise ValueError(f"Unknown weight scheme: {scheme}")

        # Ensure we have weights for all symbols
        full_weights = pd.Series(0.0, index=signals.index)
        full_weights[valid_signals.index] = weights

        return full_weights

    def _generate_results(self) -> Dict:
        """Generate comprehensive backtest results."""
        if self.returns is None or self.portfolio_value is None:
            raise ValueError("Backtest not run yet")

        return {
            "portfolio_value": self.portfolio_value,
            "returns": self.returns,
            "positions": self.positions,
            "cash": self.cash,
            "trades": self.trades,
            "initial_capital": self.initial_capital,
            "final_value": self.portfolio_value.iloc[-1],
            "total_return": (self.portfolio_value.iloc[-1] / self.initial_capital) - 1,
        }
