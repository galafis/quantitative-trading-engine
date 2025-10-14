"""
Breakout trading strategy.
"""
import pandas as pd
from app.strategies.base import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """
    Breakout strategy based on support and resistance levels.

    Generates buy signals when price breaks above resistance,
    and sell signals when price breaks below support.
    """

    def __init__(self, parameters: dict = None):
        """
        Initialize breakout strategy.

        Args:
            parameters: Strategy parameters
                - lookback_period: Period to identify support/resistance (default: 20)
                - breakout_threshold: Percentage above/below level for breakout (default: 0.02)
                - volume_confirmation: Require volume confirmation (default: True)
                - volume_multiplier: Volume must be X times average (default: 1.5)
        """
        default_params = {
            "lookback_period": 20,
            "breakout_threshold": 0.02,
            "volume_confirmation": True,
            "volume_multiplier": 1.5,
        }
        if parameters:
            default_params.update(parameters)
        super().__init__(default_params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate breakout signals based on support/resistance levels.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with 'signal' column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format")

        df = data.copy()
        lookback = self.parameters["lookback_period"]
        threshold = self.parameters["breakout_threshold"]
        volume_confirmation = self.parameters["volume_confirmation"]
        volume_multiplier = self.parameters["volume_multiplier"]

        # Calculate support and resistance levels
        df["resistance"] = df["high"].rolling(window=lookback).max()
        df["support"] = df["low"].rolling(window=lookback).min()

        # Calculate average volume
        df["avg_volume"] = df["volume"].rolling(window=lookback).mean()

        # Calculate breakout levels (with threshold)
        df["breakout_up"] = df["resistance"] * (1 + threshold)
        df["breakout_down"] = df["support"] * (1 - threshold)

        # Generate signals
        df["signal"] = 0

        # Buy signal: price breaks above resistance
        buy_condition = df["close"] > df["breakout_up"]
        if volume_confirmation:
            buy_condition = buy_condition & (df["volume"] > df["avg_volume"] * volume_multiplier)
        df.loc[buy_condition, "signal"] = 1

        # Sell signal: price breaks below support
        sell_condition = df["close"] < df["breakout_down"]
        if volume_confirmation:
            sell_condition = sell_condition & (df["volume"] > df["avg_volume"] * volume_multiplier)
        df.loc[sell_condition, "signal"] = -1

        return df
