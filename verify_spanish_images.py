import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def verify_images():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Find all Spanish destinations
    destinations = await db.destinations.find(
        {"country": "Spain"},
        {"_id": 0, "name": 1, "image": 1}
    ).sort("name", 1).to_list(100)
    
    print("\n" + "="*70)
    print("SPANISH DESTINATIONS IMAGE STATUS")
    print("="*70 + "\n")
    
    missing_count = 0
    for dest in destinations:
        image = dest.get('image')
        status = "✅" if image and image != "None" else "❌"
        
        if not image or image == "None":
            missing_count += 1
            
        print(f"{status} {dest['name']}")
        if image and image != "None":
            print(f"   {image[:80]}...")
        else:
            print(f"   NO IMAGE")
        print()
    
    print("="*70)
    print(f"Total: {len(destinations)} | With Images: {len(destinations) - missing_count} | Missing: {missing_count}")
    print("="*70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(verify_images())
