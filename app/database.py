import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://user:password@postgres:5432/reminder_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def wait_for_db():
    while True:
        try:
            engine.connect()
            print("✅ Database ready!")
            break
        except OperationalError:
            print("⏳ Waiting for database...")
            time.sleep(2)