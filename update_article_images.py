"""
Update travel report article images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('backend/.env')

# Better images for articles
ARTICLE_IMAGES = {
    "golf-equipment-airline-guide": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200",  # Airplane travel
    "best-golf-destinations-2024": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=1200",  # Beautiful golf course
    "la-finca-travel-report": "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=1200"  # Luxury golf resort
}

async def update_article_images():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("\n" + "="*70)
    print("UPDATING ARTICLE IMAGES")
    print("="*70 + "\n")
    
    for slug, image_url in ARTICLE_IMAGES.items():
        article = await db.articles.find_one({"slug": slug})
        
        if article:
            result = await db.articles.update_one(
                {"_id": article["_id"]},
                {
                    "$set": {
                        "image": image_url,
                        "updated_at": datetime.utcnow().isoformat()
                    }
                }
            )
            
            if result.modified_count > 0:
                print(f"✅ UPDATED: {article['title']}")
                print(f"   New Image: {image_url}")
                print()
        else:
            print(f"❌ NOT FOUND: {slug}")
            print()
    
    print("="*70)
    print("Article images updated!")
    print("="*70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_article_images())
