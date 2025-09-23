"""
Celery application configuration for distributed processing
"""

from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "3d_platform",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.video_processing",
        "app.tasks.colmap_processing",
        "app.tasks.file_management"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hour
    task_routes={
        "app.tasks.video_processing.*": {"queue": "video_processing"},
        "app.tasks.colmap_processing.*": {"queue": "colmap_processing"},
        "app.tasks.file_management.*": {"queue": "file_management"},
    },
    task_annotations={
        "*": {"rate_limit": "10/s"},
        "app.tasks.colmap_processing.*": {"rate_limit": "2/s"},
    }
)

# Optional configuration for monitoring
celery_app.conf.update(
    worker_send_task_events=True,
    task_send_sent_event=True,
)

if __name__ == "__main__":
    celery_app.start()



