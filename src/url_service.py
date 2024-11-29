from typing import Optional, Dict
from .url_validator import URLValidator
from .url_generator import URLGenerator
from .url_storage import URLStorage
from datetime import datetime

class URLService:
    def __init__(self, base_url: str = "http://localhost:8000/"):
        self._base_url = base_url
        self._storage = URLStorage()
    
    def shorten_url(self, long_url: str, ttl_minutes: Optional[int] = None) -> str:
        """
        Generate a shortened URL for a given long URL.
        
        Args:
            long_url (str): URL to shorten
            ttl_minutes (Optional[int]): Minutes until URL expires
        
        Returns:
            str: Shortened URL
        """
        if not URLValidator.is_valid_url(long_url):
            raise ValueError("Invalid URL format")
        
        normalized_url = URLValidator.normalize_url(long_url)
        
        # Check if URL already exists
        existing_code = self._storage.get_existing_short_code(normalized_url)
        if existing_code:
            return self._base_url + existing_code
        
        # Generate new short code
        short_code = URLGenerator.generate_short_code(normalized_url)
        
        # Store URL mapping
        short_url = self._base_url + short_code
        self._storage.store_url(short_code,URLValidator.normalize_url(short_url), normalized_url, ttl_minutes)
        return short_url
    
    def redirect_url(self, short_code: str) -> Optional[str]:
        """
        Retrieve original long URL and increment access count and check for expiry
        
        Args:
            short_key (str): Short URL key
        
        Returns:
            Optional[str]: Original long URL or None if not found
        """

        url_entry = self._storage.get_url(short_code)
        if not url_entry:
            return None
        

        
        # Increment access count
        url_entry['access_count'] += 1
        
        return url_entry['long_url']    
    
    def get_url_stats(self, short_url: str) -> Optional[Dict]:
        """
        Get access statistics for a shortened URL.
        
        Args:
            short_code (str): Short URL code
        
        Returns:
            Optional[Dict]: URL statistics
        """
        short_code=self._storage.get_existing_short_code(short_url)
        url_entry = self._storage.get_url(short_code)
        if url_entry:
        
            return {
                'access_count': url_entry['access_count'],
                'created_at': url_entry['created_at'],
                'expiry': url_entry['expiry']
            }
        return None
    
