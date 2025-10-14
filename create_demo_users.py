"""
Create demo admin and standard user accounts
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import bcrypt
import uuid
from datetime import datetime

load_dotenv('backend/.env')

async def create_demo_users():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Demo credentials
    demo_users = [
        {
            "email": "admin@dgolf.se",
            "password": "Admin123!",
            "full_name": "Admin User",
            "is_admin": True
        },
        {
            "email": "user@dgolf.se",
            "password": "User123!",
            "full_name": "Standard User",
            "is_admin": False
        }
    ]
    
    print("=" * 60)
    print("CREATING DEMO USER ACCOUNTS")
    print("=" * 60 + "\n")
    
    for user_data in demo_users:
        # Check if user already exists
        existing = await db.users.find_one({"email": user_data["email"]})
        
        if existing:
            print(f"⏭️  SKIPPED: {user_data['email']} (already exists)")
            continue
        
        # Hash password
        hashed_password = bcrypt.hashpw(
            user_data["password"].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Create user document (matching User model in user_models.py)
        user_doc = {
            "id": str(uuid.uuid4()),
            "email": user_data["email"],
            "hashed_password": hashed_password,
            "full_name": user_data["full_name"],
            "is_active": True,
            "is_admin": user_data["is_admin"],
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None
        }
        
        # Insert user
        result = await db.users.insert_one(user_doc)
        
        if result.inserted_id:
            print(f"✅ CREATED: {user_data['email']}")
            print(f"   Full Name: {user_data['full_name']}")
            print(f"   Admin: {user_data['is_admin']}")
            print(f"   Password: {user_data['password']}")
            print()
            
            # Create user profile for the new user
            from datetime import timezone as tz
            profile_doc = {
                "id": str(uuid.uuid4()),
                "user_id": user_doc["id"],
                "preferences": {
                    "budget_min": 0,
                    "budget_max": 50000,
                    "preferred_countries": [],
                    "playing_level": "Intermediate",
                    "accommodation_preference": "Any",
                    "trip_duration_days": None,
                    "group_size": None,
                    "phone_number": None,
                    "travel_frequency": None,
                    "preferred_travel_months": [],
                    "dietary_requirements": None,
                    "special_requests": None,
                    "previous_golf_destinations": [],
                    "handicap": None
                },
                "conversation_summary": "",
                "conversation_history": [],
                "past_inquiries": [],
                "kyc_notes": "",
                "kyc_completed": False,
                "tier": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            await db.user_profiles.insert_one(profile_doc)
            print(f"   ✅ Created user profile")
            print()
    
    print("=" * 60)
    print("DEMO USER CREDENTIALS")
    print("=" * 60 + "\n")
    
    print("🔑 ADMIN ACCOUNT:")
    print("   Email: admin@dgolf.se")
    print("   Password: Admin123!")
    print("   Dashboard: /admin")
    print()
    
    print("👤 STANDARD USER ACCOUNT:")
    print("   Email: user@dgolf.se")
    print("   Password: User123!")
    print("   Dashboard: /dashboard")
    print()
    
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_demo_users())
