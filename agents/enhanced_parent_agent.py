"""
Enhanced Parent Agent with LLM Integration
Combines traditional API-based agents with LLM-powered natural language understanding
"""
import os
from typing import Dict, Optional, List
from .geocoding_agent import GeocodingAgent
from .weather_agent import WeatherAgent
from .places_agent import PlacesAgent

# LLM agents (optional if Ollama is available)
try:
    from .llm_intent_agent import LLMIntentAgent
    from .llm_response_agent import LLMResponseAgent
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

class EnhancedParentAgent:
    """
    Enhanced orchestrator that uses LLMs for better intent detection and response generation.
    Falls back to traditional methods if LLMs are unavailable.
    """
    
    def __init__(self, use_llm: bool = True):
        # Traditional agents (always available)
        self.geocoding_agent = GeocodingAgent()
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
        
        # LLM agents (optional)
        self.use_llm = use_llm and LLM_AVAILABLE
        if self.use_llm:
            try:
                self.llm_intent_agent = LLMIntentAgent(model="phi3:mini")
                self.llm_response_agent = LLMResponseAgent(model="phi3:mini")
                print("✅ LLM agents initialized successfully!")
            except Exception as e:
                print(f"⚠️  LLM initialization failed: {e}")
                self.use_llm = False
        
        if not self.use_llm:
            print("🔄 Using traditional regex-based processing")
    
    def process_query(self, user_input: str) -> str:
        """
        Process user query with enhanced LLM capabilities or traditional fallback.
        """
        if self.use_llm:
            return self._process_with_llm(user_input)
        else:
            return self._process_traditional(user_input)
    
    def _process_with_llm(self, user_input: str) -> str:
        """Process query using LLM-powered intent detection and response generation."""
        try:
            # Step 1: LLM Intent Analysis
            intent_analysis = self.llm_intent_agent.analyze_query(user_input)
            
            if not intent_analysis.get("success", False):
                # Fallback to traditional if LLM fails
                return self._process_traditional(user_input)
            
            location = intent_analysis.get("location")
            intents = intent_analysis.get("intents", [])
            
            if not location:
                return "I couldn't identify a location in your query. Could you please specify where you'd like to go?"
            
            # Step 2: Get coordinates
            geocode_result = self.geocoding_agent.geocode(location)
            if not geocode_result:
                return f"I couldn't find information for '{location}'. Please check the spelling or try a different location."
            
            lat = geocode_result['lat']
            lon = geocode_result['lon']
            display_name = geocode_result.get('display_name', location)
            
            # Step 3: Gather data based on intents
            data = {
                'location': display_name,
                'coordinates': {'lat': lat, 'lon': lon},
                'weather_data': None,
                'places_data': None
            }
            
            # Get weather if needed
            if 'weather' in intents:
                weather_data = self.weather_agent.get_weather(lat, lon)
                data['weather_data'] = weather_data
            
            # Get places if needed
            if 'places' in intents or 'attractions' in intents:
                places = self.places_agent.get_tourist_places(lat, lon, limit=5)
                data['places_data'] = places
            
            # Step 4: Generate natural language response using LLM
            response = self.llm_response_agent.generate_response(
                query=user_input,
                intent_analysis=intent_analysis,
                data=data
            )
            
            return response
            
        except Exception as e:
            print(f"LLM processing error: {e}")
            # Fallback to traditional processing
            return self._process_traditional(user_input)
    
    def _process_traditional(self, user_input: str) -> str:
        """Traditional processing (your existing logic)."""
        from .parent_agent import ParentAgent
        traditional_agent = ParentAgent()
        return traditional_agent.process_query(user_input)
    
    def process_query_with_map_data(self, user_input: str) -> Dict:
        """
        Enhanced version with map data for frontend integration.
        """
        if self.use_llm:
            return self._process_with_map_data_llm(user_input)
        else:
            from .parent_agent import ParentAgent
            traditional_agent = ParentAgent()
            return traditional_agent.process_query_with_map_data(user_input)
    
    def _process_with_map_data_llm(self, user_input: str) -> Dict:
        """Process query with LLM and return structured data for map integration."""
        try:
            # Get LLM analysis
            intent_analysis = self.llm_intent_agent.analyze_query(user_input)
            
            if not intent_analysis.get("success", False):
                return {
                    'response': "I couldn't understand your query. Please try rephrasing it.",
                    'place_name': None,
                    'coordinates': None,
                    'weather_data': None,
                    'places_data': []
                }
            
            location = intent_analysis.get("location")
            intents = intent_analysis.get("intents", [])
            
            # Get coordinates
            geocode_result = self.geocoding_agent.geocode(location)
            if not geocode_result:
                return {
                    'response': f"I couldn't find '{location}'. Please check the spelling.",
                    'place_name': location,
                    'coordinates': None,
                    'weather_data': None,
                    'places_data': []
                }
            
            lat = geocode_result['lat']
            lon = geocode_result['lon']
            display_name = geocode_result.get('display_name', location)
            
            # Gather data
            weather_data = None
            places_data = []
            
            if 'weather' in intents:
                weather_data = self.weather_agent.get_weather(lat, lon)
            
            if 'places' in intents or 'attractions' in intents:
                places_data = self.places_agent.get_tourist_places_with_coords(lat, lon, limit=5)
            
            # Generate response
            data = {
                'location': display_name,
                'coordinates': {'lat': lat, 'lon': lon},
                'weather_data': weather_data,
                'places_data': places_data
            }
            
            response = self.llm_response_agent.generate_response(
                query=user_input,
                intent_analysis=intent_analysis,
                data=data
            )
            
            return {
                'response': response,
                'place_name': display_name,
                'coordinates': {'lat': lat, 'lon': lon},
                'weather_data': weather_data,
                'places_data': places_data
            }
            
        except Exception as e:
            print(f"LLM processing error: {e}")
            # Fallback to traditional
            from .parent_agent import ParentAgent
            traditional_agent = ParentAgent()
            return traditional_agent.process_query_with_map_data(user_input)
    
    def get_system_status(self) -> Dict:
        """Get status of all system components."""
        return {
            "llm_available": self.use_llm,
            "traditional_agents": {
                "geocoding": True,
                "weather": True,
                "places": True
            },
            "llm_agents": {
                "intent": self.use_llm,
                "response": self.use_llm
            }
        }