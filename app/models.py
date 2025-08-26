from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class FitnessClass(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    # stored in UTC
    start_time_utc = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False, default=20)

    bookings = relationship("Booking", back_populates="klass", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False, index=True)

    klass = relationship("FitnessClass", back_populates="bookings")

    __table_args__ = (UniqueConstraint("class_id", "client_email", name="uq_booking_per_email_per_class"),)
