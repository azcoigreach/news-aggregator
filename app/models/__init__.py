"""
Database models for the News Aggregator application.
"""
from .topic import Topic
from .source import Source
from .article import Article
from .fact_check import FactCheck
from .summary import Summary
from .correlation import Correlation
from .configuration import Configuration

__all__ = [
    "Topic",
    "Source", 
    "Article",
    "FactCheck",
    "Summary",
    "Correlation",
    "Configuration"
]
