"""
Health check endpoints.
"""
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Quantitative Trading Engine",
    }


@router.get("/")
def root():
    """
    Root endpoint.
    """
    return {
        "message": "Quantitative Trading Engine API",
        "version": "1.0.0",
        "docs": "/docs",
    }
