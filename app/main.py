"""
Main FastAPI application for the News Aggregator.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
from typing import Dict, Any

from .core.config import settings
from .core.database import init_db, close_db
from .api.v1.api import api_router
from .api.v1.endpoints import health

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting News Aggregator application")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down News Aggregator application")
    close_db()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-powered news aggregation and fact-checking system",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler."""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Include health check endpoint
app.include_router(health.router, prefix="/health", tags=["health"])


@app.get("/", tags=["root"])
async def root() -> Dict[str, Any]:
    """Root endpoint with application information."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "description": "AI-powered news aggregation and fact-checking system",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1"
    }


@app.get("/info", tags=["info"])
async def get_info() -> Dict[str, Any]:
    """Get application information and status."""
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
        "database_url": settings.database.url,
        "redis_url": settings.redis.url,
        "celery_broker": settings.celery.broker_url,
        "openai_enabled": bool(settings.openai.api_key),
        "claude_enabled": bool(settings.claude.api_key),
        "mcp_enabled": settings.mcp.enabled,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
