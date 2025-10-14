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

    def get_latest_price(self, symbol: str) -> float:
        """
        Get latest price for a symbol.

        Args:
            symbol: Trading symbol

        Returns:
            Latest price
        """
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            raise ValueError(f"No data available for {symbol}")
        return data["Close"].iloc[-1]  # type: ignore[no-any-return]

    def get_symbols_list(self) -> list:
        """
        Get list of available symbols.

        Returns:
            List of symbols
        """
        # Common Brazilian market symbols
        return [
            "^BVSP",  # Bovespa Index
            "PETR4.SA",  # Petrobras
            "VALE3.SA",  # Vale
            "ITUB4.SA",  # Itaú
            "BBDC4.SA",  # Bradesco
            "ABEV3.SA",  # Ambev
            "B3SA3.SA",  # B3
            "WEGE3.SA",  # WEG
            "RENT3.SA",  # Localiza
            "MGLU3.SA",  # Magazine Luiza
        ]
