# New Features: Map Integration & Favorites

## 🗺️ Map Integration

The system now includes interactive map visualization using Leaflet.js:

### Features:
- **Interactive Map**: Visual display of searched locations
- **Location Markers**: Main location marked in red, tourist attractions in blue
- **Automatic Zoom**: Map centers on the searched location
- **Tourist Attractions**: All found places are marked on the map with clickable popups

### API Endpoint:
- `POST /query/map` - Returns query results with coordinates for map integration

### Response Format:
```json
{
  "response": "Formatted text response",
  "place_name": "Location name",
  "coordinates": {"lat": 12.9716, "lon": 77.5946},
  "weather_data": {...},
  "places_data": [
    {"name": "Place 1", "lat": 12.97, "lon": 77.59},
    ...
  ]
}
```

## ⭐ Favorites System

Users can now save their favorite places for quick access:

### Features:
- **Save Favorites**: Add any searched location to favorites
- **View Favorites**: See all saved places with coordinates
- **Remove Favorites**: Delete favorites you no longer need
- **Persistent Storage**: Favorites are saved in `favorites.json`

### API Endpoints:

1. **Get All Favorites**
   - `GET /favorites`
   - Returns list of all saved favorites

2. **Add Favorite**
   - `POST /favorites`
   - Body: `{place_name, coordinates, weather_data, places_data}`
   - Adds a new favorite

3. **Add from Query**
   - `POST /favorites/add-from-query`
   - Body: `{query: "..."}`
   - Processes query and automatically adds to favorites

4. **Remove Favorite**
   - `DELETE /favorites/{id}`
   - Removes a favorite by ID

### Storage:
Favorites are stored in `favorites.json` in the project root with the following structure:
```json
[
  {
    "id": 1,
    "place_name": "Bangalore",
    "coordinates": {"lat": 12.9716, "lon": 77.5946},
    "weather_data": {...},
    "places_data": [...]
  }
]
```

## 🎨 Frontend Interface

A beautiful web interface has been created at `frontend/index.html`:

### Features:
- **Modern UI**: Gradient design with responsive layout
- **Interactive Map**: Real-time map updates with markers
- **Query Interface**: Easy-to-use search bar
- **Favorites Panel**: View and manage saved places
- **Real-time Updates**: Instant feedback on all actions

### How to Use:

1. **Start the API Server**:
   ```bash
   cd api
   python main.py
   ```

2. **Open the Frontend**:
   - Open `frontend/index.html` in your web browser
   - Or serve it with a simple HTTP server:
     ```bash
     cd frontend
     python -m http.server 8080
     ```
     Then visit `http://localhost:8080`

3. **Use the Interface**:
   - Enter a query in the search box
   - Click "Search" to get results
   - View the map with markers
   - Click "Add to Favorites" to save
   - Manage favorites in the bottom panel

## 🔧 Technical Details

### Enhanced Agents:

1. **Places Agent**:
   - New method: `get_tourist_places_with_coords()`
   - Returns places with coordinates for map integration

2. **Parent Agent**:
   - New method: `process_query_with_map_data()`
   - Returns comprehensive data including coordinates

### New Utilities:

- **FavoritesManager** (`utils/favorites_manager.py`):
  - Handles all favorites operations
  - JSON-based storage
  - CRUD operations for favorites

## 📝 Example Usage

### Using the API:

```python
import requests

# Query with map data
response = requests.post("http://localhost:8000/query/map", 
    json={"query": "I'm going to Bangalore, what's the weather?"})
data = response.json()

# Add to favorites
requests.post("http://localhost:8000/favorites/add-from-query",
    json={"query": "I'm going to Bangalore, what's the weather?"})

# Get all favorites
favorites = requests.get("http://localhost:8000/favorites").json()
```

## 🚀 Benefits

1. **Visual Understanding**: Maps help users understand location context
2. **Quick Access**: Favorites allow users to quickly revisit places
3. **Better UX**: Interactive interface makes the system more user-friendly
4. **Data Persistence**: Favorites are saved between sessions

## 📋 Future Enhancements

Potential additions:
- User authentication for multiple users
- Share favorites with friends
- Export favorites to CSV/JSON
- Route planning between favorites
- Weather alerts for favorite places
- Integration with calendar for trip planning

