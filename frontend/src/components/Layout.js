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
      <header className="sticky top-0 z-50 w-full border-b border-emerald-100 bg-white/90 backdrop-blur-md supports-[backdrop-filter]:bg-white/80 shadow-sm transition-all duration-300">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link 
              to="/" 
              className="flex items-center space-x-3 group transition-transform duration-300 hover:scale-105" 
              data-testid="logo-link"
            >
              <div className="relative">
                <img 
                  src="https://customer-assets.emergentagent.com/job_golfguy-platform/artifacts/lyponq0h_image.png" 
                  alt="DGolf Logo" 
                  className="h-12 w-12 object-contain transition-all duration-300 group-hover:brightness-110"
                />
              </div>
              <span className="text-2xl font-semibold bg-gradient-to-r from-emerald-600 to-emerald-800 bg-clip-text text-transparent" style={{ fontFamily: "'Dancing Script', cursive" }}>
                DGolf - Din nästa Golfresa
              </span>
            </Link>

            {/* Navigation */}
            {!isAdminPage && (
              <nav className="hidden md:flex items-center space-x-8">
                <NavLink to="/destinations" label="Destinations" testId="nav-destinations" />
                <NavLink to="/articles" label="Travel Reports" testId="nav-articles" />
                <NavLink to="/about" label="About" testId="nav-about" />
                <NavLink to="/contact" label="Contact" testId="nav-contact" />
              </nav>
            )}

            {/* Auth Buttons */}
            <div className="flex items-center gap-2">
              {!isAuthenticated ? (
                <>
                  <Link to="/login">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="hover:bg-emerald-50 hover:text-emerald-700 transition-all duration-300"
                      data-testid="login-button"
                    >
                      <LogIn className="h-4 w-4 mr-2" />
                      Sign In
                    </Button>
                  </Link>
                  <Link to="/register">
                    <Button 
                      size="sm" 
                      className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-md hover:shadow-lg hover:shadow-emerald-200 transition-all duration-300"
                      data-testid="register-button"
                    >
                      Get Started
                    </Button>
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/profile">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="hover:bg-emerald-50 hover:text-emerald-700 transition-all duration-300"
                      data-testid="profile-link"
                    >
                      My Profile
                    </Button>
                  </Link>
                  {isAdmin && !isAdminPage && (
                    <Link to="/admin">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="border-emerald-200 hover:bg-emerald-50 hover:border-emerald-400 hover:text-emerald-700 transition-all duration-300"
                        data-testid="admin-dashboard-link"
                      >
                        <UserCog className="h-4 w-4 mr-2" />
                        Admin
                      </Button>
                    </Link>
                  )}
                  <Link to="/dashboard">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="hidden sm:inline-flex text-gray-700 hover:text-emerald-600 hover:bg-emerald-50 transition-all duration-300 font-medium"
                      data-testid="dashboard-link"
                    >
                      {user?.full_name}
                    </Button>
                  </Link>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={handleLogout} 
                    className="hover:bg-red-50 hover:text-red-700 transition-all duration-300"
                    data-testid="logout-button"
                  >
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
        <footer className="border-t border-emerald-100 bg-gradient-to-b from-white to-emerald-50/30 mt-20">
          <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {/* About */}
              <div>
                <div className="flex items-center space-x-2 mb-4 group">
                  <img 
                    src="https://customer-assets.emergentagent.com/job_golfguy-platform/artifacts/lyponq0h_image.png" 
                    alt="DGolf Logo" 
                    className="h-10 w-10 object-contain"
                  />
                  <span className="text-xl font-semibold bg-gradient-to-r from-emerald-600 to-emerald-800 bg-clip-text text-transparent" style={{ fontFamily: "'Dancing Script', cursive" }}>
                    DGolf
                  </span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Din partner till din nästa golfresa. Upptäck exklusiva golfresor sedan 2010.
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
              <p>&copy; {new Date().getFullYear()} DGolf. Alla rättigheter förbehållna.</p>
              <p className="mt-2 text-xs">
                Golfresspecialister sedan 2010. Din nästa golfresa börjar här.
              </p>
            </div>
          </div>
        </footer>
      )}
      
      {/* Mobile Bottom Navigation */}
      <div className="mobile-nav-bottom md:hidden">
        <a href="/" className={`mobile-nav-item ${location.pathname === '/' ? 'active' : ''}`}>
          <span className="text-lg mb-1">🏠</span>
          <span className="text-xs font-medium">Home</span>
        </a>
        <a href="/destinations" className={`mobile-nav-item ${location.pathname === '/destinations' ? 'active' : ''}`}>
          <span className="text-lg mb-1">⛳</span>
          <span className="text-xs font-medium">Golf</span>
        </a>
        <a href="/search" className={`mobile-nav-item ${location.pathname === '/search' ? 'active' : ''}`}>
          <span className="text-lg mb-1">🔍</span>
          <span className="text-xs font-medium">Search</span>
        </a>
        <a href="/dashboard" className={`mobile-nav-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>
          <span className="text-lg mb-1">📊</span>
          <span className="text-xs font-medium">Trips</span>
        </a>
        <a href="/profile" className={`mobile-nav-item ${location.pathname === '/profile' ? 'active' : ''}`}>
          <span className="text-lg mb-1">👤</span>
          <span className="text-xs font-medium">Profile</span>
        </a>
      </div>
    </div>
  );
};

// Active Navigation Link Component
function NavLink({ to, label, testId }) {
  const location = useLocation();
  const isActive = location.pathname === to || location.pathname.startsWith(to + '/');

  return (
    <Link 
      to={to}
      className={`relative text-sm font-medium transition-all duration-300 ${
        isActive 
          ? 'text-emerald-600' 
          : 'text-gray-700 hover:text-emerald-600'
      }`}
      data-testid={testId}
    >
      {label}
      {/* Active indicator */}
      <span 
        className={`absolute -bottom-2 left-0 h-0.5 bg-gradient-to-r from-emerald-500 to-emerald-600 transition-all duration-300 ${
          isActive ? 'w-full' : 'w-0'
        }`}
      />
      {/* Hover indicator */}
      <span 
        className={`absolute -bottom-2 left-0 h-0.5 bg-gradient-to-r from-emerald-400 to-emerald-500 transition-all duration-300 ${
          isActive ? 'w-0' : 'w-0 group-hover:w-full'
        }`}
      />
    </Link>
  );
}

export default Layout;
