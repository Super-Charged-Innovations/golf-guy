"""
Unified destination maintenance utility
Consolidates fix_spanish_destinations.py, fix_missing_slugs.py, update_published_field.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import re
import argparse
from datetime import datetime

load_dotenv('backend/.env')

def generate_slug(name):
    """Generate a URL-friendly slug from the resort name"""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

class DestinationMaintenance:
    def __init__(self):
        self.mongo_url = os.environ.get('MONGO_URL')
        self.db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
        self.client = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.db_name]
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
    
    async def fix_missing_slugs(self, dry_run=False):
        """Add missing slugs to destinations"""
        print("🔍 Checking for destinations without slugs...")
        
        no_slug = await self.db.destinations.find({
            '$or': [
                {'slug': {'$exists': False}},
                {'slug': None},
                {'slug': ''}
            ]
        }).to_list(length=None)
        
        if not no_slug:
            print("✅ All destinations have slugs!")
            return 0
        
        print(f"Found {len(no_slug)} destinations without slugs")
        
        if dry_run:
            for dest in no_slug:
                slug = generate_slug(dest['name'])
                print(f"  Would add slug: {dest['name']} -> {slug}")
            return len(no_slug)
        
        updated = 0
        for dest in no_slug:
            slug = generate_slug(dest['name'])
            result = await self.db.destinations.update_one(
                {'id': dest['id']},
                {'$set': {'slug': slug, 'updated_at': datetime.utcnow().isoformat()}}
            )
            if result.modified_count > 0:
                print(f"✅ Added slug: {dest['name']} -> {slug}")
                updated += 1
        
        return updated
    
    async def fix_missing_fields(self, dry_run=False):
        """Add missing required fields to destinations"""
        print("🔍 Checking for destinations with missing fields...")
        
        all_dests = await self.db.destinations.find({}).to_list(length=None)
        needs_fix = []
        
        for dest in all_dests:
            missing_fields = []
            
            if 'short_desc' not in dest or not dest.get('short_desc'):
                missing_fields.append('short_desc')
            if 'long_desc' not in dest or not dest.get('long_desc'):
                missing_fields.append('long_desc')
            if 'price_to' not in dest or not dest.get('price_to'):
                missing_fields.append('price_to')
            if 'region' not in dest or not dest.get('region'):
                missing_fields.append('region')
            if 'currency' not in dest or dest.get('currency') != 'SEK':
                missing_fields.append('currency')
            if 'destination_type' not in dest or not dest.get('destination_type'):
                missing_fields.append('destination_type')
            
            if missing_fields:
                needs_fix.append((dest, missing_fields))
        
        if not needs_fix:
            print("✅ All destinations have required fields!")
            return 0
        
        print(f"Found {len(needs_fix)} destinations with missing fields")
        
        if dry_run:
            for dest, fields in needs_fix:
                print(f"  {dest['name']}: missing {', '.join(fields)}")
            return len(needs_fix)
        
        updated = 0
        for dest, fields in needs_fix:
            update_data = {}
            
            if 'short_desc' in fields:
                desc = dest.get('description', '')
                short_desc = desc.split('.')[0] + '.' if '.' in desc else desc[:150] + '...'
                update_data['short_desc'] = short_desc
            
            if 'long_desc' in fields:
                update_data['long_desc'] = dest.get('description', '')
            
            if 'price_to' in fields:
                price_from = dest.get('price_from', 5000)
                update_data['price_to'] = price_from + 1500
            
            if 'region' in fields:
                update_data['region'] = dest.get('location', '')
            
            if 'currency' in fields:
                update_data['currency'] = 'SEK'
            
            if 'destination_type' in fields:
                update_data['destination_type'] = 'golf_resort'
            
            update_data['updated_at'] = datetime.utcnow().isoformat()
            
            result = await self.db.destinations.update_one(
                {'id': dest['id']},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                print(f"✅ Fixed: {dest['name']}")
                updated += 1
        
        return updated
    
    async def set_published_status(self, status=True, country=None, dry_run=False):
        """Set published status for destinations"""
        query = {'published': {'$exists': False}} if status else {}
        if country:
            query['country'] = country
        
        dests = await self.db.destinations.find(query).to_list(length=None)
        
        if not dests:
            print(f"✅ No destinations to update!")
            return 0
        
        print(f"Found {len(dests)} destinations to set published={status}")
        
        if dry_run:
            for dest in dests:
                print(f"  Would set published={status}: {dest['name']}")
            return len(dests)
        
        result = await self.db.destinations.update_many(
            query,
            {'$set': {
                'published': status,
                'updated_at': datetime.utcnow().isoformat()
            }}
        )
        
        print(f"✅ Updated {result.modified_count} destinations")
        return result.modified_count
    
    async def validate_data(self):
        """Validate all destination data"""
        print("🔍 Validating destination data...")
        
        all_dests = await self.db.destinations.find({}).to_list(length=None)
        issues = []
        
        for dest in all_dests:
            dest_issues = []
            
            # Check required fields
            required_fields = ['id', 'name', 'slug', 'country', 'short_desc', 'long_desc', 
                             'price_from', 'price_to', 'images', 'highlights']
            for field in required_fields:
                if field not in dest or not dest.get(field):
                    dest_issues.append(f"Missing {field}")
            
            # Check data quality
            if 'short_desc' in dest and len(dest.get('short_desc', '')) > 200:
                dest_issues.append("short_desc too long (>200 chars)")
            
            if 'price_from' in dest and 'price_to' in dest:
                if dest['price_from'] >= dest['price_to']:
                    dest_issues.append("price_from >= price_to")
            
            if 'images' in dest and not isinstance(dest['images'], list):
                dest_issues.append("images not an array")
            
            if 'highlights' in dest and len(dest.get('highlights', [])) < 3:
                dest_issues.append("Less than 3 highlights")
            
            if dest_issues:
                issues.append((dest['name'], dest_issues))
        
        if not issues:
            print("✅ All destinations validated successfully!")
            return 0
        
        print(f"\n⚠️  Found issues in {len(issues)} destinations:\n")
        for name, dest_issues in issues:
            print(f"  {name}:")
            for issue in dest_issues:
                print(f"    - {issue}")
        
        return len(issues)
    
    async def generate_report(self):
        """Generate a comprehensive report"""
        print("\n" + "="*60)
        print("📊 DESTINATION DATABASE REPORT")
        print("="*60 + "\n")
        
        total = await self.db.destinations.count_documents({})
        published = await self.db.destinations.count_documents({'published': True})
        featured = await self.db.destinations.count_documents({'featured': True})
        
        print(f"Total Destinations: {total}")
        print(f"Published: {published}")
        print(f"Featured: {featured}")
        print(f"Unpublished: {total - published}\n")
        
        # By country
        print("By Country:")
        pipeline = [
            {'$group': {'_id': '$country', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ]
        countries = await self.db.destinations.aggregate(pipeline).to_list(length=None)
        
        for country in countries:
            print(f"  {country['_id']}: {country['count']} resorts")
        
        print("\n" + "="*60 + "\n")

async def main():
    parser = argparse.ArgumentParser(description='Destination Maintenance Utility')
    parser.add_argument('--action', type=str, required=True,
                       choices=['fix-slugs', 'fix-fields', 'publish', 'unpublish', 'validate', 'report', 'all'],
                       help='Maintenance action to perform')
    parser.add_argument('--country', type=str, help='Filter by country')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    maintenance = DestinationMaintenance()
    
    try:
        await maintenance.connect()
        
        if args.action == 'fix-slugs' or args.action == 'all':
            print("\n🔧 Fixing missing slugs...")
            count = await maintenance.fix_missing_slugs(dry_run=args.dry_run)
            print(f"✅ {'Would update' if args.dry_run else 'Updated'} {count} destinations\n")
        
        if args.action == 'fix-fields' or args.action == 'all':
            print("\n🔧 Fixing missing fields...")
            count = await maintenance.fix_missing_fields(dry_run=args.dry_run)
            print(f"✅ {'Would update' if args.dry_run else 'Updated'} {count} destinations\n")
        
        if args.action == 'publish':
            print("\n🔧 Setting destinations as published...")
            count = await maintenance.set_published_status(True, args.country, args.dry_run)
            print(f"✅ {'Would update' if args.dry_run else 'Updated'} {count} destinations\n")
        
        if args.action == 'unpublish':
            print("\n🔧 Setting destinations as unpublished...")
            count = await maintenance.set_published_status(False, args.country, args.dry_run)
            print(f"✅ {'Would update' if args.dry_run else 'Updated'} {count} destinations\n")
        
        if args.action == 'validate' or args.action == 'all':
            print("\n🔍 Validating data...")
            issues = await maintenance.validate_data()
            if issues == 0:
                print("✅ No issues found!\n")
        
        if args.action == 'report' or args.action == 'all':
            await maintenance.generate_report()
        
    finally:
        await maintenance.close()

if __name__ == "__main__":
    asyncio.run(main())
