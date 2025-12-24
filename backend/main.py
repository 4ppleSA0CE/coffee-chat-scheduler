"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine
import os

# Import models to register them with SQLModel
from models import Booking

# Import routers
from routes.auth import router as auth_router
from routes.test import router as test_router
from routes.availability import router as availability_router
from routes.bookings import router as bookings_router

# Initialize FastAPI app
app = FastAPI(
    title="Coffee Chat Scheduler",
    description="API for scheduling coffee chats via Google Calendar",
    version="1.0.0"
)

# Configure CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
# Handle both single URL and comma-separated URLs for multiple environments
allowed_origins = [origin.strip() for origin in FRONTEND_URL.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(test_router)
app.include_router(availability_router)
app.include_router(bookings_router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Coffee Chat Scheduler API", "version": "1.0.0"}


# Create database tables on startup
@app.on_event("startup")
def create_tables():
    """Create database tables if they don't exist"""
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created/verified successfully")
    except Exception as e:
        print(f"Warning: Could not connect to database during startup: {e}")
        print("Database tables will be created on first use")
        # Don't fail startup - tables will be created when first accessed
