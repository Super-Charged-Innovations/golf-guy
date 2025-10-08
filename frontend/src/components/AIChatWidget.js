import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { MessageCircle, X, Send, Loader2, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const AIChatWidget = () => {
  const { isAuthenticated, token, user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && isAuthenticated && recommendations.length === 0) {
      loadRecommendations();
    }
  }, [isOpen, isAuthenticated]);

  const loadRecommendations = async () => {
    setLoadingRecs(true);
    try {
      const response = await axios.get(`${API}/ai/recommendations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setLoadingRecs(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    if (!isAuthenticated) {
      toast.error('Please sign in to chat with our AI assistant');
      return;
    }

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to UI
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await axios.post(
        `${API}/ai/chat`,
        { message: userMessage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Add AI response to UI
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.data.response 
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to send message. Please try again.');
      // Remove user message on error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) {
    return (
      <Button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg bg-gradient-to-br from-emerald-500 to-emerald-700 hover:from-emerald-600 hover:to-emerald-800 text-white z-50"
        data-testid="ai-chat-button"
      >
        <MessageCircle className="h-6 w-6" />
      </Button>
    );
  }

  return (
    <Card className="fixed bottom-6 right-6 w-[380px] h-[600px] shadow-2xl z-50 flex flex-col overflow-hidden border-2 border-emerald-200" data-testid="ai-chat-widget">
      {/* Header */}
      <div className="bg-gradient-to-br from-emerald-500 to-emerald-700 p-4 flex items-center justify-between text-white">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5" />
          <div>
            <h3 className="font-semibold">Golf Guy AI Assistant</h3>
            <p className="text-xs text-emerald-100">Powered by GPT-5</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsOpen(false)}
          className="text-white hover:bg-emerald-600"
          data-testid="close-chat-button"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>

      {/* Messages Area */}
      <ScrollArea className="flex-1 p-4 bg-gradient-to-br from-white via-emerald-50/20 to-white">
        <div className="space-y-4">
          {/* Welcome Message */}
          {messages.length === 0 && (
            <div className="bg-white rounded-lg p-4 shadow-sm border border-emerald-100">
              <p className="text-sm mb-2">
                👋 Hi {user?.full_name || 'there'}! I'm your personal golf travel assistant.
              </p>
              <p className="text-sm text-muted-foreground">
                I can help you discover perfect golf destinations, suggest packages, and answer questions about courses and resorts.
              </p>
              
              {/* Recommendations */}
              {loadingRecs ? (
                <div className="mt-4 flex items-center justify-center">
                  <Loader2 className="h-4 w-4 animate-spin text-emerald-600" />
                  <span className="ml-2 text-xs text-muted-foreground">Loading personalized recommendations...</span>
                </div>
              ) : recommendations.length > 0 ? (
                <div className="mt-4">
                  <p className="text-xs font-semibold text-emerald-700 mb-2">✨ Recommended for you:</p>
                  {recommendations.slice(0, 3).map((rec, idx) => (
                    <div key={idx} className="mb-2 p-2 bg-emerald-50 rounded text-xs">
                      <p className="font-medium text-emerald-900">{rec.destination_name}</p>
                      <p className="text-emerald-700 mt-1">{rec.reason}</p>
                    </div>
                  ))}
                </div>
              ) : null}
            </div>
          )}

          {/* Chat Messages */}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  msg.role === 'user'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-white shadow-sm border border-emerald-100'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white shadow-sm border border-emerald-100 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-emerald-600" />
                  <span className="text-sm text-muted-foreground">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="p-4 border-t bg-white">
        <div className="flex gap-2">
          <Input
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about golf destinations..."
            className="flex-1"
            disabled={loading}
            data-testid="chat-input"
          />
          <Button
            onClick={sendMessage}
            disabled={loading || !inputMessage.trim()}
            className="bg-emerald-600 hover:bg-emerald-700"
            data-testid="send-message-button"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-xs text-center text-muted-foreground mt-2">
          AI responses may vary. Always verify details before booking.
        </p>
      </div>
    </Card>
  );
};

export default AIChatWidget;
