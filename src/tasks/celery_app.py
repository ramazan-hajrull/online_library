from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,  # нужен, чтобы можно было опрашивать статус отчёта по task_id
    include=[
        "src.tasks.tasks"
    ]
)


celery_instance.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


# Периодические задачи (нужен отдельный процесс `celery -A src.tasks.celery_app.celery_instance beat`)
celery_instance.conf.beat_schedule = {
    "cleanup-expired-cache-every-hour": {
        "task": "cleanup_expired_cache",
        "schedule": crontab(minute=0),
    },
    "refresh-materialized-views-every-15-min": {
        "task": "refresh_materialized_views",
        "schedule": crontab(minute="*/15"),
    },
}
