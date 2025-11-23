"""
FastAPI Backend for Multi-Agent Tourism System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.parent_agent import ParentAgent
from agents.enhanced_parent_agent import EnhancedParentAgent
from utils.favorites_manager import FavoritesManager

app = FastAPI(
    title="Multi-Agent Tourism System",
    description="AI-powered tourism assistant with weather and places information",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize parent agent and favorites manager
parent_agent = ParentAgent()
enhanced_parent_agent = EnhancedParentAgent()
favorites_manager = FavoritesManager()


class QueryRequest(BaseModel):
    """Request model for user queries"""
    query: str


class QueryResponse(BaseModel):
    """Response model for query results"""
    response: str
    place_name: Optional[str] = None

class QueryResponseWithMap(BaseModel):
    """Response model with map data"""
    response: str
    place_name: Optional[str] = None
    coordinates: Optional[Dict] = None
    weather_data: Optional[Dict] = None
    places_data: Optional[List[Dict]] = None

class FavoriteRequest(BaseModel):
    """Request model for adding favorites"""
    place_name: str
    coordinates: Dict
    weather_data: Optional[Dict] = None
    places_data: Optional[List[Dict]] = None


@app.get("/")
async def root():
    """Root endpoint"""
    system_status = enhanced_parent_agent.get_system_status()
    return {
        "message": "Multi-Agent Tourism System API",
        "version": "3.0.0",
        "features": ["Map Integration", "Favorites", "LLM Enhancement"],
        "llm_status": system_status["llm_available"],
        "endpoints": {
            "/query": "POST - Process tourism queries (traditional)",
            "/query/enhanced": "POST - Process queries with LLM (if available)",
            "/query/map": "POST - Process queries with map data",
            "/favorites": "GET - Get all favorites",
            "/favorites": "POST - Add favorite",
            "/favorites/{id}": "DELETE - Remove favorite",
            "/health": "GET - Health check",
            "/status": "GET - System component status"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "tourism-agent"}

@app.get("/status")
async def system_status():
    """Get detailed system status"""
    return enhanced_parent_agent.get_system_status()


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Main endpoint to process user tourism queries.
    
    Accepts natural language queries about places and returns:
    - Weather information
    - Tourist attractions
    - Or both based on query intent
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query through parent agent
        response = parent_agent.process_query(request.query)
        
        return QueryResponse(
            response=response,
            place_name=parent_agent.extract_place_name(request.query)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/query/enhanced", response_model=QueryResponse)
async def process_query_enhanced(request: QueryRequest):
    """
    Enhanced endpoint using LLM for better intent detection and response generation.
    Falls back to traditional processing if LLM is unavailable.
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query through enhanced parent agent
        response = enhanced_parent_agent.process_query(request.query)
        
        return QueryResponse(
            response=response,
            place_name=enhanced_parent_agent.llm_intent_agent.analyze_query(request.query).get("location") if enhanced_parent_agent.use_llm else parent_agent.extract_place_name(request.query)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhanced query: {str(e)}"
        )

@app.post("/query/map", response_model=QueryResponseWithMap)
async def process_query_with_map(request: QueryRequest):
    """
    Process query and return data with coordinates for map integration.
    
    Returns:
    - Response text
    - Place name
    - Coordinates (lat, lon)
    - Weather data
    - Places data with coordinates
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query with map data
        result = parent_agent.process_query_with_map_data(request.query)
        
        return QueryResponseWithMap(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

# Favorites endpoints
@app.get("/favorites")
async def get_favorites():
    """Get all user favorites."""
    return {
        "favorites": favorites_manager.get_favorites(),
        "count": len(favorites_manager.get_favorites())
    }

@app.post("/favorites")
async def add_favorite(request: FavoriteRequest):
    """Add a place to favorites."""
    result = favorites_manager.add_favorite(
        place_name=request.place_name,
        coordinates=request.coordinates,
        weather_data=request.weather_data,
        places_data=request.places_data
    )
    
    if result['success']:
        return result
    else:
        raise HTTPException(status_code=400, detail=result['message'])

@app.delete("/favorites/{favorite_id}")
async def remove_favorite(favorite_id: int):
    """Remove a favorite by ID."""
    result = favorites_manager.remove_favorite(favorite_id)
    
    if result['success']:
        return result
    else:
        raise HTTPException(status_code=404, detail=result['message'])

@app.post("/favorites/add-from-query")
async def add_favorite_from_query(request: QueryRequest):
    """
    Process a query and automatically add the result to favorites.
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query with map data
        result = parent_agent.process_query_with_map_data(request.query)
        
        if not result['coordinates']:
            raise HTTPException(status_code=400, detail="Could not geocode the place")
        
        # Add to favorites
        favorite_result = favorites_manager.add_favorite(
            place_name=result['place_name'],
            coordinates=result['coordinates'],
            weather_data=result['weather_data'],
            places_data=result['places_data']
        )
        
        return favorite_result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

