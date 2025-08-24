"""
Health check endpoints for monitoring application status.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis
import structlog
from typing import Dict, Any

from ....core.database import get_db
from ....core.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", tags=["health"])
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "news-aggregator",
        "version": "0.1.0"
    }


@router.get("/db", tags=["health"])
async def database_health(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Database health check."""
    try:
        # Test database connection
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        
        return {
            "status": "healthy",
            "database": "postgresql",
            "connection": "established"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )


@router.get("/redis", tags=["health"])
async def redis_health() -> Dict[str, Any]:
    """Redis health check."""
    try:
        # Test Redis connection
        r = redis.from_url(settings.redis.url)
        r.ping()
        
        return {
            "status": "healthy",
            "redis": "connected",
            "url": settings.redis.url
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Redis connection failed"
        )


@router.get("/celery", tags=["health"])
async def celery_health() -> Dict[str, Any]:
    """Celery health check."""
    try:
        # Test Celery broker connection
        r = redis.from_url(settings.celery.broker_url)
        r.ping()
        
        return {
            "status": "healthy",
            "celery": "broker_connected",
            "broker_url": settings.celery.broker_url
        }
    except Exception as e:
        logger.error(f"Celery health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Celery broker connection failed"
        )


@router.get("/ai-models", tags=["health"])
async def ai_models_health() -> Dict[str, Any]:
    """AI models health check."""
    health_status = {
        "status": "healthy",
        "models": {}
    }
    
    # Check OpenAI
    if settings.openai.api_key:
        health_status["models"]["openai"] = {
            "status": "configured",
            "model": settings.openai.model
        }
    else:
        health_status["models"]["openai"] = {
            "status": "not_configured"
        }
    
    # Check Claude
    if settings.claude.api_key:
        health_status["models"]["claude"] = {
            "status": "configured",
            "model": settings.claude.model
        }
    else:
        health_status["models"]["claude"] = {
            "status": "not_configured"
        }
    
    # Check MCP
    health_status["models"]["mcp"] = {
        "status": "enabled" if settings.mcp.enabled else "disabled",
        "servers": len(settings.mcp.servers)
    }
    
    return health_status


@router.get("/full", tags=["health"])
async def full_health_check(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Comprehensive health check for all components."""
    health_checks = {
        "application": {"status": "healthy"},
        "database": await database_health(db),
        "redis": await redis_health(),
        "celery": await celery_health(),
        "ai_models": await ai_models_health()
    }
    
    # Determine overall status
    all_healthy = all(
        check.get("status") == "healthy" or check.get("status") == "configured"
        for check in health_checks.values()
    )
    
    overall_status = "healthy" if all_healthy else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": "2024-01-01T00:00:00Z",  # TODO: Add actual timestamp
        "checks": health_checks
    }
