# DGolf Platform - Vercel Deployment Instructions

## Overview
This guide shows how to deploy the DGolf platform to Vercel. Since Vercel doesn't natively support FastAPI backends, we'll deploy the **React frontend only** to Vercel and keep the backend on a separate platform.

---

## Prerequisites

1. GitHub repository with your code
2. Vercel account (free tier works)
3. Backend deployed elsewhere (Render, Railway, or Emergent)
4. MongoDB database accessible from internet (MongoDB Atlas recommended)

---

## Part 1: Prepare Frontend for Vercel Deployment

### Step 1: Update Frontend Structure

Since Vercel needs the frontend at the root or in a specific directory, you have two options:

**Option A: Deploy from /frontend subdirectory (Recommended)**
- Keep current structure
- Set Root Directory to `frontend` in Vercel

**Option B: Move frontend to root**
- Move all files from `/app/frontend` to `/app`
- Update paths accordingly

---

## Part 2: Vercel Configuration Settings

### Framework Preset
```
Create React App
```

### Root Directory
```
frontend
```
(If you're deploying from the frontend subdirectory)

Or leave as `./` if frontend is at root.

### Build Command
```
yarn build
```

### Output Directory
```
build
```

### Install Command
```
yarn install
```

---

## Part 3: Environment Variables

Add these environment variables in Vercel dashboard:

### Required Variables:

**Key:** `REACT_APP_BACKEND_URL`  
**Value:** Your backend URL (e.g., `https://your-backend.onrender.com` or `https://dgolf-backend.railway.app`)

**Important:** 
- Do NOT include `/api` in the backend URL
- The frontend code already appends `/api` to routes
- Example: If backend is at `https://api.dgolf.com`, set `REACT_APP_BACKEND_URL=https://api.dgolf.com`

---

## Part 4: Backend Deployment Options

Since Vercel doesn't support FastAPI well, deploy your backend to one of these:

### Option 1: Render (Recommended) ✅

**Why:** Free tier, easy setup, Python support

**Steps:**
1. Create new Web Service on Render
2. Connect your GitHub repo
3. Set Root Directory: `backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Environment Variables:
   - `MONGO_URL` - Your MongoDB connection string
   - `DB_NAME` - Database name
   - `JWT_SECRET_KEY` - Your secret key
   - Any other env vars from backend/.env

### Option 2: Railway ✅

**Why:** Simple setup, good free tier

**Steps:**
1. Create new project from GitHub
2. Add FastAPI service
3. Set Root Directory: `backend`
4. Railway auto-detects Python and installs dependencies
5. Add environment variables

### Option 3: Fly.io ✅

**Why:** Good for FastAPI, global deployment

**Requires:** Docker configuration (more complex)

### Option 4: Stay on Emergent ✅

**Why:** Already configured and working

**Setup:**
- Keep backend on Emergent
- Use the preview URL as `REACT_APP_BACKEND_URL`
- Only deploy frontend to Vercel

---

## Part 5: Step-by-Step Vercel Deployment

### Using the Screenshot Configuration:

1. **Framework Preset:** Create React App ✅ (Already selected)

2. **Root Directory:** 
   ```
   frontend
   ```
   Click "Edit" and type `frontend`

3. **Build and Output Settings:**
   - Build Command: `yarn build` (or use override toggle and enter)
   - Output Directory: `build`
   - Install Command: `yarn install`

4. **Environment Variables:**
   Click "+ Add More" and add:
   ```
   Key: REACT_APP_BACKEND_URL
   Value: https://golf-travel-app.preview.emergentagent.com
   ```
   (Use your actual backend URL)

5. **Click "Deploy"**

---

## Part 6: Post-Deployment Configuration

### Update CORS on Backend

Your FastAPI backend needs to allow requests from Vercel domain:

```python
# In backend/server.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app",  # Add your Vercel domain
        "https://golf-travel-app.preview.emergentagent.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Test Your Deployment

1. Visit your Vercel URL (e.g., `https://dgolf.vercel.app`)
2. Test navigation, login, destinations
3. Check browser console for any CORS errors
4. Verify API calls work to backend

---

## Part 7: Recommended Architecture

```
┌─────────────────────────────────────────┐
│                                         │
│         Users / Browsers                │
│                                         │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌─────────┐            ┌──────────────┐
│         │            │              │
│ Vercel  │            │   Backend    │
│ (React) │◄──────────►│ (FastAPI)    │
│         │   API      │              │
│         │   Calls    │ Render/      │
│         │            │ Railway/     │
└─────────┘            │ Emergent     │
                       │              │
                       └──────┬───────┘
                              │
                              ▼
                       ┌─────────────┐
                       │             │
                       │  MongoDB    │
                       │   Atlas     │
                       │             │
                       └─────────────┘
```

---

## Part 8: Quick Start (Simplest Path)

### For Immediate Deployment:

1. **Keep backend on Emergent** (it's already working)
2. **Deploy only frontend to Vercel**
3. **Configuration:**
   - Framework: Create React App
   - Root Directory: `frontend`
   - Build Command: `yarn build`
   - Output Directory: `build`
   - Environment Variable: 
     - `REACT_APP_BACKEND_URL` = `https://golf-travel-app.preview.emergentagent.com`

4. **Deploy!**

This is the fastest way to get your site on Vercel with a custom domain while keeping all backend functionality working.

---

## Part 9: Alternative - Full Vercel Stack (Requires Rewrite)

If you want everything on Vercel:

**Use Next.js instead of CRA + FastAPI:**
- Next.js API Routes instead of FastAPI
- Vercel Serverless Functions for backend
- Would require complete backend rewrite from Python to Node.js/TypeScript

**Not recommended** unless you want to rebuild from scratch.

---

## Part 10: Troubleshooting

### Common Issues:

**Issue 1: Build fails**
- Check if all dependencies are in package.json
- Ensure build command is correct
- Check build logs in Vercel dashboard

**Issue 2: API calls fail (CORS)**
- Add Vercel domain to backend CORS settings
- Verify REACT_APP_BACKEND_URL is set correctly

**Issue 3: Environment variables not working**
- Redeploy after adding env vars
- Check variable names start with `REACT_APP_`

**Issue 4: Images not loading**
- Check image URLs are absolute
- Verify CDN images are accessible

---

## Summary

**Recommended Setup:**
- ✅ Frontend: Vercel (fast, free, CDN)
- ✅ Backend: Render/Railway/Emergent (Python support)
- ✅ Database: MongoDB Atlas (cloud, scalable)

**Deployment Time:** ~5-10 minutes  
**Cost:** Free tier available on all platforms  
**Scalability:** Excellent with this setup

---

## Next Steps

1. Push code to GitHub
2. Connect GitHub to Vercel
3. Configure settings as shown above
4. Deploy!
5. Add custom domain (optional)
6. Monitor deployment logs
7. Test production site

**Need help with deployment? Contact Emergent support or check Vercel documentation.**

---

Last Updated: 2025-09-15
