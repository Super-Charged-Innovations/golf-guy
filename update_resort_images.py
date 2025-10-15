"""
Update images for 3 specific Spanish resorts with better quality images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('backend/.env')

# Better images for these 3 resorts
RESORT_UPDATES = {
    "Las Colinas Golf & Country Club": {
        "image": "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa"  # Luxury golf course with hills
    },
    "Hotel Alicante Golf": {
        "image": "https://images.unsplash.com/photo-1593111774240-d529f12cf4bb"  # Hotel with golf course
    },
    "La Manga Club": {
        "image": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b"  # Large golf resort aerial
    }
}

async def update_resort_images():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("\n" + "="*70)
    print("UPDATING RESORT IMAGES")
    print("="*70 + "\n")
    
    for resort_name, updates in RESORT_UPDATES.items():
        # Find destination by name
        destination = await db.destinations.find_one({
            "name": {"$regex": resort_name.split()[0], "$options": "i"},
            "country": "Spain"
        })
        
        if destination:
            # Update image
            result = await db.destinations.update_one(
                {"_id": destination["_id"]},
                {
                    "$set": {
                        "image": updates["image"],
                        "images": [updates["image"]],  # Update images array too
                        "updated_at": datetime.utcnow().isoformat()
                    }
                }
            )
            
            if result.modified_count > 0:
                print(f"✅ UPDATED: {destination['name']}")
                print(f"   New Image: {updates['image']}")
                print()
            else:
                print(f"⚠️  NO CHANGES: {destination['name']}")
                print()
        else:
            print(f"❌ NOT FOUND: {resort_name}")
            print()
    
    print("="*70)
    print("Update complete!")
    print("="*70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_resort_images())
