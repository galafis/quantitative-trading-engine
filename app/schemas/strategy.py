"""
Strategy Pydantic schemas.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional, Dict, Any
from datetime import datetime


class StrategyBase(BaseModel):
    """Base strategy schema."""

    name: str = Field(..., description="Strategy name")
    description: Optional[str] = Field(None, description="Strategy description")
    strategy_type: Literal["momentum", "mean_reversion", "breakout"] = Field(
        ..., description="Strategy type (momentum, mean_reversion, breakout)"
    )
    parameters: Dict[str, Any] = Field(..., description="Strategy parameters")
    is_active: bool = Field(True, description="Whether strategy is active")


class StrategyCreate(StrategyBase):
    """Schema for creating a strategy."""

    pass


class StrategyUpdate(BaseModel):
    """Schema for updating a strategy."""

    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class StrategyResponse(StrategyBase):
    """Schema for strategy response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class BacktestRequest(BaseModel):
    """Schema for backtest request."""

    strategy_id: int = Field(..., description="Strategy ID")
    symbol: str = Field(..., description="Trading symbol")
    start_date: datetime = Field(..., description="Backtest start date")
    end_date: datetime = Field(..., description="Backtest end date")
    initial_capital: float = Field(100000.0, description="Initial capital")
    commission: float = Field(0.001, description="Commission rate")
    slippage: float = Field(0.0005, description="Slippage rate")


class BacktestResponse(BaseModel):
    """Schema for backtest response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    strategy_id: int
    symbol: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    total_return: float
    sharpe_ratio: Optional[float]
    sortino_ratio: Optional[float]
    max_drawdown: Optional[float]
    win_rate: Optional[float]
    total_trades: int
    profitable_trades: int
    losing_trades: int
    avg_profit: Optional[float]
    avg_loss: Optional[float]
    profit_factor: Optional[float]
    created_at: datetime


class TradeResponse(BaseModel):
    """Schema for trade response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    strategy_id: int
    symbol: str
    side: str
    quantity: float
    entry_price: float
    exit_price: Optional[float]
    entry_time: datetime
    exit_time: Optional[datetime]
    pnl: Optional[float]
    pnl_percent: Optional[float]
    commission: float
    slippage: float
    status: str
    notes: Optional[str]


class PerformanceMetrics(BaseModel):
    """Performance metrics schema."""

    total_return: float
    annualized_return: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: float
