from typing import Dict, Optional
from datetime import datetime, timedelta

class URLStorage:
    def __init__(self):
        self._url_map: Dict[str, Dict] = {}
    
    def store_url(self, short_code: str,short_url: str, long_url: str, 
                  ttl_minutes: Optional[int] = None) -> None:
        """
        Store a URL mapping with optional time-to-live.
        
        Args:
            short_code (str): Short URL code
            long_url (str): Original long URL
            ttl_minutes (Optional[int]): Minutes until URL expires
        """
        expiry = (datetime.now() + timedelta(minutes=ttl_minutes)) if ttl_minutes else None
        self._url_map[short_code] = {
            'long_url': long_url,
            'short_url': short_url,
            'created_at': datetime.now(),
            'access_count': 0,
            'expiry': expiry
        }
    
    def get_url(self, short_code: str) -> Optional[Dict]:
        """
        Retrieve URL details by short code.
        
        Args:
            short_code (str): Short URL code
        
        Returns:
            Optional[Dict]: URL details or None
        """
        url_entry = self._url_map.get(short_code)
        
        
        return url_entry
    
    def get_existing_short_code(self, normalized_url: str) -> Optional[str]:
        """
        Find an existing short code for a normalized URL.
        
        Args:
            normalized_url (str): Normalized long URL
        
        Returns:
            Optional[str]: Existing short code or None
        """
        for code, entry in self._url_map.items():
            if entry['long_url'] == normalized_url or entry['short_url'] == normalized_url:
                return code
        return None
    
    def cleanup_expired_urls(self) -> None:
        """
        Remove expired URLs from storage.
        """
        now = datetime.now()
        self._url_map = {
            code: entry for code, entry in self._url_map.items()
            if not entry['expiry'] or entry['expiry'] > now
        }