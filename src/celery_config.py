"""
Celery configuration and application instance
"""

import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

broker_url = os.getenv(
    "CELERY_BROKER_URL",
    os.getenv("REDIS_URL", "redis://:redis_secure_pass@redis:6379/0")
)
result_backend = os.getenv(
    "CELERY_RESULT_BACKEND",
    os.getenv("REDIS_URL", "redis://:redis_secure_pass@redis:6379/1")
)

celery_app = Celery(
    "smart_notification",
    broker=broker_url,
    backend=result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_routes={
        "tasks.send_notification_task": {"queue": "notifications"}
    },
    broker_transport_options={"visibility_timeout": 3600},
    result_expires=3600,
)
