# Coffee Chat Scheduler ☕

A single-tenant web application that allows visitors to book time slots on my personal Google Calendar.


## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Development](#-development)
- [Deployment](#-deployment)
- [Documentation](#-documentation)

## ✨ Features

- 📅 View available time slots from my Google Calendar
- 🎯 Book appointments that automatically create Google Calendar events
- 🔐 Secure OAuth 2.0 authentication with Google
- 💾 Persistent booking storage in PostgreSQL database
- 🎨 Modern, responsive UI built with React and Tailwind CSS
- 🌍 Timezone-aware scheduling

## 🛠 Tech Stack

### Frontend

- **React** - Modern UI library for building interactive user interfaces
- **Vite** - Next-generation frontend build tool for fast development and optimized production builds
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **PostCSS** - CSS transformation tool with autoprefixer support
- **ESLint** - Code linting and quality assurance
- **React Hooks** - Modern React patterns for state management and side effects

### Backend

- **Python 3.13** - Programming language
- **FastAPI** - web framework for building APIs with Python
- **Uvicorn** - ASGI server implementation
- **SQLModel** - SQL databases in Python, designed for simplicity, compatibility, and robustness
- **Pydantic** - Data validation using Python type annotations
- **psycopg2-binary** - PostgreSQL adapter for Python
- **python-dotenv** - Environment variable management

### Google Calendar Integration

- **google-auth** - Google authentication library
- **google-auth-oauthlib** - OAuth 2.0 client library for Google APIs
- **google-auth-httplib2** - HTTP transport for Google auth
- **google-api-python-client** - Official Google API Python client library

### Database

- **Supabase (PostgreSQL)** - Relational database for storing booking records

## 📁 Project Structure

```
cofee-chat-scheduler/
├── backend/                    # FastAPI backend application
│   ├── models/                # SQLModel database models
│   │   └── __init__.py
│   ├── routes/                # API route handlers
│   │   ├── auth.py           # Google OAuth authentication
│   │   ├── availability.py   # Availability endpoint
│   │   ├── bookings.py       # Booking creation endpoint
│   │   └── test.py           # Test endpoints
│   ├── services/              # Business logic services
│   │   ├── calendar_service.py  # Google Calendar API integration
│   │   └── google_auth.py      # OAuth flow handling
│   ├── config.py              # Configuration and environment variables
│   ├── database.py            # Database connection setup
│   ├── main.py                # FastAPI application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── vercel.json            # Vercel deployment configuration
│   └── venv/                  # Python virtual environment
│
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── BookingForm.jsx      # Booking form component
│   │   │   ├── DatePicker.jsx       # Date selection component
│   │   │   ├── Layout.jsx           # Main layout component
│   │   │   └── TimeSlotList.jsx     # Available time slots display
│   │   ├── services/          # API client services
│   │   │   └── api.js         # Backend API communication
│   │   ├── App.jsx            # Main React application component
│   │   ├── main.jsx           # React application entry point
│   │   └── index.css          # Global styles
│   ├── public/                # Static assets
│   ├── dist/                  # Production build output
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   └── postcss.config.js      # PostCSS configuration
│
├── ARCHITECTURE.md            # System architecture documentation
├── PHASE1_MVP.md             # MVP implementation plan
├── TICKETS.md                # Development tickets and tasks
├── TIME_FORMAT.md            # Time format documentation
├── STARTUP.md                # Startup guide
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v18 or higher) - For frontend development
- **Python 3.13** - For backend development
- **PostgreSQL** - Database (or use Supabase free tier)
- **Google Cloud Project** - For Google Calendar API access
- **Git** - Version control

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd cofee-chat-scheduler
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

#### 4. Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/callback
GOOGLE_REFRESH_TOKEN=your_refresh_token_here

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Application Configuration
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
TIMEZONE=America/Toronto
```

For the frontend, create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

#### 5. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (OAuth client ID)
5. Add authorized redirect URIs
6. Download credentials and add them to your `.env` file

### Running the Application

#### Start Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

#### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

#### Access API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔐 Environment Variables

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_CLIENT_ID` | Google OAuth 2.0 client ID | Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 2.0 client secret | Yes |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL | Yes |
| `GOOGLE_REFRESH_TOKEN` | OAuth refresh token | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `FRONTEND_URL` | Frontend application URL | Yes |
| `BACKEND_URL` | Backend API URL | No |
| `TIMEZONE` | Application timezone (default: America/Toronto) | No |

### Frontend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | No (defaults to http://localhost:8000) |

## 📡 API Endpoints

### Authentication

- `GET /api/auth/login` - Initiate Google OAuth login
- `GET /api/auth/callback` - OAuth callback handler
- `GET /api/auth/status` - Check authentication status

### Availability

- `GET /api/availability?date=YYYY-MM-DD` - Get available time slots for a specific date

**Response:**
```json
{
  "date": "2024-01-15",
  "available_slots": [
    {
      "start_time": "2024-01-15T09:00:00-05:00",
      "end_time": "2024-01-15T09:30:00-05:00"
    }
  ]
}
```

### Bookings

- `POST /api/bookings` - Create a new booking

**Request Body:**
```json
{
  "attendee_name": "John Doe",
  "attendee_email": "john@example.com",
  "start_time": "2024-01-15T09:00:00-05:00",
  "end_time": "2024-01-15T09:30:00-05:00",
  "notes": "Coffee chat discussion"
}
```

**Response:**
```json
{
  "id": 1,
  "attendee_name": "John Doe",
  "attendee_email": "john@example.com",
  "start_time": "2024-01-15T09:00:00-05:00",
  "end_time": "2024-01-15T09:30:00-05:00",
  "notes": "Coffee chat discussion",
  "created_at": "2024-01-14T10:00:00Z"
}
```

### Health Check

- `GET /` - API health check and version info

## 💻 Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Building for Production

#### Frontend

```bash
cd frontend
npm run build
```

The production build will be in the `frontend/dist/` directory.

#### Backend

The backend is ready for deployment as-is. For Vercel deployment, the `vercel.json` configuration handles the setup automatically.

### Code Quality

#### Frontend Linting

```bash
cd frontend
npm run lint
```

## 🚢 Deployment

### Vercel Deployment

This project is configured for deployment on Vercel:

1. **Backend**: Configured via `backend/vercel.json`
   - Uses `@vercel/python` runtime
   - Automatically handles FastAPI application

2. **Frontend**: Standard Vite build
   - Build command: `npm run build`
   - Output directory: `dist`

### Environment Variables in Production

Make sure to set all required environment variables in your Vercel project settings:
- Go to Project Settings → Environment Variables
- Add all variables from the [Environment Variables](#-environment-variables) section
