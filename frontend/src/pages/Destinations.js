import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { AspectRatio } from '../components/ui/aspect-ratio';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { ArrowRight, MapPin, Sparkles } from 'lucide-react';
import { useScrollAnimation } from '../hooks/useScrollAnimation';

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
      <section className="relative bg-gradient-to-br from-emerald-50 via-emerald-100/30 to-white py-16 md:py-24 overflow-hidden">
        {/* Animated background accent */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-10 right-10 w-64 h-64 bg-emerald-400 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-10 left-10 w-96 h-96 bg-emerald-300 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        </div>
        
        <div className="relative max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-100 text-emerald-700 mb-6 animate-fade-in-up">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-medium">Premium Golf Destinations</span>
          </div>
          <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 text-gray-900 animate-fade-in-up animate-delay-100">
            Golf Destinations
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto animate-fade-in-up animate-delay-200">
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
              {filteredDestinations.map((dest, index) => (
                <DestinationCard key={dest.id} dest={dest} index={index} />
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
