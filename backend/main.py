from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi.responses import RedirectResponse, JSONResponse

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Validate required environment variables at startup
if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
    raise ValueError("Missing required environment variables: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, or GOOGLE_REDIRECT_URI")

app = FastAPI()

def create_flow():
    """Create and return an OAuth Flow object"""
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [GOOGLE_REDIRECT_URI]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    
    return flow

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/auth/google")
def google_auth():
    """Initiate OAuth flow - redirects user to Google login"""
    try:
        flow = create_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',  # Required to get refresh token
            include_granted_scopes='true',
            prompt='consent'  # Force consent screen to ensure we get refresh token
        )
        return RedirectResponse(url=authorization_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth initiation failed: {str(e)}")

@app.get("/auth/callback")
def callback(code: str = None, error: str = None):
    """Handle OAuth callback - exchange code for tokens"""
    # Handle OAuth errors (user denied access, etc.)
    if error:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth error: {error}. User may have denied access."
        )
    
    if not code:
        raise HTTPException(
            status_code=400,
            detail="No authorization code received from Google"
        )
    
    try:
        flow = create_flow()
        flow.fetch_token(code=code)
        
        # Get credentials
        credentials = flow.credentials
        
        # Extract refresh token (this is what you need to save!)
        refresh_token = credentials.refresh_token
        
        if not refresh_token:
            return JSONResponse(
                status_code=400,
                content={"error": "No refresh token received. Make sure prompt='consent' is set."}
            )
        
        # For now, print it so you can copy to .env
        # In production, you'd store this securely
        print(f"\n=== IMPORTANT: Save this refresh token to your .env file ===")
        print(f"GOOGLE_REFRESH_TOKEN={refresh_token}")
        print(f"================================================================\n")
        
        return JSONResponse(content={
            "message": "OAuth successful! Check your terminal for the refresh token.",
            "refresh_token": refresh_token,
            "instructions": "Copy the refresh_token above and add it to your .env file as GOOGLE_REFRESH_TOKEN"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")

def get_credentials():
    """Get credentials using refresh token"""
    if not GOOGLE_REFRESH_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_REFRESH_TOKEN not set in environment variables"
        )
    
    credentials = Credentials(
        token=None,  # We'll refresh it
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=SCOPES
    )
    
    # Refresh the access token
    request = Request()
    credentials.refresh(request)
    
    return credentials

@app.get("/api/test/calendar")
def test_calendar():
    """Test endpoint to verify calendar API access"""
    try:
        # Get credentials using refresh token
        credentials = get_credentials()
        
        # Build the Calendar API service
        service = build('calendar', 'v3', credentials=credentials)
        
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