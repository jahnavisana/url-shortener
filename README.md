# URL Shortener Service

## Overview

A robust and efficient URL shortening service built with FastAPI, providing features like URL shortening, redirection, and access statistics tracking.

## Features

- Generate short URLs from long URLs
- Optional time-to-live (TTL) for shortened URLs
- URL validation and normalization
- Access statistics tracking
- Automatic URL expiration

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
uvicorn src.main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Shorten URL
- **POST** `/shorten`
- Request Body:
  ```json
  {
    "long_url": "https://example.com/very/long/url",
    "ttl_minutes": 60  // Optional
  }
  ```
- Response: Shortened URL

### Retrieve URL Statistics
- **GET** `/stats?url={url}`
- Returns access count and creation time for a URL

### Redirect
- **GET** `/{short_code}`
- Redirects to the original long URL

## Configuration

- Modify `base_url` in `URLService` to change the base domain
- Adjust TTL settings as needed

