import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '../components/ui/carousel';
import { MapPin, ArrowRight, Check } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function DestinationDetail() {
  const { slug } = useParams();
  const [destination, setDestination] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDestination();
  }, [slug]);

  const loadDestination = async () => {
    try {
      const response = await axios.get(`${API}/destinations/${slug}`);
      setDestination(response.data);
    } catch (error) {
      console.error('Error loading destination:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!destination) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Destination Not Found</h2>
          <p className="text-muted-foreground mb-6">The destination you're looking for doesn't exist.</p>
          <Link to="/destinations">
            <Button>View All Destinations</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Gallery Carousel */}
      <section className="relative bg-black">
        <Carousel className="w-full" data-testid="gallery-carousel">
          <CarouselContent>
            {destination.images.map((image, idx) => (
              <CarouselItem key={idx}>
                <div className="relative h-[50vh] md:h-[60vh]">
                  <img 
                    src={image} 
                    alt={`${destination.name} - ${idx + 1}`}
                    className="w-full h-full object-cover"
                  />
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselPrevious className="left-4" />
          <CarouselNext className="right-4" />
        </Carousel>
      </section>

      {/* Destination Info */}
      <section className="py-12 md:py-16">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {/* Main Content */}
            <div className="lg:col-span-2">
              <div className="flex items-center gap-2 text-muted-foreground mb-4">
                <MapPin className="h-5 w-5" />
                <span className="text-lg">{destination.country}</span>
                {destination.region && <span>• {destination.region}</span>}
              </div>

              <h1 className="font-playfair text-4xl sm:text-5xl font-bold mb-6">{destination.name}</h1>

              <p className="text-lg text-muted-foreground mb-8">{destination.short_desc}</p>

              {/* Highlights */}
              {destination.highlights && destination.highlights.length > 0 && (
                <div className="mb-8">
                  <h3 className="font-semibold text-lg mb-4">Highlights</h3>
                  <div className="grid grid-cols-2 gap-3">
                    {destination.highlights.map((highlight, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <Check className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                        <span>{highlight}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Long Description */}
              <div className="prose max-w-none">
                <h3 className="font-semibold text-xl mb-4">About This Destination</h3>
                <p className="text-muted-foreground leading-relaxed">{destination.long_desc}</p>
              </div>
            </div>

            {/* Sidebar - Booking Card */}
            <div className="lg:col-span-1">
              <Card className="p-6 sticky top-24" data-testid="booking-card">
                <div className="mb-6">
                  <p className="text-sm text-muted-foreground mb-1">Starting from</p>
                  <p className="text-3xl font-bold text-primary" data-testid="price-from">
                    {destination.price_from.toLocaleString()} {destination.currency}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">per person</p>
                </div>

                <div className="space-y-3 mb-6">
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-sm text-muted-foreground">Price Range</span>
                    <span className="text-sm font-medium">
                      {destination.price_from.toLocaleString()} - {destination.price_to.toLocaleString()} {destination.currency}
                    </span>
                  </div>
                </div>

                <Link to="/contact" state={{ destination: destination.name }}>
                  <Button className="w-full bg-primary hover:bg-primary/90 mb-3" size="lg" data-testid="inquiry-button">
                    Start Inquiry
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>

                <a href="tel:+46812345678">
                  <Button variant="outline" className="w-full" size="lg" data-testid="call-button">
                    Call +46 8 123 456 78
                  </Button>
                </a>

                <div className="mt-6 pt-6 border-t">
                  <p className="text-sm text-muted-foreground text-center">
                    Protected by travel insurance
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-secondary/30">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-playfair text-3xl font-bold mb-4">Ready to Explore {destination.name}?</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Get in touch and we'll create the perfect golf package for you
          </p>
          <Link to="/destinations">
            <Button variant="outline" size="lg" data-testid="view-more-button">
              View More Destinations
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
