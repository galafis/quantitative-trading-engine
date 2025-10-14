"""
Momentum trading strategy.
"""
import pandas as pd
from app.strategies.base import BaseStrategy


class MomentumStrategy(BaseStrategy):
    """
    Momentum strategy based on moving average crossover.

    Generates buy signals when fast MA crosses above slow MA,
    and sell signals when fast MA crosses below slow MA.
    """

    def __init__(self, parameters: dict | None = None):
        """
        Initialize momentum strategy.

        Args:
            parameters: Strategy parameters
                - fast_period: Fast moving average period (default: 10)
                - slow_period: Slow moving average period
                  (default: 30)
                - ma_type: Type of moving average
                  ('sma' or 'ema', default: 'sma')
        """
        default_params = {
            "fast_period": 10,
            "slow_period": 30,
            "ma_type": "sma",
        }
        if parameters:
            default_params.update(parameters)
        super().__init__(default_params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate momentum signals based on moving average crossover.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with 'signal' column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format")

        df = data.copy()
        fast_period = self.parameters["fast_period"]
        slow_period = self.parameters["slow_period"]
        ma_type = self.parameters["ma_type"]

        # Calculate moving averages
        if ma_type == "sma":
            df["fast_ma"] = df["close"].rolling(window=fast_period).mean()
            df["slow_ma"] = df["close"].rolling(window=slow_period).mean()
        elif ma_type == "ema":
            df["fast_ma"] = df["close"].ewm(span=fast_period, adjust=False).mean()
            df["slow_ma"] = df["close"].ewm(span=slow_period, adjust=False).mean()
        else:
            raise ValueError(f"Invalid MA type: {ma_type}")

        # Generate signals
        df["signal"] = 0
        df.loc[df["fast_ma"] > df["slow_ma"], "signal"] = 1  # Buy
        df.loc[df["fast_ma"] < df["slow_ma"], "signal"] = -1  # Sell

        # Detect crossovers
        # (only generate signal on crossover, not continuously)
        df["position"] = df["signal"].diff()

        return df
