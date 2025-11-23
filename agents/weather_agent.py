"""
Weather Agent - Fetches current weather and forecast using Open-Meteo API
"""
import requests
from typing import Optional, Dict
from datetime import datetime


class WeatherAgent:
    """
    Agent responsible for fetching weather information.
    Uses Open-Meteo API to get current weather and forecasts.
    """
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Get current weather for given coordinates.
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            
        Returns:
            Dictionary with weather information or None if error
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,precipitation_probability',
                'timezone': 'auto'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                
                return {
                    'temperature': current.get('temperature_2m'),
                    'precipitation_probability': current.get('precipitation_probability'),
                    'time': current.get('time')
                }
            
            return None
            
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def format_weather_response(self, weather_data: Dict, place_name: str) -> str:
        """
        Format weather data into a user-friendly response.
        
        Args:
            weather_data: Weather data dictionary
            place_name: Name of the place
            
        Returns:
            Formatted string response
        """
        if not weather_data:
            return f"Unable to fetch weather information for {place_name}."
        
        temp = weather_data.get('temperature')
        rain_chance = weather_data.get('precipitation_probability', 0)
        
        if temp is not None:
            return f"In {place_name} it's currently {int(temp)}C with a chance of {int(rain_chance)}% to rain."
        else:
            return f"Unable to fetch weather information for {place_name}."

