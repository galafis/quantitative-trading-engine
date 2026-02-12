"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Quantitative Trading Engine"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "Professional quantitative trading platform with "
        "backtesting and strategy optimization"
    )

    # Database
    DATABASE_URL: str = "postgresql://trading:trading123@localhost:5432/trading_db"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Market Data
    MARKET_DATA_PROVIDER: str = "yahoo"
    DEFAULT_SYMBOL: str = "^BVSP"  # Bovespa Index

    # Trading Parameters
    DEFAULT_INITIAL_CAPITAL: float = 100000.0
    DEFAULT_COMMISSION: float = 0.001  # 0.1%
    DEFAULT_SLIPPAGE: float = 0.0005  # 0.05%


settings = Settings()
