"""
Test routes for verifying API functionality
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from database import get_db, engine
from models import Booking
from services.google_auth import get_calendar_service

router = APIRouter(prefix="/api/test", tags=["test"])


@router.get("/calendar")
def test_calendar():
    """Test endpoint to verify calendar API access"""
    try:
        # Build the Calendar API service
        service = get_calendar_service()
        
        # Get calendar list (this verifies we have access)
        calendar_list = service.calendarList().list().execute()
        
        # Get primary calendar ID
        primary_calendar = None
        for calendar in calendar_list.get('items', []):
            if calendar.get('primary'):
                primary_calendar = calendar
                break
        
        if not primary_calendar:
            primary_calendar = calendar_list.get('items', [{}])[0] if calendar_list.get('items') else {}
        
        # Get some upcoming events (next 10 events)
        events_result = service.events().list(
            calendarId='primary',
            maxResults=10,
            timeMin=None,  # Get all events
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format events for response
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_events.append({
                'id': event.get('id'),
                'summary': event.get('summary', 'No title'),
                'start': start,
                'status': event.get('status')
            })
        
        return JSONResponse(content={
            "message": "Successfully accessed Google Calendar!",
            "calendar_info": {
                "id": primary_calendar.get('id'),
                "summary": primary_calendar.get('summary', 'Primary Calendar'),
                "timezone": primary_calendar.get('timeZone')
            },
            "upcoming_events": formatted_events,
            "total_calendars": len(calendar_list.get('items', []))
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Calendar API test failed: {str(e)}"
        )


@router.get("/db")
def test_database(db: Session = Depends(get_db)):
    """Test endpoint to verify database connection and table creation"""
    try:
        # Try to query the bookings table (even if empty, this verifies table exists)
        statement = select(Booking)
        bookings = db.exec(statement).all()
        booking_count = len(bookings)
        
        # Get database info
        database_url = str(engine.url).replace(engine.url.password, "***") if engine.url.password else str(engine.url)
        
        return JSONResponse(content={
            "message": "Database connection successful!",
            "database_url": database_url,
            "bookings_table_exists": True,
            "total_bookings": booking_count,
            "table_name": "bookings"
        })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database test failed: {str(e)}"
        )

