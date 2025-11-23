"""
Free LLM Response Generation Agent using Ollama
"""
from typing import Dict, List, Optional, Any

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class LLMResponseAgent:
    """
    Free LLM-powered response generation using Ollama.
    Creates natural, conversational responses instead of template-based ones.
    """
    
    def __init__(self, model: str = "phi3:mini"):
        """
        Initialize LLM Response Agent.
        
        Args:
            model: Ollama model to use
        """
        self.model = model
        self.available = OLLAMA_AVAILABLE and self._test_model()
        
        if not self.available:
            print(f"⚠️  LLM Response Generator not available. Using template responses.")
    
    def _test_model(self) -> bool:
        """Test if the model is available."""
        try:
            ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': 'Hello'}
            ])
            return True
        except:
            return False
    
    def generate_tourism_response(
        self, 
        query: str, 
        location: str,
        intent_data: Dict,
        weather_data: Optional[Dict] = None,
        places_data: Optional[List] = None
    ) -> str:
        """
        Generate a natural, helpful tourism response.
        
        Args:
            query: Original user query
            location: Extracted location
            intent_data: Intent analysis results
            weather_data: Weather information if available
            places_data: Places information if available
            
        Returns:
            Natural language response
        """
        if not self.available:
            return self._generate_template_response(location, weather_data, places_data)
        
        prompt = self._build_response_prompt(
            query, location, intent_data, weather_data, places_data
        )
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.7}  # Balanced creativity
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            print(f"LLM response generation error: {e}")
            return self._generate_template_response(location, weather_data, places_data)
    
    def _build_response_prompt(
        self, 
        query: str, 
        location: str,
        intent_data: Dict,
        weather_data: Optional[Dict],
        places_data: Optional[List]
    ) -> str:
        """Build the prompt for response generation."""
        
        # Gather available information
        info_sections = []
        
        if weather_data:
            temp = weather_data.get('temperature', 'N/A')
            rain = weather_data.get('precipitation_probability', 0)
            info_sections.append(f"Weather: {temp}°C, {rain}% chance of rain")
        
        if places_data:
            places_list = places_data[:5]  # Top 5 places
            info_sections.append(f"Tourist attractions: {', '.join(places_list)}")
        
        available_info = "\n".join(info_sections) if info_sections else "Limited information available"
        
        preferences = intent_data.get('preferences', [])
        duration = intent_data.get('duration', '')
        urgency = intent_data.get('urgency', 'casual')
        
        prompt = f"""
You are a friendly, knowledgeable tourism assistant. Generate a helpful, conversational response.

User Query: "{query}"
Location: {location}
User Preferences: {', '.join(preferences) if preferences else 'None specified'}
Trip Duration: {duration if duration else 'Not specified'}
Planning Stage: {urgency}

Available Information:
{available_info}

Guidelines:
- Be conversational and friendly
- Provide specific, actionable information
- Include practical tips when relevant
- If information is limited, acknowledge it and suggest alternatives
- Keep response concise but informative (2-3 sentences max)
- Match the user's tone and urgency level

Generate a helpful response:
"""
        return prompt
    
    def _generate_template_response(
        self, 
        location: str, 
        weather_data: Optional[Dict], 
        places_data: Optional[List]
    ) -> str:
        """Fallback template-based response when LLM is unavailable."""
        
        response_parts = []
        
        if weather_data:
            temp = weather_data.get('temperature', 'N/A')
            rain = weather_data.get('precipitation_probability', 0)
            response_parts.append(f"In {location}, it's currently {temp}°C with a {rain}% chance of rain.")
        
        if places_data:
            places_text = ", ".join(places_data[:5])
            response_parts.append(f"Here are some places you can visit: {places_text}.")
        
        if not response_parts:
            return f"I found information about {location}, but details are limited right now."
        
        return " ".join(response_parts)
    
    def generate_error_response(self, error_type: str, location: str = None) -> str:
        """Generate user-friendly error responses."""
        
        if not self.available:
            return self._template_error_response(error_type, location)
        
        error_prompts = {
            'no_location': "User didn't specify a location clearly. Ask them to clarify in a friendly way.",
            'location_not_found': f"Location '{location}' wasn't found in our databases. Suggest alternatives helpfully.",
            'api_error': "There was a technical issue getting information. Apologize and suggest trying again."
        }
        
        prompt = f"""
You are a helpful tourism assistant. {error_prompts.get(error_type, 'Handle this error gracefully.')}\n
Generate a brief, friendly response:
"""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.5}
            )
            return response['message']['content'].strip()
        except:
            return self._template_error_response(error_type, location)
    
    def _template_error_response(self, error_type: str, location: str = None) -> str:
        """Template-based error responses."""
        
        responses = {
            'no_location': "I couldn't identify a specific location in your query. Could you please tell me which place you're interested in?",
            'location_not_found': f"I couldn't find information about '{location}'. Could you check the spelling or try a nearby city?",
            'api_error': "Sorry, I'm having trouble getting information right now. Please try again in a moment."
        }
        
        return responses.get(error_type, "I encountered an issue processing your request. Please try again.")


# Example usage
if __name__ == "__main__":
    agent = LLMResponseAgent()
    
    # Test data
    test_weather = {
        'temperature': 22,
        'precipitation_probability': 10
    }
    
    test_places = [
        "Eiffel Tower",
        "Louvre Museum", 
        "Notre-Dame Cathedral",
        "Arc de Triomphe",
        "Champs-Élysées"
    ]
    
    test_intent = {
        'intents': ['weather', 'places'],
        'preferences': ['romantic'],
        'duration': 'weekend',
        'urgency': 'planning'
    }
    
    print("🤖 Testing LLM Response Agent")
    print("=" * 50)
    
    response = agent.generate_tourism_response(
        query="Planning a romantic weekend in Paris",
        location="Paris",
        intent_data=test_intent,
        weather_data=test_weather,
        places_data=test_places
    )
    
    print(f"Generated Response:\n{response}")