"""
Enhanced LLM Response Generation Agent with Tourism-Specific Prompts
"""
from typing import Dict, List, Optional, Any
from .tourism_prompts import TourismPrompts

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class EnhancedLLMResponseAgent:
    """
    Advanced LLM response generator with tourism-specific prompts and caching.
    """
    
    def __init__(self, model: str = "qwen2.5:0.5b"):
        self.model = model
        self.available = OLLAMA_AVAILABLE and self._test_model()
        self.response_cache = {}  # Simple in-memory cache
        
        if not self.available:
            print(f"⚠️  Enhanced LLM Response Generator not available.")
    
    def _test_model(self) -> bool:
        """Test if the model is available."""
        try:
            ollama.chat(model=self.model, messages=[
                {"role": "user", "content": "test"}
            ])
            return True
        except:
            return False
    
    def generate_response(self, query: str, intent_analysis: Dict, data: Dict) -> str:
        """
        Generate contextual response using tourism-specific prompts.
        
        Args:
            query: Original user query
            intent_analysis: Results from intent analysis
            data: Gathered tourism data (weather, places, etc.)
            
        Returns:
            Natural language response
        """
        if not self.available:
            return self._fallback_response(query, data)
        
        try:
            # Create cache key for potential reuse
            cache_key = self._create_cache_key(query, intent_analysis, data)
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]
            
            # Select appropriate prompt template
            prompt_template = TourismPrompts.get_response_prompt(intent_analysis)
            
            # Format prompt with context
            formatted_prompt = TourismPrompts.format_prompt(
                prompt_template,
                location=data.get('location', 'the destination'),
                weather_info=self._format_weather_info(data.get('weather_data')),
                places_info=self._format_places_info(data.get('places_data')),
                special_context=intent_analysis.get('special_context', 'general travel'),
                group_info=intent_analysis.get('group_info', {}),
                preferences=intent_analysis.get('preferences', {}),
                budget_info=intent_analysis.get('preferences', {}).get('budget', 'not specified')
            )
            
            # Add user query context
            full_prompt = f"""
{formatted_prompt}

Original query: "{query}"

Generate a helpful, personalized response that directly addresses the user's question while incorporating the weather and places information provided. Keep the response conversational and engaging.
"""
            
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                options={
                    "temperature": 0.7,  # More creative for responses
                    "top_p": 0.9,
                    "max_tokens": 2000
                }
            )
            
            generated_response = response['message']['content'].strip()
            
            # Cache the response
            self.response_cache[cache_key] = generated_response
            
            return generated_response
            
        except Exception as e:
            print(f"Enhanced LLM response generation error: {e}")
            return self._fallback_response(query, data)
    
    def _create_cache_key(self, query: str, intent_analysis: Dict, data: Dict) -> str:
        """Create a cache key for the response."""
        import hashlib
        
        key_components = [
            query.lower(),
            data.get('location', ''),
            str(intent_analysis.get('special_context', '')),
            str(intent_analysis.get('group_info', {}).get('type', ''))
        ]
        
        key_string = '|'.join(key_components)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _format_weather_info(self, weather_data: Optional[Dict]) -> str:
        """Format weather data for prompt inclusion."""
        if not weather_data:
            return "Weather information not available"
        
        temp = weather_data.get('temperature', 'N/A')
        precipitation = weather_data.get('precipitation_probability', 0)
        
        return f"Current temperature: {temp}°C, Chance of precipitation: {precipitation}%"
    
    def _format_places_info(self, places_data: Optional[List]) -> str:
        """Format places data for prompt inclusion."""
        if not places_data:
            return "No specific attractions data available"
        
        if isinstance(places_data[0], dict):
            # Places with coordinates
            places_list = [place['name'] for place in places_data[:5]]
        else:
            # Simple places list
            places_list = places_data[:5]
        
        return "Available attractions: " + ", ".join(places_list)
    
    def _fallback_response(self, query: str, data: Dict) -> str:
        """Generate fallback response without LLM."""
        location = data.get('location', 'your destination')
        weather_info = self._format_weather_info(data.get('weather_data'))
        places_info = self._format_places_info(data.get('places_data'))
        
        return f"""Here's what I found for {location}:

Weather: {weather_info}

{places_info}

I hope this helps with your travel planning! For more detailed recommendations, please let me know your specific interests or what type of experience you're looking for."""
    
    def clear_cache(self):
        """Clear the response cache."""
        self.response_cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "cache_size": len(self.response_cache),
            "available": self.available,
            "model": self.model
        }


# Backwards compatibility
class LLMResponseAgent(EnhancedLLMResponseAgent):
    """Alias for backwards compatibility."""
    pass