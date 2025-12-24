"""
Calendar service for querying Google Calendar events
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List, Tuple, Optional
from googleapiclient.errors import HttpError
from services.google_auth import get_calendar_service
from config import TIMEZONE


def get_events_for_date(date: datetime) -> List[dict]:
    """
    Query Google Calendar for events on a specific date.
    
    Args:
        date: datetime object representing the date (timezone-aware, in local timezone)
    
    Returns:
        List of event dictionaries from Google Calendar API
    """
    try:
        service = get_calendar_service()
        
        # Convert date to timezone-aware datetime if not already
        if date.tzinfo is None:
            tz = ZoneInfo(TIMEZONE)
            date = date.replace(tzinfo=tz)
        
        # Get start and end of day in the local timezone
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Convert to UTC for API call
        start_utc = start_of_day.astimezone(ZoneInfo("UTC"))
        end_utc = end_of_day.astimezone(ZoneInfo("UTC"))
        
        # Format as RFC3339 for Google Calendar API
        time_min = start_utc.isoformat()
        time_max = end_utc.isoformat()
        
        # Query calendar events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Convert event times back to local timezone for easier processing
        processed_events = []
        local_tz = ZoneInfo(TIMEZONE)
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Parse datetime strings
            if 'T' in start:  # dateTime format
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                # Convert to local timezone
                start_dt = start_dt.astimezone(local_tz)
                end_dt = end_dt.astimezone(local_tz)
            else:  # date format (all-day events)
                start_dt = datetime.fromisoformat(start).replace(tzinfo=local_tz)
                end_dt = datetime.fromisoformat(end).replace(tzinfo=local_tz)
            
            processed_events.append({
                'id': event.get('id'),
                'start': start_dt,
                'end': end_dt,
                'summary': event.get('summary', 'No title'),
                'status': event.get('status')
            })
        
        return processed_events
        
    except HttpError as e:
        raise Exception(f"Google Calendar API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error querying calendar: {str(e)}")


def create_calendar_event(
    attendee_name: str,
    attendee_email: str,
    start_time: datetime,
    end_time: datetime,
    notes: Optional[str] = None
) -> str:
    """
    Create a Google Calendar event for a booking.
    
    Args:
        attendee_name: Name of the attendee
        attendee_email: Email address of the attendee
        start_time: Start datetime of the event (timezone-aware)
        end_time: End datetime of the event (timezone-aware)
        notes: Optional notes/reason for the meeting
    
    Returns:
        The Google Calendar event ID
    
    Raises:
        Exception if event creation fails
    """
    try:
        service = get_calendar_service()
        
        # Ensure datetimes are timezone-aware
        if start_time.tzinfo is None:
            local_tz = ZoneInfo(TIMEZONE)
            start_time = start_time.replace(tzinfo=local_tz)
        if end_time.tzinfo is None:
            local_tz = ZoneInfo(TIMEZONE)
            end_time = end_time.replace(tzinfo=local_tz)
        
        # Convert to UTC for Google Calendar API
        start_utc = start_time.astimezone(ZoneInfo("UTC"))
        end_utc = end_time.astimezone(ZoneInfo("UTC"))
        
        # Format as RFC3339 for Google Calendar API
        start_time_str = start_utc.isoformat()
        end_time_str = end_utc.isoformat()
        
        # Build event description
        description_parts = [
            f"Attendee: {attendee_name} ({attendee_email})"
        ]
        if notes:
            description_parts.append(f"\nNotes: {notes}")
        description = "\n".join(description_parts)
        
        # Create event body
        event = {
            'summary': f'Coffee Chat with {attendee_name}',
            'description': description,
            'start': {
                'dateTime': start_time_str,
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': 'UTC'
            },
            'attendees': [
                {'email': attendee_email}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 15}  # 15 minutes before
                ]
            }
        }
        
        # Insert event into calendar
        created_event = service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'  # Send email notifications to attendees
        ).execute()
        
        return created_event.get('id')
        
    except HttpError as e:
        raise Exception(f"Google Calendar API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error creating calendar event: {str(e)}")

