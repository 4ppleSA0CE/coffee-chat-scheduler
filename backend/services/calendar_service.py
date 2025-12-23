"""
Calendar service for querying Google Calendar events
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List, Tuple
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

