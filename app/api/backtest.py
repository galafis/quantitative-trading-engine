"""
Backtest API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Strategy, Backtest
from app.schemas import BacktestRequest, BacktestResponse
from app.services import BacktestEngine, MarketDataService

router = APIRouter(prefix="/backtest", tags=["backtest"])


@router.post("/", response_model=BacktestResponse, status_code=status.HTTP_201_CREATED)
def run_backtest(request: BacktestRequest, db: Session = Depends(get_db)):
    """
    Run a backtest for a strategy.
    """
    # Get strategy
    strategy = db.query(Strategy).filter(Strategy.id == request.strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Strategy with ID {request.strategy_id} not found",
        )

    # Fetch market data
    try:
        market_data_service = MarketDataService()
        data = market_data_service.get_historical_data(
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching market data: {str(e)}",
        )

    if data.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No market data available for the specified period",
        )

    # Run backtest
    try:
        backtest_engine = BacktestEngine(
            initial_capital=request.initial_capital,
            commission=request.commission,
            slippage=request.slippage,
        )

        results = backtest_engine.run(
            strategy_type=str(strategy.strategy_type),
            strategy_params=dict(strategy.parameters),
            data=data,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running backtest: {str(e)}",
        )

    # Save backtest results
    metrics = results["metrics"]
    db_backtest = Backtest(
        strategy_id=request.strategy_id,
        symbol=request.symbol,
        start_date=request.start_date,
        end_date=request.end_date,
        initial_capital=results["initial_capital"],
        final_capital=results["final_capital"],
        total_return=results["total_return"],
        sharpe_ratio=metrics.get("sharpe_ratio"),
        sortino_ratio=metrics.get("sortino_ratio"),
        max_drawdown=metrics.get("max_drawdown"),
        win_rate=metrics.get("win_rate"),
        total_trades=metrics.get("total_trades", 0),
        profitable_trades=metrics.get("profitable_trades", 0),
        losing_trades=metrics.get("losing_trades", 0),
        avg_profit=metrics.get("avg_profit"),
        avg_loss=metrics.get("avg_loss"),
        profit_factor=metrics.get("profit_factor"),
        parameters=strategy.parameters,
    )

    db.add(db_backtest)
    db.commit()
    db.refresh(db_backtest)

    return db_backtest


@router.get("/", response_model=List[BacktestResponse])
def list_backtests(
    strategy_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all backtests, optionally filtered by strategy.
    """
    query = db.query(Backtest)

    if strategy_id:
        query = query.filter(Backtest.strategy_id == strategy_id)

    backtests = query.offset(skip).limit(limit).all()
    return backtests


@router.get("/{backtest_id}", response_model=BacktestResponse)
def get_backtest(backtest_id: int, db: Session = Depends(get_db)):
    """
    Get a specific backtest by ID.
    """
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Backtest with ID {backtest_id} not found",
        )
    return backtest
