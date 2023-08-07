from celery.schedules import crontab
from celery import Celery
import config
from tasks.notification import create_notifications

celery = Celery(__name__)
celery.conf.broker_url = config.CELERY_BROKER_URL
celery.conf.result_backend = config.CELERY_RESULT_BACKEND

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
