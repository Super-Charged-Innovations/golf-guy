"""
Fix missing images with exact name matching
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('backend/.env')

# Exact mapping of resort names to images
EXACT_UPDATES = [
    {
        "search": {"name": "El Prat Golf Club", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1591468309810-02eace4bf2f0?w=1200"
    },
    {
        "search": {"name": "Hotel Enicar Sotogrande", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1653503645391-d355d1c9f934?w=1200"
    },
    {
        "search": {"name": "La Cala Resort", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1579476170948-2decc6dd582f?w=1200"
    },
    {
        "search": {"name": "La Costa Beach Golf Resort", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1652266371938-297fecd5514a?w=1200"
    },
    {
        "search": {"name": "La Finca Golf Resort", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1605144156546-91acf5e4cffd?w=1200"
    },
    {
        "search": {"name": "La Sella Golf Resort", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1651455578415-0c601702a094?w=1200"
    },
    {
        "search": {"name": "Las Lomas Village", "country": "Spain"},
        "image": "https://images.unsplash.com/photo-1604967046349-2fbf727a4005?w=1200"
    }
]

async def fix_exact_images():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("\n" + "="*70)
    print("FIXING MISSING IMAGES WITH EXACT NAME MATCHING")
    print("="*70 + "\n")
    
    updated_count = 0
    
    for update in EXACT_UPDATES:
        destination = await db.destinations.find_one(update["search"])
        
        if destination:
            result = await db.destinations.update_one(
                {"_id": destination["_id"]},
                {
                    "$set": {
                        "image": update["image"],
                        "images": [update["image"]],
                        "updated_at": datetime.utcnow().isoformat()
                    }
                }
            )
            
            if result.modified_count > 0:
                print(f"✅ UPDATED: {destination['name']}")
                print(f"   {update['image']}")
                print()
                updated_count += 1
            else:
                print(f"⚠️  NO CHANGE: {destination['name']}")
                print()
        else:
            print(f"❌ NOT FOUND: {update['search']['name']}")
            print()
    
    print("="*70)
    print(f"Updated {updated_count} resorts")
    print("="*70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_exact_images())
