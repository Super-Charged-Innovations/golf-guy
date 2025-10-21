import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { Mail, Phone, MapPin, Send, Users, Award, Plane, Shield } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Contact() {
  const location = useLocation();
  const [destinations, setDestinations] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    destination_id: '',
    destination_name: '',
    dates: '',
    group_size: '',
    budget: '',
    message: ''
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadDestinations();
    
    // Pre-fill destination if passed from detail page
    if (location.state?.destination) {
      setFormData(prev => ({
        ...prev,
        destination_name: location.state.destination
      }));
    }
  }, [location]);

  const loadDestinations = async () => {
    try {
      const response = await axios.get(`${API}/destinations?published=true`);
      setDestinations(response.data);
    } catch (error) {
      console.error('Error loading destinations:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleDestinationChange = (value) => {
    const dest = destinations.find(d => d.id === value);
    setFormData(prev => ({
      ...prev,
      destination_id: value,
      destination_name: dest ? dest.name : ''
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.name || !formData.email) {
      toast.error('Please fill in all required fields');
      return;
    }

    setSubmitting(true);
    try {
      await axios.post(`${API}/inquiries`, formData);
      toast.success('Inquiry sent successfully! We\'ll get back to you soon.');
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        destination_id: '',
        destination_name: '',
        dates: '',
        group_size: '',
        budget: '',
        message: ''
      });
    } catch (error) {
      console.error('Error submitting inquiry:', error);
      toast.error('Failed to send inquiry. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      {/* Hero Header */}
      <section className="bg-gradient-to-br from-emerald-50 via-emerald-100/30 to-white py-12 md:py-16">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4">Contact Us</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We're happy to help you with your next golf trip
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-16 md:py-20">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {/* Contact Info */}
            <div className="lg:col-span-1 space-y-8">
              <div>
                <h2 className="font-playfair text-2xl font-bold mb-6">Contact Information</h2>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <Mail className="h-5 w-5 text-emerald-600 mt-1" />
                    <div>
                      <p className="font-medium">Email</p>
                      <a href="mailto:info@dgolf.se" className="text-muted-foreground hover:text-emerald-600 transition-colors">
                        info@dgolf.se
                      </a>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <svg className="h-5 w-5 text-emerald-600 mt-1" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                    </svg>
                    <div>
                      <p className="font-medium">Instagram</p>
                      <a href="https://instagram.com/dgolfswe" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-emerald-600 transition-colors">
                        @dgolfswe
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              {/* Why Choose DGolf */}
              <div className="pt-8 border-t">
                <h3 className="font-semibold text-lg mb-4">Why Choose DGolf?</h3>
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center">
                      <Users className="h-4 w-4 text-emerald-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Personal Service</p>
                      <p className="text-xs text-muted-foreground">We have handpicked what we consider the best options and presented them on our website. We can provide accurate answers directly as we have experienced these destinations ourselves.</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center">
                      <Award className="h-4 w-4 text-emerald-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Expert Knowledge</p>
                      <p className="text-xs text-muted-foreground">Over 40 years of combined experience and 350+ courses played worldwide.</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center">
                      <Plane className="h-4 w-4 text-emerald-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Flexibility</p>
                      <p className="text-xs text-muted-foreground">Trips with or without flights, flexible trip duration, and transfer solutions.</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center">
                      <Shield className="h-4 w-4 text-emerald-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">Peace of Mind</p>
                      <p className="text-xs text-muted-foreground">Travel guarantee and support throughout your entire journey.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <div className="lg:col-span-2">
              <Card className="p-8">
                <h2 className="font-playfair text-2xl font-bold mb-6">Send Us an Inquiry</h2>
                <form onSubmit={handleSubmit} className="space-y-6" data-testid="contact-form">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="name">Name *</Label>
                      <Input
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        required
                        data-testid="name-input"
                        placeholder="Your name"
                      />
                    </div>
                    <div>
                      <Label htmlFor="email">Email *</Label>
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        data-testid="email-input"
                        placeholder="your@email.com"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="phone">Phone</Label>
                      <Input
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        data-testid="phone-input"
                        placeholder="+46..."
                      />
                    </div>
                    <div>
                      <Label htmlFor="destination">Destination</Label>
                      <Select 
                        value={formData.destination_id} 
                        onValueChange={handleDestinationChange}
                      >
                        <SelectTrigger data-testid="destination-select">
                          <SelectValue placeholder="Select a destination" />
                        </SelectTrigger>
                        <SelectContent>
                          {destinations.map(dest => (
                            <SelectItem key={dest.id} value={dest.id}>{dest.name}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <Label htmlFor="dates">Travel Dates</Label>
                      <Input
                        id="dates"
                        name="dates"
                        value={formData.dates}
                        onChange={handleChange}
                        data-testid="dates-input"
                        placeholder="e.g., March 2025"
                      />
                    </div>
                    <div>
                      <Label htmlFor="group_size">Group Size</Label>
                      <Input
                        id="group_size"
                        name="group_size"
                        type="number"
                        value={formData.group_size}
                        onChange={handleChange}
                        data-testid="group-size-input"
                        placeholder="Number of golfers"
                      />
                    </div>
                    <div>
                      <Label htmlFor="budget">Budget (SEK)</Label>
                      <Input
                        id="budget"
                        name="budget"
                        value={formData.budget}
                        onChange={handleChange}
                        data-testid="budget-input"
                        placeholder="e.g., 15000-20000"
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="message">Message</Label>
                    <Textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      rows={5}
                      data-testid="message-textarea"
                      placeholder="Tell us more about your ideal golf trip..."
                    />
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full bg-primary hover:bg-primary/90" 
                    size="lg"
                    disabled={submitting}
                    data-testid="submit-button"
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
                </form>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
