from fastapi import FastAPI
from datetime import datetime, timezone
from dateutil import parser
from .celery_app import celery_app 

from .database import engine, SessionLocal, wait_for_db
from .models import Base, Reminder

#############################################
#format testing :
# message : terserah
# run-at : 2026-04-01T21:00:00+07:00
#############################################


app = FastAPI()

@app.on_event("startup")
def startup():
    wait_for_db()
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Reminder API running"}

@app.post("/reminder")
def create_reminder(message: str, run_at: str):
    db = SessionLocal()

    run_time = parser.parse(run_at).astimezone(timezone.utc)

    reminder = Reminder(
        message=message,
        run_at=run_time,
        status="scheduled"
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    db.close()

    return {"id": reminder.id, "status": "scheduled"}

@app.get("/reminders")
def get_reminders():
    db = SessionLocal()

    reminders = db.query(Reminder).all()

    result = []
    for r in reminders:
        result.append({
            "id": r.id,
            "message": r.message,
            "run_at": r.run_at,
            "status": r.status
        })

    db.close()
    return result

from fastapi import HTTPException

@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: int):
    db = SessionLocal()

    reminder = db.query(Reminder).get(reminder_id)

    if not reminder:
        db.close()
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()
    db.close()

    return {"message": f"Reminder {reminder_id} deleted"}