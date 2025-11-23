"""
Geocoding Agent - Converts place names to coordinates using Nominatim API
"""
import requests
import time
from typing import Optional, Dict, Tuple


class GeocodingAgent:
    """
    Agent responsible for geocoding place names to coordinates.
    Uses Nominatim API to get latitude and longitude.
    """
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'Tourism-AI-Agent/1.0'
        }
    
    def geocode(self, place_name: str) -> Optional[Dict[str, float]]:
        """
        Geocode a place name to get its coordinates.
        
        Args:
            place_name: Name of the place to geocode
            
        Returns:
            Dictionary with 'lat' and 'lon' keys, or None if place not found
        """
        try:
            params = {
                'q': place_name,
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            # Respect rate limiting
            time.sleep(1)
            
            if response.status_code == 200:
                # Ensure proper encoding
                response.encoding = 'utf-8'
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    display_name = result.get('display_name', place_name)
                    
                    # Clean up display name encoding
                    try:
                        import unicodedata
                        # Normalize unicode characters
                        normalized = unicodedata.normalize('NFKD', display_name)
                        # Convert to ASCII, replacing non-ASCII chars
                        clean_display_name = normalized.encode('ascii', errors='ignore').decode('ascii')
                        if len(clean_display_name.strip()) > 0:
                            display_name = clean_display_name.strip()
                    except:
                        pass
                    
                    return {
                        'lat': float(result['lat']),
                        'lon': float(result['lon']),
                        'display_name': display_name
                    }
            
            return None
            
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def get_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates as a tuple (lat, lon).
        
        Args:
            place_name: Name of the place
            
        Returns:
            Tuple of (latitude, longitude) or None
        """
        result = self.geocode(place_name)
        if result:
            return (result['lat'], result['lon'])
        return None

