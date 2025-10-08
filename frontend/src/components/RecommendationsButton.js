import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Badge } from './ui/badge';
import { Sparkles, Loader2, TrendingUp, X } from 'lucide-react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const RecommendationsButton = () => {
  const { isAuthenticated, token } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const [tierStatus, setTierStatus] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      checkTierStatus();
    }
  }, [isAuthenticated]);

  const checkTierStatus = async () => {
    try {
      const response = await axios.get(`${API}/profile/tier-status`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTierStatus(response.data);
      
      // Show notification bubble if tier 0
      if (response.data.tier === 0) {
        setHasUnread(true);
      }
    } catch (error) {
      console.error('Failed to fetch tier status:', error);
    }
  };

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/ai/recommendations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRecommendations(response.data.recommendations || []);
      setHasUnread(false);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
      toast.error('Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenRecommendations = () => {
    if (!isAuthenticated) {
      toast.error('Please sign in to view recommendations');
      return;
    }
    
    setIsOpen(true);
    if (recommendations.length === 0) {
      loadRecommendations();
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <>
      {/* Floating button with notification badge */}
      <div className="relative inline-block">
        <Button
          onClick={handleOpenRecommendations}
          variant="outline"
          className="gap-2 relative"
          data-testid="recommendations-button"
        >
          <Sparkles className="h-4 w-4 text-emerald-600" />
          <span className="hidden sm:inline">AI Picks</span>
        </Button>
        
        {hasUnread && (
          <div className="absolute -top-1 -right-1 h-3 w-3 bg-emerald-500 rounded-full animate-pulse" 
               data-testid="notification-badge" />
        )}
      </div>

      {/* Recommendations Dialog */}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-[600px] max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-emerald-600" />
              AI Recommendations
            </DialogTitle>
          </DialogHeader>

          <div className="space-y-4 py-4">
            {/* Tier Status Banner */}
            {tierStatus && (
              <div className={`p-4 rounded-lg border ${
                tierStatus.tier === 0 
                  ? 'bg-amber-50 border-amber-200' 
                  : 'bg-emerald-50 border-emerald-200'
              }`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <TrendingUp className={`h-4 w-4 ${
                      tierStatus.tier === 0 ? 'text-amber-600' : 'text-emerald-600'
                    }`} />
                    <span className="text-sm font-medium">
                      {tierStatus.tier === 0 ? 'Complete Your Profile' : `Tier ${tierStatus.tier} Member`}
                    </span>
                  </div>
                  <Badge variant={tierStatus.tier === 0 ? 'outline' : 'default'}>
                    {tierStatus.tier === 0 ? 'Getting Started' : `Tier ${tierStatus.tier}`}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  {tierStatus.message}
                </p>
                {tierStatus.tier === 0 && (
                  <Button
                    size="sm"
                    className="mt-3"
                    onClick={() => {
                      setIsOpen(false);
                      navigate('/profile');
                    }}
                  >
                    Complete Profile
                  </Button>
                )}
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="flex flex-col items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-emerald-600 mb-4" />
                <p className="text-sm text-muted-foreground">
                  Generating personalized recommendations...
                </p>
              </div>
            )}

            {/* Recommendations List */}
            {!loading && recommendations.length > 0 && (
              <div className="space-y-3">
                {recommendations.map((rec, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-lg border bg-white hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-lg text-emerald-900">
                        {rec.destination_name}
                      </h3>
                      {rec.match_score !== undefined && (
                        <Badge variant="secondary">
                          {Math.round(rec.match_score * 100)}% Match
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">
                      {rec.reason}
                    </p>
                    {rec.highlight && (
                      <p className="text-sm font-medium text-emerald-700">
                        {rec.highlight}
                      </p>
                    )}
                    {rec.is_kyc_prompt && (
                      <Button
                        size="sm"
                        className="mt-3 w-full"
                        onClick={() => {
                          setIsOpen(false);
                          navigate('/profile');
                        }}
                      >
                        Get Started
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Empty State */}
            {!loading && recommendations.length === 0 && (
              <div className="text-center py-12">
                <Sparkles className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-50" />
                <p className="text-sm text-muted-foreground">
                  No recommendations yet. Complete your profile to get started!
                </p>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};
