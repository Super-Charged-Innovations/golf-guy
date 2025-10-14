import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));
  const [loading, setLoading] = useState(true);

  const fetchCurrentUser = useCallback(async (authToken) => {
    try {
      const response = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      
      // If token is invalid (401/403), clear it
      if (error.response?.status === 401 || error.response?.status === 403) {
        localStorage.removeItem('auth_token');
        setToken(null);
        setUser(null);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Check if user is already logged in
    if (token) {
      fetchCurrentUser(token);
    } else {
      setUser(null);
      setLoading(false);
    }
  }, [token, fetchCurrentUser]);

  const register = async (email, password, fullName) => {
    try {
      const response = await axios.post(`${API}/auth/register`, {
        email,
        password,
        full_name: fullName
      });
      
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('auth_token', access_token);
      
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Registration failed'
      };
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, {
        email,
        password
      });
      
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('auth_token', access_token);
      
      return { success: true, user: userData };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  const logout = () => {
    // Clear all auth-related localStorage first
    localStorage.removeItem('auth_token');
    localStorage.removeItem('demo_admin');
    localStorage.removeItem('demo_client');
    
    // Then update state
    setUser(null);
    setToken(null);
    setLoading(false);
  };

  const value = {
    user,
    token,
    loading,
    register,
    login,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.is_admin || false
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
