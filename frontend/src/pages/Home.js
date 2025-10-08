import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '../components/ui/carousel';
import { AspectRatio } from '../components/ui/aspect-ratio';
import AIChatWidget from '../components/AIChatWidget';
import { RecommendationsButton } from '../components/RecommendationsButton';
import { Star, ArrowRight, Shield, Award, Users, Sparkles } from 'lucide-react';
import { useScrollAnimation } from '../hooks/useScrollAnimation';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Home() {
  const [heroSlides, setHeroSlides] = useState([]);
  const [featuredDestinations, setFeaturedDestinations] = useState([]);
  const [featuredArticles, setFeaturedArticles] = useState([]);
  const [partners, setPartners] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [instagram, setInstagram] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHomeData();
  }, []);

  const loadHomeData = async () => {
    try {
      const [heroRes, destRes, articlesRes, partnersRes, testimonialsRes, instagramRes] = await Promise.all([
        axios.get(`${API}/hero`),
        axios.get(`${API}/destinations?featured=true&published=true`),
        axios.get(`${API}/articles?featured=true&published=true`),
        axios.get(`${API}/partners?active=true`),
        axios.get(`${API}/testimonials?published=true`),
        axios.get(`${API}/instagram/latest`)
      ]);

      setHeroSlides(heroRes.data);
      setFeaturedDestinations(destRes.data.slice(0, 4));
      setFeaturedArticles(articlesRes.data.slice(0, 3));
      setPartners(partnersRes.data);
      setTestimonials(testimonialsRes.data.slice(0, 3));
      setInstagram(instagramRes.data);
    } catch (error) {
      console.error('Error loading home data:', error);
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

  return (
    <div>
      {/* AI Chat Widget */}
      <AIChatWidget />
      
      {/* Hero Carousel */}
      <section className="relative" data-testid="hero-section">
        <Carousel className="w-full" data-testid="hero-carousel">
          <CarouselContent>
            {heroSlides.map((slide) => (
              <CarouselItem key={slide.id}>
                <div className="relative h-[60vh] md:h-[70vh]">
                  <div className="absolute inset-0 bg-gradient-to-r from-black/50 to-black/20 z-10" />
                  <img 
                    src={slide.image} 
                    alt={slide.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 z-20 flex items-center">
                    <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 w-full">
                      <div className="max-w-2xl text-white">
                        {slide.kicker && (
                          <p className="uppercase tracking-[0.2em] text-xs mb-2 text-accent">{slide.kicker}</p>
                        )}
                        <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4">
                          {slide.title}
                        </h1>
                        <p className="text-lg sm:text-xl mb-6 text-white/90">{slide.subtitle}</p>
                        <div className="flex flex-wrap gap-3">
                          <Link to={slide.cta_url}>
                            <Button 
                              size="lg" 
                              className="bg-primary hover:bg-primary/90 text-white"
                              data-testid="hero-cta-button"
                            >
                              {slide.cta_text}
                              <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                          </Link>
                          <div className="flex gap-3">
                            <Link to="/destinations">
                              <Button size="lg" variant="outline" className="bg-white hover:bg-white/90 text-primary border-white">
                                View All Destinations
                              </Button>
                            </Link>
                            <RecommendationsButton />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselPrevious className="left-4" data-testid="hero-prev-button" />
          <CarouselNext className="right-4" data-testid="hero-next-button" />
        </Carousel>
      </section>

      {/* Trust Bar */}
      <section className="bg-primary/5 py-8 border-b">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div className="flex flex-col items-center" data-testid="trust-item-1">
              <Shield className="h-12 w-12 text-primary mb-3" />
              <h3 className="font-semibold mb-1">Travel Guarantee</h3>
              <p className="text-sm text-muted-foreground">Protected by Eastern DGolf insurance</p>
            </div>
            <div className="flex flex-col items-center" data-testid="trust-item-2">
              <Award className="h-12 w-12 text-primary mb-3" />
              <h3 className="font-semibold mb-1">Expert Service</h3>
              <p className="text-sm text-muted-foreground">15+ years creating golf experiences</p>
            </div>
            <div className="flex flex-col items-center" data-testid="trust-item-3">
              <Users className="h-12 w-12 text-primary mb-3" />
              <h3 className="font-semibold mb-1">10,000+ Happy Golfers</h3>
              <p className="text-sm text-muted-foreground">Join thousands of satisfied travelers</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Destinations */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-4">Featured Destinations</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Discover our handpicked selection of the world's finest golf destinations
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredDestinations.map((dest) => (
              <Card key={dest.id} className="group overflow-hidden hover:shadow-lg transition-all duration-200" data-testid="destination-card">
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
                  <div className="p-4">
                    <h3 className="font-playfair text-lg font-semibold mb-1">{dest.name}</h3>
                    <p className="text-sm text-muted-foreground mb-3">{dest.country}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">
                        from <span className="font-semibold text-primary">{dest.price_from.toLocaleString()} SEK</span>
                      </span>
                      <Button size="sm" variant="ghost" data-testid="destination-view-button">
                        View <ArrowRight className="ml-1 h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </Link>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/destinations">
              <Button size="lg" variant="outline" data-testid="view-all-destinations-button">
                View All Destinations
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Articles */}
      <section className="py-16 md:py-24 bg-secondary/30">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-4">Latest Travel Reports</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Read about real golf experiences from our travelers
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {featuredArticles.map((article) => (
              <Card key={article.id} className="overflow-hidden hover:shadow-lg transition-shadow" data-testid="article-card">
                <Link to={`/articles/${article.slug}`}>
                  <AspectRatio ratio={16/9}>
                    <img 
                      src={article.image} 
                      alt={article.title}
                      className="w-full h-full object-cover"
                    />
                  </AspectRatio>
                  <div className="p-6">
                    {article.category && (
                      <Badge variant="outline" className="mb-3">{article.category}</Badge>
                    )}
                    <h3 className="font-playfair text-xl font-semibold mb-2">{article.title}</h3>
                    <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{article.excerpt}</p>
                    <Button variant="ghost" size="sm" data-testid="article-read-button">
                      Read More <ArrowRight className="ml-1 h-3 w-3" />
                    </Button>
                  </div>
                </Link>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/articles">
              <Button size="lg" variant="outline" data-testid="view-all-articles-button">
                View All Articles
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      {testimonials.length > 0 && (
        <section className="py-16 md:py-24 bg-white">
          <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-4">What Our Golfers Say</h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Real experiences from real travelers
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {testimonials.map((testimonial) => (
                <Card key={testimonial.id} className="p-6" data-testid="testimonial-card">
                  <div className="flex gap-1 mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`h-4 w-4 ${i < testimonial.rating ? 'fill-accent text-accent' : 'text-muted'}`}
                      />
                    ))}
                  </div>
                  <p className="font-playfair text-lg mb-4 italic">"{testimonial.content}"</p>
                  <div>
                    <p className="font-semibold">{testimonial.name}</p>
                    {testimonial.trip_date && (
                      <p className="text-sm text-muted-foreground">{testimonial.trip_date}</p>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Partners */}
      {partners.length > 0 && (
        <section className="py-12 border-t bg-secondary/20" data-testid="partners-section">
          <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
            <h3 className="text-center text-sm uppercase tracking-wider text-muted-foreground mb-8">Our Partners</h3>
            <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12">
              {partners.map((partner) => (
                <div key={partner.id} className="grayscale hover:grayscale-0 opacity-60 hover:opacity-100 transition-all">
                  <img 
                    src={partner.logo} 
                    alt={partner.name}
                    className="h-12 w-auto"
                  />
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-16 md:py-24 bg-gradient-to-br from-primary/10 via-sky-mist to-sand/30">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-4">Ready to Start Your Golf Journey?</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Tell us about your dream golf trip and we'll create a custom package just for you
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/contact">
              <Button size="lg" className="bg-primary hover:bg-primary/90" data-testid="cta-contact-button">
                Get Custom Quote
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <a href="tel:+46812345678">
              <Button size="lg" variant="outline" data-testid="cta-phone-button">
                Call +46 8 123 456 78
              </Button>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
