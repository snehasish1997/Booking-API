from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

from .db import SessionLocal, engine, Base
from . import models, schemas
from .utils import to_tz

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

app = FastAPI(title="Omnify Booking System", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/classes", response_model=list[schemas.ClassOut])
def list_classes(tz: str = Query(default="Asia/Kolkata", description="Choose your timezone"),
                 db: Session = Depends(get_db)):
    # fetch classes and available slots
    classes = db.scalars(select(models.FitnessClass)).all()
    result = []
    for c in classes:
        booked = db.scalar(select(func.count(models.Booking.id)).where(models.Booking.class_id == c.id)) or 0
        available = max(0, c.capacity - booked)
        result.append(schemas.ClassOut(
            id=c.id,
            name=c.name,
            instructor=c.instructor,
            start_time=to_tz(c.start_time_utc, tz),
            timezone=tz,
            capacity=c.capacity,
            available_slots=available
        ))
    return result

@app.post("/book", response_model=schemas.BookingOut, status_code=201)
def create_booking(payload: schemas.BookingIn, db: Session = Depends(get_db)):
    # Check class exists
    klass = db.get(models.FitnessClass, payload.class_id)
    if not klass:
        raise HTTPException(status_code=404, detail="Class not found")

    # Check capacity
    booked = db.scalar(select(func.count(models.Booking.id)).where(models.Booking.class_id == klass.id)) or 0
    if booked >= klass.capacity:
        raise HTTPException(status_code=409, detail="Class is full")

    # Enforce unique per email per class
    existing = db.scalar(select(func.count(models.Booking.id)).where(
        models.Booking.class_id == klass.id, models.Booking.client_email == payload.client_email))
    if existing:
        raise HTTPException(status_code=409, detail="You already booked this class with this email")

    booking = models.Booking(
        class_id=klass.id,
        client_name=payload.client_name.strip(),
        client_email=str(payload.client_email).lower(),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.get("/bookings", response_model=list[schemas.BookingOut])
def get_bookings(email: str = Query(..., description="Client email"),
                 db: Session = Depends(get_db)):
    # simple validation by pydantic would be better, but keep param simple
    email_norm = email.strip().lower()
    items = db.scalars(select(models.Booking).where(models.Booking.client_email == email_norm)).all()
    return items
