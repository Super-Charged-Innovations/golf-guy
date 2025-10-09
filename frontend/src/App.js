import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import MobileLayout from './components/mobile/MobileLayout';
import Home from './pages/Home';
import Destinations from './pages/Destinations';
import DestinationDetail from './pages/DestinationDetail';
import Articles from './pages/Articles';
import ArticleDetail from './pages/ArticleDetail';
import Contact from './pages/Contact';
import About from './pages/About';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminDashboard from './pages/AdminDashboard';
import ProfileKYC from './pages/ProfileKYC';
import ClientDashboard from './pages/ClientDashboard';
import PrivacySettings from './pages/PrivacySettings';
import ScrollToTop from './components/ScrollToTop';
import CookieConsent from './components/CookieConsent';
import { Toaster } from './components/ui/sonner';
import { useDeviceDetection } from './hooks/usePWA';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ScrollToTop />
        <Toaster position="top-center" />
        <CookieConsent />
        <Routes>
          {/* Auth Routes (no layout) */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Main Routes with responsive layout */}
          <Route path="/" element={<ResponsiveLayout />}>
            <Route index element={<Home />} />
            <Route path="destinations" element={<Destinations />} />
            <Route path="destinations/:slug" element={<DestinationDetail />} />
            <Route path="articles" element={<Articles />} />
            <Route path="articles/:slug" element={<ArticleDetail />} />
            <Route path="contact" element={<Contact />} />
            <Route path="about" element={<About />} />
            <Route path="dashboard" element={<ClientDashboard />} />
            <Route path="profile" element={<ProfileKYC />} />
            <Route path="privacy" element={<PrivacySettings />} />
            <Route path="admin" element={<AdminDashboard />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

// Responsive layout component that chooses between mobile and desktop
const ResponsiveLayout = () => {
  const { isMobile } = useDeviceDetection();
  
  return isMobile ? <MobileLayout /> : <Layout />;
};

export default App;
