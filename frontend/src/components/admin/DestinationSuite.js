import React, { useState } from 'react';
import axios from 'axios';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '../ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Badge } from '../ui/badge';
import { Card } from '../ui/card';
import { Switch } from '../ui/switch';
import { toast } from 'sonner';
import { Plus, X, Save, Trash2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const DestinationFormDialog = ({ open, onOpenChange, destination, onSave }) => {
  const isEdit = !!destination;
  
  // Basic Info State
  const [formData, setFormData] = useState(destination || {
    name: '',
    slug: '',
    country: '',
    region: '',
    short_desc: '',
    long_desc: '',
    destination_type: 'golf_course',
    price_from: 0,
    price_to: 0,
    currency: 'SEK',
    images: [],
    video_url: '',
    highlights: [],
    courses: [],
    amenities: {
      spa: false,
      restaurants: 0,
      pools: 0,
      gym: false,
      kids_club: false,
      conference_facilities: false,
      beach_access: false,
      additional: []
    },
    packages: [],
    climate: '',
    best_time_to_visit: '',
    nearest_airport: '',
    transfer_time: '',
    featured: false,
    published: true,
    seo: { title: '', description: '', canonical: '' }
  });

  // Temporary states for adding items
  const [newImage, setNewImage] = useState('');
  const [newHighlight, setNewHighlight] = useState('');
  const [newAmenity, setNewAmenity] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNestedChange = (parent, field, value) => {
    setFormData(prev => ({
      ...prev,
      [parent]: { ...prev[parent], [field]: value }
    }));
  };

  const addImage = () => {
    if (newImage.trim()) {
      setFormData(prev => ({
        ...prev,
        images: [...prev.images, newImage.trim()]
      }));
      setNewImage('');
    }
  };

  const removeImage = (index) => {
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index)
    }));
  };

  const addHighlight = () => {
    if (newHighlight.trim()) {
      setFormData(prev => ({
        ...prev,
        highlights: [...prev.highlights, newHighlight.trim()]
      }));
      setNewHighlight('');
    }
  };

  const removeHighlight = (index) => {
    setFormData(prev => ({
      ...prev,
      highlights: prev.highlights.filter((_, i) => i !== index)
    }));
  };

  const addAmenity = () => {
    if (newAmenity.trim()) {
      setFormData(prev => ({
        ...prev,
        amenities: {
          ...prev.amenities,
          additional: [...prev.amenities.additional, newAmenity.trim()]
        }
      }));
      setNewAmenity('');
    }
  };

  const removeAmenity = (index) => {
    setFormData(prev => ({
      ...prev,
      amenities: {
        ...prev.amenities,
        additional: prev.amenities.additional.filter((_, i) => i !== index)
      }
    }));
  };

  // Generate slug from name
  const generateSlug = () => {
    const slug = formData.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
    handleChange('slug', slug);
  };

  const handleSubmit = async () => {
    // Validation
    if (!formData.name || !formData.slug || !formData.country) {
      toast.error('Please fill in all required fields (Name, Slug, Country)');
      return;
    }

    setSubmitting(true);
    try {
      if (isEdit) {
        await axios.put(`${API}/destinations/${destination.id}`, formData);
        toast.success('Destination updated successfully!');
      } else {
        await axios.post(`${API}/destinations`, formData);
        toast.success('Destination created successfully!');
      }
      onSave();
      onOpenChange(false);
    } catch (error) {
      console.error('Error saving destination:', error);
      toast.error('Failed to save destination. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-playfair">
            {isEdit ? 'Edit Destination' : 'Create New Destination'}
          </DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="basic" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="basic">Basic Info</TabsTrigger>
            <TabsTrigger value="media">Media</TabsTrigger>
            <TabsTrigger value="courses">Courses</TabsTrigger>
            <TabsTrigger value="amenities">Amenities</TabsTrigger>
            <TabsTrigger value="packages">Packages</TabsTrigger>
          </TabsList>

          {/* Basic Info Tab */}
          <TabsContent value="basic" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <Label htmlFor="name">Destination Name *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => handleChange('name', e.target.value)}
                  placeholder="e.g., Costa del Sol Golf Collection"
                  data-testid="dest-name-input"
                />
              </div>

              <div>
                <Label htmlFor="slug">URL Slug *</Label>
                <div className="flex gap-2">
                  <Input
                    id="slug"
                    value={formData.slug}
                    onChange={(e) => handleChange('slug', e.target.value)}
                    placeholder="costa-del-sol"
                    data-testid="dest-slug-input"
                  />
                  <Button type="button" variant="outline" size="sm" onClick={generateSlug}>
                    Generate
                  </Button>
                </div>
              </div>

              <div>
                <Label htmlFor="destination_type">Type *</Label>
                <Select value={formData.destination_type} onValueChange={(val) => handleChange('destination_type', val)}>
                  <SelectTrigger data-testid="dest-type-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="golf_course">Golf Course Only</SelectItem>
                    <SelectItem value="golf_resort">Golf Resort</SelectItem>
                    <SelectItem value="both">Course & Resort</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="country">Country *</Label>
                <Input
                  id="country"
                  value={formData.country}
                  onChange={(e) => handleChange('country', e.target.value)}
                  placeholder="Spain"
                  data-testid="dest-country-input"
                />
              </div>

              <div>
                <Label htmlFor="region">Region</Label>
                <Input
                  id="region"
                  value={formData.region}
                  onChange={(e) => handleChange('region', e.target.value)}
                  placeholder="Andalusia"
                />
              </div>

              <div className="col-span-2">
                <Label htmlFor="short_desc">Short Description *</Label>
                <Textarea
                  id="short_desc"
                  value={formData.short_desc}
                  onChange={(e) => handleChange('short_desc', e.target.value)}
                  rows={2}
                  placeholder="Brief description for listing pages..."
                />
              </div>

              <div className="col-span-2">
                <Label htmlFor="long_desc">Full Description *</Label>
                <Textarea
                  id="long_desc"
                  value={formData.long_desc}
                  onChange={(e) => handleChange('long_desc', e.target.value)}
                  rows={4}
                  placeholder="Detailed description for destination page..."
                />
              </div>

              <div>
                <Label htmlFor="price_from">Price From (SEK) *</Label>
                <Input
                  id="price_from"
                  type="number"
                  value={formData.price_from}
                  onChange={(e) => handleChange('price_from', parseInt(e.target.value) || 0)}
                  data-testid="dest-price-from-input"
                />
              </div>

              <div>
                <Label htmlFor="price_to">Price To (SEK) *</Label>
                <Input
                  id="price_to"
                  type="number"
                  value={formData.price_to}
                  onChange={(e) => handleChange('price_to', parseInt(e.target.value) || 0)}
                />
              </div>

              <div>
                <Label htmlFor="climate">Climate</Label>
                <Input
                  id="climate"
                  value={formData.climate}
                  onChange={(e) => handleChange('climate', e.target.value)}
                  placeholder="Mediterranean, year-round sunshine"
                />
              </div>

              <div>
                <Label htmlFor="best_time">Best Time to Visit</Label>
                <Input
                  id="best_time"
                  value={formData.best_time_to_visit}
                  onChange={(e) => handleChange('best_time_to_visit', e.target.value)}
                  placeholder="March to November"
                />
              </div>

              <div>
                <Label htmlFor="airport">Nearest Airport</Label>
                <Input
                  id="airport"
                  value={formData.nearest_airport}
                  onChange={(e) => handleChange('nearest_airport', e.target.value)}
                  placeholder="Malaga Airport (AGP)"
                />
              </div>

              <div>
                <Label htmlFor="transfer">Transfer Time</Label>
                <Input
                  id="transfer"
                  value={formData.transfer_time}
                  onChange={(e) => handleChange('transfer_time', e.target.value)}
                  placeholder="45 minutes"
                />
              </div>

              <div className="flex items-center gap-2">
                <Switch
                  id="featured"
                  checked={formData.featured}
                  onCheckedChange={(checked) => handleChange('featured', checked)}
                />
                <Label htmlFor="featured">Featured Destination</Label>
              </div>

              <div className="flex items-center gap-2">
                <Switch
                  id="published"
                  checked={formData.published}
                  onCheckedChange={(checked) => handleChange('published', checked)}
                />
                <Label htmlFor="published">Published</Label>
              </div>
            </div>

            {/* Highlights */}
            <div>
              <Label>Highlights</Label>
              <div className="flex gap-2 mb-2">
                <Input
                  value={newHighlight}
                  onChange={(e) => setNewHighlight(e.target.value)}
                  placeholder="Add a highlight..."
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addHighlight())}
                />
                <Button type="button" onClick={addHighlight} size="sm">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex flex-wrap gap-2">
                {formData.highlights.map((highlight, idx) => (
                  <Badge key={idx} variant="secondary" className="gap-1">
                    {highlight}
                    <X className="h-3 w-3 cursor-pointer" onClick={() => removeHighlight(idx)} />
                  </Badge>
                ))}
              </div>
            </div>
          </TabsContent>

          {/* Media Tab */}
          <TabsContent value="media" className="space-y-4">
            <div>
              <Label>Images (URLs)</Label>
              <div className="flex gap-2 mb-2">
                <Input
                  value={newImage}
                  onChange={(e) => setNewImage(e.target.value)}
                  placeholder="https://example.com/image.jpg"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addImage())}
                  data-testid="image-url-input"
                />
                <Button type="button" onClick={addImage} size="sm">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <div className="grid grid-cols-3 gap-4">
                {formData.images.map((img, idx) => (
                  <Card key={idx} className="relative group">
                    <img src={img} alt={`Preview ${idx + 1}`} className="w-full h-32 object-cover rounded" />
                    <Button
                      type="button"
                      variant="destructive"
                      size="sm"
                      className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                      onClick={() => removeImage(idx)}
                    >
                      <X className="h-3 w-3" />
                    </Button>
                  </Card>
                ))}
              </div>
            </div>

            <div>
              <Label htmlFor="video_url">Video URL (YouTube, Vimeo)</Label>
              <Input
                id="video_url"
                value={formData.video_url}
                onChange={(e) => handleChange('video_url', e.target.value)}
                placeholder="https://youtube.com/watch?v=..."
              />
            </div>
          </TabsContent>

          {/* Courses Tab */}
          <TabsContent value="courses" className="space-y-4">
            <div className="flex justify-between items-center mb-4">
              <Label className="text-lg">Golf Courses</Label>
              <Button
                type="button"
                size="sm"
                onClick={() => {
                  setFormData(prev => ({
                    ...prev,
                    courses: [...prev.courses, { par: 72, holes: 18, length_meters: 6000, difficulty: 'Medium', designer: '', year_established: null, course_type: 'Parkland' }]
                  }));
                }}
                data-testid="add-course-button"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add Course
              </Button>
            </div>

            {formData.courses.map((course, idx) => (
              <Card key={idx} className="p-4">
                <div className="flex justify-between items-center mb-3">
                  <h4 className="font-semibold">Course {idx + 1}</h4>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setFormData(prev => ({
                        ...prev,
                        courses: prev.courses.filter((_, i) => i !== idx)
                      }));
                    }}
                  >
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <Label>Holes</Label>
                    <Input
                      type="number"
                      value={course.holes || ''}
                      onChange={(e) => {
                        const updated = [...formData.courses];
                        updated[idx].holes = parseInt(e.target.value) || null;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                    />
                  </div>
                  <div>
                    <Label>Par</Label>
                    <Input
                      type="number"
                      value={course.par || ''}
                      onChange={(e) => {
                        const updated = [...formData.courses];
                        updated[idx].par = parseInt(e.target.value) || null;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                    />
                  </div>
                  <div>
                    <Label>Length (meters)</Label>
                    <Input
                      type="number"
                      value={course.length_meters || ''}
                      onChange={(e) => {
                        const updated = [...formData.courses];
                        updated[idx].length_meters = parseInt(e.target.value) || null;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                    />
                  </div>
                  <div>
                    <Label>Difficulty</Label>
                    <Select
                      value={course.difficulty}
                      onValueChange={(val) => {
                        const updated = [...formData.courses];
                        updated[idx].difficulty = val;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Easy">Easy</SelectItem>
                        <SelectItem value="Medium">Medium</SelectItem>
                        <SelectItem value="Hard">Hard</SelectItem>
                        <SelectItem value="Championship">Championship</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Course Type</Label>
                    <Select
                      value={course.course_type}
                      onValueChange={(val) => {
                        const updated = [...formData.courses];
                        updated[idx].course_type = val;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Links">Links</SelectItem>
                        <SelectItem value="Parkland">Parkland</SelectItem>
                        <SelectItem value="Desert">Desert</SelectItem>
                        <SelectItem value="Mountain">Mountain</SelectItem>
                        <SelectItem value="Coastal">Coastal</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Year Established</Label>
                    <Input
                      type="number"
                      value={course.year_established || ''}
                      onChange={(e) => {
                        const updated = [...formData.courses];
                        updated[idx].year_established = parseInt(e.target.value) || null;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                    />
                  </div>
                  <div className="col-span-3">
                    <Label>Designer</Label>
                    <Input
                      value={course.designer || ''}
                      onChange={(e) => {
                        const updated = [...formData.courses];
                        updated[idx].designer = e.target.value;
                        setFormData(prev => ({ ...prev, courses: updated }));
                      }}
                      placeholder="e.g., Robert Trent Jones"
                    />
                  </div>
                </div>
              </Card>
            ))}

            {formData.courses.length === 0 && (
              <div className="text-center py-8 text-muted-foreground">
                No courses added yet. Click "Add Course" to get started.
              </div>
            )}
          </TabsContent>

          {/* Amenities Tab */}
          <TabsContent value="amenities" className="space-y-4">
            <Label className="text-lg">Resort Amenities</Label>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center gap-2">
                <Switch
                  id="spa"
                  checked={formData.amenities.spa}
                  onCheckedChange={(checked) => handleNestedChange('amenities', 'spa', checked)}
                />
                <Label htmlFor="spa">Spa & Wellness</Label>
              </div>

              <div className="flex items-center gap-2">
                <Switch
                  id="gym"
                  checked={formData.amenities.gym}
                  onCheckedChange={(checked) => handleNestedChange('amenities', 'gym', checked)}
                />
                <Label htmlFor="gym">Gym / Fitness Center</Label>
              </div>

              <div className="flex items-center gap-2">
                <Switch
                  id="kids_club"
                  checked={formData.amenities.kids_club}
                  onCheckedChange={(checked) => handleNestedChange('amenities', 'kids_club', checked)}
                />
                <Label htmlFor="kids_club">Kids Club</Label>
              </div>

              <div className="flex items-center gap-2">
                <Switch
                  id="conference"
                  checked={formData.amenities.conference_facilities}
                  onCheckedChange={(checked) => handleNestedChange('amenities', 'conference_facilities', checked)}
                />
                <Label htmlFor="conference">Conference Facilities</Label>
              </div>

              <div className="flex items-center gap-2">
                <Switch
                  id="beach"
                  checked={formData.amenities.beach_access}
                  onCheckedChange={(checked) => handleNestedChange('amenities', 'beach_access', checked)}
                />
                <Label htmlFor="beach">Beach Access</Label>
              </div>

              <div>
                <Label htmlFor="restaurants">Number of Restaurants</Label>
                <Input
                  id="restaurants"
                  type="number"
                  value={formData.amenities.restaurants}
                  onChange={(e) => handleNestedChange('amenities', 'restaurants', parseInt(e.target.value) || 0)}
                />
              </div>

              <div>
                <Label htmlFor="pools">Number of Pools</Label>
                <Input
                  id="pools"
                  type="number"
                  value={formData.amenities.pools}
                  onChange={(e) => handleNestedChange('amenities', 'pools', parseInt(e.target.value) || 0)}
                />
              </div>
            </div>

            <div>
              <Label>Additional Amenities</Label>
              <div className="flex gap-2 mb-2">
                <Input
                  value={newAmenity}
                  onChange={(e) => setNewAmenity(e.target.value)}
                  placeholder="e.g., Tennis courts, Concierge service..."
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addAmenity())}
                />
                <Button type="button" onClick={addAmenity} size="sm">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex flex-wrap gap-2">
                {formData.amenities.additional.map((amenity, idx) => (
                  <Badge key={idx} variant="secondary" className="gap-1">
                    {amenity}
                    <X className="h-3 w-3 cursor-pointer" onClick={() => removeAmenity(idx)} />
                  </Badge>
                ))}
              </div>
            </div>
          </TabsContent>

          {/* Packages Tab - Placeholder for now */}
          <TabsContent value="packages" className="space-y-4">
            <div className="text-center py-8 text-muted-foreground">
              <p className="mb-2">Package management coming soon!</p>
              <p className="text-sm">For now, packages can be managed through the price range fields in Basic Info.</p>
            </div>
          </TabsContent>
        </Tabs>

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={submitting}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={submitting} data-testid="save-destination-button">
            {submitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Saving...
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                {isEdit ? 'Update' : 'Create'} Destination
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default DestinationFormDialog;
