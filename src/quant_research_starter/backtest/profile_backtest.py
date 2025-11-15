"""Simple profiler to identify hotspots in backtest."""

import cProfile
import pstats
import sys
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from quant_research_starter.backtest.vectorized import VectorizedBacktest
from quant_research_starter.data import SampleDataLoader


def profile_backtest():
    """Profile the backtest to identify hotspots."""
    loader = SampleDataLoader()
    prices = loader.load_sample_prices()

    signals = prices.pct_change(20).fillna(0)

    profiler = cProfile.Profile()
    profiler.enable()

    backtest = VectorizedBacktest(
        prices=prices,
        signals=signals,
        initial_capital=1_000_000,
        transaction_cost=0.001,
    )
    backtest.run(weight_scheme="rank")

    profiler.disable()

    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats("cumulative")
    stats.print_stats(20)

    print("Top 20 functions by cumulative time:")
    print(s.getvalue())

    stats.sort_stats("tottime")
    stats.print_stats(20)

    print("\nTop 20 functions by total time:")
    s2 = StringIO()
    stats = pstats.Stats(profiler, stream=s2)
    stats.sort_stats("tottime")
    stats.print_stats(20)
    print(s2.getvalue())


if __name__ == "__main__":
    profile_backtest()
