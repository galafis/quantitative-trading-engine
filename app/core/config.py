"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Quantitative Trading Engine"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "Professional quantitative trading platform with "
        "backtesting and strategy optimization"
    )

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "postgresql://trading:trading123@localhost:5432/trading_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    # Market Data
    MARKET_DATA_PROVIDER: str = "yahoo"
    DEFAULT_SYMBOL: str = "^BVSP"  # Bovespa Index

    # Trading Parameters
    DEFAULT_INITIAL_CAPITAL: float = 100000.0
    DEFAULT_COMMISSION: float = 0.001  # 0.1%
    DEFAULT_SLIPPAGE: float = 0.0005  # 0.05%

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
