# Multi-Agent Tourism System

A sophisticated AI-powered tourism assistant that uses multiple specialized agents to provide weather information and tourist attraction recommendations for any location.

## 📋 Project Overview

This project implements a **multi-agent system** where specialized AI agents work together to help users plan their trips. The system can:
- Get current weather information for any place
- Find up to 5 tourist attractions in a location
- Handle both weather and places queries simultaneously
- Gracefully handle invalid or non-existent places

## 🎯 High-Level Goal

**What the user should ultimately be able to do:**
Users can input natural language queries about places they want to visit, and the system will automatically:
1. Identify the place name from the query
2. Get coordinates using geocoding
3. Fetch weather information (if requested)
4. Find tourist attractions (if requested)
5. Return a formatted, user-friendly response

## 🤖 How the Multi-Agent System Works

The system uses a **hierarchical agent architecture**:

1. **Parent Agent (Orchestrator)**: Analyzes user input, extracts place names, detects intent, and coordinates child agents
2. **Geocoding Agent**: Converts place names to coordinates using Nominatim API
3. **Weather Agent**: Fetches current weather using Open-Meteo API
4. **Places Agent**: Finds tourist attractions using Overpass API (OpenStreetMap)

### Communication Flow:
```
User Input → Parent Agent → [Extract Place] → Geocoding Agent
                                    ↓
                            [Get Coordinates]
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
            Weather Agent                    Places Agent
                    ↓                               ↓
            [Get Weather]                    [Get Places]
                    └───────────────┬───────────────┘
                                    ↓
                            [Format Response]
                                    ↓
                            User Output
```

## 📊 Does This Project Need a Dataset?

**No, this project does not need a dataset.**

### Why?
- **Real-time API Integration**: The system uses live APIs that provide current data:
  - **Open-Meteo API**: Provides real-time weather data
  - **Overpass API**: Queries OpenStreetMap's live database of places
  - **Nominatim API**: Uses OpenStreetMap's geocoding database
  
- **No Training Required**: The agents use rule-based logic and API calls rather than machine learning models that would require training data.

- **Dynamic Information**: Weather and places data change frequently, so using live APIs ensures users always get current information.

## 🔌 APIs Used

### 1. **Nominatim API** (Geocoding)
- **Base URL**: `https://nominatim.openstreetmap.org/search`
- **Purpose**: Converts place names to latitude/longitude coordinates
- **Documentation**: https://nominatim.org/release-docs/develop/api/Search/

### 2. **Open-Meteo API** (Weather)
- **Base URL**: `https://api.open-meteo.com/v1/forecast`
- **Purpose**: Fetches current temperature and precipitation probability
- **Documentation**: https://open-meteo.com/en/docs

### 3. **Overpass API** (Places/Tourism)
- **Base URL**: `https://overpass-api.de/api/interpreter`
- **Purpose**: Queries OpenStreetMap for tourist attractions, museums, parks, etc.
- **Documentation**: https://wiki.openstreetmap.org/wiki/Overpass_API

## 🛠️ Tools and Technologies

### Programming Languages
- **Python 3.8+**: Main development language

### Python Libraries
- **Streamlit**: Interactive web application framework
- **Requests**: HTTP library for API calls
- **Folium**: Interactive map visualization
- **streamlit-folium**: Streamlit integration for Folium maps
- **re**: Regular expressions for text parsing (built-in)

### Optional LLMs
- **Not Required**: The current implementation uses rule-based pattern matching for intent detection and place extraction. However, you can optionally integrate:
  - **Ollama**: For local LLM inference
  - **OpenAI API**: For GPT-based reasoning
  - **Hugging Face Transformers**: For local model inference

### Frontend
- **Streamlit**: Interactive web-based UI with real-time processing
- **Folium**: Interactive map visualization showing locations and attractions

## 🏗️ Full System Architecture

### Parent Agent Role
- **Input Analysis**: Parses user queries to extract place names and detect intent
- **Orchestration**: Coordinates all child agents
- **Response Formatting**: Combines results from multiple agents into coherent responses
- **Error Handling**: Manages errors from child agents and provides user-friendly messages

### Weather Agent Role
- **API Integration**: Connects to Open-Meteo API
- **Data Fetching**: Retrieves current temperature and precipitation probability
- **Response Formatting**: Formats weather data into natural language

### Places Agent Role
- **Overpass Query Construction**: Builds complex queries for OpenStreetMap data
- **Tourist Attraction Discovery**: Finds museums, parks, monuments, etc. within ~10km radius
- **Response Formatting**: Formats place lists into readable format

### Geocoding Agent Role
- **Place Name Resolution**: Converts place names to coordinates
- **Validation**: Verifies if places exist
- **Rate Limiting**: Respects API rate limits

### How They Communicate
- **Synchronous Communication**: Parent agent calls child agents sequentially
- **Data Flow**: Coordinates flow from Geocoding → Weather/Places agents
- **Error Propagation**: Errors bubble up to Parent Agent for handling

## 📁 Project Structure

```
Inkel_AI_Project/
├── agents/
│   ├── __init__.py
│   ├── parent_agent.py      # Main orchestrator
│   ├── geocoding_agent.py   # Nominatim API integration
│   ├── weather_agent.py     # Open-Meteo API integration
│   └── places_agent.py      # Overpass API integration
├── utils/
│   ├── __init__.py
│   └── favorites_manager.py # Favorites management
├── streamlit_app.py         # Streamlit web application
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version for deployment
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md               # This file
```

## 🚀 Step-by-Step Guide to Build the Project

### 1. Creating Project Folder Structure

```bash
mkdir -p agents api
touch agents/__init__.py
```

### 2. Implementing Geocoding Agent

