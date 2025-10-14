"""
Main FastAPI application.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import strategies, backtest, health
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    """
    # Startup
    if os.getenv("TESTING") != "true":
        Base.metadata.create_all(bind=engine)
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print("Documentation available at: /docs")

    yield

    # Shutdown
    print(f"Shutting down {settings.PROJECT_NAME}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(strategies.router, prefix=settings.API_V1_STR)
app.include_router(backtest.router, prefix=settings.API_V1_STR)
