"""
Strategy API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Strategy
from app.schemas import StrategyCreate, StrategyUpdate, StrategyResponse

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.post("/", response_model=StrategyResponse, status_code=status.HTTP_201_CREATED)
def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db)):
    """
    Create a new trading strategy.
    """
    # Check if strategy with same name exists
    existing = db.query(Strategy).filter(Strategy.name == strategy.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Strategy with name '{strategy.name}' already exists",
        )

    db_strategy = Strategy(**strategy.model_dump())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy


@router.get("/", response_model=List[StrategyResponse])
def list_strategies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all trading strategies.
    """
    strategies = db.query(Strategy).offset(skip).limit(limit).all()
    return strategies


@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    """
    Get a specific trading strategy by ID.
    """
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Strategy with ID {strategy_id} not found",
        )
    return strategy


@router.put("/{strategy_id}", response_model=StrategyResponse)
def update_strategy(
    strategy_id: int, strategy_update: StrategyUpdate, db: Session = Depends(get_db)
):
    """
    Update a trading strategy.
    """
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Strategy with ID {strategy_id} not found",
        )

    # Update only provided fields
    update_data = strategy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(strategy, field, value)

    db.commit()
    db.refresh(strategy)
    return strategy


@router.delete("/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    """
    Delete a trading strategy.
    """
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Strategy with ID {strategy_id} not found",
        )

    db.delete(strategy)
    db.commit()
    return None
