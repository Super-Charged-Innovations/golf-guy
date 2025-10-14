# Demo User Credentials

## 🔑 Admin Account
- **Email:** `admin@dgolf.se`
- **Password:** `Admin123!`
- **Dashboard:** `/admin`
- **Features:**
  - Full administrative access
  - Destination Suite (create, edit, publish destinations)
  - View all user data
  - Access to analytics

## 👤 Standard User Account
- **Email:** `user@dgolf.se`
- **Password:** `User123!`
- **Dashboard:** `/dashboard`
- **Features:**
  - View personalized recommendations
  - Browse destinations
  - Create inquiries
  - Update profile and preferences
  - Manage privacy settings

## Testing Notes

### Backend API Testing
Both users have been tested successfully via backend API:
- ✅ Login successful with correct credentials
- ✅ `full_name` field correctly returned
- ✅ `is_admin` field correctly set
- ✅ JWT token generation working
- ✅ Authenticated endpoints accessible

### Schema Changes
The user creation script now matches the User model in `backend/models/user_models.py`:
- **Required fields:** `id`, `email`, `hashed_password`, `full_name`, `is_active`, `is_admin`
- **Optional fields:** `created_at`, `last_login`
- **User profiles** are automatically created with default preferences

### Login Flow
1. User enters credentials on `/login` page
2. Frontend calls `/api/auth/login`
3. Backend validates credentials and returns JWT token + user data
4. Token stored in localStorage
5. User redirected based on role:
   - Admin users → `/admin`
   - Standard users → `/dashboard`

## Issue Fixed
**Previous Error:** `KeyError: 'full_name'`
- **Root Cause:** User documents in MongoDB were missing the `full_name` field
- **Solution:** Updated demo user creation script to include all required fields from User model
- **Status:** ✅ Resolved

## How to Recreate Users
If you need to recreate the demo users:

```bash
# Delete existing demo users
python delete_demo_users.py

# Create new demo users
python create_demo_users.py
```

## Login Page URL
- **Development:** `http://localhost:3000/login`
- **Production:** `https://dgolf-platform.preview.emergentagent.com/login`

---

**Last Updated:** 2025-09-14
**Status:** ✅ All demo accounts working correctly
