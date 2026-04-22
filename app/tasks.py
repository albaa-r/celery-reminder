from .celery_app import celery_app
from datetime import datetime, timezone

from .database import SessionLocal
from .models import Reminder

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def send_reminder(self, reminder_id: int):
    db = SessionLocal()

    reminder = db.query(Reminder).get(reminder_id)

    if not reminder:
        db.close()
        return

    # idempotency check
    if reminder.status == "done":
        db.close()
        return

    print(f"[{datetime.now()}] REMINDER: {reminder.message}")

    reminder.status = "done"
    db.commit()

    db.close()


@celery_app.task
def process_due_reminders():
    db = SessionLocal()

    now = datetime.now(timezone.utc)

    reminders = db.query(Reminder).filter(
        Reminder.run_at <= now,
        Reminder.status == "scheduled"
    ).all()

    for r in reminders:
        send_reminder.delay(r.id)

    db.close()