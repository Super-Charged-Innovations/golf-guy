import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { ArrowLeft, Calendar, User } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ArticleDetail() {
  const { slug } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticle();
  }, [slug]);

  const loadArticle = async () => {
    try {
      const response = await axios.get(`${API}/articles/${slug}`);
      setArticle(response.data);
    } catch (error) {
      console.error('Error loading article:', error);
    } finally {
      setLoading(false);
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
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Article Not Found</h2>
          <p className="text-muted-foreground mb-6">The article you're looking for doesn't exist.</p>
          <Link to="/articles">
            <Button>View All Articles</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Image */}
      <section className="relative h-[50vh] md:h-[60vh] bg-black">
        <img 
          src={article.image} 
          alt={article.title}
          className="w-full h-full object-cover opacity-80"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
      </section>

      {/* Article Content */}
      <section className="py-12 md:py-16">
        <div className="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8">
          {/* Back Button */}
          <Link to="/articles">
            <Button variant="ghost" className="mb-6" data-testid="back-button">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Articles
            </Button>
          </Link>

          {/* Article Header */}
          <div className="mb-8">
            {article.category && (
              <Badge variant="outline" className="mb-4">{article.category}</Badge>
            )}
            <h1 className="font-playfair text-4xl sm:text-5xl font-bold mb-6">{article.title}</h1>
            
            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
              {article.author && (
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4" />
                  <span>{article.author}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                <span>{formatDate(article.publish_date)}</span>
              </div>
            </div>
          </div>

          {/* Article Body */}
          <div className="prose prose-lg max-w-none">
            <p className="text-xl text-muted-foreground leading-relaxed mb-8">{article.excerpt}</p>
            <div className="text-foreground/90 leading-relaxed whitespace-pre-line">
              {article.content}
            </div>
          </div>

          {/* CTA */}
          <div className="mt-12 p-8 bg-secondary/30 rounded-lg text-center">
            <h3 className="font-playfair text-2xl font-bold mb-4">Inspired by this trip?</h3>
            <p className="text-muted-foreground mb-6">Let us create a similar experience for you</p>
            <Link to="/contact">
              <Button size="lg" className="bg-primary hover:bg-primary/90" data-testid="cta-button">
                Get Custom Quote
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
