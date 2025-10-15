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
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between gap-4">
            {/* Logo */}
            <Link 
              to="/" 
              className="flex items-center space-x-2 group transition-transform duration-300 hover:scale-105 flex-shrink-0" 
              data-testid="logo-link"
            >
              <div className="relative">
                <img 
                  src="https://customer-assets.emergentagent.com/job_golfguy-platform/artifacts/lyponq0h_image.png" 
                  alt="DGolf Logo" 
                  className="h-10 w-10 object-contain transition-all duration-300 group-hover:brightness-110"
                />
              </div>
              <span className="text-xl font-semibold bg-gradient-to-r from-emerald-600 to-emerald-800 bg-clip-text text-transparent whitespace-nowrap" style={{ fontFamily: "'Dancing Script', cursive" }}>
                DGolf
              </span>
            </Link>

            {/* Navigation */}
            {!isAdminPage && (
              <nav className="hidden md:flex items-center space-x-6 flex-grow justify-center">
                <NavLink to="/destinations" label="Destinations" testId="nav-destinations" />
                <NavLink to="/articles" label="Travel Reports" testId="nav-articles" />
                <NavLink to="/about" label="About" testId="nav-about" />
                <NavLink to="/contact" label="Contact" testId="nav-contact" />
              </nav>
            )}

            {/* Auth Buttons */}
            <div className="flex items-center gap-2 flex-shrink-0">
              {!isAuthenticated ? (
                <>
                  <Link to="/login">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="hover:bg-emerald-50 hover:text-emerald-700 transition-all duration-300"
                      data-testid="login-button"
                    >
                      <LogIn className="h-4 w-4 mr-1" />
                      <span className="hidden lg:inline">Sign In</span>
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
                  {/* Show My Profile only for non-admin users */}
                  {!isAdmin && (
                    <Link to="/profile">
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="hover:bg-emerald-50 hover:text-emerald-700 transition-all duration-300 hidden lg:inline-flex"
                        data-testid="profile-link"
                      >
                        My Profile
                      </Button>
                    </Link>
                  )}
                  
                  {/* Admin button - goes directly to admin dashboard */}
                  {isAdmin && (
                    <Link to="/admin">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="border-emerald-200 hover:bg-emerald-50 hover:border-emerald-400 hover:text-emerald-700 transition-all duration-300"
                        data-testid="admin-dashboard-link"
                      >
                        Dashboard
                      </Button>
                    </Link>
                  )}
                  
                  {/* User name - simplified */}
                  <span className="hidden lg:inline-flex text-sm text-gray-700 font-medium px-2 whitespace-nowrap">
                    {user?.full_name}
                  </span>
                  
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={handleLogout} 
                    className="hover:bg-red-50 hover:text-red-700 transition-all duration-300"
                    data-testid="logout-button"
                  >
                    <LogOut className="h-4 w-4" />
                    <span className="hidden lg:inline ml-1">Logout</span>
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
        <footer className="border-t border-emerald-100 bg-emerald-800 text-white mt-20">
          <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
              {/* About DGolf */}
              <div className="lg:col-span-1">
                <div className="flex items-center space-x-2 mb-4">
                  <img 
                    src="https://customer-assets.emergentagent.com/job_golfguy-platform/artifacts/lyponq0h_image.png" 
                    alt="DGolf Logo" 
                    className="h-10 w-10 object-contain brightness-0 invert"
                  />
                  <span className="text-xl font-semibold" style={{ fontFamily: "'Dancing Script', cursive" }}>
                    DGolf
                  </span>
                </div>
                <p className="text-sm text-emerald-100 leading-relaxed">
                  Vår mission är att du som kund ska få bästa möjliga upplevelse på din golfresa och med över 40 års samlad erfarenhet är du i trygga händer som kund hos DGolf
                </p>
              </div>

              {/* Instagram */}
              <div className="lg:col-span-1">
                <h4 className="font-semibold mb-4 text-white">@dgolfswe på Instagram</h4>
                <p className="text-sm text-emerald-100 mb-4">Senaste inläggen från dgolfswe</p>
                <div className="grid grid-cols-3 gap-2">
                  <div className="aspect-square rounded-lg overflow-hidden bg-emerald-700">
                    <img src="https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=200" alt="Golf course" className="w-full h-full object-cover" />
                  </div>
                  <div className="aspect-square rounded-lg overflow-hidden bg-emerald-700">
                    <img src="https://images.unsplash.com/photo-1579476170948-2decc6dd582f?w=200" alt="Golf course" className="w-full h-full object-cover" />
                  </div>
                  <div className="aspect-square rounded-lg overflow-hidden bg-emerald-700">
                    <img src="https://images.unsplash.com/photo-1587453451984-c9d4be800788?w=200" alt="Golf course" className="w-full h-full object-cover" />
                  </div>
                </div>
              </div>

              {/* Our Partnerships */}
              <div className="lg:col-span-1">
                <h4 className="font-semibold mb-4 text-white">Våra samarbeten</h4>
                <div className="space-y-4">
                  <div className="bg-white/10 rounded-lg p-3 backdrop-blur-sm">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-2xl">❤️</span>
                      <p className="font-medium text-sm">Ronald McDonald Hus i Lund</p>
                    </div>
                    <p className="text-xs text-emerald-100">Stödjer familjer med sjuka barn</p>
                  </div>
                  <div className="bg-white/10 rounded-lg p-3 backdrop-blur-sm">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-2xl">💙</span>
                      <p className="font-medium text-sm">Barncancerfonden Södra</p>
                    </div>
                    <p className="text-xs text-emerald-100">Kampen mot barncancer</p>
                  </div>
                </div>
              </div>

              {/* Quick Links */}
              <div className="lg:col-span-1">
                <h4 className="font-semibold mb-4 text-white">Snabblänkar</h4>
                <ul className="space-y-2 text-sm">
                  <li><Link to="/destinations" className="text-emerald-100 hover:text-white transition-colors">Alla destinationer</Link></li>
                  <li><Link to="/about" className="text-emerald-100 hover:text-white transition-colors">Resegaranti</Link></li>
                  <li><Link to="/about" className="text-emerald-100 hover:text-white transition-colors">Om DGolf</Link></li>
                </ul>
              </div>

              {/* Contact & Newsletter */}
              <div className="lg:col-span-1">
                <h4 className="font-semibold mb-4 text-white">Kontakt</h4>
                <ul className="space-y-3 text-sm mb-6">
                  <li className="flex items-center gap-2">
                    <Phone className="h-4 w-4 text-emerald-300" />
                    <a href="tel:0760196485" className="text-emerald-100 hover:text-white transition-colors">0760-196485</a>
                  </li>
                  <li className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-emerald-300" />
                    <a href="mailto:info@dgolf.se" className="text-emerald-100 hover:text-white transition-colors">info@dgolf.se</a>
                  </li>
                </ul>
                
                <h4 className="font-semibold mb-3 text-white text-sm">Nyhetsbrev</h4>
                <p className="text-xs text-emerald-100 mb-3">Få de senaste erbjudandena och nyheter direkt i din inkorg.</p>
                <form className="space-y-2">
                  <input 
                    type="text" 
                    placeholder="Ditt namn" 
                    className="w-full px-3 py-2 rounded-md bg-white/10 border border-emerald-600 text-white placeholder-emerald-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
                  />
                  <input 
                    type="email" 
                    placeholder="Din e-postadress" 
                    className="w-full px-3 py-2 rounded-md bg-white/10 border border-emerald-600 text-white placeholder-emerald-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
                  />
                  <button 
                    type="submit" 
                    className="w-full px-4 py-2 bg-amber-500 hover:bg-amber-600 text-emerald-900 font-semibold rounded-md transition-colors text-sm"
                  >
                    Prenumerera
                  </button>
                </form>
              </div>
            </div>

            {/* Bottom Bar */}
            <div className="mt-8 pt-6 border-t border-emerald-700 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-emerald-100">
              <p>&copy; 2022-{new Date().getFullYear()} DGolf. Alla rättigheter förbehållna.</p>
              <div className="flex gap-4">
                <Link to="/privacy" className="hover:text-white transition-colors">Integritetspolicy</Link>
                <Link to="/terms" className="hover:text-white transition-colors">Användarvillkor</Link>
                <Link to="/cookies" className="hover:text-white transition-colors">Cookies</Link>
              </div>
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
