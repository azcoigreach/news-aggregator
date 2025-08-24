"""
API endpoint modules for the News Aggregator application.
"""

# Import all endpoint modules so they can be imported from this package
from . import (
    topics,
    articles,
    sources,
    crawling,
    fact_checking,
    summarization,
    correlation,
    configuration,
    monitoring,
    health
)

__all__ = [
    "topics",
    "articles", 
    "sources",
    "crawling",
    "fact_checking",
    "summarization",
    "correlation",
    "configuration",
    "monitoring",
    "health"
]
