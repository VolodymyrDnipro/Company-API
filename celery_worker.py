from celery.schedules import crontab
from celery import Celery
from config import settings
from tasks.notification import create_notifications

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.conf.beat_schedule = {
    "check_test_times_task": {
        "task": "create_notification",
        "schedule": crontab(hour=0, minute=0),
    },
}


#
@celery.task(name="check_test_times")
def check_test_times():
    create_notifications()
