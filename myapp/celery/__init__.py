from celery.schedules import crontab

from myapp import config
from myapp.app import init_celery

celery = init_celery()
celery.conf.update(config.CELERY)
celery.conf.imports = celery.conf.imports + ("myapp.celery.tasks")
celery.conf.beat_schedule = {
    "run-two-times-a-day": {
        "task": "test_task",
        "schedule": crontab(minute=0, hour="9,21"),
    },
    "run-two-times-a-day": {
        "task": "test_task",
        "schedule": crontab(minute=0, hour="9,21"),
    },
}
celery.conf.timezone = "UTC"
