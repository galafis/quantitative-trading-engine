"""
Simple Backtest Example
Author: Gabriel Demetrios Lafis

This example demonstrates how to run a simple backtest using the momentum strategy.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from app.strategies.momentum import MomentumStrategy
from app.services.backtest import BacktestEngine


def generate_sample_data(days=252):
    """Generate sample market data for demonstration."""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate realistic price data with trend
    returns = np.random.randn(days) * 0.02 + 0.0005
    prices = 100 * (1 + returns).cumprod()
    
    data = pd.DataFrame({
        'open': prices * (1 + np.random.randn(days) * 0.01),
        'high': prices * (1 + np.abs(np.random.randn(days)) * 0.02),
        'low': prices * (1 - np.abs(np.random.randn(days)) * 0.02),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    
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
    strategy = MomentumStrategy(parameters={
        'fast_period': 10,
        'slow_period': 30,
        'ma_type': 'ema'
    })
    print(f"   Fast Period: {strategy.parameters['fast_period']}")
    print(f"   Slow Period: {strategy.parameters['slow_period']}")
    print(f"   MA Type: {strategy.parameters['ma_type']}")
    print()
    
    # Initialize backtest engine
    print("🔧 Initializing Backtest Engine...")
    backtest = BacktestEngine(
        initial_capital=100000.0,
        commission=0.001,
        slippage=0.0005
    )
    print(f"   Initial Capital: ${backtest.initial_capital:,.2f}")
    print(f"   Commission: {backtest.commission * 100:.2f}%")
    print(f"   Slippage: {backtest.slippage * 100:.3f}%")
    print()
    
    # Run backtest
    print("🚀 Running backtest...")
    results = backtest.run(
        strategy_type='momentum',
        strategy_params=strategy.parameters,
        data=data
    )
    print("✅ Backtest completed!")
    print()
    
    # Display results
    print("=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    print()
    
    print(f"📈 Performance Metrics:")
    print(f"   Total Return: {results.get('total_return', 0):.2f}%")
    print(f"   Sharpe Ratio: {results.get('sharpe_ratio', 0):.2f}")
    print(f"   Max Drawdown: {results.get('max_drawdown', 0):.2f}%")
    print()
    
    print(f"📊 Trade Statistics:")
    print(f"   Total Trades: {results.get('total_trades', 0)}")
    print(f"   Winning Trades: {results.get('winning_trades', 0)}")
    print(f"   Losing Trades: {results.get('losing_trades', 0)}")
    win_rate = results.get('win_rate', 0)
    print(f"   Win Rate: {win_rate:.2f}%")
    print()
    
    print(f"💰 Profit & Loss:")
    final_capital = results.get('final_capital', backtest.initial_capital)
    print(f"   Final Capital: ${final_capital:,.2f}")
    total_profit = final_capital - backtest.initial_capital
    print(f"   Total Profit: ${total_profit:,.2f}")
    print()
    
    print("=" * 60)
    print("✅ Example completed successfully!")
    print("=" * 60)
    print()
    print("💡 Note: This example uses simulated data for demonstration.")
    print("   In production, connect to real market data sources.")


if __name__ == "__main__":
    main()
