import base64
import hashlib
import uuid

class URLGenerator:
    @staticmethod
    def generate_short_code(url: str, length: int = 8) -> str:
        """
        Generate a unique short code for a given URL.
        
        Args:
            url (str): Original URL
            length (int): Length of short code
        
        Returns:
            str: Unique short code
        """
        # Use a combination of hash and uuid for uniqueness
        hash_input = url + str(uuid.uuid4())
        hash_object = hashlib.sha256(hash_input.encode())
        
        # Base64 encode the hash and take the first 'length' characters
        short_code = base64.urlsafe_b64encode(
            hash_object.digest()
        ).decode('utf-8')[:length]
        
        return short_code