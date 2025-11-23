"""
Performance Optimization Utilities for LLM Tourism System
"""
import time
import asyncio
from typing import Dict, List, Optional, Callable, Any
from functools import wraps
import json
import os

class CacheManager:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache = {}
        self.timestamps = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self.cache:
            return None
        
        if time.time() - self.timestamps[key] > self.default_ttl:
            self.delete(key)
            return None
        
        return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with optional TTL."""
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def delete(self, key: str):
        """Delete value from cache."""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()
        self.timestamps.clear()
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "entries": len(self.cache),
            "memory_mb": sum(len(str(v)) for v in self.cache.values()) / (1024 * 1024),
            "oldest_entry": min(self.timestamps.values()) if self.timestamps else None
        }

class ModelSelector:
    """Intelligent model selection based on query complexity and performance."""
    
    def __init__(self):
        self.model_performance = {
            "qwen2.5:0.5b": {"speed": 0.9, "quality": 0.6, "size": 397},
            "phi3:mini": {"speed": 0.7, "quality": 0.8, "size": 2200},
            "llama3.1:8b": {"speed": 0.4, "quality": 0.95, "size": 4000}
        }
        self.available_models = []
        self._check_available_models()
    
    def _check_available_models(self):
        """Check which models are available in Ollama."""
        try:
            import ollama
            models_response = ollama.list()
            self.available_models = [model['name'] for model in models_response.get('models', [])]
        except:
            self.available_models = []
    
    def select_model(self, query_complexity: str = "medium", priority: str = "balanced") -> str:
        """
        Select optimal model based on query complexity and priority.
        
        Args:
            query_complexity: "simple", "medium", "complex"
            priority: "speed", "quality", "balanced"
        
        Returns:
            Best available model name
        """
        if not self.available_models:
            return "qwen2.5:0.5b"  # Default fallback
        
        # Score models based on priority
        scores = {}
        for model in self.available_models:
            if model in self.model_performance:
                perf = self.model_performance[model]
                
                if priority == "speed":
                    score = perf["speed"]
                elif priority == "quality":
                    score = perf["quality"]
                else:  # balanced
                    score = (perf["speed"] + perf["quality"]) / 2
                
                # Adjust for query complexity
                if query_complexity == "simple":
                    score += 0.1 if perf["speed"] > 0.7 else 0
                elif query_complexity == "complex":
                    score += 0.1 if perf["quality"] > 0.8 else 0
                
                scores[model] = score
        
        if scores:
            return max(scores, key=scores.get)
        return self.available_models[0]
    
    def get_model_info(self, model: str) -> Dict:
        """Get performance information for a model."""
        return self.model_performance.get(model, {"speed": 0.5, "quality": 0.5, "size": 0})

class PerformanceMonitor:
    """Monitor and log performance metrics."""
    
    def __init__(self):
        self.metrics = {
            "query_count": 0,
            "total_time": 0,
            "avg_response_time": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "model_usage": {},
            "error_count": 0
        }
    
    def log_query(self, duration: float, model: str, cached: bool = False):
        """Log a query performance metric."""
        self.metrics["query_count"] += 1
        self.metrics["total_time"] += duration
        self.metrics["avg_response_time"] = self.metrics["total_time"] / self.metrics["query_count"]
        
        if cached:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
        
        if model not in self.metrics["model_usage"]:
            self.metrics["model_usage"][model] = 0
        self.metrics["model_usage"][model] += 1
    
    def log_error(self):
        """Log an error occurrence."""
        self.metrics["error_count"] += 1
    
    def get_stats(self) -> Dict:
        """Get performance statistics."""
        cache_total = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_rate = self.metrics["cache_hits"] / cache_total if cache_total > 0 else 0
        
        return {
            **self.metrics,
            "cache_hit_rate": round(cache_rate, 3),
            "error_rate": round(self.metrics["error_count"] / max(1, self.metrics["query_count"]), 3)
        }
    
    def reset(self):
        """Reset all metrics."""
        for key in self.metrics:
            if isinstance(self.metrics[key], dict):
                self.metrics[key].clear()
            else:
                self.metrics[key] = 0

def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        print(f"{func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper

def cache_decorator(cache_manager: CacheManager, ttl: int = 3600):
    """Decorator to cache function results."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            import hashlib
            cache_key = f"{func.__name__}_{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            
            # Try to get from cache
            result = cache_manager.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

class AsyncProcessor:
    """Handle asynchronous processing for better performance."""
    
    @staticmethod
    async def gather_tourism_data(geocoding_func, weather_func, places_func, lat: float, lon: float):
        """Gather weather and places data concurrently."""
        try:
            # Run API calls concurrently
            weather_task = asyncio.create_task(
                asyncio.to_thread(weather_func, lat, lon)
            )
            places_task = asyncio.create_task(
                asyncio.to_thread(places_func, lat, lon, 5)
            )
            
            weather_data, places_data = await asyncio.gather(
                weather_task, places_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(weather_data, Exception):
                weather_data = None
            if isinstance(places_data, Exception):
                places_data = []
            
            return weather_data, places_data
            
        except Exception as e:
            print(f"Async processing error: {e}")
            return None, []

class OptimizationManager:
    """Main optimization manager that coordinates all performance features."""
    
    def __init__(self):
        self.cache = CacheManager()
        self.model_selector = ModelSelector()
        self.monitor = PerformanceMonitor()
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load optimization configuration."""
        default_config = {
            "cache_ttl": 3600,
            "max_cache_size": 1000,
            "preferred_model_priority": "balanced",
            "enable_async_processing": True,
            "log_performance": True
        }
        
        # Try to load from config file
        config_file = "config/optimization.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except:
                pass
        
        return default_config
    
    def optimize_query_processing(self, query: str, complexity: str = "medium"):
        """Get optimization recommendations for a query."""
        model = self.model_selector.select_model(
            query_complexity=complexity,
            priority=self.config["preferred_model_priority"]
        )
        
        return {
            "recommended_model": model,
            "use_cache": True,
            "cache_ttl": self.config["cache_ttl"],
            "enable_async": self.config["enable_async_processing"]
        }
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics."""
        return {
            "cache_stats": self.cache.stats(),
            "performance_stats": self.monitor.get_stats(),
            "available_models": self.model_selector.available_models,
            "config": self.config
        }
    
    def cleanup(self):
        """Cleanup resources and save stats."""
        self.cache.clear()
        self.monitor.reset()

# Global optimization manager instance
optimizer = OptimizationManager()

# Convenience functions
def get_optimal_model(query: str) -> str:
    """Get the optimal model for a query."""
    # Simple complexity estimation
    complexity = "simple"
    if len(query) > 100:
        complexity = "complex"
    elif len(query) > 50:
        complexity = "medium"
    
    recommendations = optimizer.optimize_query_processing(query, complexity)
    return recommendations["recommended_model"]

def cache_response(func, cache_key: str, ttl: int = 3600):
    """Cache a function response."""
    cached = optimizer.cache.get(cache_key)
    if cached:
        optimizer.monitor.log_query(0, "cached", True)
        return cached
    
    start_time = time.time()
    result = func()
    duration = time.time() - start_time
    
    optimizer.cache.set(cache_key, result, ttl)
    optimizer.monitor.log_query(duration, "unknown", False)
    
    return result