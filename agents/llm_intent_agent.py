"""
Free LLM Intent Detection Agent using Ollama
"""
import json
from typing import Dict, List, Optional
from .tourism_prompts import TourismPrompts

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Ollama not installed. Run: pip install ollama")


class LLMIntentAgent:
    """
    Free LLM-powered intent detection using Ollama.
    Replaces regex-based intent detection with natural language understanding.
    """
    
    def __init__(self, model: str = "phi3:mini"):
        """
        Initialize LLM Intent Agent.
        
        Args:
            model: Ollama model to use. Options:
                  - "phi3:mini" (2GB, fast, good quality)
                  - "llama3.1:8b" (4GB, slower, excellent quality) 
                  - "mistral:7b" (4GB, medium speed, very good quality)
        """
        self.model = model
        self.available = OLLAMA_AVAILABLE and self._test_model()
        
        if not self.available:
            print(f"⚠️  LLM not available. Using fallback regex detection.")
            print(f"To enable: 1) Install Ollama 2) Run: ollama pull {model}")
    
    def _test_model(self) -> bool:
        """Test if the model is available in Ollama."""
        try:
            ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': 'Hello'}
            ])
            return True
        except Exception as e:
            print(f"Model {self.model} not available: {e}")
            return False
    
    def analyze_query(self, user_input: str) -> Dict:
        """
        Analyze user query to extract intent, location, and preferences.
        
        Args:
            user_input: User's tourism query
            
        Returns:
            Dictionary with extracted information
        """
        if not self.available:
            return self._fallback_analysis(user_input)
        
        prompt = self._build_analysis_prompt(user_input)
        
        try:
            response = ollama.chat(
                model=self.model, 
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.1}  # Low temperature for consistent output
            )
            
            content = response['message']['content'].strip()
            
            # Try to extract JSON from response
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                return json.loads(json_str)
            
            # If no valid JSON, use fallback
            return self._fallback_analysis(user_input)
            
        except Exception as e:
            print(f"LLM analysis error: {e}")
            return self._fallback_analysis(user_input)
    
    def _build_analysis_prompt(self, user_input: str) -> str:
        """Build the prompt for LLM analysis."""
        return f"""
You are a tourism query analyzer. Extract information from this query and return ONLY valid JSON:

Query: "{user_input}"

Return JSON with these exact keys:
{{
    "location": "extracted place name or null if not found",
    "intents": ["list of relevant intents from: weather, places, restaurants, hotels, activities, transport"],
    "urgency": "immediate, planning, or casual",
    "duration": "extracted duration like '3 days', 'weekend', 'week' or null",
    "preferences": ["any specific interests mentioned like 'budget', 'luxury', 'family', 'romantic', 'adventure'"],
    "confidence": 0.8
}}

Examples:
"Weather in Paris?" -> {{"location": "Paris", "intents": ["weather"], "urgency": "immediate", "duration": null, "preferences": [], "confidence": 0.9}}
"Planning a romantic weekend in Tokyo" -> {{"location": "Tokyo", "intents": ["places", "hotels", "restaurants"], "urgency": "planning", "duration": "weekend", "preferences": ["romantic"], "confidence": 0.9}}
"Budget restaurants in Bangkok" -> {{"location": "Bangkok", "intents": ["restaurants"], "urgency": "immediate", "duration": null, "preferences": ["budget"], "confidence": 0.9}}

Return ONLY the JSON object:
"""
    
    def _fallback_analysis(self, user_input: str) -> Dict:
        """
        Fallback analysis using simple pattern matching.
        This is used when LLM is not available.
        """
        user_lower = user_input.lower()
        
        # Simple location extraction (improved from original)
        import re
        location_patterns = [
            r"(?:in|to|visit|going to)\s+([A-Z][a-zA-Z\s]+?)(?:\s|,|\.|$)",
            r"([A-Z][a-zA-Z\s]+?)(?:\s+weather|\s+trip|\s+places)",
            r"^([A-Z][a-zA-Z\s]+?)(?:\s|,|\?|$)"
        ]
        
        location = None
        for pattern in location_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                break
        
        # Intent detection
        intents = []
        if any(word in user_lower for word in ['weather', 'temperature', 'rain', 'hot', 'cold']):
            intents.append('weather')
        if any(word in user_lower for word in ['places', 'attractions', 'sightseeing', 'visit']):
            intents.append('places')
        if any(word in user_lower for word in ['restaurant', 'food', 'eat', 'dining']):
            intents.append('restaurants')
        if any(word in user_lower for word in ['hotel', 'accommodation', 'stay']):
            intents.append('hotels')
        if any(word in user_lower for word in ['activity', 'activities', 'things to do']):
            intents.append('activities')
        
        # Default to places if no specific intent
        if not intents:
            intents = ['places', 'weather']
        
        # Simple urgency detection
        urgency = "immediate"
        if any(word in user_lower for word in ['planning', 'plan', 'next month', 'next year']):
            urgency = "planning"
        
        # Simple preferences
        preferences = []
        if 'budget' in user_lower:
            preferences.append('budget')
        if any(word in user_lower for word in ['luxury', 'expensive', 'high-end']):
            preferences.append('luxury')
        if 'romantic' in user_lower:
            preferences.append('romantic')
        if 'family' in user_lower:
            preferences.append('family')
        
        return {
            "location": location,
            "intents": intents,
            "urgency": urgency,
            "duration": None,
            "preferences": preferences,
            "confidence": 0.6,
            "method": "fallback"
        }

    def get_model_info(self) -> Dict:
        """Get information about the current model."""
        return {
            "model": self.model,
            "available": self.available,
            "ollama_installed": OLLAMA_AVAILABLE
        }


# Example usage and testing
if __name__ == "__main__":
    agent = LLMIntentAgent()
    
    test_queries = [
        "What's the weather in Paris?",
        "I'm planning a romantic weekend in Tokyo",
        "Budget restaurants in Bangkok",
        "Things to do in New York for families",
        "Luxury hotels in Dubai for next month"
    ]
    
    print("🤖 Testing LLM Intent Agent")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent.analyze_query(query)
        print(f"Analysis: {json.dumps(result, indent=2)}")
        print("-" * 30)