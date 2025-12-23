"""
Authentication routes (OAuth)
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from services.google_auth import create_flow

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google")
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


@router.get("/callback")
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

