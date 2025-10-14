"""
Check database performance and indexes
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import time

load_dotenv('backend/.env')

async def check_indexes():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("📊 Current Indexes on destinations collection:")
    indexes = await db.destinations.index_information()
    for idx_name, idx_info in indexes.items():
        print(f"  {idx_name}: {idx_info.get('key', [])}")
    
    print("\n⏱️  Query Performance Test:")
    
    # Test 1: Query by country
    start = time.time()
    result = await db.destinations.find({'country': 'Spain', 'published': True}).to_list(length=None)
    elapsed = time.time() - start
    print(f"  Query Spain (published): {len(result)} docs in {elapsed*1000:.2f}ms")
    
    # Test 2: Query all published
    start = time.time()
    result = await db.destinations.find({'published': True}).to_list(length=None)
    elapsed = time.time() - start
    print(f"  Query All (published): {len(result)} docs in {elapsed*1000:.2f}ms")
    
    # Test 3: Query by slug
    start = time.time()
    result = await db.destinations.find_one({'slug': 'hotel-alicante-golf'})
    elapsed = time.time() - start
    print(f"  Query by slug: found in {elapsed*1000:.2f}ms")
    
    print("\n💡 Recommendations:")
    
    # Check for missing indexes
    if 'country_1' not in indexes:
        print("  ⚠️  Missing index on 'country' field - add for better performance")
    else:
        print("  ✅ Index on 'country' exists")
    
    if 'published_1' not in indexes:
        print("  ⚠️  Missing index on 'published' field - add for better performance")
    else:
        print("  ✅ Index on 'published' exists")
    
    if 'slug_1' not in indexes:
        print("  ⚠️  Missing unique index on 'slug' field - add for better performance")
    else:
        print("  ✅ Index on 'slug' exists")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_indexes())
