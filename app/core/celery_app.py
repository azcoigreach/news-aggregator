"""
Celery application configuration for background task processing.
"""
from celery import Celery
from .config import settings

# Create Celery app
celery_app = Celery(
    "news_aggregator",
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend,
    include=[
        "app.services.crawler.tasks",
        "app.services.fact_checker.tasks",
        "app.services.summarizer.tasks",
        "app.services.correlation.tasks",
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer=settings.celery.task_serializer,
    result_serializer=settings.celery.result_serializer,
    accept_content=settings.celery.accept_content,
    timezone=settings.celery.timezone,
    enable_utc=settings.celery.enable_utc,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,
)

# Optional: Configure task routing
celery_app.conf.task_routes = {
    "app.services.crawler.tasks.*": {"queue": "crawler"},
    "app.services.fact_checker.tasks.*": {"queue": "fact_checker"},
    "app.services.summarizer.tasks.*": {"queue": "summarizer"},
    "app.services.correlation.tasks.*": {"queue": "correlation"},
}

# Optional: Configure periodic tasks
celery_app.conf.beat_schedule = {
    "crawl-news": {
        "task": "app.services.crawler.tasks.crawl_all_topics",
        "schedule": 300.0,  # Every 5 minutes
    },
    "fact-check-articles": {
        "task": "app.services.fact_checker.tasks.process_pending_articles",
        "schedule": 600.0,  # Every 10 minutes
    },
    "correlate-stories": {
        "task": "app.services.correlation.tasks.find_correlations",
        "schedule": 1800.0,  # Every 30 minutes
    },
}
