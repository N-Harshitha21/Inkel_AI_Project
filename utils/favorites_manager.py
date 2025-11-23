"""
Favorites Manager - Handles user favorites storage and retrieval
"""
import json
import os
from typing import List, Dict, Optional
from pathlib import Path


class FavoritesManager:
    """
    Manages user favorites using JSON file storage.
    """
    
    def __init__(self, storage_file: str = "favorites.json"):
        """
        Initialize favorites manager.
        
        Args:
            storage_file: Path to JSON file for storing favorites
        """
        self.storage_file = storage_file
        self.favorites: List[Dict] = []
        self.load_favorites()
    
    def load_favorites(self):
        """Load favorites from JSON file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.favorites = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.favorites = []
        else:
            self.favorites = []
    
    def save_favorites(self):
        """Save favorites to JSON file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving favorites: {e}")
    
    def add_favorite(self, place_name: str, coordinates: Dict, weather_data: Optional[Dict] = None, places_data: Optional[List] = None) -> Dict:
        """
        Add a place to favorites.
        
        Args:
            place_name: Name of the place
            coordinates: Dictionary with 'lat' and 'lon'
            weather_data: Optional weather data
            places_data: Optional list of tourist places
            
        Returns:
            Dictionary with success status and favorite data
        """
        # Check if already exists
        for fav in self.favorites:
            if fav['place_name'].lower() == place_name.lower():
                return {
                    'success': False,
                    'message': 'Place already in favorites',
                    'favorite': fav
                }
        
        favorite = {
            'id': len(self.favorites) + 1,
            'place_name': place_name,
            'coordinates': coordinates,
            'weather_data': weather_data,
            'places_data': places_data or [],
            'created_at': None  # Could add timestamp if needed
        }
        
        self.favorites.append(favorite)
        self.save_favorites()
        
        return {
            'success': True,
            'message': 'Place added to favorites',
            'favorite': favorite
        }
    
    def get_favorites(self) -> List[Dict]:
        """Get all favorites."""
        return self.favorites
    
    def get_favorite(self, favorite_id: int) -> Optional[Dict]:
        """Get a specific favorite by ID."""
        for fav in self.favorites:
            if fav['id'] == favorite_id:
                return fav
        return None
    
    def remove_favorite(self, favorite_id: int) -> Dict:
        """
        Remove a favorite by ID.
        
        Args:
            favorite_id: ID of the favorite to remove
            
        Returns:
            Dictionary with success status
        """
        original_count = len(self.favorites)
        self.favorites = [f for f in self.favorites if f['id'] != favorite_id]
        
        if len(self.favorites) < original_count:
            self.save_favorites()
            return {
                'success': True,
                'message': 'Favorite removed successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Favorite not found'
            }
    
    def remove_favorite_by_name(self, place_name: str) -> Dict:
        """
        Remove a favorite by place name.
        
        Args:
            place_name: Name of the place to remove
            
        Returns:
            Dictionary with success status
        """
        original_count = len(self.favorites)
        self.favorites = [f for f in self.favorites if f['place_name'].lower() != place_name.lower()]
        
        if len(self.favorites) < original_count:
            self.save_favorites()
            return {
                'success': True,
                'message': 'Favorite removed successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Favorite not found'
            }

