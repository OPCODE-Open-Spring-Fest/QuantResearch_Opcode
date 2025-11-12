import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import optuna
import pandas as pd
from optuna.pruners import MedianPruner, NopPruner, PercentilePruner
from optuna.storages import RDBStorage
from optuna.trial import Trial

from ..backtest import VectorizedBacktest
from ..factors import MomentumFactor, SizeFactor, ValueFactor, VolatilityFactor
from ..metrics import RiskMetrics


class OptunaRunner:

    def __init__(
        self,
        search_space: Dict[str, Any],
        objective: Callable[[Trial], float],
        n_trials: int = 100,
        study_name: Optional[str] = None,
        storage: Optional[Union[str, RDBStorage]] = None,
        pruner: Optional[Union[str, optuna.pruners.BasePruner]] = None,
        direction: str = "maximize",
        random_state: Optional[int] = None,
    ):

        self.search_space = search_space
        self.objective = objective
        self.n_trials = n_trials
        self.study_name = study_name or "optuna_study"
        self.direction = direction
        self.random_state = random_state

        if storage is None:
            self.storage = None
        elif isinstance(storage, str):
            self.storage = storage
        elif isinstance(storage, RDBStorage):
            self.storage = storage
        else:
            raise ValueError(f"Invalid storage type: {type(storage)}")

        if pruner is None or pruner == "none":
            self.pruner = NopPruner()
        elif pruner == "median":
            self.pruner = MedianPruner()
        elif pruner == "percentile":
            self.pruner = PercentilePruner(percentile=25.0)
        elif isinstance(pruner, optuna.pruners.BasePruner):
            self.pruner = pruner
        else:
            raise ValueError(f"Invalid pruner: {pruner}")

        self.study: Optional[optuna.Study] = None
        self.trial_history: List[Dict[str, Any]] = []

    def optimize(self) -> Dict[str, Any]:
        """
        Run hyperparameter optimization.

        Returns:
            Dictionary with:
                - best_params: Best hyperparameters found
                - best_value: Best objective value
                - trial_history: List of all trial results
                - study: Optuna study object
        """
        self.study = optuna.create_study(
            study_name=self.study_name,
            storage=self.storage,
            load_if_exists=True,
            direction=self.direction,
            pruner=self.pruner,
            sampler=optuna.samplers.TPESampler(seed=self.random_state),
        )

        self.study.optimize(
            self.objective,
            n_trials=self.n_trials,
            show_progress_bar=True,
        )

        self.trial_history = self._collect_trial_history()

        return {
            "best_params": self.study.best_params,
            "best_value": self.study.best_value,
            "trial_history": self.trial_history,
            "study": self.study,
        }

    def _collect_trial_history(self) -> List[Dict[str, Any]]:
        """Collect history of all trials."""
        history = []
        for trial in self.study.trials:
            history.append(
                {
                    "number": trial.number,
                    "value": trial.value,
                    "params": trial.params,
                    "state": trial.state.name,
                    "datetime_start": (
                        trial.datetime_start.isoformat()
                        if trial.datetime_start
                        else None
                    ),
                    "datetime_complete": (
                        trial.datetime_complete.isoformat()
                        if trial.datetime_complete
                        else None
                    ),
                }
            )
        return history

    def save_results(self, output_path: Union[str, Path]) -> None:
        """Save optimization results to JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        results = {
            "best_params": self.study.best_params if self.study else {},
            "best_value": self.study.best_value if self.study else None,
            "n_trials": self.n_trials,
            "direction": self.direction,
            "trial_history": self.trial_history,
        }

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)


def create_backtest_objective(
    prices: pd.DataFrame,
    factor_type: str,
    initial_capital: float = 1_000_000,
    transaction_cost: float = 0.001,
    metric: str = "sharpe_ratio",
) -> Callable[[Trial], float]:
    """
    Create an objective function for backtest-based hyperparameter tuning.

    Args:
        prices: Price data DataFrame.
        factor_type: Type of factor to optimize ("momentum", "value", "size", "volatility").
        initial_capital: Initial capital for backtest.
        transaction_cost: Transaction cost rate.
        metric: Metric to optimize ("sharpe_ratio", "total_return", "cagr", etc.).

    Returns:
        Objective function that takes a Trial and returns a float.
    """
    factor_classes = {
        "momentum": MomentumFactor,
        "value": ValueFactor,
        "size": SizeFactor,
        "volatility": VolatilityFactor,
    }

    if factor_type not in factor_classes:
        raise ValueError(
            f"Unknown factor type: {factor_type}. "
            f"Supported: {list(factor_classes.keys())}"
        )

    FactorClass = factor_classes[factor_type]

    def objective(trial: Trial) -> float:
        """Objective function for Optuna trial."""
        if factor_type == "momentum":
            lookback = trial.suggest_int("lookback", 10, 252, step=1)
            skip_period = trial.suggest_int("skip_period", 0, 5, step=1)
            factor = FactorClass(lookback=lookback, skip_period=skip_period)
        elif factor_type == "volatility":
            lookback = trial.suggest_int("lookback", 10, 126, step=1)
            factor = FactorClass(lookback=lookback)
        else:
            factor = FactorClass()
        signals = factor.compute(prices)
        if signals.empty:
            return (
                float("-inf")
                if metric in ["sharpe_ratio", "total_return"]
                else float("inf")
            )

        signal_series = signals.mean(axis=1)
        signal_matrix = pd.DataFrame(
            dict.fromkeys(prices.columns, signal_series), index=signal_series.index
        )

        common_dates = prices.index.intersection(signal_matrix.index)
        if len(common_dates) == 0:
            return (
                float("-inf")
                if metric in ["sharpe_ratio", "total_return"]
                else float("inf")
            )

        prices_aligned = prices.loc[common_dates]
        signals_aligned = signal_matrix.loc[common_dates]

        try:
            backtest = VectorizedBacktest(
                prices=prices_aligned,
                signals=signals_aligned,
                initial_capital=initial_capital,
                transaction_cost=transaction_cost,
            )
            results = backtest.run(weight_scheme="rank")

            metrics_calc = RiskMetrics(results["returns"])
            metrics = metrics_calc.calculate_all()

            if trial.should_prune():
                raise optuna.TrialPruned()

            metric_value = metrics.get(metric, 0.0)
            return float(metric_value)

        except Exception:
            return (
                float("-inf")
                if metric in ["sharpe_ratio", "total_return"]
                else float("inf")
            )

    return objective


def suggest_hyperparameters(
    trial: Trial, search_space: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Suggest hyperparameters from search space definition.

    Args:
        trial: Optuna trial object.
        search_space: Dictionary defining search space.
            Format:
            {
                "param_name": {
                    "type": "int" | "float" | "categorical",
                    "low": <low_value>,  # for int/float
                    "high": <high_value>,  # for int/float
                    "choices": [<choices>],  # for categorical
                    "log": True/False,  # for float (optional)
                    "step": <step>  # for int/float (optional)
                }
            }

    Returns:
        Dictionary of suggested hyperparameters.
    """
    params = {}
    for param_name, param_config in search_space.items():
        param_type = param_config.get("type", "float")

        if param_type == "int":
            low = param_config["low"]
            high = param_config["high"]
            step = param_config.get("step", 1)
            params[param_name] = trial.suggest_int(param_name, low, high, step=step)

        elif param_type == "float":
            low = param_config["low"]
            high = param_config["high"]
            log = param_config.get("log", False)
            step = param_config.get("step", None)
            params[param_name] = trial.suggest_float(
                param_name, low, high, log=log, step=step
            )

        elif param_type == "categorical":
            choices = param_config["choices"]
            params[param_name] = trial.suggest_categorical(param_name, choices)

        else:
            raise ValueError(f"Unknown parameter type: {param_type}")

    return params
