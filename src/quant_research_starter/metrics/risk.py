"""Risk and performance metrics for quantitative strategies."""

from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd


class RiskMetrics:
    """Comprehensive risk and performance metrics calculator."""

    def __init__(
        self, returns: pd.Series, benchmark_returns: Optional[pd.Series] = None
    ):
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self._metrics: Optional[Dict] = None

    def calculate_all(self) -> Dict[str, float]:
        """Calculate all available metrics."""
        if self._metrics is None:
            self._metrics = {
                **self._calculate_return_metrics(),
                **self._calculate_risk_metrics(),
                **self._calculate_ratio_metrics(),
            }

            if self.benchmark_returns is not None:
                self._metrics.update(self._calculate_benchmark_metrics())

        return self._metrics

    def _calculate_return_metrics(self) -> Dict[str, float]:
        """Calculate return-related metrics."""
        total_return = (1 + self.returns).prod() - 1
        cagr = self._calculate_cagr()

        return {
            "total_return": total_return,
            "cagr": cagr,
            "annualized_return": cagr,
        }

    def _calculate_risk_metrics(self) -> Dict[str, float]:
        """Calculate risk-related metrics."""
        vol = self.returns.std() * np.sqrt(252)
        downside_returns = self.returns[self.returns < 0]
        downside_vol = (
            downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        )

        max_drawdown, drawdown_duration = self._calculate_drawdown()

        return {
            "volatility": vol,
            "downside_volatility": downside_vol,
            "max_drawdown": max_drawdown,
            "drawdown_duration": drawdown_duration,
            "var_95": self.returns.quantile(0.05),
            "cvar_95": self.returns[self.returns <= self.returns.quantile(0.05)].mean(),
        }

    def _calculate_ratio_metrics(self) -> Dict[str, float]:
        """Calculate risk-adjusted ratio metrics."""
        cagr = self._calculate_cagr()
        vol = self.returns.std() * np.sqrt(252)
        downside_vol = self._calculate_downside_vol()

        sharpe = cagr / vol if vol > 0 else 0
        sortino = cagr / downside_vol if downside_vol > 0 else 0
        calmar = (
            cagr / abs(self._calculate_drawdown()[0])
            if self._calculate_drawdown()[0] < 0
            else 0
        )

        return {
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "calmar_ratio": calmar,
        }

    def _calculate_benchmark_metrics(self) -> Dict[str, float]:
        """Calculate benchmark-relative metrics."""
        if self.benchmark_returns is None:
            return {}

        # Align returns
        common_index = self.returns.index.intersection(self.benchmark_returns.index)
        strategy_returns = self.returns.loc[common_index]
        benchmark_returns = self.benchmark_returns.loc[common_index]

        # Calculate alpha and beta via OLS with intercept
        x = benchmark_returns.values
        y = strategy_returns.values
        x_mean = x.mean()
        y_mean = y.mean()
        x_var = ((x - x_mean) ** 2).mean()
        cov_xy = ((x - x_mean) * (y - y_mean)).mean()
        beta = cov_xy / x_var if x_var > 0 else 0.0
        alpha_daily = y_mean - beta * x_mean
        # Convert alpha to annualized approximation
        alpha = (1 + alpha_daily) ** 252 - 1 if alpha_daily != 0 else 0.0

        strategy_cagr = self._calculate_cagr_from_returns(strategy_returns)
        benchmark_cagr = self._calculate_cagr_from_returns(benchmark_returns)
        alpha = strategy_cagr - beta * benchmark_cagr

        # Tracking error
        active_returns = strategy_returns - benchmark_returns
        tracking_error = active_returns.std() * np.sqrt(252)

        # Information ratio
        info_ratio = (
            (strategy_cagr - benchmark_cagr) / tracking_error
            if tracking_error > 0
            else 0
        )

        return {
            "alpha": alpha,
            "beta": beta,
            "tracking_error": tracking_error,
            "information_ratio": info_ratio,
            "active_return": strategy_cagr - benchmark_cagr,
        }

    def _calculate_cagr(self) -> float:
        """Calculate Compound Annual Growth Rate."""
        return self._calculate_cagr_from_returns(self.returns)

    def _calculate_cagr_from_returns(self, returns: pd.Series) -> float:
        """Calculate CAGR from return series."""
        if len(returns) == 0:
            return 0.0

        total_return = (1 + returns).prod() - 1
        years = (returns.index[-1] - returns.index[0]).days / 365.25

        return (1 + total_return) ** (1 / years) - 1 if years > 0 else 0

    def _calculate_downside_vol(self) -> float:
        """Calculate downside volatility (for Sortino ratio)."""
        downside_returns = self.returns[self.returns < 0]
        return downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0

    def _calculate_drawdown(self) -> Tuple[float, int]:
        """Calculate maximum drawdown and duration."""
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative / running_max) - 1

        max_drawdown = drawdown.min()

        # Handle edge cases safely
        if drawdown.isna().all():
            return 0.0, 0

        # Calculate duration of maximum drawdown with guards
        max_dd_idx = drawdown[drawdown == max_drawdown].index
        if len(max_dd_idx) == 0:
            return float(max_drawdown), 0
        max_dd_period = max_dd_idx[0]

        # Find the last time the running max was achieved before max_dd_period
        try:
            prior_max_mask = running_max[running_max.index <= max_dd_period]
            drawdown_start_val = prior_max_mask.max()
            start_candidates = prior_max_mask[
                prior_max_mask == drawdown_start_val
            ].index
            drawdown_start = (
                start_candidates[-1]
                if len(start_candidates) > 0
                else running_max.index[0]
            )
            drawdown_duration = (max_dd_period - drawdown_start).days
        except Exception:
            drawdown_duration = 0

        return float(max_drawdown), int(drawdown_duration)
