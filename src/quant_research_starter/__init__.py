"""Quant Research Starter package public API."""

from .backtest.vectorized import VectorizedBacktest
from .data.sample_loader import SampleDataLoader
from .data.synthetic import SyntheticDataGenerator
from .factors.momentum import CrossSectionalMomentum, MomentumFactor
from .factors.size import SizeFactor
from .factors.value import ValueFactor
from .factors.volatility import IdiosyncraticVolatility, VolatilityFactor
from .metrics.risk import RiskMetrics

__all__ = [
    "VectorizedBacktest",
    "RiskMetrics",
    "SyntheticDataGenerator",
    "SampleDataLoader",
    "MomentumFactor",
    "CrossSectionalMomentum",
    "ValueFactor",
    "SizeFactor",
    "VolatilityFactor",
    "IdiosyncraticVolatility",
]
