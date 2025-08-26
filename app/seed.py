from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import SessionLocal, engine, Base
from . import models

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # If classes already exist, skip
        if db.scalar(select(models.FitnessClass).limit(1)) is not None:
            return

        ist = ZoneInfo("Asia/Kolkata")
        now_ist = datetime.now(ist)

        data = [
            ("Yoga", "Asha", now_ist + timedelta(days=1, hours=9), 10),
            ("Zumba", "Rohit", now_ist + timedelta(days=1, hours=18), 15),
            ("HIIT", "Meera", now_ist + timedelta(days=2, hours=7), 12),
        ]
        for name, instr, start_ist, cap in data:
            # store as UTC
            start_utc = start_ist.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
            db.add(models.FitnessClass(name=name, instructor=instr, start_time_utc=start_utc, capacity=cap))
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
