from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse, StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import io
import csv


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'golftrip')]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ===== Models =====

# SEO Model
class SEO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    canonical: Optional[str] = None

# Destination Models
class Destination(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str
    country: str
    region: Optional[str] = None
    short_desc: str
    long_desc: str
    price_from: int
    price_to: int
    currency: str = "SEK"
    images: List[str] = []
    highlights: List[str] = []
    featured: bool = False
    published: bool = True
    seo: Optional[SEO] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DestinationCreate(BaseModel):
    name: str
    slug: str
    country: str
    region: Optional[str] = None
    short_desc: str
    long_desc: str
    price_from: int
    price_to: int
    currency: str = "SEK"
    images: List[str] = []
    highlights: List[str] = []
    featured: bool = False
    published: bool = True
    seo: Optional[SEO] = None

class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    short_desc: Optional[str] = None
    long_desc: Optional[str] = None
    price_from: Optional[int] = None
    price_to: Optional[int] = None
    currency: Optional[str] = None
    images: Optional[List[str]] = None
    highlights: Optional[List[str]] = None
    featured: Optional[bool] = None
    published: Optional[bool] = None
    seo: Optional[SEO] = None

# Article Models
class Article(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    publish_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    featured_until: Optional[datetime] = None
    destination_ids: List[str] = []
    image: Optional[str] = None
    published: bool = True
    seo: Optional[SEO] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ArticleCreate(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[datetime] = None
    featured_until: Optional[datetime] = None
    destination_ids: List[str] = []
    image: Optional[str] = None
    published: bool = True
    seo: Optional[SEO] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[datetime] = None
    featured_until: Optional[datetime] = None
    destination_ids: Optional[List[str]] = None
    image: Optional[str] = None
    published: Optional[bool] = None
    seo: Optional[SEO] = None

# HeroCarousel Models
class HeroCarousel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    kicker: Optional[str] = None
    image: str
    destination_id: Optional[str] = None
    cta_text: str = "Start Inquiry"
    cta_url: str = "/contact"
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HeroCarouselCreate(BaseModel):
    title: str
    subtitle: str
    kicker: Optional[str] = None
    image: str
    destination_id: Optional[str] = None
    cta_text: str = "Start Inquiry"
    cta_url: str = "/contact"
    order: int = 0
    active: bool = True

class HeroCarouselUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    kicker: Optional[str] = None
    image: Optional[str] = None
    destination_id: Optional[str] = None
    cta_text: Optional[str] = None
    cta_url: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Testimonial Models
class Testimonial(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    rating: int  # 1-5
    content: str
    destination_id: Optional[str] = None
    trip_date: Optional[str] = None
    published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TestimonialCreate(BaseModel):
    name: str
    rating: int
    content: str
    destination_id: Optional[str] = None
    trip_date: Optional[str] = None
    published: bool = True

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    rating: Optional[int] = None
    content: Optional[str] = None
    destination_id: Optional[str] = None
    trip_date: Optional[str] = None
    published: Optional[bool] = None

# Partner Models
class Partner(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str  # e.g., "insurance", "charity", "course"
    logo: str
    description: Optional[str] = None
    url: Optional[str] = None
    order: int = 0
    active: bool = True

class PartnerCreate(BaseModel):
    name: str
    type: str
    logo: str
    description: Optional[str] = None
    url: Optional[str] = None
    order: int = 0
    active: bool = True

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Inquiry Models
class InquiryNote(BaseModel):
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Inquiry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str] = None
    destination_id: Optional[str] = None
    destination_name: Optional[str] = None
    dates: Optional[str] = None
    group_size: Optional[int] = None
    budget: Optional[str] = None
    message: Optional[str] = None
    status: str = "new"  # new, in_progress, responded, closed
    notes: List[InquiryNote] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InquiryCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    destination_id: Optional[str] = None
    destination_name: Optional[str] = None
    dates: Optional[str] = None
    group_size: Optional[int] = None
    budget: Optional[str] = None
    message: Optional[str] = None

class InquiryUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[List[InquiryNote]] = None

class InquiryAddNote(BaseModel):
    text: str

# Settings Models
class Setting(BaseModel):
    model_config = ConfigDict(extra="ignore")
    key: str
    value: Any

class SettingUpdate(BaseModel):
    value: Any


# ===== Helper Functions =====

def serialize_datetime(doc: dict) -> dict:
    """Convert datetime objects to ISO strings for MongoDB storage"""
    if not doc:
        return doc
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, list):
            doc[key] = [serialize_datetime(item) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, dict):
            doc[key] = serialize_datetime(value)
    return doc

def deserialize_datetime(doc: dict, fields: List[str]) -> dict:
    """Convert ISO string timestamps back to datetime objects"""
    if not doc:
        return doc
    for field in fields:
        if field in doc and isinstance(doc[field], str):
            try:
                doc[field] = datetime.fromisoformat(doc[field])
            except:
                pass
    return doc


# ===== Routes =====

@api_router.get("/")
async def root():
    return {"message": "Golf Guy Platform API", "version": "1.0.0"}

# Destinations
@api_router.get("/destinations", response_model=List[Destination])
async def get_destinations(
    country: Optional[str] = None,
    featured: Optional[bool] = None,
    published: Optional[bool] = True
):
    query = {}
    if country:
        query["country"] = country
    if featured is not None:
        query["featured"] = featured
    if published is not None:
        query["published"] = published
    
    destinations = await db.destinations.find(query, {"_id": 0}).to_list(1000)
    for dest in destinations:
        deserialize_datetime(dest, ["created_at", "updated_at"])
    return destinations

@api_router.get("/destinations/{slug}", response_model=Destination)
async def get_destination(slug: str):
    dest = await db.destinations.find_one({"slug": slug}, {"_id": 0})
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    deserialize_datetime(dest, ["created_at", "updated_at"])
    return dest

@api_router.post("/destinations", response_model=Destination)
async def create_destination(destination: DestinationCreate):
    dest_obj = Destination(**destination.model_dump())
    doc = dest_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.destinations.insert_one(doc)
    return dest_obj

@api_router.put("/destinations/{dest_id}", response_model=Destination)
async def update_destination(dest_id: str, destination: DestinationUpdate):
    update_data = {k: v for k, v in destination.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    result = await db.destinations.update_one(
        {"id": dest_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    dest = await db.destinations.find_one({"id": dest_id}, {"_id": 0})
    deserialize_datetime(dest, ["created_at", "updated_at"])
    return dest

@api_router.delete("/destinations/{dest_id}")
async def delete_destination(dest_id: str):
    result = await db.destinations.delete_one({"id": dest_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Destination not found")
    return {"message": "Destination deleted"}

# Articles
@api_router.get("/articles", response_model=List[Article])
async def get_articles(
    category: Optional[str] = None,
    published: Optional[bool] = True,
    featured: Optional[bool] = None
):
    query = {}
    if category:
        query["category"] = category
    if published is not None:
        query["published"] = published
    if featured:
        # Featured articles have featured_until date in the future
        query["featured_until"] = {"$gt": datetime.now(timezone.utc).isoformat()}
    
    articles = await db.articles.find(query, {"_id": 0}).sort("publish_date", -1).to_list(1000)
    for article in articles:
        deserialize_datetime(article, ["publish_date", "featured_until", "created_at", "updated_at"])
    return articles

@api_router.get("/articles/{slug}", response_model=Article)
async def get_article(slug: str):
    article = await db.articles.find_one({"slug": slug}, {"_id": 0})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    deserialize_datetime(article, ["publish_date", "featured_until", "created_at", "updated_at"])
    return article

@api_router.post("/articles", response_model=Article)
async def create_article(article: ArticleCreate):
    article_obj = Article(**article.model_dump())
    doc = article_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.articles.insert_one(doc)
    return article_obj

@api_router.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: str, article: ArticleUpdate):
    update_data = {k: v for k, v in article.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    result = await db.articles.update_one(
        {"id": article_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article = await db.articles.find_one({"id": article_id}, {"_id": 0})
    deserialize_datetime(article, ["publish_date", "featured_until", "created_at", "updated_at"])
    return article

@api_router.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    result = await db.articles.delete_one({"id": article_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted"}

# Hero Carousel
@api_router.get("/hero", response_model=List[HeroCarousel])
async def get_hero_slides(active: Optional[bool] = True):
    query = {}
    if active is not None:
        query["active"] = active
    
    slides = await db.hero_carousel.find(query, {"_id": 0}).sort("order", 1).to_list(100)
    for slide in slides:
        deserialize_datetime(slide, ["created_at"])
    return slides

@api_router.post("/hero", response_model=HeroCarousel)
async def create_hero_slide(slide: HeroCarouselCreate):
    slide_obj = HeroCarousel(**slide.model_dump())
    doc = slide_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.hero_carousel.insert_one(doc)
    return slide_obj

@api_router.put("/hero/{slide_id}", response_model=HeroCarousel)
async def update_hero_slide(slide_id: str, slide: HeroCarouselUpdate):
    update_data = {k: v for k, v in slide.model_dump().items() if v is not None}
    update_data = serialize_datetime(update_data)
    
    result = await db.hero_carousel.update_one(
        {"id": slide_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Hero slide not found")
    
    slide = await db.hero_carousel.find_one({"id": slide_id}, {"_id": 0})
    deserialize_datetime(slide, ["created_at"])
    return slide

@api_router.delete("/hero/{slide_id}")
async def delete_hero_slide(slide_id: str):
    result = await db.hero_carousel.delete_one({"id": slide_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Hero slide not found")
    return {"message": "Hero slide deleted"}

# Testimonials
@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials(published: Optional[bool] = True):
    query = {}
    if published is not None:
        query["published"] = published
    
    testimonials = await db.testimonials.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for testimonial in testimonials:
        deserialize_datetime(testimonial, ["created_at"])
    return testimonials

@api_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate):
    testimonial_obj = Testimonial(**testimonial.model_dump())
    doc = testimonial_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.testimonials.insert_one(doc)
    return testimonial_obj

@api_router.put("/testimonials/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(testimonial_id: str, testimonial: TestimonialUpdate):
    update_data = {k: v for k, v in testimonial.model_dump().items() if v is not None}
    update_data = serialize_datetime(update_data)
    
    result = await db.testimonials.update_one(
        {"id": testimonial_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    testimonial = await db.testimonials.find_one({"id": testimonial_id}, {"_id": 0})
    deserialize_datetime(testimonial, ["created_at"])
    return testimonial

@api_router.delete("/testimonials/{testimonial_id}")
async def delete_testimonial(testimonial_id: str):
    result = await db.testimonials.delete_one({"id": testimonial_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return {"message": "Testimonial deleted"}

# Partners
@api_router.get("/partners", response_model=List[Partner])
async def get_partners(active: Optional[bool] = True):
    query = {}
    if active is not None:
        query["active"] = active
    
    partners = await db.partners.find(query, {"_id": 0}).sort("order", 1).to_list(1000)
    return partners

@api_router.post("/partners", response_model=Partner)
async def create_partner(partner: PartnerCreate):
    partner_obj = Partner(**partner.model_dump())
    doc = partner_obj.model_dump()
    await db.partners.insert_one(doc)
    return partner_obj

@api_router.put("/partners/{partner_id}", response_model=Partner)
async def update_partner(partner_id: str, partner: PartnerUpdate):
    update_data = {k: v for k, v in partner.model_dump().items() if v is not None}
    
    result = await db.partners.update_one(
        {"id": partner_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    partner = await db.partners.find_one({"id": partner_id}, {"_id": 0})
    return partner

@api_router.delete("/partners/{partner_id}")
async def delete_partner(partner_id: str):
    result = await db.partners.delete_one({"id": partner_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner deleted"}

# Inquiries
@api_router.get("/inquiries", response_model=List[Inquiry])
async def get_inquiries(status: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status
    
    inquiries = await db.inquiries.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for inquiry in inquiries:
        deserialize_datetime(inquiry, ["created_at", "updated_at"])
        for note in inquiry.get("notes", []):
            if isinstance(note, dict) and "created_at" in note:
                deserialize_datetime(note, ["created_at"])
    return inquiries

@api_router.get("/inquiries/{inquiry_id}", response_model=Inquiry)
async def get_inquiry(inquiry_id: str):
    inquiry = await db.inquiries.find_one({"id": inquiry_id}, {"_id": 0})
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    deserialize_datetime(inquiry, ["created_at", "updated_at"])
    for note in inquiry.get("notes", []):
        if isinstance(note, dict) and "created_at" in note:
            deserialize_datetime(note, ["created_at"])
    return inquiry

@api_router.post("/inquiries", response_model=Inquiry)
async def create_inquiry(inquiry: InquiryCreate):
    inquiry_obj = Inquiry(**inquiry.model_dump())
    doc = inquiry_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.inquiries.insert_one(doc)
    return inquiry_obj

@api_router.put("/inquiries/{inquiry_id}", response_model=Inquiry)
async def update_inquiry_status(inquiry_id: str, inquiry: InquiryUpdate):
    update_data = {k: v for k, v in inquiry.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    result = await db.inquiries.update_one(
        {"id": inquiry_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    inquiry = await db.inquiries.find_one({"id": inquiry_id}, {"_id": 0})
    deserialize_datetime(inquiry, ["created_at", "updated_at"])
    for note in inquiry.get("notes", []):
        if isinstance(note, dict) and "created_at" in note:
            deserialize_datetime(note, ["created_at"])
    return inquiry

@api_router.post("/inquiries/{inquiry_id}/notes", response_model=Inquiry)
async def add_inquiry_note(inquiry_id: str, note_data: InquiryAddNote):
    note = InquiryNote(text=note_data.text)
    note_dict = note.model_dump()
    note_dict = serialize_datetime(note_dict)
    
    result = await db.inquiries.update_one(
        {"id": inquiry_id},
        {
            "$push": {"notes": note_dict},
            "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    inquiry = await db.inquiries.find_one({"id": inquiry_id}, {"_id": 0})
    deserialize_datetime(inquiry, ["created_at", "updated_at"])
    for note in inquiry.get("notes", []):
        if isinstance(note, dict) and "created_at" in note:
            deserialize_datetime(note, ["created_at"])
    return inquiry

@api_router.get("/inquiries/export/csv")
async def export_inquiries_csv():
    inquiries = await db.inquiries.find({}, {"_id": 0}).sort("created_at", -1).to_list(10000)
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "id", "name", "email", "phone", "destination_name", "dates", 
        "group_size", "budget", "message", "status", "created_at"
    ])
    writer.writeheader()
    
    for inquiry in inquiries:
        writer.writerow({
            "id": inquiry.get("id", ""),
            "name": inquiry.get("name", ""),
            "email": inquiry.get("email", ""),
            "phone": inquiry.get("phone", ""),
            "destination_name": inquiry.get("destination_name", ""),
            "dates": inquiry.get("dates", ""),
            "group_size": inquiry.get("group_size", ""),
            "budget": inquiry.get("budget", ""),
            "message": inquiry.get("message", ""),
            "status": inquiry.get("status", ""),
            "created_at": inquiry.get("created_at", "")
        })
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=inquiries.csv"}
    )

# Instagram Mock
@api_router.get("/instagram/latest")
async def get_instagram_posts():
    # Mock Instagram posts
    return [
        {
            "id": "1",
            "caption": "Experience the stunning fairways of Costa del Sol 🏌️‍♂️",
            "media_url": "https://images.unsplash.com/photo-1683836018144-6e5f398102de?w=400",
            "permalink": "https://instagram.com/p/mock1",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "2",
            "caption": "Sunset rounds at Portugal's finest courses ⛳",
            "media_url": "https://images.unsplash.com/photo-1602798416092-03afbccf616a?w=400",
            "permalink": "https://instagram.com/p/mock2",
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        },
        {
            "id": "3",
            "caption": "Turkish golf paradise awaits 🌴",
            "media_url": "https://images.unsplash.com/photo-1668890966028-889d8f67f2b1?w=400",
            "permalink": "https://instagram.com/p/mock3",
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
        }
    ]

# Settings
@api_router.get("/settings/{key}", response_model=Setting)
async def get_setting(key: str):
    setting = await db.settings.find_one({"key": key}, {"_id": 0})
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@api_router.put("/settings/{key}", response_model=Setting)
async def update_setting(key: str, setting: SettingUpdate):
    result = await db.settings.update_one(
        {"key": key},
        {"$set": {"value": setting.value}},
        upsert=True
    )
    
    setting = await db.settings.find_one({"key": key}, {"_id": 0})
    return setting

# SEO - Sitemap
@api_router.get("/sitemap.xml", response_class=PlainTextResponse)
async def get_sitemap():
    base_url = "https://golftrip-platform.preview.emergentagent.com"
    
    # Static pages
    urls = [
        f"<url><loc>{base_url}/</loc><priority>1.0</priority></url>",
        f"<url><loc>{base_url}/destinations</loc><priority>0.9</priority></url>",
        f"<url><loc>{base_url}/articles</loc><priority>0.9</priority></url>",
        f"<url><loc>{base_url}/about</loc><priority>0.7</priority></url>",
        f"<url><loc>{base_url}/contact</loc><priority>0.8</priority></url>",
    ]
    
    # Dynamic destination pages
    destinations = await db.destinations.find({"published": True}, {"_id": 0, "slug": 1}).to_list(1000)
    for dest in destinations:
        urls.append(f"<url><loc>{base_url}/destinations/{dest['slug']}</loc><priority>0.8</priority></url>")
    
    # Dynamic article pages
    articles = await db.articles.find({"published": True}, {"_id": 0, "slug": 1}).to_list(1000)
    for article in articles:
        urls.append(f"<url><loc>{base_url}/articles/{article['slug']}</loc><priority>0.7</priority></url>")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""
    
    return sitemap

# SEO - Robots
@api_router.get("/robots.txt", response_class=PlainTextResponse)
async def get_robots():
    return """User-agent: *
Allow: /
Sitemap: https://golftrip-platform.preview.emergentagent.com/api/sitemap.xml"""


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()