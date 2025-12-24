# Deployment Guide - Coffee Chat Scheduler

This guide will walk you through deploying the Coffee Chat Scheduler application to production.

## Overview

The application consists of:
- **Backend**: FastAPI (Python) - API server
- **Frontend**: React + Vite - Static site
- **Database**: Supabase (PostgreSQL) - Already hosted

## Recommended Hosting Platforms

### Option 1: Vercel (Recommended for beginners)
- ✅ Free tier with generous limits
- ✅ Easy deployment for both frontend and backend
- ✅ Automatic HTTPS
- ✅ Environment variables management
- ✅ Automatic deployments from GitHub

### Option 2: Render
- ✅ Free tier available
- ✅ Supports FastAPI out of the box
- ✅ PostgreSQL support (though we use Supabase)
- ✅ Simple configuration

### Option 3: Railway
- ✅ Easy deployment
- ✅ Free tier available
- ✅ Good for full-stack apps

## Prerequisites

Before deploying, ensure you have:
1. ✅ All code committed to GitHub
2. ✅ Google OAuth credentials set up
3. ✅ Google Refresh Token obtained
4. ✅ Supabase database URL
5. ✅ Accounts on hosting platforms

## Step-by-Step Deployment

### Part 1: Backend Deployment (FastAPI)

#### Step 1.1: Prepare Backend for Deployment

1. **Create a startup script** (`backend/start.sh`):
   ```bash
   #!/bin/bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Create a runtime file** (if using Vercel, create `backend/vercel.json`):
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

3. **Create a Procfile** (for Render/Railway):
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

#### Step 1.2: Deploy Backend to Vercel

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Navigate to backend directory:
   ```bash
   cd backend
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy:
   ```bash
   vercel
   ```
   - Follow prompts (link to existing project or create new)
   - Set root directory: `backend`

5. Set environment variables in Vercel dashboard:
   - Go to your project → Settings → Environment Variables
   - Add all required variables (see Environment Variables section below)

6. Redeploy after setting environment variables:
   ```bash
   vercel --prod
   ```

7. Note your backend URL (e.g., `https://your-project.vercel.app`)

#### Alternative: Deploy Backend to Render

1. Go to [render.com](https://render.com) and sign up/login

2. Click "New +" → "Web Service"

3. Connect your GitHub repository

4. Configure:
   - **Name**: `coffee-chat-scheduler-api`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables (see below)

6. Click "Create Web Service"

7. Wait for deployment to complete

8. Note your backend URL (e.g., `https://your-project.onrender.com`)

### Part 2: Frontend Deployment

#### Step 2.1: Update Frontend Environment Variables

1. Update `frontend/.env` (for local testing) or production environment:
   ```
   VITE_API_URL=https://your-backend-url.vercel.app
   ```
   Replace with your actual backend URL from Part 1.

2. Update `frontend/src/services/api.js` if needed (it already uses env variable).

#### Step 2.2: Deploy Frontend to Vercel

1. Install Vercel CLI (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy:
   ```bash
   vercel
   ```
   - Follow prompts
   - Set root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`

5. Set environment variables:
   - Go to project → Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend-url.vercel.app`

6. Redeploy:
   ```bash
   vercel --prod
   ```

7. Note your frontend URL (e.g., `https://your-frontend.vercel.app`)

#### Alternative: Deploy Frontend to Netlify

1. Go to [netlify.com](https://netlify.com) and sign up/login

2. Click "Add new site" → "Import an existing project"

3. Connect your GitHub repository

4. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

5. Add environment variables:
   - Site settings → Environment variables
   - Add: `VITE_API_URL` = `https://your-backend-url.vercel.app`

6. Click "Deploy site"

### Part 3: Update Google OAuth Configuration

#### Step 3.1: Update Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)

2. Navigate to: APIs & Services → Credentials

3. Click on your OAuth 2.0 Client ID

4. **Add Authorized redirect URIs**:
   - Add your backend callback URL: `https://your-backend-url.vercel.app/auth/callback`

5. **Add Authorized JavaScript origins**:
   - Add your frontend URL: `https://your-frontend.vercel.app`
   - Add your backend URL: `https://your-backend-url.vercel.app`

6. Save changes

#### Step 3.2: Update Environment Variables

Update `GOOGLE_REDIRECT_URI` in your backend environment variables:
```
GOOGLE_REDIRECT_URI=https://your-backend-url.vercel.app/auth/callback
```

### Part 4: Update CORS Configuration

The backend should already handle CORS, but verify `FRONTEND_URL` environment variable is set:
```
FRONTEND_URL=https://your-frontend.vercel.app
```

## Required Environment Variables

### Backend Environment Variables

Set these in your hosting platform's environment variables section:

```
# Google OAuth 2.0 Credentials
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=https://your-backend-url.vercel.app/auth/callback
GOOGLE_REFRESH_TOKEN=your_refresh_token_here

# Database
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres

# Application Settings
FRONTEND_URL=https://your-frontend.vercel.app
BACKEND_URL=https://your-backend-url.vercel.app
TIMEZONE=America/Toronto
```

### Frontend Environment Variables

```
VITE_API_URL=https://your-backend-url.vercel.app
```

## Testing Your Deployment

1. **Test Backend**:
   - Visit: `https://your-backend-url.vercel.app`
   - Should see: `{"message":"Coffee Chat Scheduler API","version":"1.0.0"}`
   - Visit: `https://your-backend-url.vercel.app/docs` for API documentation

2. **Test Frontend**:
   - Visit: `https://your-frontend.vercel.app`
   - Should load the booking interface

3. **Test Full Flow**:
   - Select a date
   - View available slots
   - Create a test booking
   - Verify calendar event is created

## Common Issues & Solutions

### Issue: CORS Errors
- **Solution**: Ensure `FRONTEND_URL` is set correctly in backend environment variables
- Check that CORS middleware is configured in `backend/main.py`

### Issue: Database Connection Failed
- **Solution**: Verify `DATABASE_URL` is correct
- Check Supabase project is not paused
- Ensure connection string doesn't have `?pgbouncer=true` (or remove it)

### Issue: Google OAuth Not Working
- **Solution**: Verify redirect URI matches exactly in Google Cloud Console
- Check `GOOGLE_REDIRECT_URI` environment variable matches
- Ensure refresh token is set correctly

### Issue: Environment Variables Not Loading
- **Solution**: Verify variables are set in hosting platform (not just `.env` file)
- Redeploy after adding environment variables
- Check variable names match exactly (case-sensitive)

### Issue: Frontend Can't Connect to Backend
- **Solution**: Verify `VITE_API_URL` is set correctly
- Check backend is deployed and accessible
- Verify no CORS issues in browser console

## Post-Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] All environment variables set correctly
- [ ] Google OAuth redirect URI updated
- [ ] CORS configured properly
- [ ] Database connection working
- [ ] API endpoints responding
- [ ] Full booking flow tested
- [ ] Calendar events being created
- [ ] Email invitations being sent

## Maintenance

- Monitor your hosting platform for any errors
- Check logs regularly for issues
- Keep dependencies updated
- Monitor Supabase usage (free tier limits)
- Backup your refresh token securely

## Cost Considerations

- **Vercel**: Free tier includes 100GB bandwidth/month
- **Netlify**: Free tier includes 100GB bandwidth/month
- **Render**: Free tier with some limitations (sleeps after inactivity)
- **Supabase**: Free tier includes 500MB database, 2GB bandwidth

For a portfolio project, the free tiers should be sufficient.

