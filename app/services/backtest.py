"""
Backtesting service for strategy evaluation.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.strategies import STRATEGY_MAP


class BacktestEngine:
    """
    Backtesting engine for evaluating trading strategies.
    """

    def __init__(
        self, initial_capital: float = 100000.0, commission: float = 0.001, slippage: float = 0.0005
    ):
        """
        Initialize backtest engine.

        Args:
            initial_capital: Starting capital
            commission: Commission rate (e.g., 0.001 = 0.1%)
            slippage: Slippage rate (e.g., 0.0005 = 0.05%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.trades: List[Dict] = []
        self.equity_curve: List[float] = []

    def run(
        self, strategy_type: str, strategy_params: Dict[str, Any], data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Run backtest for a strategy.

        Args:
            strategy_type: Type of strategy
            strategy_params: Strategy parameters
            data: Historical market data

        Returns:
            Dictionary with backtest results
        """
        # Initialize strategy
        if strategy_type not in STRATEGY_MAP:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

        strategy_class = STRATEGY_MAP[strategy_type]
        strategy = strategy_class(strategy_params)

        # Generate signals
        df = strategy.generate_signals(data)

        # Simulate trading
        capital = self.initial_capital
        position = 0
        entry_price = 0
        self.trades = []
        self.equity_curve = [capital]

        for i in range(len(df)):
            row = df.iloc[i]

            # Skip if no valid signal
            if pd.isna(row["signal"]):
                self.equity_curve.append(capital)
                continue

            # Buy signal
            if row["signal"] == 1 and position == 0:
                # Calculate position size
                position_size = strategy.calculate_position_size(capital, row["close"])
                entry_price = row["close"] * (1 + self.slippage)  # Apply slippage
                position = position_size
                cost = position * entry_price
                commission_cost = cost * self.commission
                capital -= cost + commission_cost

                self.trades.append(
                    {
                        "entry_time": row.name,
                        "entry_price": entry_price,
                        "quantity": position,
                        "side": "buy",
                        "commission": commission_cost,
                    }
                )

            # Sell signal
            elif row["signal"] == -1 and position > 0:
                exit_price = row["close"] * (1 - self.slippage)  # Apply slippage
                proceeds = position * exit_price
                commission_cost = proceeds * self.commission
                capital += proceeds - commission_cost

                # Calculate P&L
                pnl = (exit_price - entry_price) * position - (
                    self.trades[-1]["commission"] + commission_cost
                )
                pnl_percent = (pnl / (entry_price * position)) * 100

                self.trades[-1].update(
                    {
                        "exit_time": row.name,
                        "exit_price": exit_price,
                        "pnl": pnl,
                        "pnl_percent": pnl_percent,
                        "status": "closed",
                    }
                )

                position = 0
                entry_price = 0

            # Update equity curve
            if position > 0:
                unrealized_pnl = (row["close"] - entry_price) * position
                self.equity_curve.append(capital + unrealized_pnl)
            else:
                self.equity_curve.append(capital)

        # Calculate performance metrics
        metrics = self.calculate_metrics(df)

        return {
            "initial_capital": self.initial_capital,
            "final_capital": capital,
            "total_return": ((capital - self.initial_capital) / self.initial_capital) * 100,
            "trades": self.trades,
            "equity_curve": self.equity_curve,
            "metrics": metrics,
        }

    def calculate_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate performance metrics.

        Args:
            data: Market data with signals

        Returns:
            Dictionary of performance metrics
        """
        if not self.trades:
            return {}

        # Filter closed trades
        closed_trades = [t for t in self.trades if t.get("status") == "closed"]

        if not closed_trades:
            return {}

        # Calculate metrics
        total_trades = len(closed_trades)
        profitable_trades = len([t for t in closed_trades if t.get("pnl", 0) > 0])
        losing_trades = len([t for t in closed_trades if t.get("pnl", 0) < 0])

        win_rate = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0

        profits = [t["pnl"] for t in closed_trades if t.get("pnl", 0) > 0]
        losses = [abs(t["pnl"]) for t in closed_trades if t.get("pnl", 0) < 0]

        avg_profit = np.mean(profits) if profits else 0
        avg_loss = np.mean(losses) if losses else 0

        profit_factor = sum(profits) / sum(losses) if losses and sum(losses) > 0 else 0

        # Calculate Sharpe ratio
        returns = pd.Series(self.equity_curve).pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0

        # Calculate Sortino ratio (downside deviation)
        downside_returns = returns[returns < 0]
        sortino_ratio = (
            (returns.mean() / downside_returns.std()) * np.sqrt(252)
            if len(downside_returns) > 0 and downside_returns.std() > 0
            else 0
        )

        # Calculate max drawdown
        equity_series = pd.Series(self.equity_curve)
        cumulative_max = equity_series.cummax()
        drawdown = (equity_series - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min() * 100

        return {
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "max_drawdown": max_drawdown,
        }
