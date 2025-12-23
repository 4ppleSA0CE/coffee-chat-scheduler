"""
Configuration and environment variables
"""
from dotenv import load_dotenv
import os

load_dotenv()

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Timezone configuration (default to America/Toronto, can be overridden via env)
TIMEZONE = os.getenv("TIMEZONE", "America/Toronto")

# Validate required environment variables at startup
if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
    raise ValueError("Missing required environment variables: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, or GOOGLE_REDIRECT_URI")

