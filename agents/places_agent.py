"""
Places Agent - Fetches tourist attractions using Overpass API
"""
import requests
from typing import Optional, List, Dict


class PlacesAgent:
    """
    Agent responsible for finding tourist attractions and places of interest.
    Uses Overpass API to query OpenStreetMap data.
    """
    
    def __init__(self):
        self.base_url = "https://overpass-api.de/api/interpreter"
    
    def get_tourist_places(self, latitude: float, longitude: float, limit: int = 5) -> List[str]:
        """
        Get tourist attractions near given coordinates.
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            limit: Maximum number of places to return (default: 5)
            
        Returns:
            List of place names
        """
        places_data = self.get_tourist_places_with_coords(latitude, longitude, limit)
        return [place['name'] for place in places_data]
    
    def get_tourist_places_with_coords(self, latitude: float, longitude: float, limit: int = 5) -> List[Dict]:
        """
        Get tourist attractions with coordinates for map integration.
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            limit: Maximum number of places to return (default: 5)
            
        Returns:
            List of dictionaries with 'name', 'lat', 'lon' keys
        """
        try:
            # Overpass QL query to find tourist attractions
            # Searches for places with tourism tags within ~10km radius
            # Also includes leisure=park and historic tags for better coverage
            query = f"""
            [out:json][timeout:15];
            (
              node["tourism"](around:10000,{latitude},{longitude});
              way["tourism"](around:10000,{latitude},{longitude});
              relation["tourism"](around:10000,{latitude},{longitude});
              node["leisure"~"^(park|theme_park)$"](around:10000,{latitude},{longitude});
              way["leisure"~"^(park|theme_park)$"](around:10000,{latitude},{longitude});
              node["historic"](around:10000,{latitude},{longitude});
              way["historic"](around:10000,{latitude},{longitude});
            );
            out body;
            >;
            out skel qt;
            """
            
            response = requests.post(
                self.base_url,
                data={'data': query},
                timeout=15
            )
            
            if response.status_code == 200:
                # Ensure proper encoding
                response.encoding = 'utf-8'
                data = response.json()
                places = []
                seen_names = set()
                
                # Extract place names and coordinates from elements
                for element in data.get('elements', []):
                    tags = element.get('tags', {})
                    name = tags.get('name')
                    
                    if not name or name in seen_names:
                        continue
                    
                    # Clean up the name - handle encoding issues
                    try:
                        # Convert to ASCII, replacing problematic characters
                        import unicodedata
                        # Normalize unicode characters
                        normalized = unicodedata.normalize('NFKD', name)
                        # Convert to ASCII, replacing non-ASCII chars
                        ascii_name = normalized.encode('ascii', errors='ignore').decode('ascii')
                        
                        # If we lost too much content, skip this entry
                        if len(ascii_name.strip()) < 3:
                            continue
                            
                        name = ascii_name.strip()
                        
                        # Additional cleanup - remove extra spaces
                        name = ' '.join(name.split())
                        
                    except Exception as e:
                        continue
                    
                    # Get coordinates
                    if 'lat' in element and 'lon' in element:
                        lat = element['lat']
                        lon = element['lon']
                    elif 'center' in element:
                        lat = element['center']['lat']
                        lon = element['center']['lon']
                    else:
                        # For ways/relations, use the first node's coordinates
                        continue
                    
                    places.append({
                        'name': name,
                        'lat': lat,
                        'lon': lon
                    })
                    seen_names.add(name)
                    
                    if len(places) >= limit:
                        break
                
                return places[:limit]
            
            return []
            
        except Exception as e:
            print(f"Places API error: {e}")
            return []
    
    def format_places_response(self, places: List[str], place_name: str) -> str:
        """
        Format places list into a user-friendly response.
        
        Args:
            places: List of place names
            place_name: Name of the location
            
        Returns:
            Formatted string response
        """
        if not places:
            return f"Unable to find tourist attractions in {place_name}."
        
        response = f"In {place_name} these are the places you can go,\n"
        for place in places:
            response += f"- {place}\n"
        
        return response.strip()

