# 🚀 Vercel Deployment Instructions - Step by Step

## ✅ Pre-Deployment Checklist (Already Done)

- [x] Backend deployed on Emergent: `https://golf-travel-app.emergent.host`
- [x] CORS configured to accept Vercel domains
- [x] Frontend configured with `.env.production`
- [x] `vercel.json` created for routing
- [x] GitHub connected to Vercel

---

## 📋 Vercel Deployment Steps

### Step 1: Prepare Code for GitHub (If Not Already Done)

1. **In Emergent**, click **"Save to GitHub"** button in the chat interface
2. Select your repository or create a new one
3. Push all latest changes (including flag fix and Vercel configuration)
4. Confirm push is successful

---

### Step 2: Go to Vercel Dashboard

1. Open [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Make sure you're logged in with the GitHub-connected account

---

### Step 3: Import Your Project

1. Click **"Add New..."** button (top right)
2. Select **"Project"** from dropdown
3. You should see your GitHub repository in the list
4. Click **"Import"** next to your repository

---

### Step 4: Configure Project Settings

**IMPORTANT**: Your React app is in the `frontend` folder, so you need to configure the root directory.

#### Basic Settings:
```
Project Name: dgolf (or your preferred name)
Framework Preset: Create React App
```

#### Root Directory:
```
Root Directory: frontend
```
**⚠️ CRITICAL**: Click "Edit" next to Root Directory and type: `frontend`

#### Build & Development Settings:
```
Build Command: yarn build
Output Directory: build
Install Command: yarn install
Development Command: yarn start
```

---

### Step 5: Add Environment Variables

**VERY IMPORTANT**: Click **"Environment Variables"** section

Add this variable:

| Key | Value | Environment |
|-----|-------|-------------|
| `REACT_APP_BACKEND_URL` | `https://golf-travel-app.emergent.host` | Production |

**Steps**:
1. Type `REACT_APP_BACKEND_URL` in the "Key" field
2. Type `https://golf-travel-app.emergent.host` in the "Value" field (NO trailing slash!)
3. Select **"Production"** checkbox (or leave all checked)
4. Click **"Add"**

---

### Step 6: Deploy!

1. Click **"Deploy"** button at the bottom
2. Wait 2-5 minutes for build to complete
3. Watch the build logs (they'll appear automatically)

---

## ✅ What to Expect During Build

You'll see logs showing:
```
Installing dependencies...
yarn install v1.22.x
Building application...
yarn build
Creating an optimized production build...
Compiled successfully!
```

**Build Success**: You'll get a deployment URL like:
- `https://dgolf-{random}.vercel.app` or
- `https://your-project-name.vercel.app`

---

## 🧪 Testing Your Deployment

### 1. Open Your Vercel URL
Click the URL shown after deployment completes

### 2. Test Homepage
- Should load without errors
- Check browser console (F12) for any errors

### 3. Test Backend Connectivity
**Login Test**:
- Go to `/login`
- Use admin credentials:
  - Email: `admin@dgolf.se`
  - Password: `Admin123!`
- Should successfully log in and redirect to admin dashboard

### 4. Test Destinations
- Go to `/destinations`
- Should load all country cards with flags ✅
- Click on a country (e.g., Spain)
- Should load destinations for that country

### 5. Check for CORS Issues
- Open browser DevTools (F12) → Console tab
- Look for any red errors mentioning "CORS"
- If no CORS errors = ✅ Backend connection working!

---

## 🔧 Troubleshooting Common Issues

### Issue 1: Build Fails with "Cannot find module"

**Solution**:
1. Check if `package.json` has all dependencies
2. In Vercel, go to Settings → General → Node.js Version
3. Try setting Node.js version to: `18.x`
4. Redeploy

### Issue 2: Blank Page / White Screen

**Check**:
1. Browser console for JavaScript errors
2. Vercel deployment logs for build errors
3. Verify environment variable `REACT_APP_BACKEND_URL` is set correctly
4. Try hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

### Issue 3: 404 on Page Refresh

**Solution**:
- Verify `vercel.json` exists in `frontend` folder with rewrite rules
- If missing, redeploy after adding it
- Vercel should automatically detect and apply rewrites

### Issue 4: API Calls Fail / CORS Errors

**Check**:
1. Verify `REACT_APP_BACKEND_URL` in Vercel environment variables
2. Confirm backend is running: Visit `https://golf-travel-app.emergent.host/api/health`
3. Backend CORS already configured to allow *.vercel.app domains ✅

### Issue 5: Images Not Loading

**Check**:
- Some external image URLs might be blocked
- Check browser console for image load errors
- This is normal for some Unsplash images (ORB policy)

---

## 🎯 Post-Deployment Actions

### 1. Update Vercel URL (Optional)
If your Vercel URL is random (e.g., `dgolf-abc123.vercel.app`), you can:
1. Go to Project Settings → Domains
2. Edit the default domain to something cleaner

### 2. Add Custom Domain (Optional)
If you own a domain:
1. Go to Project Settings → Domains
2. Click "Add"
3. Enter your domain (e.g., `dgolf.com`)
4. Follow DNS configuration instructions
5. Add the custom domain to backend CORS:
   - Update `CORS_ORIGINS` in Emergent backend .env
   - Add: `,https://dgolf.com`

### 3. Set Up Preview Deployments
Vercel automatically creates preview URLs for:
- Every Git branch
- Every pull request
- These also work with your backend CORS setup ✅

---

## 📊 Vercel Dashboard Features to Explore

### Analytics
- View visitor statistics
- Track page performance
- Monitor errors

### Deployments
- View all deployments
- Rollback to previous versions easily
- Compare deployment diffs

### Logs
- Real-time function logs
- Error tracking
- Request monitoring

---

## 🔄 Continuous Deployment

**After initial deployment**, any push to your GitHub repository will:
1. Automatically trigger a new Vercel build
2. Create a preview deployment
3. Deploy to production if pushed to main branch

**Workflow**:
```
Make changes in Emergent 
  ↓
Save to GitHub
  ↓
Vercel auto-deploys ✅
  ↓
Live in ~2 minutes!
```

---

## ✨ Quick Reference

**Your URLs:**
- Backend (Emergent): `https://golf-travel-app.emergent.host`
- Frontend (Vercel): `https://your-project.vercel.app` (will be generated)

**Admin Login:**
- Email: `admin@dgolf.se`
- Password: `Admin123!`

**Environment Variable:**
```
REACT_APP_BACKEND_URL=https://golf-travel-app.emergent.host
```

**Root Directory:**
```
frontend
```

---

## 🆘 Need Help?

**Vercel Documentation**: https://vercel.com/docs

**Common Commands** (if using Vercel CLI):
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from command line
cd frontend
vercel --prod

# Check deployment status
vercel ls
```

---

## 🎉 Success Indicators

You'll know deployment is successful when:
- ✅ Build completes without errors
- ✅ Vercel shows "Deployment Complete"
- ✅ Your URL loads the homepage
- ✅ Login works with admin credentials
- ✅ Destinations page shows country cards with flags
- ✅ No CORS errors in browser console
- ✅ Backend API calls return data (check Network tab)

---

**Last Updated**: January 2025
**Configuration Status**: ✅ Ready for Deployment

---

## 📝 Summary Checklist

Before you click Deploy:
- [ ] Root Directory set to: `frontend`
- [ ] Environment variable `REACT_APP_BACKEND_URL` added
- [ ] Framework set to: `Create React App`
- [ ] Build command: `yarn build`
- [ ] Output directory: `build`

After deployment:
- [ ] Test homepage loads
- [ ] Test login with admin credentials
- [ ] Verify destinations page works
- [ ] Check browser console for errors
- [ ] Test mobile responsiveness

**You're all set! Click Deploy and watch your app go live! 🚀**
