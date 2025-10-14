"""
Fix missing fields in newly added Spanish destinations
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

async def fix_destinations():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Find all Spanish destinations that are missing required fields
    spanish_dests = await db.destinations.find({'country': 'Spain'}).to_list(length=None)
    
    updated_count = 0
    
    for dest in spanish_dests:
        needs_update = False
        update_data = {}
        
        # Check if short_desc is missing
        if 'short_desc' not in dest or not dest.get('short_desc'):
            # Create short_desc from first sentence of description
            desc = dest.get('description', '')
            short_desc = desc.split('.')[0] + '.' if '.' in desc else desc[:150] + '...'
            update_data['short_desc'] = short_desc
            needs_update = True
        
        # Check if long_desc is missing
        if 'long_desc' not in dest or not dest.get('long_desc'):
            # Use the full description as long_desc
            update_data['long_desc'] = dest.get('description', '')
            needs_update = True
        
        # Check if price_to is missing
        if 'price_to' not in dest or not dest.get('price_to'):
            # Calculate price_to as price_from + 1500
            price_from = dest.get('price_from', 5000)
            update_data['price_to'] = price_from + 1500
            needs_update = True
        
        # Check if region is missing
        if 'region' not in dest or not dest.get('region'):
            location = dest.get('location', '')
            update_data['region'] = location
            needs_update = True
        
        # Check if currency is missing or incorrect
        if 'currency' not in dest or dest.get('currency') != 'SEK':
            update_data['currency'] = 'SEK'
            needs_update = True
        
        # Check if destination_type is missing
        if 'destination_type' not in dest or not dest.get('destination_type'):
            update_data['destination_type'] = 'golf_resort'
            needs_update = True
        
        if needs_update:
            result = await db.destinations.update_one(
                {'id': dest['id']},
                {'$set': update_data}
            )
            if result.modified_count > 0:
                print(f'✅ Updated: {dest.get("name")}')
                updated_count += 1
    
    print(f'\n📊 Total destinations updated: {updated_count}')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_destinations())
