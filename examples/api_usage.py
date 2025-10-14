"""
API Integration Example
Author: Gabriel Demetrios Lafis

This example demonstrates how to use the REST API to create strategies
and run backtests programmatically.
"""

import requests
import json
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"


def create_strategy():
    """Create a new trading strategy via API."""
    print("📝 Creating new strategy...")

    strategy_data = {
        "name": "My Momentum Strategy",
        "description": "A momentum strategy using EMA crossover",
        "strategy_type": "momentum",
        "parameters": {"fast_period": 10, "slow_period": 30, "ma_type": "ema"},
        "is_active": True,
    }

    response = requests.post(f"{API_URL}/strategies/", json=strategy_data)

    if response.status_code == 201:
        strategy = response.json()
        print(f"✅ Strategy created successfully!")
        print(f"   ID: {strategy['id']}")
        print(f"   Name: {strategy['name']}")
        print(f"   Type: {strategy['strategy_type']}")
        return strategy["id"]
    else:
        print(f"❌ Error creating strategy: {response.status_code}")
        print(response.text)
        return None


def list_strategies():
    """List all strategies."""
    print("\n📋 Listing all strategies...")

    response = requests.get(f"{API_URL}/strategies/")

    if response.status_code == 200:
        strategies = response.json()
        print(f"✅ Found {len(strategies)} strategies:")
        for strategy in strategies:
            print(f"   - {strategy['name']} (ID: {strategy['id']}, Type: {strategy['strategy_type']})")
    else:
        print(f"❌ Error listing strategies: {response.status_code}")


def run_backtest(strategy_id):
    """Run a backtest for a strategy."""
    print(f"\n🚀 Running backtest for strategy ID {strategy_id}...")

    # Calculate date range (last 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    backtest_data = {
        "strategy_id": strategy_id,
        "symbol": "AAPL",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "initial_capital": 100000,
        "commission": 0.001,
        "slippage": 0.0005,
    }

    response = requests.post(f"{API_URL}/backtest/", json=backtest_data)

    if response.status_code == 201:
        result = response.json()
        print("✅ Backtest completed successfully!")
        print(f"\n📊 Results:")
        print(f"   Total Return: {result.get('total_return', 0):.2f}%")
        print(f"   Sharpe Ratio: {result.get('sharpe_ratio', 0):.2f}")
        print(f"   Sortino Ratio: {result.get('sortino_ratio', 0):.2f}")
        print(f"   Max Drawdown: {result.get('max_drawdown', 0):.2f}%")
        print(f"   Total Trades: {result.get('total_trades', 0)}")
        print(f"   Win Rate: {result.get('win_rate', 0):.2f}%")
        print(f"   Profit Factor: {result.get('profit_factor', 0):.2f}")
        return result["id"]
    else:
        print(f"❌ Error running backtest: {response.status_code}")
        print(response.text)
        return None


def get_backtest_results(backtest_id):
    """Get detailed backtest results."""
    print(f"\n📈 Retrieving backtest results for ID {backtest_id}...")

    response = requests.get(f"{API_URL}/backtest/{backtest_id}")

    if response.status_code == 200:
        result = response.json()
        print("✅ Backtest results retrieved!")
        print(f"\n💰 Financial Metrics:")
        print(f"   Initial Capital: ${result.get('initial_capital', 0):,.2f}")
        print(f"   Final Capital: ${result.get('final_capital', 0):,.2f}")
        profit = result.get('final_capital', 0) - result.get('initial_capital', 0)
        print(f"   Total Profit/Loss: ${profit:,.2f}")
        print(f"\n📊 Risk Metrics:")
        print(f"   Sharpe Ratio: {result.get('sharpe_ratio', 0):.2f}")
        print(f"   Sortino Ratio: {result.get('sortino_ratio', 0):.2f}")
        print(f"   Max Drawdown: {result.get('max_drawdown', 0):.2f}%")
        print(f"\n🎯 Trade Statistics:")
        print(f"   Total Trades: {result.get('total_trades', 0)}")
        print(f"   Profitable: {result.get('profitable_trades', 0)}")
        print(f"   Losing: {result.get('losing_trades', 0)}")
        print(f"   Win Rate: {result.get('win_rate', 0):.2f}%")
        print(f"   Average Profit: ${result.get('avg_profit', 0):.2f}")
        print(f"   Average Loss: ${result.get('avg_loss', 0):.2f}")
        print(f"   Profit Factor: {result.get('profit_factor', 0):.2f}")
    else:
        print(f"❌ Error retrieving backtest: {response.status_code}")


def check_api_health():
    """Check if the API is running."""
    print("🔍 Checking API health...")

    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API is healthy!")
            print(f"   Service: {health_data.get('service')}")
            print(f"   Status: {health_data.get('status')}")
            return True
        else:
            print(f"⚠️  API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on http://localhost:8000")
        print("   Start the API with: uvicorn app.main:app --reload")
        return False


def main():
    """Run the API integration example."""

    print("=" * 80)
    print("Quantitative Trading Engine - API Integration Example")
    print("=" * 80)
    print()

    # Check if API is available
    if not check_api_health():
        return

    print()

    # Create a strategy
    strategy_id = create_strategy()
    if not strategy_id:
        return

    # List all strategies
    list_strategies()

    # Run a backtest
    # Note: This will fail without real market data
    # In production, ensure market data service is properly configured
    print("\n⚠️  Note: Backtest requires market data connection")
    print("   Uncomment the following lines to run backtest with real data:")
    print()
    print("   # backtest_id = run_backtest(strategy_id)")
    print("   # if backtest_id:")
    print("   #     get_backtest_results(backtest_id)")

    print()
    print("=" * 80)
    print("✅ API integration example completed!")
    print("=" * 80)
    print()
    print("💡 Next Steps:")
    print("   1. Explore the interactive API docs at http://localhost:8000/docs")
    print("   2. Configure real market data providers")
    print("   3. Create custom strategies via the API")
    print("   4. Run backtests and analyze results")


if __name__ == "__main__":
    main()
