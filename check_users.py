"""
Check existing users in the database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def check_users():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    users = await db.users.find({}).to_list(length=None)
    
    print("=" * 60)
    print("EXISTING USERS IN DATABASE")
    print("=" * 60 + "\n")
    
    if not users:
        print("❌ No users found in database!\n")
        print("You need to register users via the /register page")
    else:
        print(f"Found {len(users)} user(s):\n")
        
        for idx, user in enumerate(users, 1):
            print(f"{idx}. Email: {user.get('email')}")
            print(f"   Name: {user.get('name', 'N/A')}")
            print(f"   Role: {user.get('role', 'client')}")
            print(f"   Tier: {user.get('tier', 0)}")
            print(f"   Created: {user.get('created_at', 'N/A')}")
            print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_users())
