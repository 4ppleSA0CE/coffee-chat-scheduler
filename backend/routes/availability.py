"""
Availability API endpoint
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List
from pydantic import BaseModel
from services.calendar_service import get_events_for_date
from config import TIMEZONE

router = APIRouter(prefix="/api/availability", tags=["availability"])


# Business rules
WORKING_HOURS_START = 9  # 9:00 AM
WORKING_HOURS_END = 18  # 6:00 PM (18:00)
SLOT_DURATION_MINUTES = 30
BUFFER_MINUTES = 15
MINIMUM_LEAD_TIME_HOURS = 24


class TimeSlot(BaseModel):
    """Time slot model for API response"""
    start: str  # ISO 8601 format
    end: str  # ISO 8601 format


class AvailabilityResponse(BaseModel):
    """Response model for availability endpoint"""
    date: str
    available_slots: List[TimeSlot]
    timezone: str


def generate_time_slots(date: datetime) -> List[tuple[datetime, datetime]]:
    """
    Generate all potential time slots for a given date within working hours.
    
    Args:
        date: datetime object for the date (timezone-aware, in local timezone)
    
    Returns:
        List of (start, end) datetime tuples for all potential slots
    """
    slots = []
    local_tz = ZoneInfo(TIMEZONE)
    
    # Ensure date is timezone-aware and in local timezone
    if date.tzinfo is None:
        date = date.replace(tzinfo=local_tz)
    else:
        date = date.astimezone(local_tz)
    
    # Get start of working day
    slot_start = date.replace(hour=WORKING_HOURS_START, minute=0, second=0, microsecond=0)
    
    # Generate slots until we reach the end of working hours
    while slot_start.hour < WORKING_HOURS_END or (slot_start.hour == WORKING_HOURS_END and slot_start.minute == 0):
        slot_end = slot_start + timedelta(minutes=SLOT_DURATION_MINUTES)
        
        # Don't create a slot that extends past working hours
        if slot_end.hour > WORKING_HOURS_END or (slot_end.hour == WORKING_HOURS_END and slot_end.minute > 0):
            break
        
        slots.append((slot_start, slot_end))
        slot_start += timedelta(minutes=SLOT_DURATION_MINUTES)
    
    return slots


def is_slot_conflicting(slot_start: datetime, slot_end: datetime, events: List[dict]) -> bool:
    """
    Check if a time slot conflicts with any existing events (including buffer time).
    
    Args:
        slot_start: Start time of the slot
        slot_end: End time of the slot
        events: List of event dictionaries with 'start' and 'end' datetime fields
    
    Returns:
        True if slot conflicts, False otherwise
    """
    buffer_delta = timedelta(minutes=BUFFER_MINUTES)
    
    for event in events:
        event_start = event['start']
        event_end = event['end']
        
        # Apply buffer time (15 minutes before and after event)
        buffered_start = event_start - buffer_delta
        buffered_end = event_end + buffer_delta
        
        # Check for overlap
        # Slot conflicts if it overlaps with the buffered event time
        if slot_start < buffered_end and slot_end > buffered_start:
            return True
    
    return False


def validate_date(date_str: str) -> datetime:
    """
    Validate and parse date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
    
    Returns:
        datetime object (timezone-aware, in local timezone)
    
    Raises:
        HTTPException if date is invalid, in past, or same-day
    """
    try:
        # Parse date string
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Expected YYYY-MM-DD, got: {date_str}"
        )
    
    # Make timezone-aware in local timezone
    local_tz = ZoneInfo(TIMEZONE)
    date = date.replace(tzinfo=local_tz)
    
    # Get current time in local timezone
    now = datetime.now(local_tz)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Check if date is in the past
    if date < today_start:
        raise HTTPException(
            status_code=400,
            detail="Cannot book appointments in the past. Please select a future date."
        )
    
    # Check if date is today (same-day booking not allowed)
    if date.date() == today_start.date():
        raise HTTPException(
            status_code=400,
            detail="Cannot book same-day appointments. Please select a date at least 24 hours in advance."
        )
    
    # Check minimum lead time (24 hours from now)
    # Check if the earliest possible slot (9 AM) on the requested date is at least 24 hours away
    earliest_slot = date.replace(hour=WORKING_HOURS_START, minute=0, second=0, microsecond=0)
    min_booking_time = now + timedelta(hours=MINIMUM_LEAD_TIME_HOURS)
    if earliest_slot < min_booking_time:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot book appointments with less than {MINIMUM_LEAD_TIME_HOURS} hours lead time. Please select a date at least 24 hours in advance."
        )
    
    return date


@router.get("", response_model=AvailabilityResponse)
def get_availability(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    """
    Get available time slots for a given date.
    
    Business rules:
    - Working hours: 9:00 AM - 6:00 PM (local time)
    - Available all days (including weekends)
    - Slot duration: 30 minutes
    - Buffer time: 15 minutes before/after existing events
    - Minimum lead time: 24 hours
    """
    try:
        # Validate and parse date
        requested_date = validate_date(date)
        
        # Get existing events for the date
        try:
            events = get_events_for_date(requested_date)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error querying calendar: {str(e)}"
            )
        
        # Generate all potential time slots
        potential_slots = generate_time_slots(requested_date)
        
        # Filter out conflicting slots
        available_slots = []
        for slot_start, slot_end in potential_slots:
            if not is_slot_conflicting(slot_start, slot_end, events):
                available_slots.append(
                    TimeSlot(
                        start=slot_start.isoformat(),
                        end=slot_end.isoformat()
                    )
                )
        
        return AvailabilityResponse(
            date=date,
            available_slots=available_slots,
            timezone=TIMEZONE
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

