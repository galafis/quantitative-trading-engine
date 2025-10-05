"""
Simple Backtest Example
Author: Gabriel Demetrios Lafis

This example demonstrates how to run a simple backtest using the momentum strategy.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from app.strategies.momentum import MomentumStrategy
from app.services.backtest import BacktestEngine
from app.services.market_data import MarketDataService


def main():
    """Run a simple backtest example."""
    
    print("=" * 60)
    print("Quantitative Trading Engine - Simple Backtest Example")
    print("=" * 60)
    print()
    
    # Initialize market data service
    market_data = MarketDataService()
    
    # Fetch historical data
    print("📊 Fetching historical data for ^BVSP (Ibovespa)...")
    data = market_data.get_historical_data(
        symbol="^BVSP",
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31)
    )
    print(f"✅ Fetched {len(data)} days of data")
    print()
    
    # Create momentum strategy
    print("🎯 Creating Momentum Strategy...")
    strategy = MomentumStrategy(
        fast_period=10,
        slow_period=30,
        ma_type="ema"
    )
    print(f"   Fast Period: {strategy.fast_period}")
    print(f"   Slow Period: {strategy.slow_period}")
    print(f"   MA Type: {strategy.ma_type}")
    print()
    
    # Initialize backtest engine
    print("🔧 Initializing Backtest Engine...")
    backtest = BacktestEngine(
        strategy=strategy,
        initial_capital=100000.0,
        commission=0.001,
        slippage=0.0005
    )
    print(f"   Initial Capital: R$ {backtest.initial_capital:,.2f}")
    print(f"   Commission: {backtest.commission * 100:.2f}%")
    print(f"   Slippage: {backtest.slippage * 100:.3f}%")
    print()
    
    # Run backtest
    print("🚀 Running backtest...")
    results = backtest.run(data)
    print("✅ Backtest completed!")
    print()
    
    # Display results
    print("=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    print()
    
    print(f"📈 Performance Metrics:")
    print(f"   Total Return: {results['total_return']:.2f}%")
    print(f"   Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"   Sortino Ratio: {results['sortino_ratio']:.2f}")
    print(f"   Max Drawdown: {results['max_drawdown']:.2f}%")
    print()
    
    print(f"📊 Trade Statistics:")
    print(f"   Total Trades: {results['total_trades']}")
    print(f"   Winning Trades: {results['winning_trades']}")
    print(f"   Losing Trades: {results['losing_trades']}")
    print(f"   Win Rate: {results['win_rate']:.2f}%")
    print()
    
    print(f"💰 Profit & Loss:")
    print(f"   Final Capital: R$ {results['final_capital']:,.2f}")
    print(f"   Total Profit: R$ {results['total_profit']:,.2f}")
    print(f"   Profit Factor: {results['profit_factor']:.2f}")
    print(f"   Average P&L: R$ {results['avg_profit_loss']:,.2f}")
    print()
    
    print("=" * 60)
    print("✅ Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
