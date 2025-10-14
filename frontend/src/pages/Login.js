import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { Plane, Mail, Lock, Loader2 } from 'lucide-react';

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || '/';

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await login(formData.email, formData.password);

      if (result.success) {
        toast.success('Welcome back!');
        
        // Redirect based on user role
        const userData = result.user;
        console.log('Login successful, user data:', userData);
        
        if (userData?.is_admin) {
          console.log('Redirecting admin to /admin');
          navigate('/admin', { replace: true });
        } else {
          console.log('Redirecting user to /dashboard');
          navigate('/dashboard', { replace: true });
        }
      } else {
        console.error('Login failed:', result.error);
        toast.error(result.error || 'Login failed');
      }
    } catch (error) {
      console.error('Login exception:', error);
      toast.error('An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/10 via-sky-mist to-sand/30 flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-8" data-testid="login-card">
        {/* Logo */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center gap-2">
            <Plane className="h-10 w-10 text-primary" />
            <span className="font-playfair text-3xl font-bold text-primary">Golf Guy</span>
          </div>
        </div>

        <h1 className="text-2xl font-playfair font-bold text-center mb-2">Welcome Back</h1>
        <p className="text-center text-muted-foreground mb-6">
          Sign in to access your personalized golf travel dashboard
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="email">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="your@email.com"
                className="pl-10"
                required
                data-testid="email-input"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="pl-10"
                required
                data-testid="password-input"
              />
            </div>
          </div>

          <Button
            type="submit"
            className="w-full bg-primary hover:bg-primary/90"
            disabled={loading}
            data-testid="login-button"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Signing in...
              </>
            ) : (
              'Sign In'
            )}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm">
          <p className="text-muted-foreground">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary font-medium hover:underline">
              Sign up
            </Link>
          </p>
        </div>

        <div className="mt-4 text-center">
          <Link to="/" className="text-sm text-muted-foreground hover:text-primary">
            ← Back to home
          </Link>
        </div>
      </Card>
    </div>
  );
}
