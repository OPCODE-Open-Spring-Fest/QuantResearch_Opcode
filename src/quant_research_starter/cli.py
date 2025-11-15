"""Command-line interface for quant research pipeline."""

import json
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from tqdm import tqdm

from .backtest import VectorizedBacktest
from .data import SampleDataLoader, SyntheticDataGenerator
from .factors import MomentumFactor, SizeFactor, ValueFactor, VolatilityFactor
from .metrics import RiskMetrics, create_equity_curve_plot
from .tuning import OptunaRunner, create_backtest_objective


@click.group()
def cli():
    """Quantitative Research Starter CLI"""
    pass


@cli.command()
@click.option(
    "--output", "-o", default="data/sample_prices.csv", help="Output file path"
)
@click.option("--symbols", "-s", default=10, help="Number of symbols")
@click.option("--days", "-d", default=1000, help="Number of trading days")
def generate_data(output, symbols, days):
    """Generate synthetic price data."""
    click.echo("Generating synthetic price data...")

    generator = SyntheticDataGenerator()
    all_prices = []
    for _ in tqdm(range(symbols), desc="Generating price series"):
        prices = generator.generate_price_data(
            n_symbols=1, days=days, start_date="2020-01-01"
        )
        all_prices.append(prices)

    prices = pd.concat(all_prices, axis=1)

    # Ensure output directory exists
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    prices.to_csv(output_path)
    click.echo(f"Generated {symbols} symbols for {days} days -> {output}")


@cli.command()
@click.option(
    "--data-file",
    "-d",
    default="data_sample/sample_prices.csv",
    help="Price data file path",
)
@click.option(
    "--factors",
    "-f",
    multiple=True,
    type=click.Choice(["momentum", "value", "size", "volatility"]),
    default=["momentum", "value"],
)
@click.option(
    "--output", "-o", default="output/factors.csv", help="Output file for factors"
)
def compute_factors(data_file, factors, output):
    """Compute factors from price data."""
    click.echo(f"Computing factors: {list(factors)}")

    # Load data
    if Path(data_file).exists():
        prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    else:
        click.echo("Data file not found, using sample data...")
        loader = SampleDataLoader()
        prices = loader.load_sample_prices()

    # Compute selected factors
    factor_data = {}

    if "momentum" in factors:
        click.echo("Computing momentum factor...")
        momentum = MomentumFactor(lookback=63)
        factor_data["momentum"] = momentum.compute(prices)

    if "value" in factors:
        click.echo("Computing value factor...")
        value = ValueFactor()
        factor_data["value"] = value.compute(prices)

    if "size" in factors:
        click.echo("Computing size factor...")
        size = SizeFactor()
        factor_data["size"] = size.compute(prices)

    if "volatility" in factors:
        click.echo("Computing volatility factor...")
        vol = VolatilityFactor(lookback=21)
        factor_data["volatility"] = vol.compute(prices)

    combined_signals_dict = {}
    for k, v in tqdm(factor_data.items(), desc="Averaging factors"):
        combined_signals_dict[k] = v.mean(axis=1)

    combined_signals = pd.DataFrame(combined_signals_dict)
    combined_signals["composite"] = combined_signals.mean(axis=1)

    # Save results
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined_signals.to_csv(output_path)

    click.echo(f"Factors computed -> {output}")


