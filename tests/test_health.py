"""
Tests for health check endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


def test_health_check(client: TestClient):
    """Test basic health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "news-aggregator"
    assert data["version"] == "0.1.0"


def test_database_health_success(client: TestClient, db_session):
    """Test database health check when database is healthy."""
    response = client.get("/health/db")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "postgresql"
    assert data["connection"] == "established"


def test_redis_health_success(client: TestClient, mock_redis):
    """Test Redis health check when Redis is healthy."""
    response = client.get("/health/redis")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["redis"] == "connected"


def test_celery_health_success(client: TestClient, mock_redis):
    """Test Celery health check when broker is healthy."""
    response = client.get("/health/celery")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["celery"] == "broker_connected"


def test_ai_models_health_no_keys(client: TestClient):
    """Test AI models health check when no API keys are configured."""
    response = client.get("/health/ai-models")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models"]["openai"]["status"] == "not_configured"
    assert data["models"]["claude"]["status"] == "not_configured"
    assert data["models"]["mcp"]["status"] == "enabled"


def test_full_health_check(client: TestClient, db_session, mock_redis):
    """Test comprehensive health check endpoint."""
    response = client.get("/health/full")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "checks" in data
    
    checks = data["checks"]
    assert "application" in checks
    assert "database" in checks
    assert "redis" in checks
    assert "celery" in checks
    assert "ai_models" in checks


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "News Aggregator"
    assert data["version"] == "0.1.0"
    assert "docs" in data
    assert "health" in data
    assert "api" in data


def test_info_endpoint(client: TestClient):
    """Test info endpoint."""
    response = client.get("/info")
    assert response.status_code == 200
    
    data = response.json()
    assert "app_name" in data
    assert "version" in data
    assert "debug" in data
    assert "database_url" in data
    assert "redis_url" in data
    assert "celery_broker" in data
