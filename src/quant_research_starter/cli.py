"""Command-line interface for quant research pipeline."""

import json
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd

from .backtest import VectorizedBacktest
from .data import SampleDataLoader, SyntheticDataGenerator
from .factors import MomentumFactor, SizeFactor, ValueFactor, VolatilityFactor
from .metrics import RiskMetrics, create_equity_curve_plot


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
    prices = generator.generate_price_data(
        n_symbols=symbols, days=days, start_date="2020-01-01"
    )

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

    # Combine factors (simple average for demo)
    combined_signals = pd.DataFrame({k: v.mean(axis=1) for k, v in factor_data.items()})
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
        # Use composite signal if available, otherwise first column
        if "composite" in signals_data.columns:
            signals = signals_data["composite"]
        else:
            signals = signals_data.iloc[:, 0]
    else:
        click.echo("Signals file not found, computing demo factors...")
        momentum = MomentumFactor(lookback=63)
        signals = momentum.compute(prices).mean(axis=1)

    # Ensure signals align with prices
    common_dates = prices.index.intersection(signals.index)
    prices = prices.loc[common_dates]
    signals = signals.loc[common_dates]

    # Expand signals to all symbols (simplified - same signal for all)
    signal_matrix = pd.DataFrame(
        dict.fromkeys(prices.columns, signals), index=signals.index
    )

    # Run backtest
    backtest = VectorizedBacktest(
        prices=prices,
        signals=signal_matrix,
        initial_capital=initial_capital,
        transaction_cost=0.001,
    )

    results = backtest.run(weight_scheme="rank")

    # Calculate metrics
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

    # Generate plot
    if plot:
        plt.figure(figsize=(12, 8))

        # Plot portfolio value
        plt.subplot(2, 1, 1)
        plt.plot(results["portfolio_value"].index, results["portfolio_value"].values)
        plt.title("Portfolio Value")
        plt.ylabel("USD")
        plt.grid(True)

        # Plot returns
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

    # Generate Plotly HTML chart if requested
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


if __name__ == "__main__":
    cli()
