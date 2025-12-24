# Backend Startup Guide

This guide will help you start the FastAPI backend server.

## Prerequisites

- Python 3.8+ installed
- Virtual environment set up (already exists in `backend/venv/`)
- Environment variables configured in `.env` file

## Step-by-Step Instructions

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn (ASGI server)
- Google API clients
- Database drivers
- Other dependencies

### 4. Set Up Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# Google OAuth Configuration (Required)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
GOOGLE_REFRESH_TOKEN=your_refresh_token_here

# Database Configuration (Required)
DATABASE_URL=postgresql://user:password@host:port/database

# Optional Configuration
TIMEZONE=America/Toronto
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
```

**Note**: The `.env` file should already be in `.gitignore` to keep your secrets safe.

### 5. Start the Server

**Development mode (with auto-reload):**
```bash
uvicorn main:app --reload
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6. Verify Server is Running

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
Database tables created/verified successfully
INFO:     Application startup complete.
```

### 7. Test the Server

Open your browser and visit:
- **API Root**: http://localhost:8000/
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Quick Start Command (One-liner)

If you've already set up everything, you can start the server with:

```bash
cd backend && source venv/bin/activate && uvicorn main:app --reload
```

## Troubleshooting

### Error: "Missing required environment variables"

**Solution**: Make sure your `.env` file exists in the `backend/` directory and contains all required variables:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- `DATABASE_URL`

### Error: "DATABASE_URL not set in environment variables"

**Solution**: Add `DATABASE_URL` to your `.env` file. Format:
```
DATABASE_URL=postgresql://user:password@host:port/database
```

### Error: "ModuleNotFoundError" or "No module named 'fastapi'"

**Solution**: Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Error: Port 8000 already in use

**Solution**: Either:
1. Stop the other process using port 8000, or
2. Use a different port:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Error: Database connection failed

**Solution**: 
1. Verify your `DATABASE_URL` is correct
2. Check that your database server is running
3. Ensure network/firewall allows the connection
4. The server will still start but will show a warning - tables will be created on first use

## Next Steps

Once the server is running:

1. **Complete OAuth Authentication**: Visit http://localhost:8000/auth/google
2. **Test Calendar Access**: Visit http://localhost:8000/api/test/calendar
3. **Test Database**: Visit http://localhost:8000/api/test/db
4. **Test Bookings**: See [TESTING_BOOKINGS.md](./TESTING_BOOKINGS.md)

## Server Endpoints

Once running, the following endpoints are available:

- `GET /` - API root/info
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation
- `GET /auth/google` - Start OAuth flow
- `GET /auth/callback` - OAuth callback handler
- `GET /api/test/calendar` - Test Google Calendar access
- `GET /api/test/db` - Test database connection
- `GET /api/availability?date=YYYY-MM-DD` - Get available time slots
- `POST /api/bookings` - Create a new booking

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

