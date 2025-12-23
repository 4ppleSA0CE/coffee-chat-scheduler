"""
Database connection and session management
"""
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables")

#

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging (helpful for debugging)
)


def get_db():
    """
    Dependency function for FastAPI routes to get database session.
    Yields a database session and ensures it's closed after use.
    """
    with Session(engine) as session:
        yield session

