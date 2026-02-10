"""
Simple Backtest Example
Author: Gabriel Demetrios Lafis

This example demonstrates how to run a simple backtest using the momentum strategy.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402
import numpy as np  # noqa: E402
from datetime import datetime  # noqa: E402
from app.strategies.momentum import MomentumStrategy  # noqa: E402
from app.services.backtest import BacktestEngine  # noqa: E402


def generate_sample_data(days=252):
    """Generate sample market data for demonstration."""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq="D")

    # Generate realistic price data with trend
    returns = np.random.randn(days) * 0.02 + 0.0005
    prices = 100 * (1 + returns).cumprod()

    data = pd.DataFrame(
        {
            "open": prices * (1 + np.random.randn(days) * 0.01),
            "high": prices * (1 + np.abs(np.random.randn(days)) * 0.02),
            "low": prices * (1 - np.abs(np.random.randn(days)) * 0.02),
            "close": prices,
            "volume": np.random.randint(1000000, 10000000, days),
        },
        index=dates,
    )

    return data


def main():
    """Run a simple backtest example."""

    print("=" * 60)
    print("Quantitative Trading Engine - Simple Backtest Example")
    print("=" * 60)
    print()

    # Generate sample data
    print("📊 Generating sample market data...")
    data = generate_sample_data(days=252)
    print(f"✅ Generated {len(data)} days of data")
    print(f"   Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}")
    print()

    # Create momentum strategy
    print("🎯 Creating Momentum Strategy...")
    strategy = MomentumStrategy(
        parameters={"fast_period": 10, "slow_period": 30, "ma_type": "ema"}
    )
    print(f"   Fast Period: {strategy.parameters['fast_period']}")
    print(f"   Slow Period: {strategy.parameters['slow_period']}")
    print(f"   MA Type: {strategy.parameters['ma_type']}")
    print()

    # Initialize backtest engine
    print("🔧 Initializing Backtest Engine...")
    backtest = BacktestEngine(
        initial_capital=100000.0, commission=0.001, slippage=0.0005
    )
    print(f"   Initial Capital: ${backtest.initial_capital:,.2f}")
    print(f"   Commission: {backtest.commission * 100:.2f}%")
    print(f"   Slippage: {backtest.slippage * 100:.3f}%")
    print()

    # Run backtest
    print("🚀 Running backtest...")
    results = backtest.run(
        strategy_type="momentum", strategy_params=strategy.parameters, data=data
    )
    print("✅ Backtest completed!")
    print()

    # Display results
    print("=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    print()

    metrics = results.get("metrics", {})

    print("📈 Performance Metrics:")
    print(f"   Total Return: {results.get('total_return', 0):.2f}%")
    print(f"   Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
    print(f"   Max Drawdown: {metrics.get('max_drawdown', 0):.2f}%")
    print()

    print("📊 Trade Statistics:")
    print(f"   Total Trades: {metrics.get('total_trades', 0)}")
    print(f"   Profitable Trades: {metrics.get('profitable_trades', 0)}")
    print(f"   Losing Trades: {metrics.get('losing_trades', 0)}")
    win_rate = metrics.get("win_rate", 0)
    print(f"   Win Rate: {win_rate:.2f}%")
    print()

    print("💰 Profit & Loss:")
    final_capital = results.get("final_capital", backtest.initial_capital)
    print(f"   Final Capital: ${final_capital:,.2f}")
    total_profit = final_capital - backtest.initial_capital
    print(f"   Total Profit: ${total_profit:,.2f}")
    print()

    print("=" * 60)
    print("✅ Example completed successfully!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
