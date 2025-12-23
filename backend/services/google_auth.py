"""
Google OAuth and Calendar API services
"""
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi import HTTPException
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_REFRESH_TOKEN, SCOPES


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


def get_calendar_service():
    """Get authenticated Google Calendar API service"""
    credentials = get_credentials()
    return build('calendar', 'v3', credentials=credentials)

