import datetime
import time

from myapp.extensions import celery, db

@celery.task(name="sample_task")
def sample_task(task_type):
    time.sleep(int(task_type) * 1)
    return True
