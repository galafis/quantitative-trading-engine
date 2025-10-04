"""
Unit tests for backtesting engine.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from app.services import BacktestEngine


@pytest.fixture
def sample_data():
    """Create sample OHLCV data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'open': 100 + np.random.randn(len(dates)).cumsum(),
        'high': 102 + np.random.randn(len(dates)).cumsum(),
        'low': 98 + np.random.randn(len(dates)).cumsum(),
        'close': 100 + np.random.randn(len(dates)).cumsum(),
        'volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    data['high'] = data[['open', 'high', 'close']].max(axis=1)
    data['low'] = data[['open', 'low', 'close']].min(axis=1)
    
    return data


class TestBacktestEngine:
    """Tests for Backtest Engine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = BacktestEngine(
            initial_capital=100000,
            commission=0.001,
            slippage=0.0005
        )
        
        assert engine.initial_capital == 100000
        assert engine.commission == 0.001
        assert engine.slippage == 0.0005
    
    def test_run_momentum_strategy(self, sample_data):
        """Test running backtest with momentum strategy."""
        engine = BacktestEngine(initial_capital=100000)
        
        results = engine.run(
            strategy_type='momentum',
            strategy_params={'fast_period': 10, 'slow_period': 30},
            data=sample_data
        )
        
        assert 'initial_capital' in results
        assert 'final_capital' in results
        assert 'total_return' in results
        assert 'trades' in results
        assert 'equity_curve' in results
        assert 'metrics' in results
        
        assert results['initial_capital'] == 100000
        assert isinstance(results['final_capital'], float)
        assert isinstance(results['total_return'], float)
    
    def test_run_mean_reversion_strategy(self, sample_data):
        """Test running backtest with mean reversion strategy."""
        engine = BacktestEngine(initial_capital=50000)
        
        results = engine.run(
            strategy_type='mean_reversion',
            strategy_params={'period': 20, 'std_dev': 2},
            data=sample_data
        )
        
        assert results['initial_capital'] == 50000
        assert 'metrics' in results
    
    def test_run_breakout_strategy(self, sample_data):
        """Test running backtest with breakout strategy."""
        engine = BacktestEngine(initial_capital=75000)
        
        results = engine.run(
            strategy_type='breakout',
            strategy_params={'lookback_period': 20},
            data=sample_data
        )
        
        assert results['initial_capital'] == 75000
        assert 'metrics' in results
    
    def test_invalid_strategy_type(self, sample_data):
        """Test with invalid strategy type."""
        engine = BacktestEngine()
        
        with pytest.raises(ValueError):
            engine.run(
                strategy_type='invalid_strategy',
                strategy_params={},
                data=sample_data
            )
    
    def test_calculate_metrics(self, sample_data):
        """Test metrics calculation."""
        engine = BacktestEngine(initial_capital=100000)
        
        results = engine.run(
            strategy_type='momentum',
            strategy_params={'fast_period': 10, 'slow_period': 30},
            data=sample_data
        )
        
        metrics = results['metrics']
        
        if metrics:  # Only test if trades were generated
            assert 'total_trades' in metrics
            assert 'win_rate' in metrics
            assert 'sharpe_ratio' in metrics
            assert 'max_drawdown' in metrics
            
            assert metrics['total_trades'] >= 0
            assert 0 <= metrics['win_rate'] <= 100
    
    def test_equity_curve(self, sample_data):
        """Test equity curve generation."""
        engine = BacktestEngine(initial_capital=100000)
        
        results = engine.run(
            strategy_type='momentum',
            strategy_params={'fast_period': 5, 'slow_period': 15},
            data=sample_data
        )
        
        equity_curve = results['equity_curve']
        
        assert len(equity_curve) > 0
        assert equity_curve[0] == 100000  # First value should be initial capital
        assert all(isinstance(x, (int, float)) for x in equity_curve)
