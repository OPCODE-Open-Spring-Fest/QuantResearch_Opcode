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
            "total_return": float(total_return),
            "cagr": float(cagr),
            "annualized_return": float(cagr),
        }

    def _calculate_risk_metrics(self) -> Dict[str, float]:
        """Calculate risk-related metrics."""
        vol = float(self.returns.std(ddof=1) * np.sqrt(252))
        downside_returns = self.returns[self.returns < 0]
        downside_vol = (
            float(downside_returns.std(ddof=1) * np.sqrt(252))
            if len(downside_returns) > 0
            else 0.0
        )

        max_drawdown, drawdown_duration = self._calculate_drawdown()

        return {
            "volatility": vol,
            "downside_volatility": downside_vol,
            "max_drawdown": max_drawdown,
            "drawdown_duration": drawdown_duration,
            "var_95": float(self.returns.quantile(0.05)),
            "cvar_95": float(
                self.returns[self.returns <= self.returns.quantile(0.05)].mean()
            ),
        }

    def _calculate_ratio_metrics(self) -> Dict[str, float]:
        """Calculate risk-adjusted ratio metrics."""
        cagr = self._calculate_cagr()
        vol = float(self.returns.std(ddof=1) * np.sqrt(252))
        downside_vol = self._calculate_downside_vol()

        sharpe = float(cagr / vol) if vol > 0 else 0.0
        sortino = float(cagr / downside_vol) if downside_vol > 0 else 0.0
        dd, _ = self._calculate_drawdown()
        calmar = float(cagr / abs(dd)) if dd < 0 else 0.0

        return {
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "calmar_ratio": calmar,
        }

    def _calculate_benchmark_metrics(self) -> Dict[str, float]:
        """Calculate benchmark-relative metrics."""
        if self.benchmark_returns is None:
            return {}

        # Align returns and drop NaNs
        common_index = self.returns.index.intersection(self.benchmark_returns.index)
        strategy_returns = self.returns.loc[common_index].dropna()
        benchmark_returns = self.benchmark_returns.loc[common_index].dropna()

        if len(strategy_returns) == 0 or len(benchmark_returns) == 0:
            return {}

        # Ensure identical index after dropna
        strategy_returns, benchmark_returns = strategy_returns.align(
            benchmark_returns, join="inner"
        )

        x = benchmark_returns.values.astype(float)
        y = strategy_returns.values.astype(float)

        # If benchmark has (near) zero variance, beta is undefined; return 0.0 to keep old behavior.
        if np.allclose(np.var(x, ddof=0), 0.0):
            beta = 0.0
        else:
            # Use stable least-squares (with intercept) to get slope (beta)
            # design matrix: [x, 1]
            A = np.vstack([x, np.ones_like(x)]).T
            coeffs, *_ = np.linalg.lstsq(A, y, rcond=None)
            slope = float(coeffs[0])
            beta = slope

        # Annualized returns (CAGR) for alpha calculation
        strategy_cagr = self._calculate_cagr_from_returns(strategy_returns)
        benchmark_cagr = self._calculate_cagr_from_returns(benchmark_returns)
        alpha = float(strategy_cagr - beta * benchmark_cagr)

        # Tracking error (annualized std of active returns)
        active_returns = (strategy_returns - benchmark_returns).dropna()
        tracking_error = (
            float(active_returns.std(ddof=1) * np.sqrt(252))
            if len(active_returns) > 1
            else 0.0
        )

        # Information ratio
        info_ratio = (
            float((strategy_cagr - benchmark_cagr) / tracking_error)
            if tracking_error > 0
            else 0.0
        )

        return {
            "alpha": alpha,
            "beta": beta,
            "tracking_error": tracking_error,
            "information_ratio": info_ratio,
            "active_return": float(strategy_cagr - benchmark_cagr),
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

        return float((1 + total_return) ** (1 / years) - 1) if years > 0 else 0.0

    def _calculate_downside_vol(self) -> float:
        """Calculate downside volatility (for Sortino ratio)."""
        downside_returns = self.returns[self.returns < 0]
        return (
            float(downside_returns.std(ddof=1) * np.sqrt(252))
            if len(downside_returns) > 0
            else 0.0
        )

    def _calculate_drawdown(self) -> Tuple[float, int]:
        """Calculate maximum drawdown and duration."""
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative / running_max) - 1

        max_drawdown = float(drawdown.min()) if not drawdown.isna().all() else 0.0

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
            drawdown_duration = int((max_dd_period - drawdown_start).days)
        except Exception:
            drawdown_duration = 0

        return max_drawdown, drawdown_duration
