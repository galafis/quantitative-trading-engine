"""
Integration tests for API endpoints.
"""
import pytest
from datetime import datetime, timedelta


class TestStrategiesAPI:
    """Integration tests for strategies API endpoints."""

    def test_create_strategy(self, client):
        """Test creating a new strategy."""
        strategy_data = {
            "name": "Test Momentum Strategy",
            "description": "A test momentum strategy",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 10, "slow_period": 30, "ma_type": "sma"},
            "is_active": True,
        }

        response = client.post("/api/v1/strategies/", json=strategy_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == strategy_data["name"]
        assert data["strategy_type"] == strategy_data["strategy_type"]
        assert "id" in data

    def test_list_strategies(self, client):
        """Test listing strategies."""
        # Create a strategy first
        strategy_data = {
            "name": "List Test Strategy",
            "description": "Strategy for list test",
            "strategy_type": "mean_reversion",
            "parameters": {"period": 20, "num_std": 2},
            "is_active": True,
        }
        client.post("/api/v1/strategies/", json=strategy_data)

        # List strategies
        response = client.get("/api/v1/strategies/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_strategy(self, client):
        """Test getting a specific strategy."""
        # Create a strategy first
        strategy_data = {
            "name": "Get Test Strategy",
            "description": "Strategy for get test",
            "strategy_type": "breakout",
            "parameters": {"lookback_period": 20, "breakout_threshold": 0.02},
            "is_active": True,
        }
        create_response = client.post("/api/v1/strategies/", json=strategy_data)
        strategy_id = create_response.json()["id"]

        # Get the strategy
        response = client.get(f"/api/v1/strategies/{strategy_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == strategy_id
        assert data["name"] == strategy_data["name"]

    def test_update_strategy(self, client):
        """Test updating a strategy."""
        # Create a strategy first
        strategy_data = {
            "name": "Update Test Strategy",
            "description": "Strategy for update test",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 10, "slow_period": 30},
            "is_active": True,
        }
        create_response = client.post("/api/v1/strategies/", json=strategy_data)
        strategy_id = create_response.json()["id"]

        # Update the strategy
        update_data = {
            "name": "Updated Strategy Name",
            "description": "Updated description",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 15, "slow_period": 35},
            "is_active": False,
        }
        response = client.put(f"/api/v1/strategies/{strategy_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["is_active"] is False
        assert data["parameters"]["fast_period"] == 15

    def test_delete_strategy(self, client):
        """Test deleting a strategy."""
        # Create a strategy first
        strategy_data = {
            "name": "Delete Test Strategy",
            "description": "Strategy for delete test",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 10, "slow_period": 30},
            "is_active": True,
        }
        create_response = client.post("/api/v1/strategies/", json=strategy_data)
        strategy_id = create_response.json()["id"]

        # Delete the strategy
        response = client.delete(f"/api/v1/strategies/{strategy_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/api/v1/strategies/{strategy_id}")
        assert get_response.status_code == 404


class TestBacktestAPI:
    """Integration tests for backtest API endpoints."""

    def test_run_backtest(self, client, monkeypatch):
        """Test running a backtest."""
        # Create a strategy first
        strategy_data = {
            "name": "Backtest Strategy",
            "description": "Strategy for backtest",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 10, "slow_period": 30, "ma_type": "sma"},
            "is_active": True,
        }
        create_response = client.post("/api/v1/strategies/", json=strategy_data)
        strategy_id = create_response.json()["id"]

        # Mock market data service to avoid external API calls
        import pandas as pd
        import numpy as np
        from app.services import MarketDataService

        def mock_get_historical_data(self, symbol, start_date, end_date):
            dates = pd.date_range(start=start_date, end=end_date, freq="D")
            np.random.seed(42)
            return pd.DataFrame(
                {
                    "open": 100 + np.random.randn(len(dates)).cumsum(),
                    "high": 102 + np.random.randn(len(dates)).cumsum(),
                    "low": 98 + np.random.randn(len(dates)).cumsum(),
                    "close": 100 + np.random.randn(len(dates)).cumsum(),
                    "volume": np.random.randint(1000000, 5000000, len(dates)),
                },
                index=dates,
            )

        monkeypatch.setattr(
            MarketDataService, "get_historical_data", mock_get_historical_data
        )

        # Run backtest
        backtest_data = {
            "strategy_id": strategy_id,
            "symbol": "AAPL",
            "start_date": (datetime.now() - timedelta(days=90)).isoformat(),
            "end_date": datetime.now().isoformat(),
            "initial_capital": 100000,
            "commission": 0.001,
            "slippage": 0.0005,
        }
        response = client.post("/api/v1/backtest/", json=backtest_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["strategy_id"] == strategy_id
        assert "total_return" in data
        assert "sharpe_ratio" in data

    def test_list_backtests(self, client, monkeypatch):
        """Test listing backtests."""
        # Create strategy and run backtest first
        strategy_data = {
            "name": "List Backtest Strategy",
            "description": "Strategy for backtest list",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 10, "slow_period": 30},
            "is_active": True,
        }
        create_response = client.post("/api/v1/strategies/", json=strategy_data)
        strategy_id = create_response.json()["id"]

        # Mock market data
        import pandas as pd
        import numpy as np
        from app.services import MarketDataService

        def mock_get_historical_data(self, symbol, start_date, end_date):
            dates = pd.date_range(start=start_date, end=end_date, freq="D")
            np.random.seed(42)
            return pd.DataFrame(
                {
                    "open": 100 + np.random.randn(len(dates)).cumsum(),
                    "high": 102 + np.random.randn(len(dates)).cumsum(),
                    "low": 98 + np.random.randn(len(dates)).cumsum(),
                    "close": 100 + np.random.randn(len(dates)).cumsum(),
                    "volume": np.random.randint(1000000, 5000000, len(dates)),
                },
                index=dates,
            )

        monkeypatch.setattr(
            MarketDataService, "get_historical_data", mock_get_historical_data
        )

        backtest_data = {
            "strategy_id": strategy_id,
            "symbol": "AAPL",
            "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "end_date": datetime.now().isoformat(),
            "initial_capital": 100000,
            "commission": 0.001,
            "slippage": 0.0005,
        }
        client.post("/api/v1/backtest/", json=backtest_data)

        # List backtests
        response = client.get("/api/v1/backtest/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_backtest(self, client, monkeypatch):
        """Test getting a specific backtest."""
        # Create strategy and run backtest
        strategy_data = {
            "name": "Get Backtest Strategy",
            "description": "Strategy for get backtest",
            "strategy_type": "momentum",
            "parameters": {"fast_period": 10, "slow_period": 30},
            "is_active": True,
        }
        create_response = client.post("/api/v1/strategies/", json=strategy_data)
        strategy_id = create_response.json()["id"]

        # Mock market data
        import pandas as pd
        import numpy as np
        from app.services import MarketDataService

        def mock_get_historical_data(self, symbol, start_date, end_date):
            dates = pd.date_range(start=start_date, end=end_date, freq="D")
            np.random.seed(42)
            return pd.DataFrame(
                {
                    "open": 100 + np.random.randn(len(dates)).cumsum(),
                    "high": 102 + np.random.randn(len(dates)).cumsum(),
                    "low": 98 + np.random.randn(len(dates)).cumsum(),
                    "close": 100 + np.random.randn(len(dates)).cumsum(),
                    "volume": np.random.randint(1000000, 5000000, len(dates)),
                },
                index=dates,
            )

        monkeypatch.setattr(
            MarketDataService, "get_historical_data", mock_get_historical_data
        )

        backtest_data = {
            "strategy_id": strategy_id,
            "symbol": "AAPL",
            "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "end_date": datetime.now().isoformat(),
            "initial_capital": 100000,
            "commission": 0.001,
            "slippage": 0.0005,
        }
        backtest_response = client.post("/api/v1/backtest/", json=backtest_data)
        backtest_id = backtest_response.json()["id"]

        # Get the backtest
        response = client.get(f"/api/v1/backtest/{backtest_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == backtest_id
        assert data["strategy_id"] == strategy_id
