"""
Advanced Strategy Comparison Example
Author: Gabriel Demetrios Lafis

This example demonstrates how to compare multiple trading strategies
using the same market data and backtest parameters.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from app.strategies import MomentumStrategy, MeanReversionStrategy, BreakoutStrategy
from app.services.backtest import BacktestEngine


def generate_sample_data(days=252):
    """Generate sample market data with trend and volatility."""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq="D")

    # Generate realistic price data with trend and mean reversion
    returns = np.random.randn(days) * 0.015 + 0.0003
    prices = 100 * (1 + returns).cumprod()

    data = pd.DataFrame(
        {
            "date": dates,
            "open": prices * (1 + np.random.randn(days) * 0.005),
            "high": prices * (1 + np.abs(np.random.randn(days)) * 0.015),
            "low": prices * (1 - np.abs(np.random.randn(days)) * 0.015),
            "close": prices,
            "volume": np.random.randint(1000000, 10000000, days),
        }
    )

    return data


def run_strategy_comparison():
    """Compare multiple trading strategies."""

    print("=" * 80)
    print("Quantitative Trading Engine - Strategy Comparison Example")
    print("=" * 80)
    print()

    # Generate sample data
    print("📊 Generating sample market data...")
    data = generate_sample_data(days=252)
    print(f"✅ Generated {len(data)} days of data")
    print(f"   Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}")
    print()

    # Define strategies to compare
    strategies = [
        {
            "name": "Fast Momentum (EMA)",
            "type": "momentum",
            "params": {"fast_period": 10, "slow_period": 30, "ma_type": "ema"},
        },
        {
            "name": "Slow Momentum (SMA)",
            "type": "momentum",
            "params": {"fast_period": 20, "slow_period": 50, "ma_type": "sma"},
        },
        {
            "name": "Mean Reversion (Tight)",
            "type": "mean_reversion",
            "params": {"period": 20, "num_std": 2, "rsi_period": 14, "rsi_overbought": 70, "rsi_oversold": 30},
        },
        {
            "name": "Mean Reversion (Wide)",
            "type": "mean_reversion",
            "params": {"period": 20, "num_std": 2.5, "rsi_period": 14, "rsi_overbought": 75, "rsi_oversold": 25},
        },
        {
            "name": "Breakout (Conservative)",
            "type": "breakout",
            "params": {"lookback_period": 20, "breakout_threshold": 0.03, "volume_confirmation": True},
        },
        {
            "name": "Breakout (Aggressive)",
            "type": "breakout",
            "params": {"lookback_period": 10, "breakout_threshold": 0.015, "volume_confirmation": False},
        },
    ]

    results = []

    # Run backtest for each strategy
    for strategy_config in strategies:
        print(f"🎯 Testing: {strategy_config['name']}")

        # Initialize backtest engine
        backtest = BacktestEngine(
            initial_capital=100000.0, commission=0.001, slippage=0.0005
        )

        # Run backtest
        result = backtest.run(
            strategy_type=strategy_config["type"],
            strategy_params=strategy_config["params"],
            data=data,
        )

        # Store results
        results.append(
            {
                "name": strategy_config["name"],
                "type": strategy_config["type"],
                "total_return": result.get("total_return", 0),
                "sharpe_ratio": result.get("sharpe_ratio", 0),
                "sortino_ratio": result.get("sortino_ratio", 0),
                "max_drawdown": result.get("max_drawdown", 0),
                "total_trades": result.get("total_trades", 0),
                "win_rate": result.get("win_rate", 0),
                "profit_factor": result.get("profit_factor", 0),
                "final_capital": result.get("final_capital", 100000),
            }
        )
        print(f"   ✓ Return: {result.get('total_return', 0):.2f}% | Sharpe: {result.get('sharpe_ratio', 0):.2f}")
        print()

    # Display comparison table
    print("=" * 80)
    print("STRATEGY COMPARISON RESULTS")
    print("=" * 80)
    print()

    # Sort by total return
    results_sorted = sorted(results, key=lambda x: x["total_return"], reverse=True)

    print(f"{'Strategy':<30} {'Return':<10} {'Sharpe':<10} {'Max DD':<10} {'Trades':<8} {'Win Rate'}")
    print("-" * 80)

    for result in results_sorted:
        print(
            f"{result['name']:<30} "
            f"{result['total_return']:>8.2f}% "
            f"{result['sharpe_ratio']:>9.2f} "
            f"{result['max_drawdown']:>8.2f}% "
            f"{result['total_trades']:>7} "
            f"{result['win_rate']:>7.1f}%"
        )

    print()

    # Find best strategies
    best_return = max(results, key=lambda x: x["total_return"])
    best_sharpe = max(results, key=lambda x: x["sharpe_ratio"])
    best_drawdown = min(results, key=lambda x: abs(x["max_drawdown"]))

    print("🏆 Top Performers:")
    print(f"   Highest Return: {best_return['name']} ({best_return['total_return']:.2f}%)")
    print(f"   Best Sharpe Ratio: {best_sharpe['name']} ({best_sharpe['sharpe_ratio']:.2f})")
    print(f"   Lowest Drawdown: {best_drawdown['name']} ({best_drawdown['max_drawdown']:.2f}%)")
    print()

    # Strategy type analysis
    print("📊 Analysis by Strategy Type:")
    for strategy_type in ["momentum", "mean_reversion", "breakout"]:
        type_results = [r for r in results if r["type"] == strategy_type]
        if type_results:
            avg_return = sum(r["total_return"] for r in type_results) / len(type_results)
            avg_sharpe = sum(r["sharpe_ratio"] for r in type_results) / len(type_results)
            print(f"   {strategy_type.replace('_', ' ').title()}:")
            print(f"      Avg Return: {avg_return:.2f}% | Avg Sharpe: {avg_sharpe:.2f}")

    print()
    print("=" * 80)
    print("✅ Strategy comparison completed!")
    print("=" * 80)
    print()
    print("💡 Insights:")
    print("   - Different strategies perform better in different market conditions")
    print("   - Momentum strategies work well in trending markets")
    print("   - Mean reversion strategies excel in ranging markets")
    print("   - Breakout strategies capture large price movements")
    print("   - Always validate strategies with out-of-sample data")


if __name__ == "__main__":
    run_strategy_comparison()
