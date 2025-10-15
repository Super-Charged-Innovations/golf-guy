import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def list_spanish_destinations():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Find all Spanish destinations
    destinations = await db.destinations.find(
        {"country": "Spain"},
        {"_id": 0, "name": 1, "city": 1, "slug": 1, "image": 1}
    ).sort("name", 1).to_list(100)
    
    print(f"\n=== Found {len(destinations)} Spanish Destinations ===\n")
    
    for i, dest in enumerate(destinations, 1):
        image_status = "✅" if dest.get('image') and 'placeholder' not in dest.get('image', '').lower() else "❌"
        print(f"{i}. {dest['name']}")
        print(f"   City: {dest.get('city', 'N/A')}")
        print(f"   Slug: {dest.get('slug', 'N/A')}")
        print(f"   Image: {image_status} {dest.get('image', 'None')[:80]}")
        print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(list_spanish_destinations())
