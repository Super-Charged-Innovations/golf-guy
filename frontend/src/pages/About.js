import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Shield, Award, Users, Heart, Plane, ArrowRight } from 'lucide-react';

export default function About() {
  return (
    <div>
      {/* Hero Header */}
      <section className="bg-gradient-to-br from-primary/10 via-sky-mist to-sand/30 py-16 md:py-24">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4">About Golf Guy</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Creating unforgettable golf experiences since 2010
          </p>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-16 md:py-24">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-6">Our Story</h2>
              <div className="space-y-4 text-muted-foreground leading-relaxed">
                <p>
                  Golf Guy was founded in 2010 with a simple mission: to create exceptional golf travel experiences 
                  that combine world-class courses with unforgettable destinations.
                </p>
                <p>
                  Over the past 15 years, we've grown from a small team of golf enthusiasts to Sweden's leading 
                  golf travel specialist, helping over 10,000 golfers discover their perfect golf getaway.
                </p>
                <p>
                  We work directly with over 1,000 golf courses and 350 resorts worldwide, ensuring our clients 
                  get the best rates, tee times, and accommodations. Our partnership with Eastern DGolf provides 
                  comprehensive travel insurance and guarantees for complete peace of mind.
                </p>
              </div>
            </div>
            <div>
              <img 
                src="https://images.unsplash.com/photo-1683836018144-6e5f398102de?w=800" 
                alt="Golf course"
                className="rounded-lg shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-16 md:py-24 bg-secondary/30">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-playfair text-3xl sm:text-4xl font-bold text-center mb-12">Why Choose Golf Guy</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                <Shield className="h-12 w-12 text-primary" />
              </div>
              <h3 className="font-semibold text-xl mb-3">Travel Protection</h3>
              <p className="text-muted-foreground">
                All trips protected by Eastern DGolf insurance and guarantee for complete peace of mind
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                <Award className="h-12 w-12 text-primary" />
              </div>
              <h3 className="font-semibold text-xl mb-3">Expert Knowledge</h3>
              <p className="text-muted-foreground">
                15+ years of experience creating golf holidays with deep destination knowledge
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                <Users className="h-12 w-12 text-primary" />
              </div>
              <h3 className="font-semibold text-xl mb-3">10,000+ Happy Golfers</h3>
              <p className="text-muted-foreground">
                Join thousands of satisfied travelers who've trusted us with their golf vacations
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                <Plane className="h-12 w-12 text-primary" />
              </div>
              <h3 className="font-semibold text-xl mb-3">Tailored Packages</h3>
              <p className="text-muted-foreground">
                Custom itineraries designed around your preferences, budget, and playing ability
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                <Heart className="h-12 w-12 text-primary" />
              </div>
              <h3 className="font-semibold text-xl mb-3">Personal Service</h3>
              <p className="text-muted-foreground">
                Dedicated travel specialists available throughout your journey for support
              </p>
            </Card>

            <Card className="p-6 text-center">
              <div className="flex justify-center mb-4">
                <Award className="h-12 w-12 text-primary" />
              </div>
              <h3 className="font-semibold text-xl mb-3">Best Price Guarantee</h3>
              <p className="text-muted-foreground">
                Direct partnerships with courses and resorts ensure competitive rates
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 md:py-24">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-4">Ready to Plan Your Golf Trip?</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Let our experts create the perfect golf package for you
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/contact">
              <Button size="lg" className="bg-primary hover:bg-primary/90">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link to="/destinations">
              <Button size="lg" variant="outline">
                Explore Destinations
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
