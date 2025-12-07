import os

from celery import Celery

from datetime import timedelta

from src.settings.config.config import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("TransactionApp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "notify": {
        "task": "apps.wallets.tasks.notify.send_notification",
        "schedule": timedelta(minutes=config.task.CELERY_NOTIFY_INTERVAL),
    },
}


app.conf.timezone = "Asia/Tashkent"
