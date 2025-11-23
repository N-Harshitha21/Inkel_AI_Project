"""
Tourism AI Assistant - Streamlit Web Application
Multi-Agent Tourism System with Interactive Interface
"""

import streamlit as st
import requests
import json
import sys
import os
from typing import Dict, Any
import folium
from streamlit_folium import st_folium

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.parent_agent import ParentAgent
    try:
        from agents.enhanced_parent_agent import EnhancedParentAgent
        ENHANCED_AVAILABLE = True
    except ImportError:
        ENHANCED_AVAILABLE = False
    try:
        from utils.favorites_manager import FavoritesManager
        FAVORITES_AVAILABLE = True
    except ImportError:
        FAVORITES_AVAILABLE = False
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    ENHANCED_AVAILABLE = False
    FAVORITES_AVAILABLE = False
    st.warning("⚠️ Agent modules not found. Running in demo mode.")

def display_query_result(result, query: str):
    """Display formatted query result"""
    # Handle string responses (from basic ParentAgent.process_query)
    if isinstance(result, str):
        st.markdown(f"""
        <div class="result-card">
            <p>{result}</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Handle dictionary responses
    if not isinstance(result, dict):
        st.error("Unexpected result format")
        return
        
    if result.get('type') == 'error':
        st.markdown(f'<div class="error-msg">❌ {result["response"]}</div>', unsafe_allow_html=True)
        return
    
    # Weather information
    if 'weather' in result:
        st.markdown(f"""
        <div class="result-card weather-card">
            <h4>🌤️ Weather Information</h4>
            <p>{result['weather']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Places information
    if 'places' in result:
        places_html = "<ul>"
        for place in result['places']:
            places_html += f"<li>📍 {place}</li>"
        places_html += "</ul>"
        
        st.markdown(f"""
        <div class="result-card places-card">
            <h4>🏛️ Tourist Attractions</h4>
            {places_html}
        </div>
        """, unsafe_allow_html=True)
    
    # General response (from process_query_with_map_data)
    if 'response' in result:
        st.markdown(f"""
        <div class="result-card">
            <p>{result['response']}</p>
        </div>
        """, unsafe_allow_html=True)

def extract_coordinates(result) -> tuple:
    """Extract coordinates from result for mapping"""
    if isinstance(result, dict) and 'coordinates' in result:
        coords = result['coordinates']
        if isinstance(coords, dict) and 'lat' in coords and 'lon' in coords:
            return [coords['lat'], coords['lon']]
        elif isinstance(coords, (list, tuple)) and len(coords) >= 2:
            return coords
    return None

# Page configuration
st.set_page_config(
    page_title="🌍 Tourism AI Assistant",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4facfe;
        margin: 1rem 0;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .weather-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        color: #2d3436;
    }
    .places-card {
        background: linear-gradient(135deg, #81ecec 0%, #74b9ff 100%);
        color: #2d3436;
    }
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-msg {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_system' not in st.session_state:
    if AGENTS_AVAILABLE:
        try:
            st.session_state.agent_system = ParentAgent()
            if ENHANCED_AVAILABLE:
                st.session_state.enhanced_agent = EnhancedParentAgent()
            if FAVORITES_AVAILABLE:
                st.session_state.favorites_manager = FavoritesManager()
            st.session_state.system_ready = True
        except Exception as e:
            st.session_state.system_ready = False
            st.session_state.error_message = str(e)
    else:
        st.session_state.system_ready = False

if 'query_history' not in st.session_state:
    st.session_state.query_history = []

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Header
st.markdown("""
<div class="main-header">
    <h1>🌍 Tourism AI Assistant</h1>
    <h3>Multi-Agent Tourism System</h3>
    <p>Discover weather conditions and amazing places to visit worldwide!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    # System Status
    st.subheader("📊 System Status")
    if st.session_state.get('system_ready', False):
        st.success("✅ All agents online")
        st.info(f"📈 Queries processed: {len(st.session_state.query_history)}")
    else:
        st.warning("⚠️ Running in demo mode")
    
    # Quick Examples
    st.subheader("💡 Quick Examples")
    example_queries = [
        "Mumbai tourist places",
        "Delhi weather",
        "Bangalore attractions and weather", 
        "Plan my trip to Kerala",
        "Goa beaches and climate"
    ]
    
    for query in example_queries:
        if st.button(f"📍 {query}", key=f"example_{query}"):
            st.session_state.current_query = query

    # Favorites Section
    st.subheader("⭐ Favorites")
    if st.session_state.favorites:
        for idx, fav in enumerate(st.session_state.favorites):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(fav.get('name', 'Unnamed'))
            with col2:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.favorites.pop(idx)
                    st.rerun()
    else:
        st.info("No favorites yet")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Ask Tourism AI")
    
    # Query input
    query_input = st.text_input(
        "Enter your tourism query:",
        value=st.session_state.get('current_query', ''),
        placeholder="Ask about places, weather, or travel planning...",
        key="main_query"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    with col_btn2:
        if ENHANCED_AVAILABLE:
            enhanced_search = st.button("🚀 Enhanced AI", use_container_width=True)
        else:
            enhanced_search = False
            st.button("🚀 Enhanced AI (Unavailable)", use_container_width=True, disabled=True)
    
    with col_btn3:
        clear_button = st.button("🗑️ Clear History", use_container_width=True)

    if clear_button:
        st.session_state.query_history = []
        st.rerun()

    # Process query
    if (search_button or enhanced_search) and query_input:
        with st.spinner("🤖 Processing your tourism query..."):
            try:
                if st.session_state.get('system_ready', False):
                    # Use real agents
                    if enhanced_search and ENHANCED_AVAILABLE and hasattr(st.session_state, 'enhanced_agent'):
                        agent = st.session_state.enhanced_agent
                        result = agent.process_query(query_input)
                    else:
                        # Use basic agent with map data for better integration
                        agent = st.session_state.agent_system
                        result = agent.process_query_with_map_data(query_input)
                else:
                    # Demo mode with sample data
                    result = get_demo_response(query_input)
                
                # Add to history
                st.session_state.query_history.insert(0, {
                    'query': query_input,
                    'result': result,
                    'enhanced': enhanced_search and ENHANCED_AVAILABLE
                })
                
                # Keep only last 10 queries
                st.session_state.query_history = st.session_state.query_history[:10]
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    # Display results
    if st.session_state.query_history:
        st.header("📋 Query Results")
        
        for idx, item in enumerate(st.session_state.query_history):
            with st.expander(
                f"{'🚀' if item['enhanced'] else '🔍'} {item['query'][:50]}..." if len(item['query']) > 50 else f"{'🚀' if item['enhanced'] else '🔍'} {item['query']}",
                expanded=(idx == 0)
            ):
                display_query_result(item['result'], item['query'])

with col2:
    st.header("🗺️ Interactive Map")
    
    # Create map
    if st.session_state.query_history:
        latest_result = st.session_state.query_history[0]['result']
        coordinates = extract_coordinates(latest_result)
        
        if coordinates:
            # Create Folium map
            m = folium.Map(
                location=coordinates,
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Add marker for main location
            folium.Marker(
                coordinates,
                popup=st.session_state.query_history[0]['query'],
                tooltip="Main Location",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Add markers for places if available
            if isinstance(latest_result, dict) and 'places_data' in latest_result:
                for place in latest_result.get('places_data', []):
                    if isinstance(place, dict) and 'lat' in place and 'lon' in place:
                        folium.Marker(
                            [place['lat'], place['lon']],
                            popup=place.get('name', 'Tourist Attraction'),
                            tooltip=place.get('name', 'Attraction'),
                            icon=folium.Icon(color='green', icon='star')
                        ).add_to(m)
            
            # Display map
            map_data = st_folium(m, height=400, width=None)
            
            # Add to favorites option
            if FAVORITES_AVAILABLE and st.button("⭐ Add to Favorites"):
                favorite = {
                    'name': st.session_state.query_history[0]['query'],
                    'coordinates': coordinates,
                    'result': latest_result
                }
                if 'favorites' not in st.session_state:
                    st.session_state.favorites = []
                st.session_state.favorites.append(favorite)
                st.success("Added to favorites!")
                st.rerun()
        else:
            st.info("🗺️ Map will appear when you search for a location")
    else:
        # Default map
        default_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        st_folium(default_map, height=400, width=None)

# Functions
def get_demo_response(query: str) -> Dict[str, Any]:
    """Generate demo response when agents are not available"""
    query_lower = query.lower()
    
    # Sample data
    demo_data = {
        'mumbai': {
            'weather': "In Mumbai it's currently 28°C with a chance of 15% to rain.",
            'places': ['Gateway of India', 'Marine Drive', 'Chhatrapati Shivaji Terminus', 'Elephanta Caves', 'Juhu Beach'],
            'coordinates': [19.0760, 72.8777]
        },
        'delhi': {
            'weather': "In Delhi it's currently 22°C with a chance of 5% to rain.",
            'places': ['Red Fort', 'India Gate', 'Qutub Minar', 'Lotus Temple', 'Humayuns Tomb'],
            'coordinates': [28.6139, 77.2090]
        },
        'bangalore': {
            'weather': "In Bangalore it's currently 24°C with a chance of 20% to rain.",
            'places': ['Lalbagh Botanical Garden', 'Bangalore Palace', 'Bannerghatta National Park', 'ISKCON Temple', 'Tipu Sultan Palace'],
            'coordinates': [12.9716, 77.5946]
        }
    }
    
    # Find matching city
    city = None
    for city_name in demo_data.keys():
        if city_name in query_lower:
            city = city_name
            break
    
    if not city:
        return {
            'response': "I don't know this place exists. Could you please provide a valid place name like Mumbai, Delhi, or Bangalore?",
            'type': 'error'
        }
    
    data = demo_data[city]
    wants_weather = any(word in query_lower for word in ['weather', 'temperature', 'climate'])
    wants_places = any(word in query_lower for word in ['places', 'attractions', 'visit', 'trip'])
    
    if not wants_weather and not wants_places:
        wants_weather = wants_places = True
    
    response_parts = []
    result = {'type': 'success', 'city': city.title(), 'coordinates': data['coordinates']}
    
    if wants_weather:
        response_parts.append(data['weather'])
        result['weather'] = data['weather']
    
    if wants_places:
        places_text = f"These are the places you can go in {city.title()}: " + ", ".join(data['places'])
        response_parts.append(places_text)
        result['places'] = data['places']
    
    result['response'] = " ".join(response_parts)
    return result

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🤖 Powered by Multi-Agent AI**")
    st.caption("Weather • Places • Geocoding")

with col2:
    st.markdown("**🌐 Data Sources**")
    st.caption("Open-Meteo • OpenStreetMap • Nominatim")

with col3:
    st.markdown("**🚀 Deployment Ready**")
    st.caption("Streamlit Cloud • Local • Docker")