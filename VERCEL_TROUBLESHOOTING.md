# Vercel Deployment - Troubleshooting & Fix Guide

## Current Issue: Blank Page on https://dgolf.vercel.app/

**Error Found:** `t.map is not a function`  
**Root Cause:** API calls failing because environment variable is missing or backend is unreachable

---

## IMMEDIATE FIX - Step by Step

### Step 1: Add Environment Variable to Vercel

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Click on your `dgolf` project
3. Go to **Settings** tab
4. Click **Environment Variables** in left sidebar
5. Add the following:

**Variable 1:**
```
Name: REACT_APP_BACKEND_URL
Value: https://golf-travel-app.preview.emergentagent.com
```

6. Click **Save**
7. Go to **Deployments** tab
8. Click the **three dots (...)** on latest deployment
9. Click **Redeploy**
10. Wait 2-3 minutes for redeployment

---

### Step 2: Update Backend CORS (Critical!)

Your backend needs to allow requests from Vercel domain.

**On Emergent (where your backend is running):**

1. Edit `/app/backend/server.py`
2. Find the CORS middleware section (around line 50-70)
3. Add Vercel domain to allowed origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://golf-travel-app.preview.emergentagent.com",
        "https://dgolf.vercel.app",  # ADD THIS LINE
        "https://*.vercel.app",  # ADD THIS LINE (allows all Vercel preview deployments)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

4. Save the file
5. Restart backend: `sudo supervisorctl restart backend`

---

### Step 3: Verify Environment Variable

After redeployment, check if env var is working:

1. Go to https://dgolf.vercel.app/
2. Open browser DevTools (F12)
3. Go to Console tab
4. Type: `console.log(process.env.REACT_APP_BACKEND_URL)`
5. Should show: `https://golf-travel-app.preview.emergentagent.com`
6. If it shows `undefined`, the env var wasn't added correctly

---

## Alternative Quick Fix (Testing)

If you want to test immediately without waiting for Vercel:

### Create a vercel.json file in /frontend directory:

```json
{
  "env": {
    "REACT_APP_BACKEND_URL": "https://golf-travel-app.preview.emergentagent.com"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

Then commit and push to trigger new deployment.

---

## Why Is The Site Blank?

**The Error Chain:**
1. Vercel deploys React app ✅
2. React app tries to fetch data from API ❌
3. `REACT_APP_BACKEND_URL` is undefined (missing env var) ❌
4. API call goes to `undefined/api/hero` → fails ❌
5. Home.js gets `undefined` instead of array ❌
6. Tries to call `.map()` on undefined → **Error!** ❌
7. React error boundary doesn't exist → **Blank page** ❌

---

## Checklist to Fix

- [ ] Add `REACT_APP_BACKEND_URL` environment variable in Vercel
- [ ] Value should be: `https://golf-travel-app.preview.emergentagent.com`
- [ ] Redeploy from Vercel dashboard
- [ ] Update backend CORS to allow `https://dgolf.vercel.app`
- [ ] Test site after redeployment
- [ ] Check browser console for API errors

---

## Expected Result After Fix

✅ Home page loads with hero carousel  
✅ Destinations page shows all golf resorts  
✅ Articles page displays travel reports  
✅ Login/Register functionality works  
✅ No console errors  

---

## Long-term Recommendation

**For Production:**

1. **Deploy Backend to Render:**
   - Create free account: https://render.com
   - New Web Service
   - Connect GitHub repo
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Add all environment variables from backend/.env
   - Get Render URL (e.g., `https://dgolf-backend.onrender.com`)

2. **Update Vercel Environment Variable:**
   - Change `REACT_APP_BACKEND_URL` to your Render URL
   - Redeploy

3. **Benefits:**
   - Both services on reliable platforms
   - Independent scaling
   - Better performance
   - Professional setup

---

## Quick Debug Commands

**Check if backend is accessible:**
```bash
curl https://golf-travel-app.preview.emergentagent.com/api/hero
```

Should return JSON with hero slides.

**Check Vercel environment:**
Visit: https://dgolf.vercel.app/
Open Console and type:
```javascript
fetch(process.env.REACT_APP_BACKEND_URL + '/api/hero')
  .then(r => r.json())
  .then(console.log)
```

Should show hero data.

---

## Contact Support

If issues persist after these fixes:
- Check Vercel deployment logs
- Check browser console for specific errors
- Verify backend is running and accessible
- Test API endpoints directly with curl

---

Last Updated: 2025-09-15
Status: Awaiting environment variable addition and CORS update
