"""
Celery worker entrypoint
"""

from celery_config import celery_app
import tasks  # noqa: F401


app = celery_app
