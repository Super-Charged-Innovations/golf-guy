import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';
import DestinationFormDialog from '../components/admin/DestinationSuite';
import { 
  LayoutDashboard, 
  MapPin, 
  FileText, 
  MessageSquare, 
  Users, 
  Plus, 
  Edit, 
  Trash2,
  Download,
  Eye
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [destinations, setDestinations] = useState([]);
  const [articles, setArticles] = useState([]);
  const [inquiries, setInquiries] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [stats, setStats] = useState({ destinations: 0, articles: 0, inquiries: 0, testimonials: 0 });
  const [loading, setLoading] = useState(true);

  // Edit Dialogs
  const [editingDest, setEditingDest] = useState(null);
  const [editingArticle, setEditingArticle] = useState(null);
  const [showDestDialog, setShowDestDialog] = useState(false);
  const [showArticleDialog, setShowArticleDialog] = useState(false);

  useEffect(() => {
    const isAdmin = localStorage.getItem('demo_admin') === 'true';
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadAdminData();
  }, [navigate]);

  const loadAdminData = async () => {
    try {
      const [destRes, articlesRes, inquiriesRes, testimonialsRes] = await Promise.all([
        axios.get(`${API}/destinations`),
        axios.get(`${API}/articles`),
        axios.get(`${API}/inquiries`),
        axios.get(`${API}/testimonials`)
      ]);

      setDestinations(destRes.data);
      setArticles(articlesRes.data);
      setInquiries(inquiriesRes.data);
      setTestimonials(testimonialsRes.data);
      
      setStats({
        destinations: destRes.data.length,
        articles: articlesRes.data.length,
        inquiries: inquiriesRes.data.length,
        testimonials: testimonialsRes.data.length
      });
    } catch (error) {
      console.error('Error loading admin data:', error);
      toast.error('Failed to load admin data');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteDestination = async (id) => {
    if (!window.confirm('Are you sure you want to delete this destination?')) return;
    
    try {
      await axios.delete(`${API}/destinations/${id}`);
      toast.success('Destination deleted');
      loadAdminData();
    } catch (error) {
      toast.error('Failed to delete destination');
    }
  };

  const handleDeleteArticle = async (id) => {
    if (!window.confirm('Are you sure you want to delete this article?')) return;
    
    try {
      await axios.delete(`${API}/articles/${id}`);
      toast.success('Article deleted');
      loadAdminData();
    } catch (error) {
      toast.error('Failed to delete article');
    }
  };

  const handleUpdateInquiryStatus = async (id, newStatus) => {
    try {
      await axios.put(`${API}/inquiries/${id}`, { status: newStatus });
      toast.success('Inquiry status updated');
      loadAdminData();
    } catch (error) {
      toast.error('Failed to update inquiry');
    }
  };

  const handleExportInquiries = async () => {
    try {
      window.open(`${API}/inquiries/export/csv`, '_blank');
      toast.success('Export started');
    } catch (error) {
      toast.error('Failed to export inquiries');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-secondary/20">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-playfair text-4xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-muted-foreground">Manage your golf travel platform</p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Destinations</p>
                <p className="text-3xl font-bold" data-testid="destinations-count">{stats.destinations}</p>
              </div>
              <MapPin className="h-8 w-8 text-primary" />
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Articles</p>
                <p className="text-3xl font-bold" data-testid="articles-count">{stats.articles}</p>
              </div>
              <FileText className="h-8 w-8 text-primary" />
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Inquiries</p>
                <p className="text-3xl font-bold" data-testid="inquiries-count">{stats.inquiries}</p>
              </div>
              <MessageSquare className="h-8 w-8 text-primary" />
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Testimonials</p>
                <p className="text-3xl font-bold" data-testid="testimonials-count">{stats.testimonials}</p>
              </div>
              <Users className="h-8 w-8 text-primary" />
            </div>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Card className="p-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4 mb-6">
              <TabsTrigger value="overview" data-testid="tab-overview">
                <LayoutDashboard className="h-4 w-4 mr-2" />
                Overview
              </TabsTrigger>
              <TabsTrigger value="destinations" data-testid="tab-destinations">
                <MapPin className="h-4 w-4 mr-2" />
                Destinations
              </TabsTrigger>
              <TabsTrigger value="articles" data-testid="tab-articles">
                <FileText className="h-4 w-4 mr-2" />
                Articles
              </TabsTrigger>
              <TabsTrigger value="inquiries" data-testid="tab-inquiries">
                <MessageSquare className="h-4 w-4 mr-2" />
                Inquiries
              </TabsTrigger>
            </TabsList>

            {/* Overview Tab */}
            <TabsContent value="overview">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4">Recent Inquiries</h3>
                  <div className="space-y-3">
                    {inquiries.slice(0, 5).map(inquiry => (
                      <Card key={inquiry.id} className="p-4">
                        <div className="flex items-start justify-between">
                          <div>
                            <p className="font-medium">{inquiry.name}</p>
                            <p className="text-sm text-muted-foreground">{inquiry.email}</p>
                            {inquiry.destination_name && (
                              <p className="text-sm text-muted-foreground mt-1">
                                Destination: {inquiry.destination_name}
                              </p>
                            )}
                          </div>
                          <Badge variant={
                            inquiry.status === 'new' ? 'default' :
                            inquiry.status === 'in_progress' ? 'secondary' :
                            inquiry.status === 'responded' ? 'outline' : 'secondary'
                          }>
                            {inquiry.status}
                          </Badge>
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              </div>
            </TabsContent>

            {/* Destinations Tab */}
            <TabsContent value="destinations">
              <div className="space-y-4">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">All Destinations</h3>
                  <Button className="bg-primary" data-testid="add-destination-button">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Destination
                  </Button>
                </div>
                
                <div className="border rounded-lg">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Country</TableHead>
                        <TableHead>Price From</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {destinations.map(dest => (
                        <TableRow key={dest.id}>
                          <TableCell className="font-medium">{dest.name}</TableCell>
                          <TableCell>{dest.country}</TableCell>
                          <TableCell>{dest.price_from.toLocaleString()} {dest.currency}</TableCell>
                          <TableCell>
                            <Badge variant={dest.published ? 'default' : 'secondary'}>
                              {dest.published ? 'Published' : 'Draft'}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-right">
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => window.open(`/destinations/${dest.slug}`, '_blank')}
                              data-testid={`view-dest-${dest.id}`}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => handleDeleteDestination(dest.id)}
                              data-testid={`delete-dest-${dest.id}`}
                            >
                              <Trash2 className="h-4 w-4 text-destructive" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </TabsContent>

            {/* Articles Tab */}
            <TabsContent value="articles">
              <div className="space-y-4">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">All Articles</h3>
                  <Button className="bg-primary" data-testid="add-article-button">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Article
                  </Button>
                </div>
                
                <div className="border rounded-lg">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Title</TableHead>
                        <TableHead>Category</TableHead>
                        <TableHead>Author</TableHead>
                        <TableHead>Published</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {articles.map(article => (
                        <TableRow key={article.id}>
                          <TableCell className="font-medium">{article.title}</TableCell>
                          <TableCell>
                            {article.category && (
                              <Badge variant="outline">{article.category}</Badge>
                            )}
                          </TableCell>
                          <TableCell className="text-sm text-muted-foreground">
                            {article.author || 'N/A'}
                          </TableCell>
                          <TableCell className="text-sm">{formatDate(article.publish_date)}</TableCell>
                          <TableCell className="text-right">
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => window.open(`/articles/${article.slug}`, '_blank')}
                              data-testid={`view-article-${article.id}`}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => handleDeleteArticle(article.id)}
                              data-testid={`delete-article-${article.id}`}
                            >
                              <Trash2 className="h-4 w-4 text-destructive" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </TabsContent>

            {/* Inquiries Tab */}
            <TabsContent value="inquiries">
              <div className="space-y-4">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">All Inquiries</h3>
                  <Button 
                    variant="outline"
                    onClick={handleExportInquiries}
                    data-testid="export-inquiries-button"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Export CSV
                  </Button>
                </div>
                
                <div className="border rounded-lg">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Destination</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {inquiries.map(inquiry => (
                        <TableRow key={inquiry.id}>
                          <TableCell className="font-medium">{inquiry.name}</TableCell>
                          <TableCell className="text-sm">{inquiry.email}</TableCell>
                          <TableCell className="text-sm">{inquiry.destination_name || 'N/A'}</TableCell>
                          <TableCell className="text-sm">{formatDate(inquiry.created_at)}</TableCell>
                          <TableCell>
                            <Select 
                              value={inquiry.status}
                              onValueChange={(value) => handleUpdateInquiryStatus(inquiry.id, value)}
                            >
                              <SelectTrigger className="w-[140px]" data-testid={`status-select-${inquiry.id}`}>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="new">New</SelectItem>
                                <SelectItem value="in_progress">In Progress</SelectItem>
                                <SelectItem value="responded">Responded</SelectItem>
                                <SelectItem value="closed">Closed</SelectItem>
                              </SelectContent>
                            </Select>
                          </TableCell>
                          <TableCell className="text-right">
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button variant="ghost" size="sm" data-testid={`view-inquiry-${inquiry.id}`}>
                                  <Eye className="h-4 w-4" />
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="max-w-2xl">
                                <DialogHeader>
                                  <DialogTitle>Inquiry Details</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4">
                                  <div className="grid grid-cols-2 gap-4">
                                    <div>
                                      <Label>Name</Label>
                                      <p className="text-sm mt-1">{inquiry.name}</p>
                                    </div>
                                    <div>
                                      <Label>Email</Label>
                                      <p className="text-sm mt-1">{inquiry.email}</p>
                                    </div>
                                    <div>
                                      <Label>Phone</Label>
                                      <p className="text-sm mt-1">{inquiry.phone || 'N/A'}</p>
                                    </div>
                                    <div>
                                      <Label>Destination</Label>
                                      <p className="text-sm mt-1">{inquiry.destination_name || 'N/A'}</p>
                                    </div>
                                    <div>
                                      <Label>Travel Dates</Label>
                                      <p className="text-sm mt-1">{inquiry.dates || 'N/A'}</p>
                                    </div>
                                    <div>
                                      <Label>Group Size</Label>
                                      <p className="text-sm mt-1">{inquiry.group_size || 'N/A'}</p>
                                    </div>
                                    <div>
                                      <Label>Budget</Label>
                                      <p className="text-sm mt-1">{inquiry.budget || 'N/A'}</p>
                                    </div>
                                    <div>
                                      <Label>Status</Label>
                                      <Badge className="mt-1">{inquiry.status}</Badge>
                                    </div>
                                  </div>
                                  {inquiry.message && (
                                    <div>
                                      <Label>Message</Label>
                                      <p className="text-sm mt-1 whitespace-pre-line">{inquiry.message}</p>
                                    </div>
                                  )}
                                </div>
                              </DialogContent>
                            </Dialog>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </Card>
      </div>
    </div>
  );
}
