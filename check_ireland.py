import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def check_ireland():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Find Irish destinations
    destinations = await db.destinations.find(
        {"country": "Ireland"},
        {"_id": 0, "name": 1, "published": 1, "country": 1, "slug": 1}
    ).to_list(100)
    
    print(f"\n=== Ireland Destinations ({len(destinations)} found) ===\n")
    
    for dest in destinations:
        pub_status = "✅ Published" if dest.get('published') else "❌ Not Published"
        print(f"{dest['name']}")
        print(f"  Country: {dest.get('country')}")
        print(f"  Published: {pub_status}")
        print(f"  Slug: {dest.get('slug')}")
        print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_ireland())
