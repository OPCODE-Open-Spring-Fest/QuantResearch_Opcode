<<<<<<< HEAD
"""Factors module public API."""

from .base import Factor
from .momentum import CrossSectionalMomentum, MomentumFactor
from .size import SizeFactor
from .value import ValueFactor
from .volatility import IdiosyncraticVolatility, VolatilityFactor

__all__ = [
    "Factor",
    "MomentumFactor",
    "CrossSectionalMomentum",
    "ValueFactor",
    "SizeFactor",
    "VolatilityFactor",
    "IdiosyncraticVolatility",
]
=======
"""Factors module public API."""

from .base import Factor
from .bollinger import BollingerBandsFactor
from .momentum import CrossSectionalMomentum, MomentumFactor
from .size import SizeFactor
from .value import ValueFactor
from .volatility import IdiosyncraticVolatility, VolatilityFactor

__all__ = [
    "Factor",
    "BollingerBandsFactor",
    "CrossSectionalMomentum",
    "MomentumFactor",
    "SizeFactor",
    "ValueFactor",
    "IdiosyncraticVolatility",
    "VolatilityFactor",
]
>>>>>>> 8d5d7c51f2ba0fc6db1b9abe844cee2182014d3c
