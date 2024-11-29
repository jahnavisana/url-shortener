import re
from urllib.parse import urlparse

class URLValidator:
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate URL format and structure.
        
        Args:
            url (str): URL to validate
        
        Returns:
            bool: Whether the URL is valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize URL by removing trailing slashes and converting to lowercase.
        
        Args:
            url (str): URL to normalize
        
        Returns:
            str: Normalized URL
        """
        return url.rstrip('/').lower()