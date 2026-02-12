"""
Market data service for fetching historical data.
"""
import pandas as pd
import yfinance as yf
from datetime import datetime


class MarketDataService:
    """
    Service for fetching market data from various sources.
    """

    def __init__(self, provider: str = "yahoo"):
        """
        Initialize market data service.

        Args:
            provider: Data provider (currently only 'yahoo' supported)
        """
        self.provider = provider

    def get_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Fetch historical market data.

        Args:
            symbol: Trading symbol
            start_date: Start date
            end_date: End date
            interval: Data interval (1d, 1h, etc.)

        Returns:
            DataFrame with OHLCV data
        """
        if self.provider == "yahoo":
            return self._fetch_yahoo_data(symbol, start_date, end_date, interval)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _fetch_yahoo_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str,
    ) -> pd.DataFrame:
        """
        Fetch data from Yahoo Finance.

        Args:
            symbol: Trading symbol
            start_date: Start date
            end_date: End date
            interval: Data interval

        Returns:
            DataFrame with OHLCV data
        """
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)

        # Standardize column names
        df.columns = [col.lower() for col in df.columns]

        # Ensure required columns exist
        required_columns = ["open", "high", "low", "close", "volume"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        return df[required_columns]  # type: ignore[no-any-return]
