"""Command-line interface for quant research pipeline."""

import json
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

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

    with tqdm(total=3, desc="Data Generation") as pbar:
        pbar.set_description("Initializing data generator")
        generator = SyntheticDataGenerator()
        pbar.update(1)

        pbar.set_description("Generating price data")
        prices = generator.generate_price_data(
            n_symbols=symbols, days=days, start_date="2020-01-01"
        )
        pbar.update(1)

        # Ensure output directory exists and save
        pbar.set_description("Saving data to file")
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        prices.to_csv(output_path)
        pbar.update(1)

    click.echo(f"✅ Generated {symbols} symbols for {days} days -> {output}")


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

    # Load data with progress
    with tqdm(total=2, desc="Loading Data") as pbar:
        pbar.set_description("Checking data file")
        if Path(data_file).exists():
            prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
        else:
            click.echo("Data file not found, using sample data...")
            loader = SampleDataLoader()
            prices = loader.load_sample_prices()
        pbar.update(1)

        pbar.set_description("Data validation")
        n_symbols = len(prices.columns)
        n_days = len(prices)
        pbar.set_postfix(symbols=n_symbols, days=n_days, refresh=False)
        pbar.update(1)

    # Compute selected factors with progress tracking
    factor_data = {}
    selected_factors = list(factors)
    
    with tqdm(total=len(selected_factors) + 2, desc="Factor Computation") as pbar:
        if "momentum" in factors:
            pbar.set_description("Computing momentum factor")
            momentum = MomentumFactor(lookback=63)
            factor_data["momentum"] = momentum.compute(prices)
            pbar.update(1)

        if "value" in factors:
            pbar.set_description("Computing value factor")
            value = ValueFactor()
            factor_data["value"] = value.compute(prices)
            pbar.update(1)

        if "size" in factors:
            pbar.set_description("Computing size factor")
            size = SizeFactor()
            factor_data["size"] = size.compute(prices)
            pbar.update(1)

        if "volatility" in factors:
            pbar.set_description("Computing volatility factor")
            vol = VolatilityFactor(lookback=21)
            factor_data["volatility"] = vol.compute(prices)
            pbar.update(1)

        # Combine factors
        pbar.set_description("Combining factors")
        combined_signals = pd.DataFrame({k: v.mean(axis=1) for k, v in factor_data.items()})
        combined_signals["composite"] = combined_signals.mean(axis=1)
        pbar.update(1)

        # Save results
        pbar.set_description("Saving factor results")
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined_signals.to_csv(output_path)
        pbar.update(1)

    click.echo(f"✅ Factors computed -> {output}")


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

    # Load data and signals with progress
    with tqdm(total=4, desc="Loading Input Data") as pbar:
        pbar.set_description("Loading price data")
        if Path(data_file).exists():
            prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
        else:
            click.echo("Data file not found, using sample data...")
            loader = SampleDataLoader()
            prices = loader.load_sample_prices()
        pbar.update(1)

        pbar.set_description("Loading signal data")
        if Path(signals_file).exists():
            signals_data = pd.read_csv(signals_file, index_col=0, parse_dates=True)
            if "composite" in signals_data.columns:
                signals = signals_data["composite"]
            else:
                signals = signals_data.iloc[:, 0]
        else:
            click.echo("Signals file not found, computing demo factors...")
            momentum = MomentumFactor(lookback=63)
            signals = momentum.compute(prices).mean(axis=1)
        pbar.update(1)

        pbar.set_description("Aligning data")
        common_dates = prices.index.intersection(signals.index)
        prices = prices.loc[common_dates]
        signals = signals.loc[common_dates]
        pbar.update(1)

        pbar.set_description("Expanding signals")
        signal_matrix = pd.DataFrame(
            dict.fromkeys(prices.columns, signals), index=signals.index
        )
        pbar.update(1)

    # Run backtest (progress handled inside VectorizedBacktest)
    with tqdm(total=1, desc="Running Backtest") as pbar:
        backtest = VectorizedBacktest(
            prices=prices,
            signals=signal_matrix,
            initial_capital=initial_capital,
            transaction_cost=0.001,
        )

        results = backtest.run(weight_scheme="rank")
        pbar.update(1)

    # Calculate metrics with progress
    with tqdm(total=2, desc="Calculating Metrics") as pbar:
        pbar.set_description("Computing risk metrics")
        metrics_calc = RiskMetrics(results["returns"])
        metrics = metrics_calc.calculate_all()
        pbar.update(1)

        pbar.set_description("Saving results")
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        results_dict = {
            "metrics": metrics,
            "portfolio_value": results["portfolio_value"].tolist(),
            "dates": results["portfolio_value"].index.strftime("%Y-%m-%d").tolist(),
        }

        with open(output_path, "w") as f:
            json.dump(results_dict, f, indent=2)
        pbar.update(1)

    # Generate plots with progress
    if plot or plotly:
        with tqdm(total=plot + plotly, desc="Generating Visualizations") as pbar:
            if plot:
                pbar.set_description("Creating matplotlib plot")
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

                click.echo(f"📊 Plot saved -> {plot_path}")
                pbar.update(1)

            if plotly:
                pbar.set_description("Creating Plotly chart")
                html_path = output_path.parent / "backtest_plot.html"

                create_equity_curve_plot(
                    dates=results_dict["dates"],
                    portfolio_values=results_dict["portfolio_value"],
                    initial_capital=initial_capital,
                    output_path=str(html_path),
                    plot_type="html",
                )

                click.echo(f"📈 Interactive chart saved -> {html_path}")
                pbar.update(1)

    # Final results summary
    click.echo("🎯 Backtest completed!")
    click.echo(f"💰 Final portfolio value: ${results['final_value']:,.2f}")
    click.echo(f"📈 Total return: {results['total_return']:.2%}")
    click.echo(f"⚡ Sharpe ratio: {metrics['sharpe_ratio']:.2f}")
    click.echo(f"💾 Results saved -> {output}")


if __name__ == "__main__":
    cli()