@cli.command()
@click.option(
    "--data-file",
    "-d",
    default="data_sample/sample_prices.csv",
    help="Price data file path",
)
@click.option(
    "--signals-file",
    "-s",
    default="output/factors.csv",
    help="Factor signals file path",
)
@click.option("--initial-capital", "-c", default=1000000, help="Initial capital")
@click.option(
    "--output",
    "-o",
    default="output/backtest_results.json",
    help="Output file for results",
)
@click.option("--plot/--no-plot", default=True, help="Generate plot")
@click.option(
    "--plotly",
    is_flag=True,
    default=False,
    help="Also generate interactive Plotly HTML chart",
)
def backtest(data_file, signals_file, initial_capital, output, plot, plotly):
    """Run backtest with given signals."""
    click.echo("Running backtest...")

    # Load data
    if Path(data_file).exists():
        prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    else:
        click.echo("Data file not found, using sample data...")
        loader = SampleDataLoader()
        prices = loader.load_sample_prices()

    # Load signals
    if Path(signals_file).exists():
        signals_data = pd.read_csv(signals_file, index_col=0, parse_dates=True)
        # If a 'composite' signal column exists, use it; otherwise, fall back to the first available signal column.
        if "composite" in signals_data.columns:
            signals = signals_data["composite"]
        else:
            signals = signals_data.iloc[:, 0]
    else:
        click.echo("Signals file not found, computing demo factors...")
        momentum = MomentumFactor(lookback=63)
        signals = momentum.compute(prices).mean(axis=1)

    # Align dates
    common_dates = prices.index.intersection(signals.index)
    prices = prices.loc[common_dates]
    signals = signals.loc[common_dates]

    # Expand signals across symbols
    signal_matrix = pd.DataFrame(
        dict.fromkeys(prices.columns, signals), index=signals.index
    )

    # Use the original vectorized run() method for performance

    backtest = VectorizedBacktest(
        prices=prices,
        signals=signal_matrix,
        initial_capital=initial_capital,
        transaction_cost=0.001,
    )
    results = backtest.run(weight_scheme="rank")

    # Metrics
    metrics_calc = RiskMetrics(results["returns"])
    metrics = metrics_calc.calculate_all()

    # Save results
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results_dict = {
        "metrics": metrics,
        "portfolio_value": results["portfolio_value"].tolist(),
        "dates": results["portfolio_value"].index.strftime("%Y-%m-%d").tolist(),
    }

    with open(output_path, "w") as f:
        json.dump(results_dict, f, indent=2)

    # Plotting
    if plot:
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 1, 1)
        plt.plot(results["portfolio_value"].index, results["portfolio_value"].values)
        plt.title("Portfolio Value")
        plt.ylabel("USD")
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.bar(results["returns"].index, results["returns"].values, alpha=0.7)
        plt.title("Daily Returns")
        plt.ylabel("Return")
        plt.grid(True)

        plt.tight_layout()
        plot_path = output_path.parent / "backtest_plot.png"
        plt.savefig(plot_path)
        plt.close()

        click.echo(f"Plot saved -> {plot_path}")

    if plotly:
        html_path = output_path.parent / "backtest_plot.html"

        create_equity_curve_plot(
            dates=results_dict["dates"],
            portfolio_values=results_dict["portfolio_value"],
            initial_capital=initial_capital,
            output_path=str(html_path),
            plot_type="html",
        )

        click.echo(f"Plotly HTML chart saved -> {html_path}")

    click.echo("Backtest completed!")
    click.echo(f"Final portfolio value: ${results['final_value']:,.2f}")
    click.echo(f"Total return: {results['total_return']:.2%}")
    click.echo(f"Sharpe ratio: {metrics['sharpe_ratio']:.2f}")
    click.echo(f"Results saved -> {output}")


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="YAML configuration file for hyperparameter tuning",
)
@click.option(
    "--data-file",
    "-d",
    default="data_sample/sample_prices.csv",
    help="Price data file path",
)
@click.option(
    "--factor-type",
    "-f",
    type=click.Choice(["momentum", "value", "size", "volatility"]),
    default="momentum",
    help="Factor type to optimize",
)
@click.option(
    "--n-trials",
    "-n",
    default=100,
    help="Number of optimization trials",
)
@click.option(
    "--metric",
    "-m",
    default="sharpe_ratio",
    help="Metric to optimize (sharpe_ratio, total_return, cagr, etc.)",
)
@click.option(
    "--output",
    "-o",
    default="output/tuning_results.json",
    help="Output file for tuning results",
)
@click.option(
    "--storage",
    "-s",
    default=None,
    help="RDB storage URL (e.g., sqlite:///optuna.db) for distributed tuning",
)
@click.option(
    "--pruner",
    "-p",
    type=click.Choice(["none", "median", "percentile"]),
    default="median",
    help="Pruning strategy for early stopping",
)
@click.option(
    "--study-name",
    default="optuna_study",
    help="Name of the Optuna study",
)
def autotune(
    config,
    data_file,
    factor_type,
    n_trials,
    metric,
    output,
    storage,
    pruner,
    study_name,
):
    """Run hyperparameter optimization with Optuna."""
    click.echo("Starting hyperparameter optimization...")

    # Load configuration from YAML if provided
    search_space = None
    if config:
        with open(config, "r") as f:
            config_data = yaml.safe_load(f)
            data_file = config_data.get("data_file", data_file)
            factor_type = config_data.get("factor_type", factor_type)
            n_trials = config_data.get("n_trials", n_trials)
            metric = config_data.get("metric", metric)
            output = config_data.get("output", output)
            storage = config_data.get("storage", storage)
            pruner = config_data.get("pruner", pruner)
            study_name = config_data.get("study_name", study_name)
            search_space = config_data.get("search_space", None)

    # Load data
    if Path(data_file).exists():
        prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    else:
        click.echo("Data file not found, using sample data...")
        loader = SampleDataLoader()
        prices = loader.load_sample_prices()

    click.echo(f"Optimizing {factor_type} factor with {n_trials} trials...")
    click.echo(f"Optimizing metric: {metric}")

    # Create objective function
    objective = create_backtest_objective(
        prices=prices,
        factor_type=factor_type,
        metric=metric,
        search_space=search_space,
    )

    # Create and run Optuna runner
    runner = OptunaRunner(
        objective=objective,
        n_trials=n_trials,
        study_name=study_name,
        storage=storage,
        pruner=pruner,
        direction=(
            "maximize"
            if metric in ["sharpe_ratio", "total_return", "cagr"]
            else "minimize"
        ),
    )

    # Run optimization
    results = runner.optimize()

    # Save results
    runner.save_results(output)

    click.echo("\n" + "=" * 60)
    click.echo("Optimization Results")
    click.echo("=" * 60)
    click.echo(f"Best parameters: {results['best_params']}")
    click.echo(f"Best {metric}: {results['best_value']:.4f}")
    click.echo(f"Total trials: {len(results['trial_history'])}")
    click.echo(f"Results saved -> {output}")


if __name__ == "__main__":
    cli()
