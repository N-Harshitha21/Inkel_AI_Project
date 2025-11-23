"""
Parent Agent - Orchestrates the multi-agent tourism system
"""
import re
from typing import Dict, Optional, List
from .geocoding_agent import GeocodingAgent
from .weather_agent import WeatherAgent
from .places_agent import PlacesAgent


class ParentAgent:
    """
    Main orchestrator agent that coordinates all child agents.
    Analyzes user input and delegates tasks to appropriate agents.
    """
    
    def __init__(self):
        self.geocoding_agent = GeocodingAgent()
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
    
    def extract_place_name(self, user_input: str) -> Optional[str]:
        """
        Extract place name from user input using simple pattern matching.
        
        Args:
            user_input: User's input text
            
        Returns:
            Extracted place name or None
        """
        # Common patterns for place mentions
        patterns = [
            r"going to (?:go to |visit )?([A-Z][a-zA-Z\s]+?)(?:,|\.|$)",
            r"in ([A-Z][a-zA-Z\s]+?)(?:,|\.|$)",
            r"to ([A-Z][a-zA-Z\s]+?)(?:,|\.|$)",
            r"visit ([A-Z][a-zA-Z\s]+?)(?:,|\.|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                place = match.group(1).strip()
                # Clean up common words
                place = re.sub(r'\s+(the|a|an)\s+', ' ', place, flags=re.IGNORECASE)
                return place.strip()
        
        # Fallback: look for capitalized words (likely place names)
        words = user_input.split()
        capitalized = [w for w in words if w[0].isupper() and len(w) > 2]
        if capitalized:
            return ' '.join(capitalized[:3])  # Take first few capitalized words
        
        return None
    
    def detect_intent(self, user_input: str) -> Dict[str, bool]:
        """
        Detect user intent from input.
        
        Args:
            user_input: User's input text
            
        Returns:
            Dictionary with 'weather' and 'places' boolean flags
        """
        user_lower = user_input.lower()
        
        weather_keywords = ['temperature', 'weather', 'rain', 'hot', 'cold', 'forecast', 'temp']
        places_keywords = ['places', 'visit', 'attractions', 'tourist', 'sightseeing', 'plan', 'trip', 'tour', 'destination']
        
        # More precise matching - avoid matching "go" in "going to"
        wants_weather = any(keyword in user_lower for keyword in weather_keywords)
        # Check for places keywords, but exclude "go" if it's part of "going to"
        wants_places = any(keyword in user_lower for keyword in places_keywords)
        # Also check for "can visit" or "can go" patterns
        if 'can visit' in user_lower or 'can go' in user_lower or 'places i can' in user_lower:
            wants_places = True
        
        # If no specific intent detected, check for implicit intent
        if not wants_weather and not wants_places:
            # If user mentions "plan" or "trip", default to places
            if 'plan' in user_lower or 'trip' in user_lower:
                wants_places = True
            else:
                # Otherwise default to both
                wants_weather = True
                wants_places = True
        
        return {
            'weather': wants_weather,
            'places': wants_places
        }
    
    def process_query(self, user_input: str) -> str:
        """
        Main method to process user query and coordinate agents.
        
        Args:
            user_input: User's input text
            
        Returns:
            Formatted response string
        """
        # Extract place name
        place_name = self.extract_place_name(user_input)
        
        if not place_name:
            return "I couldn't identify a place name in your query. Please specify a location."
        
        # Geocode the place
        geocode_result = self.geocoding_agent.geocode(place_name)
        
        if not geocode_result:
            return f"I don't know this place exists. Could you please provide a valid place name?"
        
        lat = geocode_result['lat']
        lon = geocode_result['lon']
        display_name = geocode_result.get('display_name', place_name)
        
        # Detect user intent
        intent = self.detect_intent(user_input)
        
        responses = []
        
        # Get weather if requested
        if intent['weather']:
            weather_data = self.weather_agent.get_weather(lat, lon)
            weather_response = self.weather_agent.format_weather_response(
                weather_data, display_name
            )
            responses.append(weather_response)
        
        # Get places if requested
        if intent['places']:
            places = self.places_agent.get_tourist_places(lat, lon, limit=5)
            places_response = self.places_agent.format_places_response(
                places, display_name
            )
            responses.append(places_response)
        
        # Combine responses
        if len(responses) == 2:
            # If both weather and places, combine them naturally
            # Extract the places part without the "In [place] these are..." prefix
            places_text = responses[1]
            if places_text.startswith(f"In {display_name} these are the places you can go,\n"):
                places_list = places_text.replace(f"In {display_name} these are the places you can go,\n", "")
                return f"{responses[0]} And these are the places you can go:\n{places_list}"
            return f"{responses[0]} And {responses[1].lower()}"
        elif responses:
            return responses[0]
        else:
            return f"Unable to process your query for {display_name}."
    
    def process_query_with_map_data(self, user_input: str) -> Dict:
        """
        Process query and return data including coordinates for map integration.
        
        Args:
            user_input: User's input text
            
        Returns:
            Dictionary with response, place_name, coordinates, weather_data, and places_data
        """
        # Extract place name
        place_name = self.extract_place_name(user_input)
        
        if not place_name:
            return {
                'response': "I couldn't identify a place name in your query. Please specify a location.",
                'place_name': None,
                'coordinates': None,
                'weather_data': None,
                'places_data': []
            }
        
        # Geocode the place
        geocode_result = self.geocoding_agent.geocode(place_name)
        
        if not geocode_result:
            return {
                'response': f"I don't know this place exists. Could you please provide a valid place name?",
                'place_name': place_name,
                'coordinates': None,
                'weather_data': None,
                'places_data': []
            }
        
        lat = geocode_result['lat']
        lon = geocode_result['lon']
        display_name = geocode_result.get('display_name', place_name)
        
        # Detect user intent
        intent = self.detect_intent(user_input)
        
        responses = []
        weather_data = None
        places_data = []
        
        # Get weather if requested
        if intent['weather']:
            weather_data = self.weather_agent.get_weather(lat, lon)
            weather_response = self.weather_agent.format_weather_response(
                weather_data, display_name
            )
            responses.append(weather_response)
        
        # Get places if requested
        if intent['places']:
            places_data = self.places_agent.get_tourist_places_with_coords(lat, lon, limit=5)
            places = [p['name'] for p in places_data]
            places_response = self.places_agent.format_places_response(
                places, display_name
            )
            responses.append(places_response)
        
        # Combine responses
        if len(responses) == 2:
            places_text = responses[1]
            if places_text.startswith(f"In {display_name} these are the places you can go,\n"):
                places_list = places_text.replace(f"In {display_name} these are the places you can go,\n", "")
                response_text = f"{responses[0]} And these are the places you can go:\n{places_list}"
            else:
                response_text = f"{responses[0]} And {responses[1].lower()}"
        elif responses:
            response_text = responses[0]
        else:
            response_text = f"Unable to process your query for {display_name}."
        
        return {
            'response': response_text,
            'place_name': display_name,
            'coordinates': {'lat': lat, 'lon': lon},
            'weather_data': weather_data,
            'places_data': places_data
        }

