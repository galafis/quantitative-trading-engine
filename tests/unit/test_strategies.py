"""
Unit tests for trading strategies.
"""
import pytest
import pandas as pd
import numpy as np
from app.strategies import MomentumStrategy, MeanReversionStrategy, BreakoutStrategy


@pytest.fixture
def sample_data():
    """Create sample OHLCV data for testing."""
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    np.random.seed(42)

    data = pd.DataFrame(
        {
            "open": 100 + np.random.randn(len(dates)).cumsum(),
            "high": 102 + np.random.randn(len(dates)).cumsum(),
            "low": 98 + np.random.randn(len(dates)).cumsum(),
            "close": 100 + np.random.randn(len(dates)).cumsum(),
            "volume": np.random.randint(1000000, 10000000, len(dates)),
        },
        index=dates,
    )

    # Ensure high is highest and low is lowest
    data["high"] = data[["open", "high", "close"]].max(axis=1)
    data["low"] = data[["open", "low", "close"]].min(axis=1)

    return data


class TestMomentumStrategy:
    """Tests for Momentum Strategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = MomentumStrategy()
        assert strategy.parameters["fast_period"] == 10
        assert strategy.parameters["slow_period"] == 30
        assert strategy.parameters["ma_type"] == "sma"

    def test_custom_parameters(self):
        """Test strategy with custom parameters."""
        params = {"fast_period": 5, "slow_period": 20, "ma_type": "ema"}
        strategy = MomentumStrategy(params)
        assert strategy.parameters["fast_period"] == 5
        assert strategy.parameters["slow_period"] == 20
        assert strategy.parameters["ma_type"] == "ema"

    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = MomentumStrategy()
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "fast_ma" in result.columns
        assert "slow_ma" in result.columns
        assert result["signal"].isin([0, 1, -1]).all()

    def test_invalid_data(self):
        """Test with invalid data."""
        strategy = MomentumStrategy()
        invalid_data = pd.DataFrame({"invalid": [1, 2, 3]})

        with pytest.raises(ValueError):
            strategy.generate_signals(invalid_data)


class TestMeanReversionStrategy:
    """Tests for Mean Reversion Strategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = MeanReversionStrategy()
        assert strategy.parameters["period"] == 20
        assert strategy.parameters["std_dev"] == 2
        assert strategy.parameters["rsi_period"] == 14

    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = MeanReversionStrategy()
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "upper_band" in result.columns
        assert "lower_band" in result.columns
        assert "rsi" in result.columns
        assert result["signal"].isin([0, 1, -1]).all()

    def test_rsi_calculation(self, sample_data):
        """Test RSI calculation."""
        strategy = MeanReversionStrategy()
        rsi = strategy.calculate_rsi(sample_data["close"], 14)

        assert len(rsi) == len(sample_data)
        assert rsi.min() >= 0
        assert rsi.max() <= 100


class TestBreakoutStrategy:
    """Tests for Breakout Strategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = BreakoutStrategy()
        assert strategy.parameters["lookback_period"] == 20
        assert strategy.parameters["breakout_threshold"] == 0.02
        assert strategy.parameters["volume_confirmation"] is True

    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = BreakoutStrategy()
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns
        assert "resistance" in result.columns
        assert "support" in result.columns
        assert result["signal"].isin([0, 1, -1]).all()

    def test_without_volume_confirmation(self, sample_data):
        """Test without volume confirmation."""
        params = {"volume_confirmation": False}
        strategy = BreakoutStrategy(params)
        result = strategy.generate_signals(sample_data)

        assert "signal" in result.columns


class TestBaseStrategy:
    """Tests for Base Strategy functionality."""

    def test_position_sizing(self):
        """Test position size calculation."""
        strategy = MomentumStrategy()

        position_size = strategy.calculate_position_size(
            capital=100000, price=100, risk_per_trade=0.02
        )

        assert position_size > 0
        assert isinstance(position_size, int)

    def test_validate_data(self, sample_data):
        """Test data validation."""
        strategy = MomentumStrategy()
        assert strategy.validate_data(sample_data) is True

        invalid_data = pd.DataFrame({"invalid": [1, 2, 3]})
        assert strategy.validate_data(invalid_data) is False
