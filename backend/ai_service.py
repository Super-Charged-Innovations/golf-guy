"""
AI Service for Golf Guy Platform
Handles GPT-5 integration, content generation, and user recommendations
"""
import os
from typing import List, Dict, Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path
import json
import uuid

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class AIService:
    """AI Service using GPT-5-mini via Emergent LLM Key"""
    
    def __init__(self):
        self.model = "gpt-5-mini"
        self.provider = "openai"
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def _create_chat_session(self, system_message: str) -> LlmChat:
        """Create a new chat session with unique session ID"""
        session_id = f"golf-guy-{uuid.uuid4()}"
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        )
        chat.with_model(self.provider, self.model)
        return chat
    
    async def generate_destination_content(
        self, 
        course_name: str, 
        location: str,
        additional_info: Optional[str] = None
    ) -> Dict:
        """
        AI Auto-fill: Generate comprehensive destination content
        based on course name and location
        """
        system_message = "You are an expert golf travel content generator. Provide accurate, engaging content in JSON format."
        
        prompt = f"""Generate comprehensive destination content for:

Course/Resort Name: {course_name}
Location: {location}
Additional Information: {additional_info or 'None provided'}

Please provide a JSON response with the following structure:
{{
    "short_desc": "A compelling 1-2 sentence description highlighting the key appeal",
    "long_desc": "A detailed 3-4 paragraph description covering the golf experience, facilities, and appeal",
    "highlights": ["Highlight 1", "Highlight 2", "Highlight 3", "Highlight 4"],
    "climate": "Brief climate description",
    "best_time_to_visit": "Best months or seasons to visit",
    "nearby_attractions": ["Attraction 1", "Attraction 2", "Attraction 3"],
    "nearby_hotels": ["Hotel 1", "Hotel 2", "Hotel 3"],
    "transfer_info": "Nearest airport and approximate transfer time"
}}

Focus on factual, enticing content that helps travelers understand what makes this destination special."""

        try:
            chat = self._create_chat_session(system_message)
            user_message = UserMessage(text=prompt)
            response = await chat.send_message(user_message)
            
            # Parse JSON response
            content = json.loads(response)
            return content
            
        except Exception as e:
            print(f"AI Content Generation Error: {str(e)}")
            return {
                "short_desc": f"Exceptional golf experience at {course_name}",
                "long_desc": f"Located in {location}, {course_name} offers a memorable golf experience.",
                "highlights": ["Championship course", "Scenic views", "Professional facilities"],
                "climate": "Pleasant year-round",
                "best_time_to_visit": "Spring and Fall",
                "nearby_attractions": [],
                "nearby_hotels": [],
                "transfer_info": "Contact us for transfer details"
            }
    
    async def generate_recommendations(
        self,
        user_profile: Dict,
        available_destinations: List[Dict],
        recent_additions: List[Dict]
    ) -> List[Dict]:
        """
        Generate personalized recommendations based on user profile
        """
        user_context = f"""
User Profile:
- Name: {user_profile.get('name', 'User')}
- Budget Range: {user_profile.get('budget_min', 0)} - {user_profile.get('budget_max', 50000)} SEK
- Preferred Countries: {', '.join(user_profile.get('preferred_countries', []))}
- Playing Level: {user_profile.get('playing_level', 'Intermediate')}
- Accommodation Preference: {user_profile.get('accommodation_preference', 'Any')}
- Past Inquiries: {len(user_profile.get('past_inquiries', []))}
- Conversation Summary: {user_profile.get('conversation_summary', 'No previous conversations')}
"""

        destinations_summary = "\n".join([
            f"- {d['name']} ({d['country']}): {d['price_from']}-{d['price_to']} SEK, Type: {d.get('destination_type', 'golf_course')}"
            for d in available_destinations[:20]  # Limit to avoid token overflow
        ])

        recent_summary = "\n".join([
            f"- NEW: {d['name']} ({d['country']}): {d['price_from']}-{d['price_to']} SEK"
            for d in recent_additions[:5]
        ])

        prompt = f"""{user_context}

Available Destinations:
{destinations_summary}

Recently Added:
{recent_summary}

Based on this user's profile and preferences, recommend 3-5 destinations that would be perfect for them.
For each recommendation, explain WHY it's a good match.

Respond in JSON format:
{{
    "recommendations": [
        {{
            "destination_name": "Name",
            "reason": "Why this is perfect for the user",
            "match_score": 0.0-1.0,
            "highlight": "One key selling point"
        }}
    ]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a golf travel recommendation expert. Provide personalized suggestions based on user preferences."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                temperature=0.8
            )
            
            import json
            recommendations = json.loads(response.choices[0].message.content)
            return recommendations.get('recommendations', [])
            
        except Exception as e:
            print(f"AI Recommendations Error: {str(e)}")
            return []
    
    async def chat_with_context(
        self,
        user_message: str,
        user_profile: Dict,
        conversation_history: List[Dict],
        available_destinations: List[Dict]
    ) -> str:
        """
        Chat with user using GPT-5, with full context awareness
        """
        # Build system context
        system_context = f"""You are the Golf Guy AI travel assistant. You help users find perfect golf destinations and packages.

User Context:
- Name: {user_profile.get('name', 'Guest')}
- Budget: {user_profile.get('budget_min', 0)}-{user_profile.get('budget_max', 50000)} SEK
- Preferences: {', '.join(user_profile.get('preferred_countries', ['Various locations']))}
- Playing Level: {user_profile.get('playing_level', 'Intermediate')}

Available Destinations ({len(available_destinations)} total):
{', '.join([d['name'] for d in available_destinations[:15]])}...

Your Role:
1. Help users discover perfect golf destinations
2. Suggest packages based on budget and preferences
3. Provide detailed information about courses, resorts, and travel logistics
4. Be friendly, professional, and enthusiastic about golf travel
5. If asked about specific destinations, provide accurate details from the available data
6. Always consider the user's budget and preferences

Conversation Style: Professional yet friendly, like a knowledgeable travel advisor."""

        # Build conversation messages
        messages = [{"role": "system", "content": system_context}]
        
        # Add conversation history (last 10 messages to manage tokens)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI Chat Error: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again or contact our support team for assistance."
    
    async def summarize_conversation(
        self,
        conversation_history: List[Dict]
    ) -> str:
        """
        Summarize a conversation for storage in user profile
        """
        if not conversation_history:
            return "No conversation history"
        
        conversation_text = "\n".join([
            f"{msg.get('role', 'user').title()}: {msg.get('content', '')}"
            for msg in conversation_history
        ])
        
        prompt = f"""Summarize this conversation between a user and Golf Guy AI assistant. 
Focus on:
1. User's expressed preferences and interests
2. Destinations discussed
3. Budget considerations
4. Any specific requirements or constraints
5. Key decisions or next steps

Conversation:
{conversation_text}

Provide a concise summary (2-3 paragraphs) that captures the essential information for future personalization."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a conversation summarizer. Create concise, informative summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI Summarization Error: {str(e)}")
            return f"Conversation on {datetime.now(timezone.utc).strftime('%Y-%m-%d')}: User discussed golf travel options."


# Global AI service instance
ai_service = AIService()
