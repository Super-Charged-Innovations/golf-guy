import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { AspectRatio } from '../components/ui/aspect-ratio';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { ArrowRight, BookOpen } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticles();
  }, []);

  useEffect(() => {
    filterArticles();
  }, [articles, selectedCategory]);

  const loadArticles = async () => {
    try {
      const response = await axios.get(`${API}/articles?published=true`);
      setArticles(response.data);
      
      // Extract unique categories
      const uniqueCategories = [...new Set(response.data.map(a => a.category).filter(Boolean))];
      setCategories(uniqueCategories);
    } catch (error) {
      console.error('Error loading articles:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterArticles = () => {
    if (selectedCategory === 'all') {
      setFilteredArticles(articles);
    } else {
      setFilteredArticles(articles.filter(a => a.category === selectedCategory));
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading articles...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Header */}
      <section className="bg-gradient-to-br from-primary/10 via-sky-mist to-sand/30 py-16 md:py-24">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="font-playfair text-4xl sm:text-5xl lg:text-6xl font-bold mb-4">Travel Reports & Guides</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Read about real golf experiences and expert travel advice
          </p>
        </div>
      </section>

      {/* Filters */}
      <section className="border-b bg-white sticky top-16 z-40 shadow-sm">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium">Category:</span>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-[200px]" data-testid="category-filter">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map(category => (
                  <SelectItem key={category} value={category}>{category}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <span className="text-sm text-muted-foreground ml-auto">
              {filteredArticles.length} article{filteredArticles.length !== 1 ? 's' : ''}
            </span>
          </div>
        </div>
      </section>

      {/* Articles Grid */}
      <section className="py-12 md:py-16">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          {filteredArticles.length === 0 ? (
            <div className="text-center py-12">
              <BookOpen className="h-16 w-16 text-muted mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No articles found</h3>
              <p className="text-muted-foreground">Try adjusting your filters</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredArticles.map((article) => (
                <Card key={article.id} className="overflow-hidden hover:shadow-xl transition-shadow" data-testid="article-card">
                  <Link to={`/articles/${article.slug}`}>
                    <AspectRatio ratio={16/9}>
                      <img 
                        src={article.image} 
                        alt={article.title}
                        className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </AspectRatio>
                    <div className="p-6">
                      <div className="flex items-center gap-3 mb-3">
                        {article.category && (
                          <Badge variant="outline">{article.category}</Badge>
                        )}
                        <span className="text-xs text-muted-foreground">
                          {formatDate(article.publish_date)}
                        </span>
                      </div>
                      <h3 className="font-playfair text-xl font-semibold mb-2 line-clamp-2">{article.title}</h3>
                      <p className="text-sm text-muted-foreground mb-4 line-clamp-3">{article.excerpt}</p>
                      {article.author && (
                        <p className="text-xs text-muted-foreground mb-4">By {article.author}</p>
                      )}
                      <Button variant="ghost" size="sm" data-testid="article-read-button">
                        Read Article
                        <ArrowRight className="ml-1 h-3 w-3" />
                      </Button>
                    </div>
                  </Link>
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
