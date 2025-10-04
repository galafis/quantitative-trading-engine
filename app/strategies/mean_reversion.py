"""
Mean reversion trading strategy.
"""
import pandas as pd
import numpy as np
from app.strategies.base import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """
    Mean reversion strategy based on Bollinger Bands.
    
    Generates buy signals when price touches lower band,
    and sell signals when price touches upper band.
    """
    
    def __init__(self, parameters: dict = None):
        """
        Initialize mean reversion strategy.
        
        Args:
            parameters: Strategy parameters
                - period: Bollinger Bands period (default: 20)
                - std_dev: Number of standard deviations (default: 2)
                - rsi_period: RSI period for confirmation (default: 14)
                - rsi_oversold: RSI oversold level (default: 30)
                - rsi_overbought: RSI overbought level (default: 70)
        """
        default_params = {
            'period': 20,
            'std_dev': 2,
            'rsi_period': 14,
            'rsi_oversold': 30,
            'rsi_overbought': 70
        }
        if parameters:
            default_params.update(parameters)
        super().__init__(default_params)
    
    def calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Relative Strength Index.
        
        Args:
            prices: Price series
            period: RSI period
            
        Returns:
            RSI series
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate mean reversion signals based on Bollinger Bands and RSI.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with 'signal' column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format")
        
        df = data.copy()
        period = self.parameters['period']
        std_dev = self.parameters['std_dev']
        rsi_period = self.parameters['rsi_period']
        rsi_oversold = self.parameters['rsi_oversold']
        rsi_overbought = self.parameters['rsi_overbought']
        
        # Calculate Bollinger Bands
        df['middle_band'] = df['close'].rolling(window=period).mean()
        df['std'] = df['close'].rolling(window=period).std()
        df['upper_band'] = df['middle_band'] + (df['std'] * std_dev)
        df['lower_band'] = df['middle_band'] - (df['std'] * std_dev)
        
        # Calculate RSI
        df['rsi'] = self.calculate_rsi(df['close'], rsi_period)
        
        # Generate signals
        df['signal'] = 0
        
        # Buy when price touches lower band and RSI is oversold
        buy_condition = (df['close'] <= df['lower_band']) & (df['rsi'] < rsi_oversold)
        df.loc[buy_condition, 'signal'] = 1
        
        # Sell when price touches upper band and RSI is overbought
        sell_condition = (df['close'] >= df['upper_band']) & (df['rsi'] > rsi_overbought)
        df.loc[sell_condition, 'signal'] = -1
        
        return df
