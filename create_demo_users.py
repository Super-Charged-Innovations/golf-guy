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
        
        # Create user document
        user_doc = {
            "id": str(uuid.uuid4()),
            "email": user_data["email"],
            "hashed_password": hashed_password,  # Use hashed_password field name
            "name": user_data["name"],
            "role": user_data["role"],
            "tier": user_data["tier"],
            "preferences": {
                "budget": "medium",
                "group_size": 2,
                "preferred_regions": [],
                "play_style": "leisure"
            },
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Insert user
        result = await db.users.insert_one(user_doc)
        
        if result.inserted_id:
            print(f"✅ CREATED: {user_data['email']}")
            print(f"   Role: {user_data['role']}")
            print(f"   Tier: {user_data['tier']}")
            print(f"   Password: {user_data['password']}")
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
