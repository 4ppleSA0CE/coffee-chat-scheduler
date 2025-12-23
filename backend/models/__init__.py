"""
Database models using SQLModel
"""
from sqlmodel import SQLModel, Field, Column, DateTime
from datetime import datetime
from typing import Optional
from sqlalchemy import func


class Booking(SQLModel, table=True):
    """
    Booking model - stores information about calendar bookings
    """
    __tablename__ = "bookings"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    google_event_id: Optional[str] = Field(default=None, unique=True, index=True)
    attendee_name: str
    attendee_email: str = Field(index=True)
    start_time: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True))
    end_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    notes: Optional[str] = None
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    status: str = Field(default='confirmed')

