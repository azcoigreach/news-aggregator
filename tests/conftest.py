"""
Pytest configuration and fixtures for the News Aggregator application.
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.core.database import Base, get_db
from app.main import app
from app.core.config import settings


# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def mock_openai():
    """Mock OpenAI API client."""
    with patch("app.services.fact_checker.openai.OpenAI") as mock:
        mock.return_value.chat.completions.create.return_value.choices[0].message.content = "Mocked fact check response"
        yield mock


@pytest.fixture
def mock_claude():
    """Mock Claude API client."""
    with patch("app.services.fact_checker.anthropic.Anthropic") as mock:
        mock.return_value.messages.create.return_value.content[0].text = "Mocked Claude response"
        yield mock


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch("redis.from_url") as mock:
        mock_redis_instance = Mock()
        mock_redis_instance.ping.return_value = True
        mock.return_value = mock_redis_instance
        yield mock


@pytest.fixture
def sample_topic_data():
    """Sample topic data for testing."""
    return {
        "name": "AI Technology",
        "description": "News about artificial intelligence and machine learning",
        "keywords": ["artificial intelligence", "machine learning", "AI"],
        "sources": ["https://techcrunch.com", "https://wired.com"],
        "active": True,
        "priority": 5,
        "crawl_frequency": 300,
        "max_articles_per_crawl": 50,
        "enable_fact_checking": True,
        "enable_summarization": True,
        "enable_correlation": True
    }


@pytest.fixture
def sample_article_data():
    """Sample article data for testing."""
    return {
        "title": "New Breakthrough in AI Technology",
        "content": "Scientists have discovered a new method for training neural networks...",
        "url": "https://example.com/article1",
        "source_url": "https://example.com",
        "author": "John Doe",
        "published_at": "2024-01-01T10:00:00Z",
        "language": "en",
        "word_count": 500,
        "reading_time": 3
    }


@pytest.fixture
def sample_fact_check_data():
    """Sample fact check data for testing."""
    return {
        "claim": "AI can now solve complex problems",
        "verdict": "mostly_true",
        "confidence_score": 0.85,
        "explanation": "Multiple sources confirm this claim with high confidence",
        "sources": ["https://source1.com", "https://source2.com"],
        "model_used": "gpt-4",
        "processing_time": 2.5
    }
