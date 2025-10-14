#!/usr/bin/env python3
"""
Comprehensive D Golf Destination Population
Populates all destinations from dgolf.se across all countries
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

async def populate_all_dgolf_destinations():
    """Populate all dgolf.se destinations"""
    
    mongo_url = "mongodb://golfguy_app:GolfApp2024SecureDB%21@localhost:27017/test_database"
    client = AsyncIOMotorClient(mongo_url)
    db = client.test_database
    
    print("🚀 Starting comprehensive D Golf destination population...")
    
    # Clear existing destinations
    result = await db.destinations.delete_many({})
    print(f"🧹 Cleared {result.deleted_count} existing destinations")
    
    all_destinations = []
    
    # Spain destinations (expanded)
    spain_destinations = [
        {
            "name": "Hotel Alicante Golf",
            "slug": "hotel-alicante-golf",
            "country": "Spain",
            "region": "Costa Blanca",
            "short_desc": "Experience the best of golf, sun and relaxation at Hotel Alicante Golf – the perfect starting point for an unforgettable golf vacation in Spain.",
            "long_desc": "Located just minutes from golden San Juan Beach with a championship course designed by legendary Severiano Ballesteros. This destination combines excellent golf with authentic Spanish culture, making it perfect for golfers who want to experience Mediterranean lifestyle with over 300 sunny days per year.",
            "price_from": 850,
            "price_to": 1500,
            "highlights": ["Course designed by Severiano Ballesteros", "El Plantío play included", "Over 300 sunny days per year", "Close to San Juan Beach"],
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
            "featured": False
        },
        {
            "name": "Las Colinas Golf & Country Club",
            "slug": "las-colinas-golf",
            "country": "Spain",
            "region": "Costa Blanca", 
            "short_desc": "Las Colinas is renowned as one of Spain's best golf destinations, with luxurious accommodation and a championship course.",
            "long_desc": "Ranked among Spain's best golf courses, Las Colinas combines high-quality service with scenic natural surroundings. The resort offers shuttle service to the golf course and features luxury accommodation with modern amenities. Excellent value considering the premium quality offered.",
            "price_from": 1200,
            "price_to": 2500,
            "highlights": ["Ranked as one of Spain's best courses", "Luxury accommodation with high service", "Excellent value for quality", "Free shuttle service"],
            "image_url": "https://images.unsplash.com/photo-1596727147705-61a532a659bd?w=800",
            "featured": True
        },
        {
            "name": "La Manga Club",
            "slug": "la-manga-club", 
            "country": "Spain",
            "region": "Costa Cálida",
            "short_desc": "One of Europe's most renowned golf resorts with three championship courses and year-round perfect climate.",
            "long_desc": "La Manga is one of Europe's most renowned golf resorts, known for its high quality and three championship courses in a fantastic year-round climate. The South and North courses are considered the best, while the West course offers a different challenge from the other two.",
            "price_from": 1500,
            "price_to": 3000,
            "highlights": ["Three top courses on same resort", "High-class accommodation and service", "Perfect climate year-round"],
            "image_url": "https://images.unsplash.com/photo-1586944179463-5de30e9ad03e?w=800",
            "featured": True
        },
        {
            "name": "Villa Padierna Palace Hotel", 
            "slug": "villa-padierna-palace",
            "country": "Spain",
            "region": "Costa del Sol",
            "short_desc": "Villa Padierna is synonymous with elegance, luxury and three first-class golf courses near Marbella.",
            "long_desc": "Villa Padierna is synonymous with elegance, luxury and three first-class golf courses, located near Marbella. Perfect for customers with high demands for accommodation, golf and dining. Traditional Andalusian architecture meets modern luxury in this exceptional resort.",
            "price_from": 2500,
            "price_to": 5000,
            "highlights": ["Three excellent courses on site", "Luxury accommodation with first-class service", "Fantastic dining and spa experiences"],
            "image_url": "https://dgolf.se/assets/villa-padierna-palace-hotel-CtRywTuH.webp",
            "featured": True
        },
        {
            "name": "PGA Catalunya Resort",
            "slug": "pga-catalunya",
            "country": "Spain", 
            "region": "Catalonia",
            "short_desc": "Internationally renowned golf destination near Girona with two top courses and first-class facilities.",
            "long_desc": "Perfect for discerning golfers who want to play on world-class courses. Both courses rank in Spain's top 10, and the resort suits all budgets with 4 different accommodation types. Ryder Cup venue for 2031.",
            "price_from": 1800,
            "price_to": 4000,
            "highlights": ["One of Europe's best golf resorts", "Bucket list golf on Stadium Course", "Ryder Cup venue 2031"],
            "image_url": "https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?w=800",
            "featured": True
        },
        {
            "name": "La Cala Resort",
            "slug": "la-cala-resort",
            "country": "Spain",
            "region": "Costa del Sol",
            "short_desc": "Costa del Sol's largest golf resort with 63 holes on site and comprehensive service.",
            "long_desc": "With three 18-hole courses and a newly opened 9-hole course, La Cala is the largest golf resort in the Malaga area and one of Spain's most popular golf destinations. Only a short transfer of around 30 minutes from Malaga airport.",
            "price_from": 1100,
            "price_to": 2200,
            "highlights": ["Three unique courses plus 9-hole course", "Large resort with complete service", "Golf cart included"],
            "image_url": "https://images.unsplash.com/photo-1605144884288-49eb7f9bb447?w=800",
            "featured": False
        }
    ]
    
    # Portugal destinations (expanded)
    portugal_destinations = [
        {
            "name": "Praia D'El Rey Golf & Beach Resort",
            "slug": "praia-del-rey",
            "country": "Portugal",
            "region": "Silver Coast",
            "short_desc": "One of Portugal's most famous golf resorts with direct Atlantic Ocean views at Peniche.",
            "long_desc": "One of Portugal's most famous golf resorts, located at Peniche with direct views over the Atlantic. Consistently ranks at the top among D Golf customers. Features well-appointed rooms designed for golfers and 3 excellent courses to choose from.",
            "price_from": 1200,
            "price_to": 2800,
            "highlights": ["Links experience with ocean views", "Group discounts for 8+ people", "Near charming coastal towns"],
            "image_url": "https://images.unsplash.com/photo-1605144884088-bb74ade62b1b?w=800",
            "featured": True
        },
        {
            "name": "Monte Rei Golf & Country Club",
            "slug": "monte-rei-golf",
            "country": "Portugal",
            "region": "Eastern Algarve", 
            "short_desc": "One of Europe's most exclusive golf resorts with Jack Nicklaus Signature course as crown jewel.",
            "long_desc": "Monte Rei course has long been virtually unchallenged as Portugal's best golf course. This exclusive resort in eastern Algarve offers unparalleled luxury with meticulously maintained fairways and service that exceeds expectations.",
            "price_from": 3000,
            "price_to": 6000,
            "highlights": ["Jack Nicklaus Signature Course", "One of Europe's highest ranked courses", "Portugal's #1 ranked golf course"],
            "image_url": "https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?w=800",
            "featured": True
        },
        {
            "name": "Vale do Lobo",
            "slug": "vale-do-lobo",
            "country": "Portugal",
            "region": "Algarve",
            "short_desc": "One of Portugal's most exclusive golf resorts located on the Atlantic coast with two excellent courses.",
            "long_desc": "One of Portugal's most exclusive golf resorts, located on the Atlantic coast with two fine courses and one of golf's most iconic and photographed golf holes. Perfect for combining golf with beach life and gourmet dining.",
            "price_from": 2000,
            "price_to": 4500,
            "highlights": ["Two fantastic courses onsite", "Luxury beachside accommodation", "Near restaurants and nightlife"],
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
            "featured": True
        },
        {
            "name": "Troia Golf",
            "slug": "troia-golf",
            "country": "Portugal",
            "region": "Setúbal Peninsula",
            "short_desc": "One of Portugal's most scenic golf courses, located on a narrow peninsula south of Lisbon.",
            "long_desc": "Located on a narrow peninsula south of Lisbon and just a catamaran ride from Setúbal which offers culinary experiences and a rich selection of bars and nightclubs. Beautiful coastal location with sea views.",
            "price_from": 1000,
            "price_to": 2200,
            "highlights": ["Links with sea views", "Combine with Dunas Comporta", "Near nature and beach"],
            "image_url": "https://dgolf.se/assets/troia-golf-resort-sunset-CAqzUFUU.jpg",
            "featured": False
        }
    ]
    
    # Scotland destinations (expanded)
    scotland_destinations = [
        {
            "name": "The Old Course Hotel, Golf Resort & Spa",
            "slug": "old-course-hotel-st-andrews",
            "country": "Scotland",
            "region": "Fife",
            "short_desc": "One of the world's most famous golf hotels, located at The Old Course in St Andrews.",
            "long_desc": "Located at The Old Course in St Andrews with 7 different courses in the area, offering a completely unique experience. Live and breathe at this iconic place - a must-visit destination for any golf enthusiast.",
            "price_from": 5000,
            "price_to": 12000,
            "highlights": ["Located at The Old Course", "Classic golf history", "Luxury accommodation with unique views"],
            "image_url": "https://images.unsplash.com/photo-1597051667503-1d8aeac74e3e?w=800",
            "featured": True
        },
        {
            "name": "Gleneagles Hotel",
            "slug": "gleneagles-resort",
            "country": "Scotland",
            "region": "Perthshire",
            "short_desc": "World-famous resort from the early 1900s, unique as the only golf resort to host both Solheim Cup and Ryder Cup.",
            "long_desc": "With 3 fantastic courses in absolute world class, you have everything needed onsite for a fantastic experience at Gleneagles. Known as 'Scotland's crown jewel' for luxury and golf excellence.",
            "price_from": 4000,
            "price_to": 8000,
            "highlights": ["Three iconic courses", "Ryder Cup and Solheim Cup history", "Luxury resort with classic elegance"],
            "image_url": "https://images.unsplash.com/photo-1586944179463-5de30e9ad03e?w=800",
            "featured": True
        },
        {
            "name": "The Lodge at Craigielaw",
            "slug": "lodge-craigielaw",
            "country": "Scotland",
            "region": "East Lothian",
            "short_desc": "Charming golf hotel at Craigielaw Golf Club, near several of Scotland's best courses.",
            "long_desc": "Affordable accommodation and the perfect base for Scottish golf. The resort is surrounded by about 20 golf courses within 20 minutes, and we help you combine your golf trip with play on multiple courses.",
            "price_from": 800,
            "price_to": 1800,
            "highlights": ["Links experience by the coast", "Near many top courses", "Perfect for East Lothian golf packages"],
            "image_url": "https://dgolf.se/assets/craigielaw-golf-club-clubhouse-DmU6vqCA.jpg",
            "featured": False
        }
    ]
    
    # France destinations
    france_destinations = [
        {
            "name": "Le Golf National", 
            "slug": "le-golf-national",
            "country": "France",
            "region": "Paris",
            "short_desc": "Golf in the heart of French golf history, host of Ryder Cup 2018 and home to French Open.",
            "long_desc": "Experience an iconic golf experience at Le Golf National, host of Ryder Cup 2018 and home to French Open. Perfect for golfers who want to play on a world-class course near Paris. Perfect for golf groups wanting to play a real bucket-list course.",
            "price_from": 2200,
            "price_to": 4500,
            "highlights": ["Ryder Cup course", "Two 18-hole courses", "Perfect for serious golfers"],
            "image_url": "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=800",
            "featured": True
        },
        {
            "name": "Château de la Bégude",
            "slug": "chateau-begude",
            "country": "France", 
            "region": "Provence",
            "short_desc": "Golf in French Riviera atmosphere just outside the charming village of Valbonne.",
            "long_desc": "Located only 30 minutes from Nice, in southern France, you get authentic Provence: intimate, personal and genuine. In the rolling green landscape, you get two good golf courses, delightful aromas from French cuisine, and fresh flavors from locally produced rosé wine.",
            "price_from": 1800,
            "price_to": 3500,
            "highlights": ["Authentic French château atmosphere", "Course in the heart of Provence", "Perfect for golf and gastronomy"],
            "image_url": "https://dgolf.se/assets/begude-chateau-golf-DENw6tAE.jpg",
            "featured": True
        },
        {
            "name": "Terre Blanche Hotel Spa Golf Resort",
            "slug": "terre-blanche",
            "country": "France",
            "region": "Provence",
            "short_desc": "One of Europe's most exclusive golf resorts with two championship courses and Provence charm.",
            "long_desc": "Terre Blanche is one of the absolute best golf resorts in Europe, offering a fantastic environment, world-class gastronomy and two completely fantastic onsite courses that offer golf in absolute top class.",
            "price_from": 3500,
            "price_to": 7000,
            "highlights": ["Two top-class courses", "One of Europe's best spa resorts", "Perfect for exclusive golf trips"],
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "featured": True
        }
    ]
    
    # Ireland destinations
    ireland_destinations = [
        {
            "name": "The K Club",
            "slug": "k-club-ireland",
            "country": "Ireland",
            "region": "County Kildare",
            "short_desc": "One of Ireland's most famous golf resorts, host of Ryder Cup 2006.",
            "long_desc": "Top class throughout and for larger golf groups, contact us early as there are very affordable packages in the facility's apartment section, but these are very popular so contact us at D Golf in good time.",
            "price_from": 2500,
            "price_to": 5500,
            "highlights": ["Ryder Cup history", "Two top courses in world class", "Luxury resort with highest standard"],
            "image_url": "https://images.unsplash.com/photo-1589197331493-c4bdbaaa7f44?w=800",
            "featured": True
        },
        {
            "name": "Druids Glen Hotel & Golf Resort",
            "slug": "druids-glen",
            "country": "Ireland",
            "region": "County Wicklow",
            "short_desc": "One of Ireland's most beloved golf resorts, known as 'Europe's Augusta'.",
            "long_desc": "Known for its lush nature and spectacular design and high standard of accommodation and facilities. The resort features two world-class courses in beautiful Irish countryside.",
            "price_from": 1800,
            "price_to": 3800,
            "highlights": ["Two courses in world class", "Known as 'Europe's Augusta'", "Perfect location near Dublin"],
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
            "featured": True
        },
        {
            "name": "Carton House",
            "slug": "carton-house",
            "country": "Ireland",
            "region": "County Kildare",
            "short_desc": "Historic manor resort with two top courses and proximity to Ireland's capital.",
            "long_desc": "A perfect base for your Ireland adventure that can be combined with either play at Ryder Cup course K Club, Europe's Augusta Glen course, or one of Portmarnock's two courses.",
            "price_from": 1500,
            "price_to": 3200,
            "highlights": ["Two onsite courses with good variation", "Affordable packages", "Near Dublin for combination trips"],
            "image_url": "https://images.unsplash.com/photo-1589197331493-c4bdbaaa7f44?w=800",
            "featured": False
        }
    ]
    
    # England destinations
    england_destinations = [
        {
            "name": "The Belfry Hotel & Resort",
            "slug": "the-belfry",
            "country": "England",
            "region": "Warwickshire",
            "short_desc": "Host of Ryder Cup more times than any other course, home to iconic Brabazon Course.",
            "long_desc": "A short transfer from Birmingham airport to one of the British Isles' best golf resorts with 3 full courses onsite, good accommodation and the legendary Belair nightclub - a unique resort with everything in one place.",
            "price_from": 1600,
            "price_to": 3500,
            "highlights": ["Ryder Cup history up close", "Three courses to choose from", "Perfect for golf weekends"],
            "image_url": "https://dgolf.se/assets/the-belfry-resort-sunset-aerial-BoxkjlaZ.jpg",
            "featured": True
        },
        {
            "name": "Forest of Arden Hotel & Country Club",
            "slug": "forest-arden",
            "country": "England", 
            "region": "Warwickshire",
            "short_desc": "Classic English golf resort in beautiful parkland setting with championship course and rich history.",
            "long_desc": "The facilities are good and maintain a traditional style where you have everything you need for a pleasant golf trip. Very short transfer from the airport and you are close to the Ryder Cup course Brabazon at The Belfry.",
            "price_from": 1200,
            "price_to": 2800,
            "highlights": ["Championship course with history", "Scenic environment with lots of wildlife", "Suits both competition and vacation"],
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
            "featured": False
        }
    ]
    
    # Mauritius destinations
    mauritius_destinations = [
        {
            "name": "Ambre Resort & Spa",
            "slug": "ambre-mauritius",
            "country": "Mauritius",
            "region": "East Coast",
            "short_desc": "Adults-only paradise resort with access to spectacular Île aux Cerfs golf course.",
            "long_desc": "A paradise resort exclusively for adults, with access to one of the most spectacular courses on the island - Bernhard Langer designed Île aux Cerfs, reached via a short boat transfer.",
            "price_from": 4500,
            "price_to": 8500,
            "highlights": ["Very affordable all-inclusive hotel", "Play on unique Île aux Cerfs course", "Perfect for couples and small groups"],
            "image_url": "https://dgolf.se/assets/ile-aux-cerfs-aerial-BNgeC_P9.jpg",
            "featured": True
        },
        {
            "name": "Anahita Golf & Spa Resort",
            "slug": "anahita-mauritius",
            "country": "Mauritius",
            "region": "East Coast",
            "short_desc": "Five-star resort on Mauritius east coast with championship course designed by Ernie Els.",
            "long_desc": "A five-star resort on Mauritius east coast with its own championship course designed by Ernie Els. Perfect for longer stays with luxury beachside accommodation and world-class amenities.",
            "price_from": 5500,
            "price_to": 12000,
            "highlights": ["Ernie Els-designed championship course", "Luxury beachside accommodation", "Perfect for extended stays"],
            "image_url": "https://images.unsplash.com/photo-1589197331493-c4bdbaaa7f44?w=800",
            "featured": True
        }
    ]
    
    # Turkey destinations
    turkey_destinations = [
        {
            "name": "Regnum Carya Golf & Spa Resort",
            "slug": "regnum-carya",
            "country": "Turkey",
            "region": "Belek",
            "short_desc": "One of Turkey's most exclusive golf resorts with championship Carya course onsite.",
            "long_desc": "Almost 6-star all-inclusive in luxury class with championship course Carya onsite and access to National course. Five-star service and fantastic world-class facilities.",
            "price_from": 1800,
            "price_to": 4200,
            "highlights": ["Play golf both day and night", "All-inclusive of highest quality", "Perfect for groups and tournaments"],
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "featured": True
        },
        {
            "name": "Maxx Royal Belek Golf Resort",
            "slug": "maxx-royal-belek",
            "country": "Turkey",
            "region": "Belek",
            "short_desc": "Five-star luxury resort with Colin Montgomerie-designed course in Belek.",
            "long_desc": "The hotel is considered one of the absolute best in the area and maintains a very high level in everything from rooms and facilities to dining options.",
            "price_from": 2200,
            "price_to": 5000,
            "highlights": ["Championship course on site", "Premium all-inclusive", "Luxurious accommodation options"],
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "featured": True
        }
    ]
    
    # Italy destinations
    italy_destinations = [
        {
            "name": "Verdura Golf & Spa Resort",
            "slug": "verdura-sicily",
            "country": "Italy",
            "region": "Sicily",
            "short_desc": "One of Southern Europe's most exclusive golf resorts with two courses designed by Kyle Phillips.",
            "long_desc": "The level of accommodation and golf takes us to levels of absolute world class. Located on Sicily's beautiful coast with two championship courses and luxury amenities.",
            "price_from": 4000,
            "price_to": 8500,
            "highlights": ["Two top courses in world class by the sea", "Luxury resort with highest standard", "Perfect for golf & relaxation"],
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "featured": True
        },
        {
            "name": "Marco Simone Golf & Country Club",
            "slug": "marco-simone",
            "country": "Italy", 
            "region": "Rome",
            "short_desc": "Italy's most famous golf facility and host of Ryder Cup 2023.",
            "long_desc": "A resort perfect for golf groups wanting to play a world-class course and combine with big city life in Rome. For groups of 6 people, there are really good and affordable packages to this fantastic facility.",
            "price_from": 2500,
            "price_to": 5500,
            "highlights": ["Ryder Cup history", "Championship course in world class", "Proximity to Rome"],
            "image_url": "https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?w=800",
            "featured": True
        }
    ]
    
    # Cyprus destinations
    cyprus_destinations = [
        {
            "name": "Aphrodite Hills Golf Resort",
            "slug": "aphrodite-hills",
            "country": "Cyprus",
            "region": "Paphos",
            "short_desc": "One of the Mediterranean's most famous golf resorts, located on a cliff with sea views.",
            "long_desc": "Located on a cliff with sea views between Paphos and Limassol, Aphrodite Hills offers both luxury accommodation and world-class golf. The facility has three different types of accommodation: hotel, apartments or villas.",
            "price_from": 1800,
            "price_to": 4200,
            "highlights": ["One of Europe's best golf courses", "Luxury resort with all-inclusive option", "Perfect climate for year-round golf"],
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "featured": True
        },
        {
            "name": "Korineum Golf & Beach Resort",
            "slug": "korineum-golf",
            "country": "Cyprus",
            "region": "North Cyprus",
            "short_desc": "Unique golf vacation in Northern Cyprus with spectacular views over Mediterranean and Kyrenia mountains.",
            "long_desc": "Korineum Golf & Beach Resort combines first-class golf with beach and relaxation in a quiet environment. The resort has everything needed for a fantastic golf trip and the beach club is a must when you're there.",
            "price_from": 1400,
            "price_to": 3000,
            "highlights": ["18-hole course in unique environment", "Perfect for quiet and relaxing golf trip", "Combination of golf, beach and nature"],
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "featured": False
        }
    ]
    
    # USA destinations
    usa_destinations = [
        {
            "name": "Pebble Beach Golf Links",
            "slug": "pebble-beach",
            "country": "USA",
            "region": "California",
            "short_desc": "One of the world's most famous golf destinations, located on California's dramatic coast.",
            "long_desc": "Play on courses that regularly host major championships and enjoy unbeatable views of the Pacific Ocean. This iconic destination combines championship golf with luxury accommodation.",
            "price_from": 8000,
            "price_to": 20000,
            "highlights": ["One of the world's most iconic courses", "Spectacular ocean views", "Championship quality on all courses"],
            "image_url": "https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?w=800",
            "featured": True
        },
        {
            "name": "PGA National Resort",
            "slug": "pga-national-miami",
            "country": "USA",
            "region": "Florida",
            "short_desc": "One of Florida's most famous golf resorts with five courses and annual PGA Tour host.",
            "long_desc": "A fantastic resort that blends history with new influences. High level on everything from accommodation to culinary experiences on the resort.",
            "price_from": 3500,
            "price_to": 8000,
            "highlights": ["Five courses on same facility", "Play on official tour course", "Luxurious facilities"],
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800", 
            "featured": True
        }
    ]
    
    # Combine all destinations
    all_country_destinations = [
        ("Spain", spain_destinations),
        ("Portugal", portugal_destinations), 
        ("Scotland", scotland_destinations),
        ("France", france_destinations),
        ("Ireland", ireland_destinations),
        ("England", england_destinations),
        ("Italy", italy_destinations),
        ("Mauritius", mauritius_destinations),
        ("Turkey", turkey_destinations),
        ("Cyprus", cyprus_destinations),
        ("USA", usa_destinations)
    ]
    
    total_count = 0
    
    # Insert all destinations
    for country_name, destinations in all_country_destinations:
        print(f"\n🌍 Processing {country_name} ({len(destinations)} destinations)...")
        
        for dest_data in destinations:
            # Create complete destination object
            destination = {
                "id": str(uuid.uuid4()),
                "name": dest_data["name"],
                "slug": dest_data["slug"],
                "country": dest_data["country"],
                "region": dest_data["region"],
                "short_desc": dest_data["short_desc"],
                "long_desc": dest_data["long_desc"],
                "destination_type": "golf_resort",
                "price_from": dest_data["price_from"],
                "price_to": dest_data["price_to"],
                "currency": "SEK",
                "images": [dest_data["image_url"]],
                "highlights": dest_data["highlights"],
                "courses": [{
                    "par": 72,
                    "holes": 18,
                    "length_meters": 6200,
                    "difficulty": "Championship",
                    "course_type": "Championship"
                }],
                "amenities": {
                    "spa": True,
                    "restaurants": 2,
                    "pools": 1,
                    "gym": True,
                    "conference_facilities": True,
                    "beach_access": "coast" in dest_data["region"].lower() or "beach" in dest_data["long_desc"].lower(),
                    "additional": ["Pro shop", "Practice facilities"]
                },
                "packages": [
                    {
                        "id": f"weekend-{dest_data['slug']}",
                        "name": "Weekend Golf Package",
                        "duration_nights": 2,
                        "duration_days": 3,
                        "price": int(dest_data["price_from"] * 0.9),
                        "currency": "SEK",
                        "inclusions": ["2 rounds of golf", "2 nights accommodation", "Breakfast"],
                        "description": f"Weekend golf getaway at {dest_data['name']}"
                    }
                ],
                "featured": dest_data["featured"],
                "published": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            await db.destinations.insert_one(destination)
            print(f"✅ Created: {dest_data['name']}")
            total_count += 1
    
    print(f"\n🎉 Comprehensive destination population complete!")
    print(f"📊 Total destinations added: {total_count}")
    print(f"🌍 Countries represented: {len(all_country_destinations)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(populate_all_dgolf_destinations())