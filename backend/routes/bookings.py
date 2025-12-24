"""
Booking API endpoint
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import Session
from models import Booking
from database import get_db
from services.calendar_service import get_events_for_date, create_calendar_event
from routes.availability import is_slot_conflicting, WORKING_HOURS_START, WORKING_HOURS_END, SLOT_DURATION_MINUTES
from config import TIMEZONE

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


class BookingRequest(BaseModel):
    """Request model for creating a booking"""
    attendee_name: str
    attendee_email: EmailStr
    start_time: str  # ISO 8601 format datetime string
    end_time: str  # ISO 8601 format datetime string
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    """Response model for booking confirmation"""
    id: int
    google_event_id: Optional[str]
    attendee_name: str
    attendee_email: str
    start_time: str  # ISO 8601 format
    end_time: str  # ISO 8601 format
    notes: Optional[str]
    status: str
    created_at: str  # ISO 8601 format


def parse_datetime(dt_str: str) -> datetime:
    """
    Parse ISO 8601 datetime string to timezone-aware datetime.
    
    Args:
        dt_str: ISO 8601 formatted datetime string
    
    Returns:
        timezone-aware datetime object
    
    Raises:
        HTTPException if parsing fails
    """
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        # Ensure timezone-aware
        if dt.tzinfo is None:
            local_tz = ZoneInfo(TIMEZONE)
            dt = dt.replace(tzinfo=local_tz)
        return dt
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid datetime format. Expected ISO 8601 format, got: {dt_str}"
        )


def validate_time_slot(start_time: datetime, end_time: datetime) -> None:
    """
    Validate that a time slot meets business rules.
    
    Args:
        start_time: Start datetime of the slot
        end_time: End datetime of the slot
    
    Raises:
        HTTPException if validation fails
    """
    local_tz = ZoneInfo(TIMEZONE)
    now = datetime.now(local_tz)
    
    # Ensure timezone-aware
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=local_tz)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=local_tz)
    
    # Convert to local timezone for validation
    start_time = start_time.astimezone(local_tz)
    end_time = end_time.astimezone(local_tz)
    
    # Check if slot is in the past
    if start_time < now:
        raise HTTPException(
            status_code=400,
            detail="Cannot book appointments in the past. Please select a future time slot."
        )
    
    # Check minimum lead time (24 hours)
    min_booking_time = now + timedelta(hours=24)
    if start_time < min_booking_time:
        raise HTTPException(
            status_code=400,
            detail="Cannot book appointments with less than 24 hours lead time. Please select a time slot at least 24 hours in advance."
        )
    
    # Check duration is exactly 30 minutes
    duration = end_time - start_time
    expected_duration = timedelta(minutes=SLOT_DURATION_MINUTES)
    if duration != expected_duration:
        raise HTTPException(
            status_code=400,
            detail=f"Slot duration must be exactly {SLOT_DURATION_MINUTES} minutes."
        )
    
    # Check working hours - slot must start during working hours
    # Allow slots that start at or after WORKING_HOURS_START and end by WORKING_HOURS_END
    if start_time.hour < WORKING_HOURS_START:
        raise HTTPException(
            status_code=400,
            detail=f"Bookings must start at or after {WORKING_HOURS_START}:00."
        )
    
    # Check that slot doesn't extend past working hours
    if end_time.hour > WORKING_HOURS_END or (end_time.hour == WORKING_HOURS_END and end_time.minute > 0):
        raise HTTPException(
            status_code=400,
            detail=f"Bookings must end by {WORKING_HOURS_END}:00."
        )


def is_slot_available(start_time: datetime, end_time: datetime) -> bool:
    """
    Check if a specific time slot is currently available.
    
    Args:
        start_time: Start datetime of the slot
        end_time: End datetime of the slot
    
    Returns:
        True if slot is available, False otherwise
    """
    try:
        # Get events for the date
        events = get_events_for_date(start_time)
        
        # Check if slot conflicts with existing events
        return not is_slot_conflicting(start_time, end_time, events)
    except Exception:
        # If we can't check, assume not available for safety
        return False


@router.post("", response_model=BookingResponse, status_code=201)
def create_booking(booking_request: BookingRequest, db: Session = Depends(get_db)):
    """
    Create a new booking.
    
    This endpoint:
    1. Validates the booking request
    2. Checks if the time slot is still available
    3. Creates a Google Calendar event
    4. Stores the booking in the database
    5. Returns the booking confirmation
    """
    try:
        # Parse datetime strings
        start_time = parse_datetime(booking_request.start_time)
        end_time = parse_datetime(booking_request.end_time)
        
        # Validate time slot meets business rules
        validate_time_slot(start_time, end_time)
        
        # Check if slot is still available (race condition protection)
        if not is_slot_available(start_time, end_time):
            raise HTTPException(
                status_code=409,
                detail="The requested time slot is no longer available. Please select another time."
            )
        
        # Create Google Calendar event
        try:
            google_event_id = create_calendar_event(
                attendee_name=booking_request.attendee_name,
                attendee_email=booking_request.attendee_email,
                start_time=start_time,
                end_time=end_time,
                notes=booking_request.notes
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create calendar event: {str(e)}"
            )
        
        # Store booking in database
        # Convert times to UTC for storage
        start_time_utc = start_time.astimezone(ZoneInfo("UTC"))
        end_time_utc = end_time.astimezone(ZoneInfo("UTC"))
        
        booking = Booking(
            google_event_id=google_event_id,
            attendee_name=booking_request.attendee_name,
            attendee_email=booking_request.attendee_email,
            start_time=start_time_utc,
            end_time=end_time_utc,
            notes=booking_request.notes,
            status='confirmed'
        )
        
        try:
            db.add(booking)
            db.commit()
            db.refresh(booking)
        except Exception as e:
            # If database save fails, we should ideally delete the calendar event
            # For MVP, we'll just raise an error
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save booking to database: {str(e)}"
            )
        
        # Return booking confirmation
        # Convert times back to local timezone for response
        start_time_local = booking.start_time.astimezone(ZoneInfo(TIMEZONE))
        end_time_local = booking.end_time.astimezone(ZoneInfo(TIMEZONE))
        created_at_local = booking.created_at.astimezone(ZoneInfo(TIMEZONE))
        
        return BookingResponse(
            id=booking.id,
            google_event_id=booking.google_event_id,
            attendee_name=booking.attendee_name,
            attendee_email=booking.attendee_email,
            start_time=start_time_local.isoformat(),
            end_time=end_time_local.isoformat(),
            notes=booking.notes,
            status=booking.status,
            created_at=created_at_local.isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

