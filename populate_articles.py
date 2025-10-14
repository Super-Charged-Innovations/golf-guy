#!/usr/bin/env python3
"""
Populate articles based on dgolf.se content
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

async def populate_articles():
    """Populate database with dgolf.se-style articles"""
    
    mongo_url = "mongodb://golfguy_app:GolfApp2024SecureDB%21@localhost:27017/test_database"
    client = AsyncIOMotorClient(mongo_url)
    db = client.test_database
    
    print("📝 Populating articles with D Golf content...")
    
    # Clear existing articles
    result = await db.articles.delete_many({})
    print(f"🧹 Cleared {result.deleted_count} existing articles")
    
    articles = [
        {
            "id": str(uuid.uuid4()),
            "title": "Golf Equipment and Airline Weight Limits: Travel Guide",
            "slug": "golf-equipment-airline-guide", 
            "content": "Complete guide to traveling with golf equipment, including airline weight limits, packing tips, and destination-specific considerations for golf travelers.",
            "excerpt": "Essential travel guide for golfers covering equipment regulations and packing strategies.",
            "category": "Travel Tips",
            "author": "Golf Guy Editorial Team",
            "publish_date": datetime.now(timezone.utc).isoformat(),
            "image": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Best Golf Destinations 2024: Traveler Rankings",
            "slug": "best-golf-destinations-2024",
            "content": "Discover the top-rated golf destinations for 2024 based on thousands of traveler reviews, including Monte Rei, Gleneagles, and PGA Catalunya.",
            "excerpt": "Annual ranking of the world's best golf destinations based on real traveler experiences.",
            "category": "Destination Guides",
            "author": "Golf Guy Editorial Team", 
            "publish_date": datetime.now(timezone.utc).isoformat(),
            "featured_until": datetime.now(timezone.utc).isoformat(),
            "image": "https://images.unsplash.com/photo-1586944179463-5de30e9ad03e?w=800",
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "La Finca Golf Resort: Weekly Travel Report",
            "slug": "la-finca-travel-report",
            "content": "Experience La Finca Golf Resort - your exclusive golf trip to Alicante and Costa Blanca. Read our latest travel report from this fantastic destination featuring championship golf and luxury accommodation.",
            "excerpt": "Latest travel report from La Finca Golf Resort showcasing the complete golf vacation experience.",
            "category": "Travel Reports",
            "author": "Golf Guy Travel Team",
            "publish_date": datetime.now(timezone.utc).isoformat(),
            "image": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert articles
    for article in articles:
        await db.articles.insert_one(article)
        print(f"✅ Created article: {article['title']}")
    
    print(f"\n📝 Article population complete! Added {len(articles)} articles based on D Golf content")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(populate_articles())