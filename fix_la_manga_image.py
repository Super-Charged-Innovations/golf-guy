import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('backend/.env')

async def fix_la_manga_image():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Find La Manga Club
    destination = await db.destinations.find_one({
        "name": {"$regex": "La Manga", "$options": "i"},
        "country": "Spain"
    })
    
    if destination:
        print(f"\n✅ Found: {destination['name']}")
        print(f"Current Image: {destination.get('image', 'None')}")
        
        # Update with a working golf resort image
        new_image = "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=1200"
        
        result = await db.destinations.update_one(
            {"_id": destination["_id"]},
            {
                "$set": {
                    "image": new_image,
                    "images": [new_image],
                    "updated_at": datetime.utcnow().isoformat()
                }
            }
        )
        
        if result.modified_count > 0:
            print(f"\n✅ UPDATED La Manga Club image")
            print(f"New Image: {new_image}")
        else:
            print("\n⚠️  No changes made")
    else:
        print("\n❌ La Manga Club not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_la_manga_image())
