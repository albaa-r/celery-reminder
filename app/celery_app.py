from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"]
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_always_eager=False
)

celery_app.conf.beat_schedule = {
    "check-reminders-every-10-seconds": {
        "task": "app.tasks.process_due_reminders",
        "schedule": 10.0,
    },
}

print("BROKER:", celery_app.conf.broker_url)