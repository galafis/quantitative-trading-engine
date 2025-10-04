"""
Trading strategies.
"""
from app.strategies.base import BaseStrategy
from app.strategies.momentum import MomentumStrategy
from app.strategies.mean_reversion import MeanReversionStrategy
from app.strategies.breakout import BreakoutStrategy

STRATEGY_MAP = {
    'momentum': MomentumStrategy,
    'mean_reversion': MeanReversionStrategy,
    'breakout': BreakoutStrategy
}

__all__ = [
    "BaseStrategy",
    "MomentumStrategy",
    "MeanReversionStrategy",
    "BreakoutStrategy",
    "STRATEGY_MAP"
]
