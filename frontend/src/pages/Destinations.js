import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { AspectRatio } from '../components/ui/aspect-ratio';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { ArrowRight, MapPin } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Destinations() {
  const [destinations, setDestinations] = useState([]);
  const [filteredDestinations, setFilteredDestinations] = useState([]);
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDestinations();
  }, []);

  useEffect(() => {
    filterDestinations();
  }, [destinations, selectedCountry]);

  const loadDestinations = async () => {
    try {
      const response = await axios.get(`${API}/destinations?published=true`);
      setDestinations(response.data);
      
      // Extract unique countries
      const uniqueCountries = [...new Set(response.data.map(d => d.country))];
      setCountries(uniqueCountries);
    } catch (error) {
      console.error('Error loading destinations:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterDestinations = () => {
    if (selectedCountry === 'all') {
      setFilteredDestinations(destinations);
    } else {
      setFilteredDestinations(destinations.filter(d => d.country === selectedCountry));
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading destinations...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Header */}
      <section className="bg-gradient-to-br from-primary/10 via-sky-mist to-sand/30 py-16 md:py-24">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4">Golf Destinations</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Explore our curated collection of the world's finest golf destinations
          </p>
        </div>
      </section>

      {/* Filters */}
      <section className="border-b bg-white sticky top-16 z-40 shadow-sm">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium">Filter by:</span>
            <Select value={selectedCountry} onValueChange={setSelectedCountry}>
              <SelectTrigger className="w-[200px]" data-testid="country-filter">
                <SelectValue placeholder="All Countries" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Countries</SelectItem>
                {countries.map(country => (
                  <SelectItem key={country} value={country}>{country}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <span className="text-sm text-muted-foreground ml-auto">
              {filteredDestinations.length} destination{filteredDestinations.length !== 1 ? 's' : ''}
            </span>
          </div>
        </div>
      </section>

      {/* Destinations Grid */}
      <section className="py-12 md:py-16">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          {filteredDestinations.length === 0 ? (
            <div className="text-center py-12">
              <MapPin className="h-16 w-16 text-muted mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No destinations found</h3>
              <p className="text-muted-foreground">Try adjusting your filters</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredDestinations.map((dest) => (
                <Card key={dest.id} className="group overflow-hidden hover:shadow-xl transition-all duration-300" data-testid="destination-card">
                  <Link to={`/destinations/${dest.slug}`}>
                    <div className="relative">
                      <AspectRatio ratio={4/3}>
                        <img 
                          src={dest.images[0]} 
                          alt={dest.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      </AspectRatio>
                      {dest.featured && (
                        <Badge className="absolute top-3 left-3 bg-accent text-accent-foreground">
                          Featured
                        </Badge>
                      )}
                    </div>
                    <div className="p-6">
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                        <MapPin className="h-4 w-4" />
                        <span>{dest.country}</span>
                        {dest.region && <span>• {dest.region}</span>}
                      </div>
                      <h3 className="font-playfair text-xl font-semibold mb-2">{dest.name}</h3>
                      <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{dest.short_desc}</p>
                      
                      {/* Highlights */}
                      {dest.highlights && dest.highlights.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {dest.highlights.slice(0, 3).map((highlight, idx) => (
                            <Badge key={idx} variant="outline" className="text-xs">{highlight}</Badge>
                          ))}
                        </div>
                      )}

                      <div className="flex items-center justify-between pt-4 border-t">
                        <div>
                          <p className="text-xs text-muted-foreground">From</p>
                          <p className="font-semibold text-primary text-lg">
                            {dest.price_from.toLocaleString()} {dest.currency}
                          </p>
                        </div>
                        <Button size="sm" data-testid="destination-view-button">
                          View Details
                          <ArrowRight className="ml-1 h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </Link>
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-secondary/30">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-playfair text-3xl font-bold mb-4">Can't Find What You're Looking For?</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Let us create a custom golf package tailored to your preferences
          </p>
          <Link to="/contact">
            <Button size="lg" className="bg-primary hover:bg-primary/90" data-testid="custom-quote-button">
              Get Custom Quote
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
