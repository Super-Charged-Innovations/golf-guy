# Vercel Frontend Deployment Guide
## DGolf Platform - Frontend on Vercel + Backend on Emergent

---

## ✅ Completed Steps

### Phase 1: Backend Deployed on Emergent
- **Backend URL**: `https://golf-travel-app.emergent.host`
- **Status**: ✅ Live and running
- **CORS**: ✅ Configured to allow all Vercel domains (*.vercel.app)

### Phase 2: Frontend Configuration
- **Backend URL**: ✅ Updated in `.env.production`
- **Vercel Config**: ✅ Created `vercel.json` for routing
- **CORS Support**: ✅ Backend now accepts all Vercel preview URLs

---

## 🚀 Next Steps: Deploy Frontend to Vercel

### Step 1: Save Code to GitHub (If Not Already Done)
1. In Emergent chat interface, look for **"Save to GitHub"** button
2. Click it and push your code to your connected GitHub repository
3. Make sure the latest changes are pushed (including `vercel.json` and `.env.production`)

### Step 2: Import Project to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Find your GitHub repository in the list
4. Click **"Import"**

### Step 3: Configure Build Settings
Vercel should auto-detect your React app, but verify these settings:

**Framework Preset**: `Create React App`

**Root Directory**: `frontend` (if your React app is in a frontend folder)

**Build Command**: 
```bash
yarn build
```

**Output Directory**: 
```
build
```

**Install Command**: 
```bash
yarn install
```

### Step 4: Configure Environment Variables
In the Vercel project settings, add this environment variable:

| Key | Value |
|-----|-------|
| `REACT_APP_BACKEND_URL` | `https://golf-travel-app.emergent.host` |

**Important**: 
- ✅ No trailing slash
- ✅ Use HTTPS
- ✅ This is your Emergent backend URL

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. You'll get a URL like: `https://dgolf-{random}.vercel.app`

### Step 6: Set Up Custom Domain (Optional)
1. In Vercel project settings, go to **"Domains"**
2. Add your custom domain (e.g., `dgolf.com`)
3. Follow Vercel's DNS configuration instructions

### Step 7: Update Backend CORS (If Using Custom Domain)
If you set up a custom domain, you need to add it to backend CORS:

1. Go to your Emergent deployment settings
2. Update the `CORS_ORIGINS` environment variable to include your custom domain
3. Example: Add `,https://dgolf.com` to the existing CORS_ORIGINS value

---

## 🧪 Testing Your Deployment

### 1. Check Frontend Loading
- Open your Vercel URL
- Verify homepage loads correctly
- Check browser console for errors (F12)

### 2. Test API Connectivity
- Try logging in with admin credentials:
  - Email: `admin@dgolf.se`
  - Password: `Admin123!`
- Browse destinations
- Check if data loads from backend

### 3. Check CORS
- Open browser DevTools (F12) → Network tab
- Make API requests (login, fetch destinations)
- Ensure no CORS errors in console
- API calls should show status 200 (success)

### 4. Test Features
- ✅ Login/Logout
- ✅ View destinations
- ✅ Admin dashboard (if admin)
- ✅ Create inquiries
- ✅ AI recommendations

---

## 🔧 Troubleshooting

### Issue: "Network Error" or API calls fail

**Solution**:
1. Check browser console for CORS errors
2. Verify `REACT_APP_BACKEND_URL` is set correctly in Vercel
3. Confirm backend is running: Visit `https://golf-travel-app.emergent.host/api/health`
4. Check backend logs in Emergent dashboard

### Issue: "404 Not Found" on refresh

**Solution**:
- Verify `vercel.json` exists in frontend root with rewrite rules
- Redeploy if needed

### Issue: Environment variables not working

**Solution**:
1. Go to Vercel Project Settings → Environment Variables
2. Ensure `REACT_APP_BACKEND_URL` is set for **Production**
3. Redeploy the project (Vercel → Deployments → Redeploy)

### Issue: Build fails on Vercel

**Check**:
- Build logs in Vercel dashboard
- Ensure `package.json` has all dependencies
- Verify Node.js version compatibility

---

## 📊 Architecture Overview

```
User Browser
     ↓
Vercel Frontend (React)
     ↓ HTTPS API Calls
Emergent Backend (FastAPI)
     ↓
MongoDB (Emergent)
```

**Benefits of this setup:**
- ✅ Vercel's global CDN for fast frontend delivery
- ✅ Emergent's managed backend infrastructure
- ✅ Automatic SSL/HTTPS on both
- ✅ Independent scaling
- ✅ Easy preview deployments on Vercel

---

## 🎯 Quick Commands

### Redeploy Frontend (After Code Changes)
```bash
# Push to GitHub
git add .
git commit -m "Update frontend"
git push

# Vercel auto-deploys on push
```

### Check Backend Health
```bash
curl https://golf-travel-app.emergent.host/api/health
```

### View Frontend Build Logs
- Go to Vercel Dashboard → Your Project → Deployments → View Build Logs

---

## 📝 Important URLs

| Service | URL |
|---------|-----|
| **Backend (Emergent)** | https://golf-travel-app.emergent.host |
| **Frontend (Vercel)** | Will be generated after deployment |
| **Admin Login** | /login (Email: admin@dgolf.se) |
| **Backend API Docs** | https://golf-travel-app.emergent.host/docs |

---

## ✨ Production Checklist

Before going live:
- [ ] Test all features thoroughly
- [ ] Set up custom domain on Vercel
- [ ] Update CORS for custom domain
- [ ] Test on multiple browsers (Chrome, Safari, Firefox)
- [ ] Test on mobile devices
- [ ] Set up Vercel analytics (optional)
- [ ] Configure environment for production
- [ ] Review API rate limits
- [ ] Set up monitoring/alerts

---

## 💡 Tips

1. **Preview Deployments**: Every Git push creates a preview URL on Vercel
2. **Environment Variables**: Can be different for Production/Preview/Development
3. **Caching**: Vercel caches static assets automatically
4. **Rollbacks**: Easy to rollback to previous deployment in Vercel
5. **CORS**: Backend automatically allows all *.vercel.app domains

---

## 🆘 Need Help?

**Vercel Issues**:
- Check Vercel documentation: https://vercel.com/docs
- View build logs in Vercel dashboard

**Backend Issues**:
- Check Emergent deployment logs
- Verify environment variables in Emergent

**CORS Issues**:
- Ensure origin is allowed in backend CORS_ORIGINS
- Backend automatically allows *.vercel.app domains

---

**Last Updated**: 2025-01-XX
**Status**: ✅ Ready for Vercel Deployment
