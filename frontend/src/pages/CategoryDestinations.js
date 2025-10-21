import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { 
  ArrowRight, 
  MapPin, 
  Calendar,
  Users,
  Star,
  Plane
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Country data matching dgolf.se structure
const COUNTRY_CONFIG = {
  spain: {
    name: "Spain",
    swedish_name: "Spanien", 
    flagCode: "ES",
    description: "Experience fantastic golf courses year-round with warm climate and beautiful landscapes",
    color: "from-red-500 to-yellow-500"
  },
  portugal: {
    name: "Portugal",
    swedish_name: "Portugal",
    flagCode: "PT", 
    description: "Combine beautiful coast with world-class golf courses and Portuguese hospitality",
    color: "from-green-600 to-red-500"
  },
  scotland: {
    name: "Scotland", 
    swedish_name: "Skottland",
    flagCode: "GB-SCT",
    description: "The birthplace of golf, home to St Andrews and world's most legendary links courses",
    color: "from-blue-600 to-blue-800"
  },
  france: {
    name: "France",
    swedish_name: "Frankrike",
    flagCode: "FR",
    description: "Historic golf courses in Provence with traditional French architecture", 
    color: "from-blue-500 to-red-500"
  },
  ireland: {
    name: "Ireland",
    swedish_name: "Irland", 
    flagCode: "IE",
    description: "Scenic golf with cultural experiences and legendary Irish hospitality",
    color: "from-green-600 to-green-800"
  },
  england: {
    name: "England",
    swedish_name: "England",
    flagCode: "GB-ENG",
    description: "Championship golf courses with rich history and traditional British culture",
    color: "from-red-600 to-blue-600"
  },
  italy: {
    name: "Italy",
    swedish_name: "Italien",
    flagCode: "IT", 
    description: "Mediterranean golf with Italian cuisine and stunning landscapes",
    color: "from-green-500 to-red-500"
  },
  mauritius: {
    name: "Mauritius",
    swedish_name: "Mauritius",
    flagCode: "MU",
    description: "Tropical paradise golf with luxury resorts and pristine beaches",
    color: "from-cyan-500 to-blue-600"
  },
  turkey: {
    name: "Turkey", 
    swedish_name: "Turkiet",
    flagCode: "TR",
    description: "All-inclusive golf resorts with exceptional value and Mediterranean charm",
    color: "from-red-500 to-yellow-500"
  },
  usa: {
    name: "USA",
    swedish_name: "USA", 
    flagCode: "US",
    description: "Championship golf courses from coast to coast with diverse landscapes",
    color: "from-red-500 to-blue-600"
  },
  cyprus: {
    name: "Cyprus",
    swedish_name: "Cypern",
    flagCode: "CY",
    description: "Mediterranean golf with year-round sunshine and island hospitality",
    color: "from-orange-500 to-green-600"
  },
  czechia: {
    name: "Czechia",
    swedish_name: "Tjeckien",
    flagCode: "CZ",
    description: "Combine golf with historic Prague and Czech culture",
    color: "from-blue-500 to-red-500"
  },
  morocco: {
    name: "Morocco",
    swedish_name: "Marocko",
    flagCode: "MA",
    description: "Exotic golf experiences with Moroccan hospitality and desert landscapes",
    color: "from-red-500 to-green-600"
  },
  bulgaria: {
    name: "Bulgaria",
    swedish_name: "Bulgarien",
    flagCode: "BG",
    description: "Affordable golf with Black Sea coastal beauty and mountain views",
    color: "from-white via-green-500 to-red-500"
  },
  norway: {
    name: "Norway",
    swedish_name: "Norge",
    flagCode: "NO",
    description: "Unique Nordic golf with midnight sun experiences and fjord views",
    color: "from-red-500 to-blue-600"
  }
};

const CategoryDestinations = () => {
  const navigate = useNavigate();
  const [destinationsByCountry, setDestinationsByCountry] = useState({});
  const [loading, setLoading] = useState(true);
  const [totalDestinations, setTotalDestinations] = useState(0);

  useEffect(() => {
    loadDestinationsByCountry();
  }, []);

  const loadDestinationsByCountry = async () => {
    try {
      const response = await axios.get(`${API}/destinations?published=true`);
      const destinations = response.data || [];
      
      console.log('Total destinations loaded:', destinations.length);
      console.log('Countries found:', [...new Set(destinations.map(d => d.country))]);
      
      // Group destinations by country
      const grouped = destinations.reduce((acc, dest) => {
        const country = dest.country.toLowerCase();
        if (!acc[country]) {
          acc[country] = [];
        }
        acc[country].push(dest);
        return acc;
      }, {});

      console.log('Grouped by country:', Object.keys(grouped));
      setDestinationsByCountry(grouped);
      setTotalDestinations(destinations.length);
      
    } catch (error) {
      console.error('Error loading destinations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExploreCountry = (country) => {
    navigate(`/destinations/list?country=${country}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-emerald-50/30 to-white py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="w-16 h-16 bg-gray-200 rounded-full mx-auto mb-4 animate-pulse" />
            <div className="h-8 bg-gray-200 rounded w-64 mx-auto mb-4 animate-pulse" />
            <div className="h-4 bg-gray-200 rounded w-96 mx-auto animate-pulse" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, index) => (
              <Card key={index} className="h-48 bg-gray-200 animate-pulse" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50/30 to-white py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-emerald-100 rounded-full mb-4">
            <Plane className="w-8 h-8 text-emerald-600" />
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            All Our Golf Destinations
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Explore all the world's best golf courses and enjoy unforgettable golf experiences 
            at fantastic destinations around the world.
          </p>
          
          <div className="mt-6 flex items-center justify-center gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              <span>{Object.keys(destinationsByCountry).length} Countries</span>
            </div>
            <div className="flex items-center gap-2">
              <Star className="w-4 h-4" />
              <span>{totalDestinations} Premium Resorts</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              <span>Year-round Travel</span>
            </div>
          </div>
        </div>

        {/* Country Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {Object.entries(destinationsByCountry)
            .sort(([,a], [,b]) => b.length - a.length) // Sort by number of destinations
            .map(([countryKey, destinations]) => {
              const countryConfig = COUNTRY_CONFIG[countryKey] || {
                name: countryKey.charAt(0).toUpperCase() + countryKey.slice(1),
                flagCode: "🌍",
                description: `Golf destinations in ${countryKey}`,
                color: "from-gray-500 to-gray-700"
              };
              
              const featuredDestinations = destinations.filter(d => d.featured);
              
              return (
                <Card 
                  key={countryKey}
                  className="group hover:shadow-xl transition-all duration-300 cursor-pointer border-0 bg-white overflow-hidden"
                  onClick={() => handleExploreCountry(countryConfig.name)}
                >
                  <div className="h-32 relative overflow-hidden">
                    {/* Background Golf Course Image */}
                    <div className="absolute inset-0">
                      <img 
                        src={destinations[0]?.image || destinations[0]?.images?.[0] || "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=600"}
                        alt={countryConfig.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                      />
                      {/* Dark overlay for text visibility - no gradient color */}
                      <div className="absolute inset-0 bg-black/40"></div>
                    </div>
                    
                    {/* Flag and Country Name */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center text-white relative z-10">
                        <div className="mb-2 filter drop-shadow-2xl">
                          <CountryFlag countryCode={countryConfig.flagCode} size="6xl" />
                        </div>
                        <h3 className="text-2xl font-bold tracking-wide drop-shadow-lg">
                          {countryConfig.name}
                        </h3>
                      </div>
                    </div>
                    
                    {/* Decorative Circles */}
                    <div className="absolute inset-0 opacity-10">
                      <div className="absolute top-4 right-4 w-20 h-20 border-2 border-white rounded-full" />
                      <div className="absolute bottom-4 left-4 w-16 h-16 border-2 border-white rounded-full" />
                    </div>
                  </div>
                  
                  <CardContent className="p-6">
                    {/* Resort Count */}
                    <div className="flex items-center justify-between mb-3">
                      <Badge variant="secondary" className="bg-emerald-50 text-emerald-700">
                        {destinations.length} resort{destinations.length !== 1 ? 's' : ''}
                      </Badge>
                      {featuredDestinations.length > 0 && (
                        <Badge variant="outline" className="border-amber-300 text-amber-700">
                          <Star className="w-3 h-3 mr-1 fill-current" />
                          {featuredDestinations.length} featured
                        </Badge>
                      )}
                    </div>
                    
                    {/* Description */}
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {countryConfig.description}
                    </p>
                    
                    {/* Sample Destinations */}
                    <div className="space-y-2 mb-4">
                      {destinations.slice(0, 2).map((dest, index) => (
                        <div key={dest.id} className="flex items-center gap-2 text-sm">
                          <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                          <span className="text-gray-700 font-medium">
                            {dest.name}
                          </span>
                          <span className="text-gray-500">
                            ({dest.region})
                          </span>
                        </div>
                      ))}
                      {destinations.length > 2 && (
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <div className="w-2 h-2 bg-gray-300 rounded-full" />
                          <span>+ {destinations.length - 2} more destinations</span>
                        </div>
                      )}
                    </div>
                    
                    {/* Price Range */}
                    <div className="flex items-center justify-between text-sm mb-4">
                      <span className="text-gray-500">Price range:</span>
                      <span className="font-medium text-gray-900">
                        {Math.min(...destinations.map(d => d.price_from))} - {Math.max(...destinations.map(d => d.price_to))} SEK
                      </span>
                    </div>
                    
                    {/* Explore Button */}
                    <Button 
                      className="w-full bg-emerald-600 hover:bg-emerald-700 text-white group-hover:bg-emerald-700 transition-colors"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleExploreCountry(countryConfig.name);
                      }}
                    >
                      Explore {countryConfig.name}
                      <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </CardContent>
                </Card>
              );
            })
          }
        </div>

        {/* Call to Action Section */}
        <div className="bg-gradient-to-br from-emerald-600 to-emerald-800 rounded-3xl p-8 md:p-12 text-white text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Can't Find What You're Looking For?
            </h2>
            <p className="text-emerald-100 text-lg mb-6 leading-relaxed">
              We have more destinations and can customize trips according to your wishes. 
              Contact us for personalized advice and exclusive golf packages.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button 
                size="lg"
                className="bg-white text-emerald-600 hover:bg-gray-100 font-semibold px-8"
                onClick={() => navigate('/contact')}
              >
                <Users className="mr-2 w-5 h-5" />
                Contact Our Golf Experts
              </Button>
              
              <Button 
                size="lg"
                variant="outline"
                className="border-white text-white hover:bg-white/10 px-8"
                onClick={() => navigate('/articles')}
              >
                Read Travel Guides
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </div>
            
            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div className="bg-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold mb-1">300+</div>
                <div className="text-emerald-100 text-sm">Golf Courses</div>
              </div>
              <div className="bg-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold mb-1">15+</div>
                <div className="text-emerald-100 text-sm">Countries</div>
              </div>
              <div className="bg-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold mb-1">20+</div>
                <div className="text-emerald-100 text-sm">Years Experience</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoryDestinations;