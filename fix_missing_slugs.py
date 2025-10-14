"""
Add missing slugs to destinations
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import re

load_dotenv('backend/.env')

def generate_slug(name):
    """Generate a URL-friendly slug from the resort name"""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

async def fix_missing_slugs():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Find destinations without slug or with null slug
    no_slug = await db.destinations.find({'$or': [{'slug': {'$exists': False}}, {'slug': None}]}).to_list(length=None)
    
    for dest in no_slug:
        slug = generate_slug(dest['name'])
        await db.destinations.update_one(
            {'id': dest['id']},
            {'$set': {'slug': slug}}
        )
        print(f'✅ Added slug to: {dest["name"]} -> {slug}')
    
    print(f'\n📊 Total slugs added: {len(no_slug)}')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_missing_slugs())