**File**: `agents/geocoding_agent.py`
- Uses Nominatim API to convert place names to coordinates
- Handles rate limiting (1 second delay)
- Returns lat/lon or None if place not found

### 3. Implementing Weather Agent

**File**: `agents/weather_agent.py`
- Connects to Open-Meteo API
- Fetches current temperature and precipitation probability
- Formats response as: "In [place] it's currently X°C with a chance of Y% to rain."

### 4. Implementing Places Agent

**File**: `agents/places_agent.py`
- Uses Overpass API to query OpenStreetMap
- Searches for tourism-related tags (museums, parks, monuments, etc.)
- Returns up to 5 places within ~10km radius
- Formats as bulleted list

### 5. Implementing Parent Agent

**File**: `agents/parent_agent.py`
- Extracts place names using regex patterns
- Detects intent (weather, places, or both)
- Coordinates all child agents
- Combines responses intelligently

### 6. Building Streamlit Web Application

**File**: `streamlit_app.py`
- Interactive web interface using Streamlit
- Real-time query processing with ParentAgent
- Interactive map visualization with Folium
- Query history and favorites management
- Beautiful UI with modern design

### 7. Optional: Adding LLM Reasoning

You can enhance the system by:
- Using LLMs for better place name extraction
- Improving intent detection with NLP
- Generating more natural responses

Example integration:
```python
# Using Ollama
import ollama
response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': query}])
```

### 7. Testing the System

Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

Test with example queries:
- "I'm going to go to Bangalore, let's plan my trip."
- "I'm going to go to Bangalore, what is the temperature there"
- "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"

## 📝 Example Inputs + Outputs

### Example 1: Places Query
**Input**: `"I'm going to go to Bangalore, let's plan my trip."`

**Output**:
```
In Bangalore these are the places you can go,
- Lalbagh
- Sri Chamarajendra Park
- Bangalore palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

### Example 2: Weather Query
**Input**: `"I'm going to go to Bangalore, what is the temperature there"`

**Output**:
```
In Bangalore it's currently 24°C with a chance of 35% to rain.
```

### Example 3: Combined Query
**Input**: `"I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"`

**Output**:
```
In Bangalore it's currently 24°C with a chance of 35% to rain. And these are the places you can go:
- Lalbagh
- Sri Chamarajendra Park
- Bangalore palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

### Example 4: Incorrect Place Handling
**Input**: `"I'm going to visit Xyzabc123, what's the weather?"`

**Output**:
```
I don't know this place exists. Could you please provide a valid place name?
```

## ✅ Final Summary

### What the Final System Can Do

1. **Natural Language Understanding**: Parses user queries to extract place names and intent
2. **Multi-Agent Coordination**: Orchestrates specialized agents for different tasks
3. **Real-Time Data**: Provides current weather and up-to-date place information
4. **Error Handling**: Gracefully handles invalid places and API errors
5. **Flexible Queries**: Supports weather-only, places-only, or combined queries
6. **Interactive Web Interface**: Beautiful Streamlit app with map visualization

### Why This Project is Useful for an AI Intern Role

1. **Multi-Agent Systems**: Demonstrates understanding of agent-based architectures
2. **API Integration**: Shows ability to work with multiple external APIs
3. **System Design**: Displays skills in designing modular, maintainable systems
4. **Problem Solving**: Shows ability to break down complex problems into smaller components
5. **Production-Ready Code**: Includes error handling, rate limiting, and proper structure
6. **Documentation**: Comprehensive documentation shows communication skills

### Key Skills Demonstrated

- ✅ **Python Programming**: Object-oriented design, error handling, API integration
- ✅ **System Architecture**: Multi-agent design patterns, separation of concerns
- ✅ **API Integration**: RESTful API consumption, rate limiting, error handling
- ✅ **Web Development**: Streamlit, interactive UI design, map visualization
- ✅ **Natural Language Processing**: Text parsing, intent detection, pattern matching
- ✅ **Problem Decomposition**: Breaking complex problems into manageable agents
- ✅ **Documentation**: Clear, comprehensive project documentation

## 🚀 Quick Start

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit Application**:
```bash
streamlit run streamlit_app.py
```

3. **Access the Application**:
- The app will automatically open in your browser at `http://localhost:8501`
- Enter your tourism queries in the input field
- View results with interactive map visualization

4. **Test with Example Queries**:
- "I'm going to go to Bangalore, let's plan my trip."
- "I'm going to go to Bangalore, what is the temperature there"
- "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"

## 🚀 Deploy to Streamlit Cloud

The application is already deployed and live at:
**https://inkelaiproject-3m5gqfpepa7aeh8g89xmfv.streamlit.app/**

### Deployment Steps (Already Completed):

1. **Repository Setup**: Code is pushed to GitHub at https://github.com/N-Harshitha21/Inkel_AI_Project

2. **Streamlit Cloud Configuration**:
   - Main file path: `streamlit_app.py`
   - Python version: `3.11` (from runtime.txt)
   - All dependencies in `requirements.txt`

3. **Required Files Present**:
   - ✅ `streamlit_app.py` - Main application
   - ✅ `requirements.txt` - All dependencies
   - ✅ `runtime.txt` - Python version
   - ✅ `.streamlit/config.toml` - Streamlit configuration
   - ✅ `agents/` - All agent modules
   - ✅ `utils/` - Utility modules

### To Deploy Your Own Instance:

1. Fork/clone the repository
2. Go to https://share.streamlit.io
3. Click "New app"
4. Connect your GitHub repository
5. Set main file path to: `streamlit_app.py`
6. Click "Deploy"

The app will be live in a few minutes!

---

## 📄 License

This project is created for educational purposes as part of an AI Intern role assessment.

