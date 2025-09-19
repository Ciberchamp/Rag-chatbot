import json
import hashlib
import os
# Task 3 of assignment implemented here
class Cache:
    def __init__(self, cache_file="cache.json"):
        self.cache_file = cache_file
        self.cache = self.load_cache()
    
    def load_cache(self):
        """Load cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def get_hash(self, text: str) -> str:
        """Generate hash for text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, query: str):
        """Get cached response for query"""
        query_hash = self.get_hash(query)
        return self.cache.get(query_hash)
    
    def set(self, query: str, response: dict):
        """Cache response for query"""
        query_hash = self.get_hash(query)
        self.cache[query_hash] = response
        self.save_cache()