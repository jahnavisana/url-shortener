# URL Shortener Service

## Overview

A robust and efficient URL shortening service built with FastAPI, providing features like URL shortening, redirection, and access statistics tracking.

## Architecture

The project follows a modular, layered architecture with clear separation of concerns:

### Components

1. **URLValidator (`url_validator.py`)**: 
   - Handles URL validation and normalization
   - Ensures URL format consistency
   - Provides methods to validate and normalize URLs

2. **URLGenerator (`url_generator.py`)**: 
   - Responsible for generating unique short codes
   - Uses SHA-256 hashing and base64 encoding
   - Incorporates UUID to ensure uniqueness

3. **URLStorage (`url_storage.py`)**: 
   - In-memory storage for URL mappings
   - Supports optional TTL for shortened URLs
   - Provides methods for storing, retrieving, and cleaning up URLs

4. **URLService (`url_service.py`)**: 
   - Main business logic layer
   - Coordinates between validator, generator, and storage
   - Handles URL shortening, redirection, and statistics retrieval

5. **Main Application (`main.py`)**: 
   - FastAPI web application
   - Defines REST API endpoints
   - Implements background task for cleaning expired URLs

## Key Features

- URL validation and normalization
- Unique short code generation
- Optional time-to-live (TTL) for shortened URLs
- Access statistics tracking
- Background cleanup of expired URLs

## Design Decisions and Challenges

### Short Code Generation
- Used a combination of SHA-256 hash and UUID to ensure high uniqueness
- Base64 encoding provides a compact representation
- Configurable length for short codes

### URL Storage
- In-memory storage using a dictionary for simplicity
- Implemented a cleanup mechanism for expired URLs
- Tracks access count and creation time for each URL

### Error Handling
- Comprehensive input validation
- Clear error messages for invalid URLs
- Proper HTTP status codes for different scenarios

### Performance Considerations
- Fast O(1) lookup for URL retrieval
- Background task for periodic URL cleanup
- Minimal overhead in short code generation

## Tech Stack

- Python 3.8+
- FastAPI
- Pydantic
- hashlib
- uuid
- base64

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jahnavisana/url-shortener.git
cd url-shortener
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Shorten URL
- **POST** `/shorten`
- Request Body:
  ```json
  {
    "long_url": "https://example.com/very/long/url",
    "ttl_minutes": 60  (Optional)
  }
  ```
- Response: Shortened URL

### Retrieve URL Statistics
- **GET** `/stats?url={url}`
- Returns access count and creation time for a URL

### Redirect
- **GET** `/{short_code}`
- Redirects to the original long URL

## Potential Improvements

- Persistent storage (e.g., Redis, PostgreSQL)
- Rate limiting
- More advanced URL analytics
- Support for custom short codes
- Caching mechanisms

