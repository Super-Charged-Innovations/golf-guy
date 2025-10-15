import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def check_articles():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    articles = await db.articles.find(
        {},
        {"_id": 0, "title": 1, "image": 1, "slug": 1}
    ).to_list(100)
    
    print(f"\n=== Found {len(articles)} Articles ===\n")
    
    for i, article in enumerate(articles, 1):
        image_status = "✅" if article.get('image') else "❌"
        print(f"{i}. {article['title']}")
        print(f"   Slug: {article.get('slug')}")
        print(f"   Image: {image_status} {article.get('image', 'None')[:80]}")
        print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_articles())
