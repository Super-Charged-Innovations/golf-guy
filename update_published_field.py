"""
Add published=True field to all destinations that don't have it
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def add_published_field():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Update all destinations without published field to published=True
    result = await db.destinations.update_many(
        {'published': {'$exists': False}},
        {'$set': {'published': True}}
    )
    
    print(f'✅ Updated {result.modified_count} destinations to published=True')
    
    # Verify Spanish destinations
    spain_count = await db.destinations.count_documents({'country': 'Spain', 'published': True})
    print(f'🇪🇸 Spanish published destinations: {spain_count}')
    
    # Verify total
    total_published = await db.destinations.count_documents({'published': True})
    print(f'📦 Total published destinations: {total_published}')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_published_field())
