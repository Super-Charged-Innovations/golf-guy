"""
Advanced Search and Filtering Service
Implements intelligent search with AI-powered recommendations and filtering
"""
from typing import List, Optional, Dict, Any, Union
from datetime import date, datetime, timezone
import logging
from core.database import get_database
from ai_service import ai_service
import json
import math

logger = logging.getLogger(__name__)

class SearchFilters:
    """Search and filter configuration"""
    
    def __init__(self):
        self.COUNTRIES = [
            'Spain', 'Portugal', 'Scotland', 'Ireland', 'England', 
            'France', 'Italy', 'Turkey', 'Morocco', 'Dubai', 
            'Thailand', 'Mauritius', 'South Africa', 'USA', 'Canada'
        ]
        
        self.DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard', 'Championship']
        self.ACCOMMODATION_TYPES = ['Luxury', 'Mid-range', 'Budget']
        self.COURSE_TYPES = ['Links', 'Parkland', 'Desert', 'Mountain', 'Coastal', 'Highland']
        
        self.SORT_OPTIONS = {
            'relevance': 'Most Relevant',
            'price_asc': 'Price: Low to High',
            'price_desc': 'Price: High to Low',
            'name_asc': 'Name: A to Z',
            'rating_desc': 'Highest Rated',
            'newest': 'Newest First'
        }

class SearchRequest:
    """Search request with filters"""
    
    def __init__(
        self,
        query: Optional[str] = None,
        countries: List[str] = None,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        check_in: Optional[date] = None,
        check_out: Optional[date] = None,
        players: int = 1,
        accommodation: List[str] = None,
        course_difficulty: List[str] = None,
        course_type: List[str] = None,
        amenities: List[str] = None,
        featured_only: bool = False,
        sort_by: str = 'relevance',
        page: int = 1,
        limit: int = 20,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[int] = None
    ):
        self.query = query
        self.countries = countries or []
        self.price_min = price_min
        self.price_max = price_max
        self.check_in = check_in
        self.check_out = check_out
        self.players = players
        self.accommodation = accommodation or []
        self.course_difficulty = course_difficulty or []
        self.course_type = course_type or []
        self.amenities = amenities or []
        self.featured_only = featured_only
        self.sort_by = sort_by
        self.page = page
        self.limit = limit
        self.lat = lat
        self.lng = lng
        self.radius_km = radius_km

