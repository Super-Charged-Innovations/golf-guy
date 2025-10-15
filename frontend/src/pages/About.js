import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Shield, Award, Users, Heart, Plane, ArrowRight } from 'lucide-react';

export default function About() {
  return (
    <div>
      {/* Hero Header */}
      <section className="bg-gradient-to-br from-emerald-50 via-emerald-100/30 to-white py-12 md:py-16">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4">About DGolf</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Your partner for unforgettable golf experiences around the world
          </p>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-16 md:py-20">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="font-playfair text-3xl sm:text-4xl font-bold mb-6">Our Expertise</h2>
              <div className="space-y-4 text-muted-foreground leading-relaxed">
                <p>
                  At DGolf, we have played over 350 golf courses worldwide and stayed at more than 150 different facilities around the globe. We offer you tailor-made trips where we strive to fulfill all your wishes to make your trip the best you've ever experienced.
                </p>
                <p>
                  We always provide flexible trip durations and even trips where we only arrange the golf and transfers. We also organize activities that extend beyond the golf course, including restaurant bookings, wine tastings, and other exciting combinations if you wish.
                </p>
                <p>
                  The advantage with us is that we have seen an enormous amount of products available on the market and can therefore advise you in a credible way when it comes to finding the right product for you and your fellow travelers.
                </p>
                <p>
                  Let DGolf calculate your next trip - we arrange your journey both with and without flights at great prices.
                </p>
              </div>
            </div>
            <div>
              <img 
                src="https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800" 
                alt="Golf course aerial view"
                className="rounded-lg shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-emerald-50">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl sm:text-5xl font-bold text-emerald-700 mb-2">350+</div>
              <div className="text-sm text-muted-foreground">Courses Played</div>
            </div>
            <div>
              <div className="text-4xl sm:text-5xl font-bold text-emerald-700 mb-2">150+</div>
              <div className="text-sm text-muted-foreground">Resorts Visited</div>
            </div>
            <div>
              <div className="text-4xl sm:text-5xl font-bold text-emerald-700 mb-2">40+</div>
              <div className="text-sm text-muted-foreground">Years Combined Experience</div>
            </div>
            <div>
              <div className="text-4xl sm:text-5xl font-bold text-emerald-700 mb-2">24/7</div>
              <div className="text-sm text-muted-foreground">Support During Travel</div>
            </div>
          </div>
        </div>
      </section>

      {/* Travel Guarantee */}
      <section className="py-16 md:py-20">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-emerald-600 to-emerald-800 rounded-2xl p-8 md:p-12 text-white">
            <div className="flex items-start gap-6">
              <Shield className="h-16 w-16 flex-shrink-0" />
              <div>
                <h2 className="font-playfair text-2xl sm:text-3xl font-bold mb-4">Travel Protection & Peace of Mind</h2>
                <p className="text-emerald-50 leading-relaxed mb-4">
                  For your extra peace of mind during your trip, we have had a partnership with Eastongolf for several years. They provide travel guarantees for all DGolf trips and handle all administration related to your upcoming golf trip in collaboration with us.
                </p>
                <p className="text-emerald-50">
                  This means you can travel with complete confidence, knowing that you're protected and supported every step of the way.
                </p>
              </div>
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
