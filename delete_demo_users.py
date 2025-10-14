"""
Delete demo users to recreate them
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def delete_demo_users():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Delete the demo users
    result = await db.users.delete_many({
        "email": {"$in": ["admin@dgolf.se", "user@dgolf.se"]}
    })
    
    print(f"✅ Deleted {result.deleted_count} demo users")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(delete_demo_users())
