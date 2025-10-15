"""
Update all Spanish golf destinations with scraped data and images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('backend/.env')

# Resort data from dgolf.se with matched images
SPANISH_RESORTS = {
    "Hotel Alicante Golf": {
        "city": "Alicante",
        "region": "Costa Blanca",
        "short_desc": "Spela golf vid Medelhavets pärla",
        "long_desc": "Upplev det bästa av golf, sol och avkoppling på Hotel Alicante Golf – den perfekta utgångspunkten för en oförglömlig golfsemester i Spanien. Här bor du bara några minuter från den gyllene stranden San Juan Beach och har en mästerskapsbana designad av legendariske Severiano Ballesteros precis utanför dörren.",
        "highlights": [
            "Bana designad av Severiano Ballesteros",
            "Spel på El Plantio ingår i alla våra paket",
            "Solsäker destination med över 300 soldagar per år"
        ],
        "image": "https://images.unsplash.com/photo-1605147861225-7bcd55f8e513"
    },
    "Oliva Nova Golf Resort": {
        "city": "Alicante", 
        "region": "Costa Blanca",
        "short_desc": "Golf vid havet på Spaniens östkust",
        "long_desc": "Upplev en av Spaniens mest natursköna golfresorter där havet möter den gröna fairwayen. Oliva Nova erbjuder en utmärkt kombination av golf, strandliv och avkoppling, endast några steg från Medelhavets strand.",
        "highlights": [
            "Bana designad av Severiano Ballesteros",
            "Boende på banan",
            "Kombinera golf med sol och bad"
        ],
        "image": "https://images.unsplash.com/photo-1720446548662-6845735ba69d"
    },
    "Las Colinas Golf & Country Club": {
        "city": "Alicante",
        "region": "Costa Blanca",
        "short_desc": "En exklusiv golfoas på Costa Blanca",
        "long_desc": "Las Colinas är känd som en av Spaniens bästa golf destinationer, med lyxigt boende och en mästerskapsbana i toppklass. Här kombineras hög service med naturskön miljö. Från boendet till golfbanan kan det vara avstånd så det finns antingen en gratis shuttle eller road buggy som transport.",
        "highlights": [
            "Rankad som en av Spaniens bästa banor",
            "Lyxboende med hög service",
            "Prisvärt sett till den höga kvaliteten som erbjuds"
        ],
        "image": "https://images.unsplash.com/photo-1591468309810-02eace4bf2f0"
    },
    "Valle del Este Golf Resort": {
        "city": "Almería",
        "region": "Costa de Almería",
        "short_desc": "Halvpension och en spektakulär golfbana onsite",
        "long_desc": "Valle del Este kombinerar spektakulära golfhål med utsikt över både berg och hav, perfekt beläget i soliga Almería. I alla våra paket erbjuder vi halvpension vilket gör att paketen blir väldigt prisvärda.",
        "highlights": [
            "Bra ingångs resort om man ska åka på sin första golfresa utomlands",
            "Boende på banan med halvpension",
            "Bra träningsmöjligheter"
        ],
        "image": "https://images.unsplash.com/photo-1579476170948-2decc6dd582f"
    },
    "La Finca Golf Resort": {
        "city": "Alicante",
        "region": "Costa Blanca",
        "short_desc": "Lyx och golf i hjärtat av Costa Blanca",
        "long_desc": "La Finca är känd för sin moderna stil och golfbana av hög klass, perfekt för dig som vill kombinera bekvämt boende med bra golf. Hotellet lever väl upp till sina 5 stjärnor och erbjuder rymliga rum, bra restauranger och fina faciliteter.",
        "highlights": [
            "Vill du spela en av de bästa banorna i området är detta rätt destination",
            "Lyxigt boende på resorten",
            "Året runt-spel"
        ],
        "image": "https://images.unsplash.com/photo-1605144156546-91acf5e4cffd"
    },
    "Mar Menor Golf Resort": {
        "city": "Murcia",
        "region": "Costa Cálida",
        "short_desc": "Golf och avkoppling vid lagunen",
        "long_desc": "Här får du en kombination av golf, avkoppling och strandliv vid Spaniens största saltvatten lagun. Resorten är idealisk för både par och grupper. Antingen bor ni i den 5 stjärniga hotelldelen eller finns det även lägenheter på resorten.",
        "highlights": [
            "Välskött och utmanande bana",
            "Bra instegs variant till första golfresan",
            "Prisvärda paket"
        ],
        "image": "https://images.unsplash.com/photo-1605144156698-804de50de0ca"
    },
    "La Manga Club": {
        "city": "Murcia",
        "region": "Costa Cálida",
        "short_desc": "Ikonisk golfresort med hela 3 banor onsite",
        "long_desc": "La Manga är en av Europas mest välkända golf resorter, känd för sin höga kvalitet och sina tre mästerskapsbanor i ett fantastiskt klimat året runt. Södra och Norra är de bästa banorna sett till våra tankar och vad våra kunder tycker men Västra banan bör prövas då den skiljer sig en del från de övriga två.",
        "highlights": [
            "Tre toppbanor på samma resort",
            "Högklassigt boende och service",
            "Perfekt klimat året runt"
        ],
        "image": "https://images.unsplash.com/photo-1604967046349-2fbf727a4005"
    },
    "Las Lomas Village": {
        "city": "Murcia",
        "region": "Costa Cálida",
        "short_desc": "Charmig golfby inom La Manga Club",
        "long_desc": "Las Lomas är en pittoresk och lugn del av La Manga Club, perfekt för golfare som söker avkoppling men med tillgång till alla resortens banor och faciliteter. Här bor man i lägenheter och har ca en transfer på 7-8min till första tee på La Manga.",
        "highlights": [
            "Tillgång till tre förstklassiga banor på La Manga",
            "Lugn miljö med komplett service",
            "Bra Longstay alternativ"
        ],
        "image": "https://images.unsplash.com/photo-1587453451984-c9d4be800788"
    },
    "La Sella Golf Resort": {
        "city": "Alicante",
        "region": "Costa Blanca",
        "short_desc": "27 hålsanläggning som erbjuder en bra variation",
        "long_desc": "La Sella erbjuder spel i en grönskande miljö mellan bergen och Medelhavet, perfekt för golfare som uppskattar lugn och skönhet. La Sella är i vår mening ett av de bättre golfhotellen i Europa där rummen är väl tilltagna och väldesignade för just golfare.",
        "highlights": [
            "27 hål onsite",
            "Vacker natur och lugn miljö",
            "Fina Longstay möjligheter"
        ],
        "image": "https://images.unsplash.com/photo-1651455578415-0c601702a094"
    },
    "PGA Catalunya Resort": {
        "city": "Girona",
        "region": "Catalunya",
        "short_desc": "Ryder cupanläggning 2031",
        "long_desc": "PGA Catalunya är ett internationellt känt golfresmål nära Girona med två toppbanor och förstklassiga faciliteter. Perfekt för den kräsne golfaren som vill spela på banor i världsklass. Båda banorna på anläggningen ligger med på topp 10 listan i Spanien.",
        "highlights": [
            "En av Europas bästa golfresorter",
            "Bucket listgolf på Stadium Course",
            "Perfekt för golfaren som vill spela på det bästa"
        ],
        "image": "https://images.unsplash.com/photo-1580935534074-ef1018d60620"
    },
    "Emporda Golf Resort": {
        "city": "Girona",
        "region": "Catalunya",
        "short_desc": "36 hål onsite med fin variation",
        "long_desc": "Nyrenoverat hotell i en lugn miljö med två fina banor onsite som erbjuder fin variation. Mycket fina faciliteter på plats och även ett riktigt bra spa som är värt ett besök under er vistelse. En trevlig och lugn atmosfär omgärdar detta magiska område.",
        "highlights": [
            "Vacker natur och avkopplande miljö",
            "Utmanande golf i varierad terräng",
            "36 hål onsite"
        ],
        "image": "https://images.unsplash.com/photo-1606443192517-919653213206"
    },
    "La Costa Beach Golf Resort": {
        "city": "Girona",
        "region": "Catalunya",
        "short_desc": "Beachresort med Pals som hemmabana",
        "long_desc": "La Costa Beach är en modern golfresort som ligger på stranden med Pals GC bara en kort promenad bort. Perfekt kombination av stad, strand och golf med tillgång till en av Spaniens mest anrika golfbanor.",
        "highlights": [
            "Perfekt kombination av stad, strand och golf",
            "Spela på en av de mest anrika golfbanorna i Spanien",
            "Bra kombo möjligheter med Emporda"
        ],
        "image": "https://images.unsplash.com/photo-1652266371938-297fecd5514a"
    },
    "El Prat Golf Club": {
        "city": "Barcelona",
        "region": "Catalunya",
        "short_desc": "45 golfhål nära Barcelona",
        "long_desc": "El Prat är en av Spaniens mest kända banor och erbjuder en spännande och tekniskt krävande golfupplevelse nära Barcelonas centrum. Som arrangör på Europatouren så håller golfen en hög klass på El Prat. Boendet är på en ok nivå och hotellet erbjuder en bra variation av restauranger.",
        "highlights": [
            "Utmanande golf på en internationellt erkänd bana",
            "Närhet till Barcelona",
            "Toppklass på golfen"
        ],
        "image": "https://images.unsplash.com/photo-1591468309810-02eace4bf2f0"
    },
    "Torremirona Golf Resort": {
        "city": "Girona",
        "region": "Catalunya",
        "short_desc": "Perfekt Golfresort för alla typer av golfare",
        "long_desc": "Torremirona erbjuder en toppmodern bana i naturskön miljö nära Girona, perfekt för dig som vill spela golf på hög nivå med komfort. Resorten kombinerar modern design med naturlig skönhet.",
        "highlights": [
            "Modern och välskött bana",
            "Bekvämt boende nära golfbanan",
            "Naturskönt och lugnt läge"
        ],
        "image": "https://images.unsplash.com/photo-1587453451984-c9d4be800788"
    },
    "Villa Padierna Palace Hotel": {
        "city": "Marbella",
        "region": "Costa del Sol",
        "short_desc": "Lyx och golf på Costa del Sol med 54 hål onsite",
        "long_desc": "Villa Padierna är synonymt med elegans, lyx och tre förstklassiga golfbanor, beläget nära Marbella. Vill du uppleva en helhet där du som kund ställer höga krav på boende, golf och mat så är detta rätt resort för dig.",
        "highlights": [
            "Tre fina banor på plats",
            "Lyxboende med förstklassig service",
            "Fantastiska mat- och spaupplevelser"
        ],
        "image": "https://images.unsplash.com/photo-1720446548662-6845735ba69d"
    },
    "La Cala Resort": {
        "city": "Mijas",
        "region": "Costa del Sol",
        "short_desc": "Costa del Sols största golfresort med 63 hål onsite",
        "long_desc": "Med tre 18-hålsbanor och en nyöppnad 9 håls bana är La Cala den största golfresorten i Malaga området och en av Spaniens mest populära golfdestinationer. Endast en kort transfer från Malagas flygplats är ni på plats på La Cala på runt 30 min.",
        "highlights": [
            "Tre unika banor på samma plats + en 9 hålare",
            "Stor resort med komplett service",
            "Golfbil ingår"
        ],
        "image": "https://images.unsplash.com/photo-1579476170948-2decc6dd582f"
    },
    "SO/ Sotogrande": {
        "city": "Sotogrande",
        "region": "Costa del Sol",
        "short_desc": "27 håls resort bland Spaniens mest exklusiva banor",
        "long_desc": "En exklusiv resort vid Costa del Sols västra ände, nära Gibraltar och några av Spaniens bästa banor. 27 hål onsite som erbjuder en kuperad resa där dina taktiska kunskaper sätts på prov.",
        "highlights": [
            "Tillgång till världsberömda banor",
            "Lyxboende med modern design",
            "Nära havet och marinan"
        ],
        "image": "https://images.unsplash.com/photo-1651455578415-0c601702a094"
    },
    "Atalaya Park Hotel & Golf Resort": {
        "city": "Estepona",
        "region": "Costa del Sol",
        "short_desc": "36 håls bana i hjärtat av Costa del Sol",
        "long_desc": "En prisvärd resort med 36 hål i varierande terräng som passar alla nivåer. Beläget nära Estepona och Marbella, med närhet till ett stort utbud av golfbanor och sevärdheter. Vi har prisvärda paket med både halvpension och semi all incl.",
        "highlights": [
            "Prisvärd golf med stora möjligheter",
            "Två bra golfbanor onsite",
            "Nära Costa del Sols bästa sevärdheter"
        ],
        "image": "https://images.unsplash.com/photo-1705783501055-f109f2f9cfb4"
    },
    "Hotel Enicar Sotogrande": {
        "city": "Sotogrande",
        "region": "Costa del Sol",
        "short_desc": "Trevligt boende i exklusiva Sotogrande området",
        "long_desc": "Enicar Sotogrande erbjuder ett riktigt bra boende alternativ i detta exklusiva område där ni har det mesta som gäst på hotellet. Bra poolområde och en trevlig restaurang. Inom 15 min når ni toppbanorna i området.",
        "highlights": [
            "Tillgång till världsberömda banor",
            "Mycket prisvärt boende",
            "Perfekt för om ni vill lägga pengarna på toppgolf"
        ],
        "image": "https://images.unsplash.com/photo-1653503645391-d355d1c9f934"
    },
    "Son Antem Golf Resort & Spa": {
        "city": "Llucmajor",
        "region": "Mallorca",
        "short_desc": "Golf i Mallorcas gröna hjärta",
        "long_desc": "Son Antem är en prisbelönt resort på Mallorca med två 18-hålsslingor, perfekt för golfaren som vill kombinera semester med spel på kvalitetsbanor. Bara 20 min från flygplatsen och 25 min från centrala Palma är Son Antem en riktigt stor kundfavorit.",
        "highlights": [
            "Två varierade och välskötta banor",
            "Bekvämt boende med alla faciliteter",
            "Centralt läge för utflykter på Mallorca"
        ],
        "image": "https://images.pexels.com/photos/12673871/pexels-photo-12673871.jpeg"
    },
    "Pula Golf Club": {
        "city": "Son Servera",
        "region": "Mallorca",
        "short_desc": "Utmanande bana på Mallorca",
        "long_desc": "Pula GC är en av Mallorcas bästa golfbanor, känd för sin utmanande design och vackra miljö nära stranden. Perfekt kombination av golf och strandliv på den vackra ön Mallorca.",
        "highlights": [
            "Utmanande bana med teknisk karaktär",
            "Nära stranden och semesterorter",
            "Passar alla golfare"
        ],
        "image": "https://images.pexels.com/photos/1710007/pexels-photo-1710007.jpeg"
    }
}

async def update_spanish_destinations():
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'golf_guy_platform')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("\n" + "="*70)
    print("UPDATING SPANISH GOLF DESTINATIONS WITH COMPLETE DATA")
    print("="*70 + "\n")
    
    updated_count = 0
    
    for resort_name, resort_data in SPANISH_RESORTS.items():
        # Try to find by name (case insensitive and flexible matching)
        destination = await db.destinations.find_one({
            "country": "Spain",
            "name": {"$regex": resort_name.split()[0], "$options": "i"}
        })
        
        if destination:
            # Prepare update data
            update_data = {
                "city": resort_data["city"],
                "region": resort_data["region"],
                "short_desc": resort_data["short_desc"],
                "long_desc": resort_data["long_desc"],
                "highlights": resort_data["highlights"],
                "image": resort_data["image"],
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Update the destination
            result = await db.destinations.update_one(
                {"_id": destination["_id"]},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                print(f"✅ UPDATED: {destination['name']}")
                print(f"   City: {resort_data['city']}")
                print(f"   Region: {resort_data['region']}")
                print(f"   Image: {resort_data['image'][:60]}...")
                print()
                updated_count += 1
            else:
                print(f"⚠️  NO CHANGES: {destination['name']}")
                print()
        else:
            print(f"❌ NOT FOUND: {resort_name}")
            print()
    
    print("="*70)
    print(f"SUMMARY: Updated {updated_count} out of {len(SPANISH_RESORTS)} resorts")
    print("="*70)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_spanish_destinations())