class SearchService:
    """Advanced search service with AI integration"""
    
    def __init__(self):
        self.filters = SearchFilters()
        self.search_cache = {}  # Cache search results
        
    async def search_destinations(
        self, 
        search_request: SearchRequest,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Advanced destination search with filtering and AI recommendations
        """
        
        try:
            db = await get_database()
            
            # Build MongoDB query
            query = await self._build_search_query(search_request)
            
            # Execute search
            destinations = await db.destinations.find(
                query, 
                {"_id": 0}
            ).to_list(1000)  # Get more for better sorting
            
            # Apply post-query filtering
            filtered_destinations = self._apply_post_filters(destinations, search_request)
            
            # Calculate relevance scores
            scored_destinations = await self._calculate_relevance_scores(
                filtered_destinations, 
                search_request,
                user_profile
            )
            
            # Sort results
            sorted_destinations = self._sort_destinations(scored_destinations, search_request.sort_by)
            
            # Paginate results
            total_count = len(sorted_destinations)
            start_idx = (search_request.page - 1) * search_request.limit
            end_idx = start_idx + search_request.limit
            paginated_results = sorted_destinations[start_idx:end_idx]
            
            # Generate AI insights if user profile available
            ai_insights = None
            if user_profile and search_request.query:
                ai_insights = await self._generate_search_insights(
                    search_request, 
                    paginated_results,
                    user_profile
                )
            
            return {
                "destinations": paginated_results,
                "total_count": total_count,
                "page": search_request.page,
                "total_pages": math.ceil(total_count / search_request.limit),
                "filters_applied": self._get_applied_filters(search_request),
                "ai_insights": ai_insights,
                "search_suggestions": await self._generate_search_suggestions(search_request),
                "search_stats": {
                    "query": search_request.query,
                    "execution_time_ms": 0,  # TODO: Implement timing
                    "result_count": total_count
                }
            }
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise
    
    async def _build_search_query(self, search_request: SearchRequest) -> Dict:
        """Build MongoDB query from search parameters"""
        
        query = {"published": True}  # Only published destinations
        
        # Text search
        if search_request.query:
            query["$text"] = {"$search": search_request.query}
        
        # Country filter
        if search_request.countries:
            query["country"] = {"$in": search_request.countries}
        
        # Price range filter
        price_filter = {}
        if search_request.price_min is not None:
            price_filter["$gte"] = search_request.price_min
        if search_request.price_max is not None:
            price_filter["$lte"] = search_request.price_max
        
        if price_filter:
            # Use $or to match either price_from or price_to in range
            query["$or"] = [
                {"price_from": price_filter},
                {"price_to": price_filter}
            ]
        
        # Featured filter
        if search_request.featured_only:
            query["featured"] = True
        
        # Course difficulty filter
        if search_request.course_difficulty:
            query["courses.difficulty"] = {"$in": search_request.course_difficulty}
        
        # Course type filter
        if search_request.course_type:
            query["courses.course_type"] = {"$in": search_request.course_type}
        
        # Location-based search (if coordinates provided)
        if search_request.lat and search_request.lng and search_request.radius_km:
            query["location_coordinates"] = {
                "$geoWithin": {
                    "$centerSphere": [
                        [search_request.lng, search_request.lat],
                        search_request.radius_km / 6378.1  # Earth's radius in km
                    ]
                }
            }
        
        return query
    
    def _apply_post_filters(self, destinations: List[Dict], search_request: SearchRequest) -> List[Dict]:
        """Apply filters that can't be done in MongoDB query"""
        
        filtered = destinations[:]
        
        # Amenities filter
        if search_request.amenities:
            filtered = [
                dest for dest in filtered
                if dest.get('amenities') and any(
                    amenity.lower() in str(dest['amenities']).lower()
                    for amenity in search_request.amenities
                )
            ]
        
        # Accommodation filter
        if search_request.accommodation:
            # This would filter based on available packages/hotels
            # For now, we'll use a simple keyword match
            filtered = [
                dest for dest in filtered
                if any(
                    acc.lower() in dest.get('long_desc', '').lower()
                    for acc in search_request.accommodation
                )
            ]
        
        return filtered
    
    async def _calculate_relevance_scores(
        self, 
        destinations: List[Dict],
        search_request: SearchRequest,
        user_profile: Optional[Dict] = None
    ) -> List[Dict]:
        """Calculate relevance scores for search results"""
        
        scored_destinations = []
        
        for dest in destinations:
            score = 0
            
            # Text relevance score
            if search_request.query:
                query_words = search_request.query.lower().split()
                text_content = f"{dest.get('name', '')} {dest.get('short_desc', '')} {dest.get('long_desc', '')}".lower()
                
                for word in query_words:
                    if word in text_content:
                        score += 10
                    
                # Boost score for exact matches in name
                if search_request.query.lower() in dest.get('name', '').lower():
                    score += 50
            
            # User preference matching
            if user_profile:
                prefs = user_profile.get('preferences', {})
                
                # Country preference
                if dest.get('country') in prefs.get('preferred_countries', []):
                    score += 30
                
                # Budget matching
                budget_min = prefs.get('budget_min', 0)
                budget_max = prefs.get('budget_max', 100000)
                dest_price_avg = (dest.get('price_from', 0) + dest.get('price_to', 0)) / 2
                
                if budget_min <= dest_price_avg <= budget_max:
                    score += 20
                
                # Playing level matching
                playing_level = prefs.get('playing_level', 'Intermediate')
                if playing_level in dest.get('highlights', []):
                    score += 15
            
            # Featured destinations boost
            if dest.get('featured'):
                score += 25
            
            # Quality indicators
            if dest.get('images') and len(dest['images']) > 3:
                score += 5
            
            if dest.get('packages') and len(dest['packages']) > 0:
                score += 10
            
            # Add score to destination
            dest['relevance_score'] = score
            scored_destinations.append(dest)
        
        return scored_destinations
    
    def _sort_destinations(self, destinations: List[Dict], sort_by: str) -> List[Dict]:
        """Sort destinations based on sort criteria"""
        
        if sort_by == 'relevance':
            return sorted(destinations, key=lambda x: x.get('relevance_score', 0), reverse=True)
        elif sort_by == 'price_asc':
            return sorted(destinations, key=lambda x: x.get('price_from', 0))
        elif sort_by == 'price_desc':
            return sorted(destinations, key=lambda x: x.get('price_to', 0), reverse=True)
        elif sort_by == 'name_asc':
            return sorted(destinations, key=lambda x: x.get('name', ''))
        elif sort_by == 'rating_desc':
            # TODO: Implement rating system
            return destinations
        elif sort_by == 'newest':
            return sorted(destinations, key=lambda x: x.get('created_at', ''), reverse=True)
        else:
            return destinations
    
    def _get_applied_filters(self, search_request: SearchRequest) -> Dict[str, Any]:
        """Get summary of applied filters"""
        
        applied = {}
        
        if search_request.query:
            applied['search_query'] = search_request.query
        
        if search_request.countries:
            applied['countries'] = search_request.countries
            
        if search_request.price_min is not None or search_request.price_max is not None:
            applied['price_range'] = {
                'min': search_request.price_min,
                'max': search_request.price_max
            }
        
        if search_request.check_in and search_request.check_out:
            applied['travel_dates'] = {
                'check_in': search_request.check_in.isoformat(),
                'check_out': search_request.check_out.isoformat()
            }
        
        if search_request.players > 1:
            applied['players'] = search_request.players
            
        if search_request.featured_only:
            applied['featured_only'] = True
            
        return applied
    
    async def _generate_search_insights(
        self, 
        search_request: SearchRequest,
        results: List[Dict],
        user_profile: Dict
    ) -> Optional[str]:
        """Generate AI insights about search results"""
        
        try:
            # Prepare context for AI
            context = {
                "search_query": search_request.query,
                "result_count": len(results),
                "user_preferences": user_profile.get('preferences', {}),
                "top_results": [r.get('name') for r in results[:3]]
            }
            
            insight_prompt = f"""
            Based on this golf travel search:
            Query: {search_request.query}
            Results found: {len(results)}
            User preferences: Budget {user_profile.get('preferences', {}).get('budget_min', 0)}-{user_profile.get('preferences', {}).get('budget_max', 50000)} SEK
            
            Provide a brief, helpful insight about these search results in 1-2 sentences.
            Focus on value, recommendations, or interesting observations about the destinations found.
            """
            
            # This would use AI service in real implementation
            return f"Found {len(results)} destinations matching your search. Based on your preferences, I recommend checking out the top-rated options for the best value."
            
        except Exception as e:
            logger.error(f"Error generating search insights: {str(e)}")
            return None
    
    async def _generate_search_suggestions(self, search_request: SearchRequest) -> List[str]:
        """Generate search suggestions based on current search"""
        
        suggestions = []
        
        # If no query provided, suggest popular searches
        if not search_request.query:
            suggestions = [
                "luxury golf resorts",
                "links courses Scotland",
                "Spain golf packages",
                "championship golf courses",
                "golf with spa"
            ]
        else:
            # Generate suggestions based on current query
            query_lower = search_request.query.lower()
            
            if 'spain' in query_lower:
                suggestions.extend([
                    "Spain Costa del Sol",
                    "Spain Mallorca golf",
                    "Spain luxury resorts"
                ])
            elif 'scotland' in query_lower:
                suggestions.extend([
                    "Scotland St Andrews",
                    "Scotland links courses",
                    "Scotland Highlands golf"
                ])
            elif 'luxury' in query_lower:
                suggestions.extend([
                    "luxury golf spa resorts",
                    "5-star golf hotels",
                    "premium golf packages"
                ])
            else:
                # Generic suggestions
                suggestions = [
                    f"{search_request.query} packages",
                    f"{search_request.query} luxury",
                    f"{search_request.query} all-inclusive"
                ]
        
        return suggestions[:5]  # Return top 5 suggestions
    
    async def get_search_filters_data(self) -> Dict[str, Any]:
        """Get all available filter options with counts"""
        
        try:
            db = await get_database()
            
            # Get country counts
            country_pipeline = [
                {"$match": {"published": True}},
                {"$group": {"_id": "$country", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            country_counts = await db.destinations.aggregate(country_pipeline).to_list(None)
            
            # Get price ranges
            price_pipeline = [
                {"$match": {"published": True}},
                {"$group": {
                    "_id": None,
                    "min_price": {"$min": "$price_from"},
                    "max_price": {"$max": "$price_to"},
                    "avg_price": {"$avg": {"$avg": ["$price_from", "$price_to"]}}
                }}
            ]
            price_stats = await db.destinations.aggregate(price_pipeline).to_list(1)
            
            # Get course difficulty counts
            difficulty_pipeline = [
                {"$match": {"published": True}},
                {"$unwind": "$courses"},
                {"$group": {"_id": "$courses.difficulty", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            difficulty_counts = await db.destinations.aggregate(difficulty_pipeline).to_list(None)
            
            return {
                "countries": [
                    {"name": item["_id"], "count": item["count"]} 
                    for item in country_counts
                ],
                "price_range": price_stats[0] if price_stats else {
                    "min_price": 0, "max_price": 100000, "avg_price": 25000
                },
                "difficulty_levels": [
                    {"name": item["_id"], "count": item["count"]} 
                    for item in difficulty_counts if item["_id"]
                ],
                "course_types": [
                    {"name": course_type, "available": True} 
                    for course_type in self.filters.COURSE_TYPES
                ],
                "sort_options": self.filters.SORT_OPTIONS
            }
            
        except Exception as e:
            logger.error(f"Error getting filter data: {str(e)}")
            return {}
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in kilometers"""
        
        from math import radians, cos, sin, asin, sqrt
        
        # Convert decimal degrees to radians
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        # Haversine formula
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radius of Earth in kilometers
        r = 6371
        
        return c * r
    
    async def get_popular_searches(self) -> List[Dict]:
        """Get popular search terms and destinations"""
        
        # In real implementation, this would analyze search logs
        # For now, return curated popular searches
        return [
            {
                "query": "Scotland golf",
                "count": 156,
                "trend": "up",
                "description": "Classic links courses and whisky"
            },
            {
                "query": "Spain luxury resorts",
                "count": 134,
                "trend": "up", 
                "description": "Premium resorts with championship courses"
            },
            {
                "query": "Portugal Algarve",
                "count": 89,
                "trend": "steady",
                "description": "Coastal golf with perfect weather"
            },
            {
                "query": "Turkey all inclusive",
                "count": 67,
                "trend": "up",
                "description": "Exceptional value luxury golf"
            },
            {
                "query": "Ireland golf tours",
                "count": 45,
                "trend": "down",
                "description": "Scenic golf with cultural experiences"
            }
        ]

# Global search service instance
search_service = SearchService()