"""
Fix missing images for remaining Spanish resorts
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('backend/.env')

# Working golf resort images for missing destinations
MISSING_IMAGES = {
    "El Prat Golf Club": "https://images.unsplash.com/photo-1591468309810-02eace4bf2f0?w=1200",
    "Hotel Enicar Sotogrande": "https://images.unsplash.com/photo-1653503645391-d355d1c9f934?w=1200",
    "La Cala Resort": "https://images.unsplash.com/photo-1579476170948-2decc6dd582f?w=1200",
    "La Costa Beach Golf Resort": "https://images.unsplash.com/photo-1652266371938-297fecd5514a?w=1200",
    "La Finca Golf Resort": "https://images.unsplash.com/photo-1605144156546-91acf5e4cffd?w=1200",
    "La Sella Golf Resort": "https://images.unsplash.com/photo-1651455578415-0c601702a094?w=1200",
    "Las Lomas Village": "https://images.unsplash.com/photo-1587453451984-c9d4be800788?w=1200"
}

async def fix_missing_images():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("\n" + "="*70)
    print("FIXING MISSING SPANISH RESORT IMAGES")
    print("="*70 + "\n")
    
    updated_count = 0
    
    for resort_name, image_url in MISSING_IMAGES.items():
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
                        "image": image_url,
                        "images": [image_url],
                        "updated_at": datetime.utcnow().isoformat()
                    }
                }
            )
            
            if result.modified_count > 0:
                print(f"✅ UPDATED: {destination['name']}")
                print(f"   Image: {image_url}")
                print()
                updated_count += 1
        else:
            print(f"❌ NOT FOUND: {resort_name}")
            print()
    
    print("="*70)
    print(f"Updated {updated_count} out of {len(MISSING_IMAGES)} resorts")
    print("="*70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_missing_images())
