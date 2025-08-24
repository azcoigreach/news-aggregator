"""
Main API router for v1 endpoints.
"""
from fastapi import APIRouter

from .endpoints import (
    topics,
    articles,
    sources,
    crawling,
    fact_checking,
    summarization,
    correlation,
    configuration,
    monitoring
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(crawling.router, prefix="/crawling", tags=["crawling"])
api_router.include_router(fact_checking.router, prefix="/fact-checking", tags=["fact-checking"])
api_router.include_router(summarization.router, prefix="/summarization", tags=["summarization"])
api_router.include_router(correlation.router, prefix="/correlation", tags=["correlation"])
api_router.include_router(configuration.router, prefix="/configuration", tags=["configuration"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
