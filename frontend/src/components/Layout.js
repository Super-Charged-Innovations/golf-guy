import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { MapPin, Mail, Phone, Plane, LogIn, UserCog, LogOut } from 'lucide-react';

export const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, isAuthenticated, isAdmin, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const isAdminPage = location.pathname.startsWith('/admin');

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2" data-testid="logo-link">
              <Plane className="h-8 w-8 text-primary" />
              <span className="font-playfair text-2xl font-bold text-primary">Golf Guy</span>
            </Link>

            {/* Navigation */}
            {!isAdminPage && (
              <nav className="hidden md:flex items-center space-x-6">
                <Link to="/destinations" className="text-sm font-medium hover:text-primary transition-colors" data-testid="nav-destinations">
                  Destinations
                </Link>
                <Link to="/articles" className="text-sm font-medium hover:text-primary transition-colors" data-testid="nav-articles">
                  Travel Reports
                </Link>
                <Link to="/about" className="text-sm font-medium hover:text-primary transition-colors" data-testid="nav-about">
                  About
                </Link>
                <Link to="/contact" className="text-sm font-medium hover:text-primary transition-colors" data-testid="nav-contact">
                  Contact
                </Link>
              </nav>
            )}

            {/* Auth Buttons */}
            <div className="flex items-center gap-2">
              {!isAuthenticated ? (
                <>
                  <Link to="/login">
                    <Button variant="ghost" size="sm" data-testid="login-button">
                      <LogIn className="h-4 w-4 mr-2" />
                      Sign In
                    </Button>
                  </Link>
                  <Link to="/register">
                    <Button variant="outline" size="sm" data-testid="register-button">
                      Get Started
                    </Button>
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/profile">
                    <Button variant="ghost" size="sm" data-testid="profile-link">
                      My Profile
                    </Button>
                  </Link>
                  {isAdmin && !isAdminPage && (
                    <Link to="/admin">
                      <Button variant="outline" size="sm" data-testid="admin-dashboard-link">
                        <UserCog className="h-4 w-4 mr-2" />
                        Admin
                      </Button>
                    </Link>
                  )}
                  <span className="text-sm text-muted-foreground hidden sm:inline">
                    {user?.full_name}
                  </span>
                  <Button variant="ghost" size="sm" onClick={handleLogout} data-testid="logout-button">
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      {!isAdminPage && (
        <footer className="border-t bg-secondary/30 mt-20">
          <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {/* About */}
              <div>
                <div className="flex items-center space-x-2 mb-4">
                  <Plane className="h-6 w-6 text-primary" />
                  <span className="font-playfair text-xl font-bold text-primary">Golf Guy</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Creating unforgettable golf experiences since 2010. Your trusted partner for golf travel worldwide.
                </p>
              </div>

              {/* Quick Links */}
              <div>
                <h4 className="font-semibold mb-4">Explore</h4>
                <ul className="space-y-2 text-sm">
                  <li><Link to="/destinations" className="text-muted-foreground hover:text-primary transition-colors">Destinations</Link></li>
                  <li><Link to="/articles" className="text-muted-foreground hover:text-primary transition-colors">Travel Reports</Link></li>
                  <li><Link to="/about" className="text-muted-foreground hover:text-primary transition-colors">About Us</Link></li>
                  <li><Link to="/contact" className="text-muted-foreground hover:text-primary transition-colors">Contact</Link></li>
                </ul>
              </div>

              {/* Support */}
              <div>
                <h4 className="font-semibold mb-4">Support</h4>
                <ul className="space-y-2 text-sm">
                  <li><a href="#" className="text-muted-foreground hover:text-primary transition-colors">Travel Guarantee</a></li>
                  <li><a href="#" className="text-muted-foreground hover:text-primary transition-colors">FAQ</a></li>
                  <li><a href="#" className="text-muted-foreground hover:text-primary transition-colors">Privacy Policy</a></li>
                  <li><a href="#" className="text-muted-foreground hover:text-primary transition-colors">Terms of Service</a></li>
                </ul>
              </div>

              {/* Contact */}
              <div>
                <h4 className="font-semibold mb-4">Contact</h4>
                <ul className="space-y-3 text-sm">
                  <li className="flex items-start gap-2">
                    <Mail className="h-4 w-4 mt-0.5 text-primary" />
                    <span className="text-muted-foreground">info@golfguy.com</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Phone className="h-4 w-4 mt-0.5 text-primary" />
                    <span className="text-muted-foreground">+46 8 123 456 78</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <MapPin className="h-4 w-4 mt-0.5 text-primary" />
                    <span className="text-muted-foreground">Stockholm, Sweden</span>
                  </li>
                </ul>
              </div>
            </div>

            <div className="mt-12 pt-8 border-t text-center text-sm text-muted-foreground">
              <p>&copy; {new Date().getFullYear()} Golf Guy. All rights reserved.</p>
              <p className="mt-2 text-xs">
                Golf travel specialists since 2010. Creating unforgettable golf experiences worldwide.
              </p>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
};

export default Layout;
