#!/usr/bin/env python3
"""
Direct database population script for dgolf.se content
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from services.dgolf_populator import dgolf_populator
from datetime import datetime, timezone
import uuid

async def main():
    """Populate database with dgolf.se destinations"""
    
    # Connect to MongoDB
    mongo_url = "mongodb://golfguy_app:GolfApp2024SecureDB%21@localhost:27017/test_database"
    client = AsyncIOMotorClient(mongo_url)
    db = client.test_database
    
    print("🚀 Starting D Golf content population...")
    
    # Clear existing demo destinations
    result = await db.destinations.delete_many({
        "name": {"$regex": "Golf|Course|Resort|Club"}
    })
    print(f"🧹 Cleared {result.deleted_count} existing demo destinations")
    
    # Populate with real dgolf.se data
    spain_destinations = [
        {
            "id": str(uuid.uuid4()),
            "name": "Hotel Alicante Golf",
            "slug": "hotel-alicante-golf",
            "country": "Spain",
            "region": "Costa Blanca",
            "short_desc": "Experience the best of golf, sun and relaxation at Hotel Alicante Golf – the perfect starting point for an unforgettable golf vacation in Spain.",
            "long_desc": "Experience the best of golf, sun and relaxation at Hotel Alicante Golf – the perfect starting point for an unforgettable golf vacation in Spain. Here you stay just minutes from the golden San Juan Beach and have a championship course designed by legendary Severiano Ballesteros right outside your door. This destination combines excellent golf with authentic Spanish culture and cuisine, making it perfect for golfers of all levels who want to experience the Mediterranean lifestyle.",
            "destination_type": "golf_resort",
            "price_from": 800,
            "price_to": 1500,
            "currency": "SEK",
            "images": ["https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800"],
            "highlights": [
                "Course designed by Severiano Ballesteros",
                "El Plantío play included in all packages",
                "Sun-safe destination with over 300 sunny days per year",
                "Close to golden San Juan Beach"
            ],
            "courses": [{
                "par": 72,
                "holes": 18,
                "length_meters": 6100,
                "difficulty": "Championship",
                "designer": "Severiano Ballesteros",
                "course_type": "Championship",
                "year_established": 1989
            }],
            "amenities": {
                "spa": False,
                "restaurants": 2,
                "pools": 1,
                "gym": True,
                "kids_club": False,
                "conference_facilities": True,
                "beach_access": True,
                "additional": ["Golf shop", "Practice facilities", "Caddies available"]
            },
            "packages": [
                {
                    "id": "alicante-weekend",
                    "name": "Weekend Golf Package",
                    "duration_nights": 2,
                    "duration_days": 3,
                    "price": 720,
                    "currency": "SEK",
                    "inclusions": ["2 rounds of golf", "2 nights accommodation", "Breakfast", "Golf cart"],
                    "description": "Perfect weekend golf getaway to Costa Blanca"
                },
                {
                    "id": "alicante-week",
                    "name": "Week Golf Package",
                    "duration_nights": 7,
                    "duration_days": 8,
                    "price": 1200,
                    "currency": "SEK",
                    "inclusions": ["5 rounds of golf", "7 nights accommodation", "Half board", "Golf cart", "Airport transfers"],
                    "description": "Complete week-long golf vacation in sunny Alicante"
                }
            ],
            "location_coordinates": {"lat": 38.3452, "lng": -0.4810},
            "climate": "Mediterranean climate with over 300 sunny days per year",
            "best_time_to_visit": "March to November",
            "nearest_airport": "Alicante Airport (ALC)",
            "transfer_time": "25 minutes",
            "featured": False,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Las Colinas Golf & Country Club",
            "slug": "las-colinas-golf",
            "country": "Spain", 
            "region": "Costa Blanca",
            "short_desc": "Las Colinas is renowned as one of Spain's best golf destinations, with luxurious accommodation and a championship course of the highest class.",
            "long_desc": "Las Colinas is renowned as one of Spain's best golf destinations, with luxurious accommodation and a championship course of the highest class. Here, high service is combined with scenic natural surroundings. From the accommodation to the golf course there may be distance, so there is either a free shuttle that can be pre-booked, or the alternative is to take a road buggy as transport that is exchanged for a regular golf cart before the golf round. This exclusive resort offers an unparalleled golf experience with attention to every detail.",
            "destination_type": "golf_resort",
            "price_from": 1200,
            "price_to": 2500,
            "currency": "SEK",
            "images": ["https://images.unsplash.com/photo-1596727147705-61a532a659bd?w=800"],
            "highlights": [
                "Ranked as one of Spain's best courses",
                "Luxury accommodation with high service",
                "Excellent value considering the high quality offered",
                "Free shuttle service to golf course"
            ],
            "courses": [{
                "par": 72,
                "holes": 18,
                "length_meters": 6350,
                "difficulty": "Championship",
                "course_type": "Championship",
                "year_established": 2010
            }],
            "amenities": {
                "spa": True,
                "restaurants": 3,
                "pools": 2,
                "gym": True,
                "kids_club": True,
                "conference_facilities": True,
                "beach_access": False,
                "additional": ["Shuttle service", "Pro shop", "Practice academy", "Luxury villas"]
            },
            "packages": [
                {
                    "id": "colinas-premium",
                    "name": "Premium Golf Package",
                    "duration_nights": 4,
                    "duration_days": 5,
                    "price": 2200,
                    "currency": "SEK",
                    "inclusions": ["4 rounds premium golf", "4 nights luxury accommodation", "Half board", "Spa access", "Shuttle service"],
                    "description": "Premium golf experience at one of Spain's top-rated courses"
                }
            ],
            "location_coordinates": {"lat": 38.0522, "lng": -0.7658},
            "climate": "Mediterranean climate with year-round golf",
            "best_time_to_visit": "Year-round destination",
            "nearest_airport": "Alicante Airport (ALC)",
            "transfer_time": "45 minutes",
            "featured": True,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Villa Padierna Palace Hotel",
            "slug": "villa-padierna-palace",
            "country": "Spain",
            "region": "Costa del Sol",
            "short_desc": "Villa Padierna is synonymous with elegance, luxury and three first-class golf courses, located near Marbella.",
            "long_desc": "Villa Padierna is synonymous with elegance, luxury and three first-class golf courses, located near Marbella. If you want to experience a complete package where you as a customer have high demands for accommodation, golf and food, this is the right resort for you. The resort combines Andalusian architecture with modern luxury, creating an unforgettable experience in the heart of Costa del Sol. Each of the three courses offers unique challenges and stunning views of the Mediterranean landscape.",
            "destination_type": "golf_resort",
            "price_from": 2500,
            "price_to": 5000,
            "currency": "SEK",
            "images": ["https://dgolf.se/assets/villa-padierna-palace-hotel-CtRywTuH.webp"],
            "highlights": [
                "Three excellent courses on site",
                "Luxury accommodation with first-class service",
                "Fantastic dining and spa experiences",
                "Traditional Andalusian architecture"
            ],
            "courses": [
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6200,
                    "difficulty": "Championship", 
                    "course_type": "Mediterranean",
                    "year_established": 1990
                },
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6100,
                    "difficulty": "Championship",
                    "course_type": "Parkland",
                    "year_established": 1995
                },
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 5950,
                    "difficulty": "Medium",
                    "course_type": "Resort",
                    "year_established": 2000
                }
            ],
            "amenities": {
                "spa": True,
                "restaurants": 4,
                "pools": 3,
                "gym": True,
                "kids_club": True,
                "conference_facilities": True,
                "beach_access": True,
                "additional": ["Luxury spa", "Fine dining restaurants", "Beach club", "Tennis courts", "Equestrian center"]
            },
            "packages": [
                {
                    "id": "padierna-luxury",
                    "name": "Luxury Golf Experience",
                    "duration_nights": 4,
                    "duration_days": 5,
                    "price": 4500,
                    "currency": "SEK",
                    "inclusions": ["4 rounds on 3 different courses", "4 nights palace accommodation", "Half board", "Spa treatments", "Private transfers"],
                    "description": "Ultimate luxury golf experience with three championship courses"
                }
            ],
            "location_coordinates": {"lat": 36.4978, "lng": -5.1573},
            "climate": "Mediterranean climate with mild winters and warm summers",
            "best_time_to_visit": "Year-round, best March-June and September-November",
            "nearest_airport": "Málaga Airport (AGP)",
            "transfer_time": "1 hour",
            "featured": True,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert Spain destinations
    for dest in spain_destinations:
        await db.destinations.insert_one(dest)
        print(f"✅ Created: {dest['name']}")
    
    # Portugal destinations
    portugal_destinations = [
        {
            "id": str(uuid.uuid4()),
            "name": "Praia D'El Rey Golf & Beach Resort",
            "slug": "praia-del-rey",
            "country": "Portugal",
            "region": "Silver Coast",
            "short_desc": "One of Portugal's most famous golf resorts, the fantastic Praia del Rey, located at Peniche with direct views over the Atlantic.",
            "long_desc": "One of Portugal's most famous golf resorts, the fantastic Praia del Rey, located at Peniche with direct views over the Atlantic. This resort is always at the top when D Golf's customers get to choose. Fantastic well-appointed rooms adapted for golfers and 3 fine courses to choose from primarily. The resort combines links golf with beachside luxury, offering an authentic Portuguese golf experience with stunning ocean views and challenging coastal winds.",
            "destination_type": "golf_resort",
            "price_from": 1200,
            "price_to": 2800,
            "currency": "SEK",
            "images": ["https://images.unsplash.com/photo-1605144884088-bb74ade62b1b?w=800"],
            "highlights": [
                "Links experience with ocean views",
                "Good group discounts for larger golf groups 8+ people",
                "Near charming coastal towns",
                "Three excellent courses to choose from"
            ],
            "courses": [
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6477,
                    "difficulty": "Championship",
                    "course_type": "Links",
                    "designer": "Cabell Robinson",
                    "year_established": 1997
                }
            ],
            "amenities": {
                "spa": True,
                "restaurants": 2,
                "pools": 1,
                "gym": True,
                "kids_club": True,
                "conference_facilities": True,
                "beach_access": True,
                "additional": ["Tennis court", "Diving center", "Horseback riding", "Spa treatments"]
            },
            "packages": [
                {
                    "id": "praia-links",
                    "name": "Atlantic Links Package",
                    "duration_nights": 5,
                    "duration_days": 6,
                    "price": 2400,
                    "currency": "SEK",
                    "inclusions": ["5 rounds of golf", "5 nights accommodation", "Half board", "Golf cart", "Ocean views"],
                    "description": "Atlantic links golf experience with stunning ocean views"
                }
            ],
            "location_coordinates": {"lat": 39.3500, "lng": -9.2833},
            "climate": "Atlantic maritime climate with mild temperatures year-round",
            "best_time_to_visit": "April to October",
            "nearest_airport": "Lisbon Airport (LIS)",
            "transfer_time": "1 hour 15 minutes",
            "featured": True,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Monte Rei Golf & Country Club",
            "slug": "monte-rei-golf",
            "country": "Portugal",
            "region": "Eastern Algarve",
            "short_desc": "Monte Rei is one of Europe's most exclusive golf resorts with Jack Nicklaus Signature course as its crown jewel.",
            "long_desc": "Monte Rei is one of Europe's most exclusive golf resorts with Jack Nicklaus Signature course as its crown jewel. Monte Rei course has for a long time been quite unrivaled on the throne as Portugal's best course. The resort offers an unparalleled luxury experience in the eastern Algarve, with meticulously maintained fairways, premium amenities, and service that exceeds expectations. Every detail has been crafted to provide the ultimate golf vacation experience.",
            "destination_type": "golf_resort", 
            "price_from": 3000,
            "price_to": 6000,
            "currency": "SEK",
            "images": ["https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?w=800"],
            "highlights": [
                "Jack Nicklaus Signature Course",
                "One of Europe's highest ranked courses",
                "Good prices for groups of 6 or more",
                "Portugal's #1 ranked golf course"
            ],
            "courses": [{
                "par": 72,
                "holes": 18,
                "length_meters": 6400,
                "difficulty": "Championship",
                "designer": "Jack Nicklaus",
                "course_type": "Signature",
                "year_established": 2007
            }],
            "amenities": {
                "spa": True,
                "restaurants": 3,
                "pools": 2,
                "gym": True,
                "kids_club": True,
                "conference_facilities": True,
                "beach_access": False,
                "additional": ["Luxury spa", "Fine dining", "Tennis academy", "Equestrian center", "Villa accommodations"]
            },
            "location_coordinates": {"lat": 37.1833, "lng": -7.4500},
            "climate": "Mediterranean climate with over 300 days of sunshine",
            "best_time_to_visit": "Year-round destination",
            "nearest_airport": "Faro Airport (FAO)",
            "transfer_time": "45 minutes",
            "featured": True,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Scotland destinations
    scotland_destinations = [
        {
            "id": str(uuid.uuid4()),
            "name": "The Old Course Hotel, Golf Resort & Spa",
            "slug": "old-course-hotel-st-andrews",
            "country": "Scotland",
            "region": "Fife",
            "short_desc": "One of the world's most famous golf hotels, located at The Old Course in St Andrews.",
            "long_desc": "One of the world's most famous golf hotels, located at The Old Course in St Andrews. With 7 different courses in the area, you have a completely unique experience ahead of you. Live and breathe at this iconic place, a must at some point in life. Experience the birthplace of golf with access to legendary courses including the Old Course, New Course, and nearby championship venues. The hotel offers unparalleled views and direct access to golf history.",
            "destination_type": "golf_resort",
            "price_from": 5000,
            "price_to": 12000,
            "currency": "SEK",
            "images": ["https://images.unsplash.com/photo-1597051667503-1d8aeac74e3e?w=800"],
            "highlights": [
                "Directly at The Old Course",
                "Classic golf history",
                "Luxury accommodation with unique views",
                "Access to 7 courses in the area"
            ],
            "courses": [
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6721,
                    "difficulty": "Championship",
                    "designer": "Old Tom Morris",
                    "course_type": "Historic Links",
                    "year_established": 1400
                }
            ],
            "amenities": {
                "spa": True,
                "restaurants": 4,
                "pools": 1,
                "gym": True,
                "kids_club": False,
                "conference_facilities": True,
                "beach_access": True,
                "additional": ["Golf museum", "Caddie service", "Golf shop", "Whisky bar", "Historic tours"]
            },
            "location_coordinates": {"lat": 56.3398, "lng": -2.7967},
            "climate": "Temperate oceanic climate",
            "best_time_to_visit": "May to September",
            "nearest_airport": "Edinburgh Airport (EDI)",
            "transfer_time": "1 hour 30 minutes",
            "featured": True,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gleneagles",
            "slug": "gleneagles-resort",
            "country": "Scotland",
            "region": "Perthshire",
            "short_desc": "A world-famous resort with origins from the early 1900s, unique as the only golf resort that has hosted both the Solheim Cup and Ryder Cup.",
            "long_desc": "A world-famous resort with origins from the early 1900s that is completely unique as the only golf resort that has hosted both the Solheim Cup and Ryder Cup. With 3 fantastic courses in absolute world class, you have everything you need on site for a fantastic experience at Gleneagles. Known as the 'Palace in the Glens,' this legendary Scottish resort combines championship golf with Highland luxury, offering an experience that defines Scottish golf hospitality.",
            "destination_type": "golf_resort",
            "price_from": 4000,
            "price_to": 8000,
            "currency": "SEK",
            "images": ["https://images.unsplash.com/photo-1586944179463-5de30e9ad03e?w=800"],
            "highlights": [
                "Three iconic courses",
                "Ryder Cup and Solheim Cup history",
                "Luxury resort with classic elegance",
                "Only resort to host both major team competitions"
            ],
            "courses": [
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6219,
                    "difficulty": "Championship",
                    "designer": "James Braid",
                    "course_type": "Championship",
                    "year_established": 1919
                },
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6060,
                    "difficulty": "Championship",
                    "designer": "James Braid",
                    "course_type": "Championship",
                    "year_established": 1924
                },
                {
                    "par": 72,
                    "holes": 18,
                    "length_meters": 5965,
                    "difficulty": "Medium",
                    "course_type": "Parkland",
                    "year_established": 1980
                }
            ],
            "amenities": {
                "spa": True,
                "restaurants": 5,
                "pools": 2,
                "gym": True,
                "kids_club": True,
                "conference_facilities": True,
                "beach_access": False,
                "additional": ["World-class spa", "Michelin dining", "Falconry", "Off-road driving", "Highland activities"]
            },
            "location_coordinates": {"lat": 56.3962, "lng": -3.4374},
            "climate": "Temperate climate with four distinct seasons",
            "best_time_to_visit": "May to October",
            "nearest_airport": "Edinburgh Airport (EDI)",
            "transfer_time": "1 hour",
            "featured": True,
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert Portugal destinations
    for dest in portugal_destinations:
        await db.destinations.insert_one(dest)
        print(f"✅ Created: {dest['name']}")
    
    # Insert Scotland destinations  
    for dest in scotland_destinations:
        await db.destinations.insert_one(dest)
        print(f"✅ Created: {dest['name']}")
    
    print(f"\n🎉 Population complete!")
    print(f"📊 Total destinations added: {len(spain_destinations) + len(portugal_destinations) + len(scotland_destinations)}")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(main())