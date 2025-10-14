"""
Populate Spanish golf destinations from curated data into database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
import re

load_dotenv('backend/.env')

def generate_slug(name):
    """Generate a URL-friendly slug from the resort name"""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

# List of Spanish resorts to scrape (excluding the 6 we already have)
RESORTS_TO_SCRAPE = [
    {"name": "Oliva Nova", "region": "Alicante"},
    {"name": "Valle del Este", "region": "Alicante"},
    {"name": "La Finca Golf Resort", "region": "Alicante"},
    {"name": "Mar Menor Golf Resort", "region": "Alicante"},
    {"name": "Las Lomas", "region": "Alicante"},
    {"name": "La Sella", "region": "Alicante"},
    {"name": "Emporda", "region": "Barcelona"},
    {"name": "La Costa Beach", "region": "Barcelona"},
    {"name": "El Prat", "region": "Barcelona"},
    {"name": "Torremirona", "region": "Barcelona"},
    {"name": "S/O Sotogrande", "region": "Malaga"},
    {"name": "Atalaya Park", "region": "Malaga"},
    {"name": "Enicar Sotogrande", "region": "Malaga"},
    {"name": "Son Antem", "region": "Mallorca"},
    {"name": "Pula GC", "region": "Mallorca"}
]

# Manually curated data from dgolf.se scraping
RESORT_DATA = {
    "Oliva Nova": {
        "name": "Oliva Nova Golf Resort",
        "location": "Alicante",
        "country": "Spain",
        "description": "Experience one of Spain's most scenic golf resorts where the sea meets the green fairways. Oliva Nova offers an excellent combination of golf, beach life, and relaxation, just steps from the Mediterranean coast. This beautiful resort features a championship course designed by Severiano Ballesteros, with accommodations right on the course.",
        "highlights": [
            "Championship course designed by Severiano Ballesteros",
            "On-course accommodation with beach access",
            "Perfect combination of golf, sun, and Mediterranean Sea",
            "Year-round sunshine and excellent playing conditions"
        ],
        "price_from": 8500,
        "images": [
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "Valle del Este": {
        "name": "Valle del Este Golf Resort",
        "location": "Almería, Alicante",
        "country": "Spain",
        "description": "Valle del Este combines spectacular golf holes with views of both mountains and sea, perfectly located in sunny Almería. All our packages include half board, making them excellent value. This resort is an ideal entry point for your first international golf trip abroad.",
        "highlights": [
            "Great entry-level resort for first-time golf travelers",
            "On-course accommodation with half board included",
            "Spectacular views of mountains and Mediterranean Sea",
            "Excellent practice facilities",
            "Very affordable packages with high quality"
        ],
        "price_from": 7200,
        "images": [
            "https://images.unsplash.com/photo-1592919505780-303950717480?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "La Finca Golf Resort": {
        "name": "La Finca Golf Resort",
        "location": "Algorfa, Costa Blanca",
        "country": "Spain",
        "description": "La Finca is renowned for its modern style and high-class golf course, perfect for those who want to combine comfortable accommodation with excellent golf. The hotel lives up to its 5-star rating, offering spacious rooms, fine restaurants, and excellent facilities in the heart of Costa Blanca.",
        "highlights": [
            "Play one of the best courses in the region",
            "Luxurious 5-star accommodation on the resort",
            "Year-round golf with excellent conditions",
            "Modern facilities and fine dining options",
            "Championship course with stunning views"
        ],
        "price_from": 10500,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1592919505780-303950717480?w=800"
        ]
    },
    "Mar Menor Golf Resort": {
        "name": "Mar Menor Golf Resort",
        "location": "Los Alcázares, Murcia",
        "country": "Spain",
        "description": "Here you get a combination of golf, relaxation, and beach life by Spain's largest saltwater lagoon. The resort is ideal for both couples and groups. You can stay in either the 5-star hotel or in resort apartments. For apartments, we recommend choosing the hotel breakfast, which is on a completely different level than what's served in the clubhouse.",
        "highlights": [
            "Well-maintained and challenging championship course",
            "Great entry-level option for your first golf trip",
            "Affordable packages with excellent value",
            "Choice of 5-star hotel or resort apartments",
            "Located by Spain's largest saltwater lagoon"
        ],
        "price_from": 6800,
        "images": [
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "Las Lomas": {
        "name": "Las Lomas Village",
        "location": "La Manga Club, Murcia",
        "country": "Spain",
        "description": "Las Lomas is a picturesque and peaceful part of La Manga Club, perfect for golfers seeking relaxation while having access to all the resort's courses and facilities. Accommodations are in apartments with a 7-8 minute transfer to the first tee at La Manga, which we pre-book for maximum convenience. Currently, only studio apartments have been renovated - we highly recommend these, though larger apartments for 4-6 people are also available.",
        "highlights": [
            "Access to three world-class courses at La Manga Club",
            "Peaceful village atmosphere with complete service",
            "Excellent long-stay option with apartment living",
            "Pre-booked transfers to golf courses included",
            "Renovated studio apartments available"
        ],
        "price_from": 7500,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800"
        ]
    },
    "La Sella": {
        "name": "La Sella Golf Resort",
        "location": "Dénia, Alicante",
        "country": "Spain",
        "description": "La Sella offers golf in a lush environment between the mountains and the Mediterranean, perfect for golfers who appreciate tranquility and natural beauty. In our opinion, La Sella is one of Europe's better golf hotels, with spacious, well-designed rooms specifically for golfers. The resort also features attractive apartments perfect for longer stays, a lovely pool area, and several dining options.",
        "highlights": [
            "27-hole golf facility on site",
            "Beautiful natural setting between mountains and sea",
            "Excellent long-stay accommodation options",
            "Spacious rooms designed specifically for golfers",
            "Multiple dining venues and lovely pool area"
        ],
        "price_from": 9200,
        "images": [
            "https://images.unsplash.com/photo-1592919505780-303950717480?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "Emporda": {
        "name": "Emporda Golf Resort",
        "location": "Girona, Catalonia",
        "country": "Spain",
        "description": "Newly renovated hotel in a peaceful setting with two excellent on-site courses offering great variety. Exceptional facilities on site including an excellent spa worth visiting during your stay. A pleasant and calm atmosphere surrounds this magical area near the Costa Brava.",
        "highlights": [
            "Beautiful nature and relaxing environment",
            "Challenging golf in varied terrain",
            "36 holes on site with fine variety",
            "Newly renovated hotel and facilities",
            "Excellent spa and wellness center"
        ],
        "price_from": 8900,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800"
        ]
    },
    "La Costa Beach": {
        "name": "La Costa Beach Golf Resort",
        "location": "Pals, Girona",
        "country": "Spain",
        "description": "La Costa Beach is a modern golf resort located on the beach with Pals Golf Club just a short walk away. This resort offers a perfect combination of city, beach, and golf, allowing you to play on one of Spain's most prestigious golf courses while enjoying beachfront accommodation.",
        "highlights": [
            "Perfect combination of city, beach, and golf",
            "Play at prestigious Pals Golf Club nearby",
            "Excellent combination options with Emporda Golf",
            "Modern beachfront resort facilities",
            "Costa Brava location with cultural attractions"
        ],
        "price_from": 8400,
        "images": [
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "El Prat": {
        "name": "El Prat Golf Club",
        "location": "Barcelona",
        "country": "Spain",
        "description": "El Prat is one of Spain's most renowned courses, offering an exciting and technically demanding golf experience near Barcelona's city center. As a European Tour host venue, the golf at El Prat maintains exceptional quality. The accommodation is of good standard, and the hotel offers an excellent variety of restaurants.",
        "highlights": [
            "Challenging golf on an internationally recognized course",
            "Close proximity to Barcelona city center",
            "45 holes of championship golf",
            "European Tour host venue",
            "Multiple dining options on site"
        ],
        "price_from": 9800,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1592919505780-303950717480?w=800"
        ]
    },
    "Torremirona": {
        "name": "Torremirona Golf Resort",
        "location": "Navata, Girona",
        "country": "Spain",
        "description": "Torremirona offers a state-of-the-art course in scenic natural surroundings near Girona, perfect for those who want to play high-level golf with comfort. The resort combines modern facilities with traditional Catalan charm in a peaceful countryside setting.",
        "highlights": [
            "Modern and well-maintained championship course",
            "Comfortable accommodation near the golf course",
            "Scenic and peaceful location",
            "Easy access from Girona airport",
            "Traditional Catalan hospitality"
        ],
        "price_from": 7800,
        "images": [
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "S/O Sotogrande": {
        "name": "SO/ Sotogrande",
        "location": "Sotogrande, Andalusia",
        "country": "Spain",
        "description": "An exclusive resort at the western end of Costa del Sol, near Gibraltar and some of Spain's best courses. The resort features 27 holes on site offering an undulating journey where your tactical skills are put to the test. Modern luxury design meets championship golf in this prestigious location.",
        "highlights": [
            "Access to world-famous Valderrama and nearby championship courses",
            "Luxury accommodation with modern design",
            "27-hole challenging layout on site",
            "Near the marina and Mediterranean Sea",
            "Exclusive Sotogrande location"
        ],
        "price_from": 12500,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1592919505780-303950717480?w=800"
        ]
    },
    "Atalaya Park": {
        "name": "Atalaya Park Hotel & Golf Resort",
        "location": "Estepona, Costa del Sol",
        "country": "Spain",
        "description": "An affordable resort with 36 holes in varied terrain suitable for all skill levels. Located near Estepona and Marbella, with proximity to a wide range of golf courses and attractions. We offer affordable packages with half board and semi all-inclusive options. The resort provides shuttles to and from both golf courses.",
        "highlights": [
            "Affordable golf with great possibilities",
            "Two excellent golf courses on site (36 holes)",
            "Near Costa del Sol's best attractions",
            "Shuttle service to both courses included",
            "Half board and semi all-inclusive packages available"
        ],
        "price_from": 6500,
        "images": [
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    },
    "Enicar Sotogrande": {
        "name": "Hotel Enicar Sotogrande",
        "location": "Sotogrande, Andalusia",
        "country": "Spain",
        "description": "Enicar Sotogrande offers an excellent accommodation option in this exclusive area where you have everything as a hotel guest. Good pool area and a pleasant restaurant. Within 15 minutes you can reach the top courses in the area, and we naturally have a couple of other options for you from the slightly lower shelf as well.",
        "highlights": [
            "Access to world-famous courses in Sotogrande",
            "Very affordable accommodation option",
            "Perfect if you want to spend money on premium golf",
            "Good pool area and dining facilities",
            "Strategic location near championship courses"
        ],
        "price_from": 5800,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800"
        ]
    },
    "Son Antem": {
        "name": "Son Antem Golf Resort & Spa",
        "location": "Mallorca",
        "country": "Spain",
        "description": "Son Antem is an award-winning resort in Mallorca with two 18-hole courses, perfect for golfers who want to combine vacation with play on quality courses. Just 20 minutes from the airport and 25 minutes from central Palma, Son Antem is a real customer favorite at D Golf, offering the perfect Mallorcan golf experience.",
        "highlights": [
            "Two varied and well-maintained 18-hole courses",
            "Comfortable accommodation with all facilities",
            "Central location for excursions in Mallorca",
            "Award-winning resort with spa facilities",
            "Easy access from Palma airport"
        ],
        "price_from": 9500,
        "images": [
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "https://images.unsplash.com/photo-1592919505780-303950717480?w=800"
        ]
    },
    "Pula GC": {
        "name": "Pula Golf Club",
        "location": "Son Servera, Mallorca",
        "country": "Spain",
        "description": "Pula GC is one of Mallorca's best golf courses, known for its challenging design and beautiful environment near the beach. This technically demanding course offers stunning views and excellent playing conditions year-round, making it a favorite among discerning golfers visiting Mallorca.",
        "highlights": [
            "Challenging course with technical character",
            "Near the beach and holiday resorts",
            "Suitable for all golfers seeking quality",
            "Beautiful coastal views",
            "Year-round excellent conditions"
        ],
        "price_from": 8200,
        "images": [
            "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800",
            "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
        ]
    }
}

async def populate_spanish_resorts():
    """Populate the database with Spanish golf resorts"""
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    inserted_count = 0
    skipped_count = 0
    
    print("Starting Spanish resort population...")
    print(f"Total resorts to process: {len(RESORT_DATA)}")
    print("-" * 60)
    
    for resort_key, resort_info in RESORT_DATA.items():
        # Check if resort already exists
        existing = await db.destinations.find_one({
            "name": resort_info["name"],
            "country": "Spain"
        })
        
        if existing:
            print(f"⏭️  SKIPPED: {resort_info['name']} (already exists)")
            skipped_count += 1
            continue
        
        # Prepare destination document
        destination = {
            "id": str(uuid.uuid4()),
            "name": resort_info["name"],
            "location": resort_info["location"],
            "country": resort_info["country"],
            "description": resort_info["description"],
            "highlights": resort_info["highlights"],
            "price_from": resort_info["price_from"],
            "price_currency": "SEK",
            "images": resort_info["images"],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "featured": False,
            "category": "Golf Resort"
        }
        
        # Insert into database
        result = await db.destinations.insert_one(destination)
        
        if result.inserted_id:
            print(f"✅ INSERTED: {resort_info['name']} ({resort_info['location']})")
            inserted_count += 1
        else:
            print(f"❌ FAILED: {resort_info['name']}")
    
    print("-" * 60)
    print(f"\n📊 Summary:")
    print(f"   ✅ Successfully inserted: {inserted_count}")
    print(f"   ⏭️  Skipped (already exist): {skipped_count}")
    print(f"   📦 Total processed: {len(RESORT_DATA)}")
    
    # Verify total Spanish resorts
    total_spanish = await db.destinations.count_documents({"country": "Spain"})
    print(f"\n🇪🇸 Total Spanish resorts in database: {total_spanish}")
    
    client.close()
    print("\n✨ Spanish resort population complete!")

if __name__ == "__main__":
    asyncio.run(populate_spanish_resorts())
