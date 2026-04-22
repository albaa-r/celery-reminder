from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    run_at = Column(DateTime)
    status = Column(String, default="scheduled")