"""
Base strategy class for all trading strategies.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    
    All strategies must implement the generate_signals method.
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize strategy with parameters.
        
        Args:
            parameters: Dictionary of strategy parameters
        """
        self.parameters = parameters
        self.name = self.__class__.__name__
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on market data.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with additional 'signal' column (1=buy, -1=sell, 0=hold)
        """
        pass
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate input data has required columns.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        return all(col in data.columns for col in required_columns)
    
    def calculate_position_size(
        self, 
        capital: float, 
        price: float, 
        risk_per_trade: float = 0.02
    ) -> int:
        """
        Calculate position size based on capital and risk.
        
        Args:
            capital: Available capital
            price: Current price
            risk_per_trade: Risk per trade as fraction of capital
            
        Returns:
            Number of shares/contracts to trade
        """
        risk_amount = capital * risk_per_trade
        position_size = int(risk_amount / price)
        return max(1, position_size)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get strategy parameters."""
        return self.parameters
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """Set strategy parameters."""
        self.parameters.update(parameters)
