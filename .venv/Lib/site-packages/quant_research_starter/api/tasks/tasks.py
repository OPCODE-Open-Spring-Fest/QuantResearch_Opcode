"""Celery tasks for running backtests and emitting progress via Redis pub/sub."""
from __future__ import annotations
import os
import json
import time
from celery.utils.log import get_task_logger
from redis import Redis

from .celery_app import celery_app

from quant_research_starter.backtest.vectorized import VectorizedBacktest
from quant_research_starter.data.sample_loader import SampleDataLoader
from quant_research_starter.metrics.risk import RiskMetrics

from ..tasks.sync_db import update_job_status
from .. import models
from ..db import DATABASE_URL

logger = get_task_logger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = Redis.from_url(REDIS_URL)


@celery_app.task(bind=True, name="quant_research_starter.api.tasks.tasks.run_backtest")
def run_backtest(self, job_id: str, params: dict):
    """Run a backtest synchronously in worker process and publish progress to Redis."""
    logger.info("Starting backtest job %s", job_id)
    channel = f"backtest:{job_id}"
    redis_client.publish(channel, json.dumps({"type": "started"}))
    try:
        # mark job as running in DB
        update_job_status(job_id, "running")
    except Exception:
        logger.exception("Failed to update job status to running")

    # Load prices
    data_file = params.get("data_file")
    if data_file and os.path.exists(data_file):
        import pandas as pd

        prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    else:
        loader = SampleDataLoader()
        prices = loader.load_sample_prices()

    # Signals
    signals_file = params.get("signals_file")
    if signals_file and os.path.exists(signals_file):
        import pandas as pd

        signals_df = pd.read_csv(signals_file, index_col=0, parse_dates=True)
        if "composite" in signals_df.columns:
            signals = signals_df["composite"]
        else:
            signals = signals_df.iloc[:, 0]
    else:
        # compute demo momentum
        from quant_research_starter.factors.momentum import MomentumFactor

        mom = MomentumFactor(lookback=63)
        signals = mom.compute(prices).mean(axis=1)

    # Align & expand
    common_dates = prices.index.intersection(signals.index)
    prices = prices.loc[common_dates]
    signals = signals.loc[common_dates]
    signal_matrix = signals.to_frame().T
    signal_matrix = signal_matrix.reindex(columns=prices.columns).ffill().T

    # Run backtest
    backtester = VectorizedBacktest(prices=prices, signals=signal_matrix, initial_capital=params.get("initial_capital", 1_000_000))
    redis_client.publish(channel, json.dumps({"type": "progress", "percent": 10}))

    results = backtester.run(weight_scheme=params.get("weight_scheme", "rank"))
    redis_client.publish(channel, json.dumps({"type": "progress", "percent": 90}))

    # Metrics
    rm = RiskMetrics(results["returns"])
    metrics = rm.calculate_all()

    out = {
        "metrics": metrics,
        "portfolio_value": results["portfolio_value"].tolist(),
        "dates": results["portfolio_value"].index.strftime("%Y-%m-%d").tolist(),
    }

    output_dir = os.getenv("OUTPUT_DIR", "output")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"backtest_{job_id}.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    # Update job record in DB with result path and mark done
    try:
        update_job_status(job_id, "done", result_path=out_path)
    except Exception:
        logger.exception("Failed to update job status to done")

    # Publish done
    redis_client.publish(channel, json.dumps({"type": "done", "result_path": out_path}))

    return {"job_id": job_id, "result_path": out_path}
