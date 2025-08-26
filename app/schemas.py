from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ClassOut(BaseModel):
    id: int
    name: str
    instructor: str
    start_time: datetime
    timezone: str
    capacity: int
    available_slots: int

    class Config:
        from_attributes = True

class BookingIn(BaseModel):
    class_id: int = Field(..., gt=0)
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr

    class Config:
        from_attributes = True
