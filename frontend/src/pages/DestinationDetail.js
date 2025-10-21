import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '../components/ui/carousel';
import { MapPin, ArrowRight, Check, Send } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function DestinationDetail() {
  const { slug } = useParams();
  const [destination, setDestination] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showInquiryDialog, setShowInquiryDialog] = useState(false);
  const [inquiryForm, setInquiryForm] = useState({
    name: '',
    email: '',
    phone: '',
    dates: '',
    group_size: '',
    budget: '',
    message: ''
  });
  const [submitting, setSubmitting] = useState(false);

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

  const handleInquiryChange = (e) => {
    const { name, value } = e.target;
    setInquiryForm(prev => ({ ...prev, [name]: value }));
  };

  const handleInquirySubmit = async (e) => {
    e.preventDefault();
    
    if (!inquiryForm.name || !inquiryForm.email) {
      toast.error('Please fill in all required fields');
      return;
    }

    setSubmitting(true);
    try {
      await axios.post(`${API}/inquiries`, {
        ...inquiryForm,
        destination_id: destination.id,
        destination_name: destination.name
      });
      
      toast.success('Inquiry sent successfully! We\'ll get back to you soon.');
      
      // Reset form and close dialog
      setInquiryForm({
        name: '',
        email: '',
        phone: '',
        dates: '',
        group_size: '',
        budget: '',
        message: ''
      });
      setShowInquiryDialog(false);
    } catch (error) {
      console.error('Error submitting inquiry:', error);
      toast.error('Failed to send inquiry. Please try again.');
    } finally {
      setSubmitting(false);
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

                <Button 
                  className="w-full bg-emerald-600 hover:bg-emerald-700 mb-3" 
                  size="lg" 
                  data-testid="inquiry-button"
                  onClick={() => setShowInquiryDialog(true)}
                >
                  Start Inquiry
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>

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

      {/* Inquiry Dialog */}
      <Dialog open={showInquiryDialog} onOpenChange={setShowInquiryDialog}>
        <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-playfair text-2xl">Inquire About {destination.name}</DialogTitle>
            <p className="text-sm text-muted-foreground">Fill out the form below and we'll get back to you shortly</p>
          </DialogHeader>

          <form onSubmit={handleInquirySubmit} className="space-y-5 py-4">
            {/* Name and Email */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="inquiry-name">Name *</Label>
                <Input
                  id="inquiry-name"
                  name="name"
                  value={inquiryForm.name}
                  onChange={handleInquiryChange}
                  required
                  placeholder="Your full name"
                />
              </div>
              <div>
                <Label htmlFor="inquiry-email">Email *</Label>
                <Input
                  id="inquiry-email"
                  name="email"
                  type="email"
                  value={inquiryForm.email}
                  onChange={handleInquiryChange}
                  required
                  placeholder="your@email.com"
                />
              </div>
            </div>

            {/* Phone */}
            <div>
              <Label htmlFor="inquiry-phone">Phone</Label>
              <Input
                id="inquiry-phone"
                name="phone"
                value={inquiryForm.phone}
                onChange={handleInquiryChange}
                placeholder="+46..."
              />
            </div>

            {/* Travel Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="inquiry-dates">Travel Dates</Label>
                <Input
                  id="inquiry-dates"
                  name="dates"
                  value={inquiryForm.dates}
                  onChange={handleInquiryChange}
                  placeholder="e.g., March 2025"
                />
              </div>
              <div>
                <Label htmlFor="inquiry-group">Group Size</Label>
                <Input
                  id="inquiry-group"
                  name="group_size"
                  type="number"
                  value={inquiryForm.group_size}
                  onChange={handleInquiryChange}
                  placeholder="Number of golfers"
                />
              </div>
              <div>
                <Label htmlFor="inquiry-budget">Budget (SEK)</Label>
                <Input
                  id="inquiry-budget"
                  name="budget"
                  value={inquiryForm.budget}
                  onChange={handleInquiryChange}
                  placeholder="e.g., 15000-20000"
                />
              </div>
            </div>

            {/* Message */}
            <div>
              <Label htmlFor="inquiry-message">Message</Label>
              <Textarea
                id="inquiry-message"
                name="message"
                value={inquiryForm.message}
                onChange={handleInquiryChange}
                rows={4}
                placeholder="Tell us more about your ideal golf trip to this destination..."
              />
            </div>

            {/* Destination Info Display */}
            <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-200">
              <p className="text-sm font-medium text-emerald-900">Selected Destination:</p>
              <p className="text-lg font-semibold text-emerald-700">{destination.name}</p>
              <p className="text-xs text-emerald-600">{destination.country} • {destination.region}</p>
            </div>

            {/* Submit Button */}
            <div className="flex gap-3 pt-4">
              <Button 
                type="button"
                variant="outline"
                onClick={() => setShowInquiryDialog(false)}
                className="flex-1"
                disabled={submitting}
              >
                Cancel
              </Button>
              <Button 
                type="submit" 
                className="flex-1 bg-emerald-600 hover:bg-emerald-700"
                disabled={submitting}
              >
                {submitting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Sending...
                  </>
                ) : (
                  <>
                    Send Inquiry
                    <Send className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
