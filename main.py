from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import asyncio
from pydantic import BaseModel
from typing import Optional
from src.url_service import URLService
from src.url_validator import URLValidator
from src.url_storage import URLStorage
app = FastAPI()
url_service = URLService()
async def clean_expired_urls():
    while True:
        url_service._storage.cleanup_expired_urls()  # Using the instance from url_service
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(clean_expired_urls())

class ShortenURLRequest(BaseModel):
    long_url: str
    ttl_minutes: Optional[int] = None

class ShortenURLResponse(BaseModel):
    short_url: str

class URLStatsResponse(BaseModel):
    short_code: str
    access_count: int
    created_at: str
    expiry: str| None

@app.post("/shorten", response_model=ShortenURLResponse)
def shorten_url(request: ShortenURLRequest):
    """
    Shorten a given long URL with optional TTL (time-to-live).
    """
    try:
        short_url = url_service.shorten_url(request.long_url, ttl_minutes=request.ttl_minutes)
        return ShortenURLResponse(short_url=short_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/stats", response_model=URLStatsResponse)
def get_url_stats( url: Optional[str] = None):
    """
    Get access statistics for a URL by either short code or long URL.
    """
    if not url:
        raise HTTPException(status_code=400, detail="Provide either a short URL or a long URL.")

    if url:
        if not URLValidator.is_valid_url(url):
            raise HTTPException(status_code=400, detail="Invalid URL format.")
        
        normalized_url = URLValidator.normalize_url(url)
        short_code = url_service._storage.get_existing_short_code(normalized_url)
        if not short_code:
            raise HTTPException(status_code=404, detail="URL not found.")

    url_stats = url_service.get_url_stats(normalized_url)
    if not url_stats:
        raise HTTPException(status_code=404, detail="Statistics not found for the URL.")
    return URLStatsResponse(
        short_code=short_code,
        access_count=url_stats["access_count"],
        created_at=url_stats["created_at"].isoformat(),
        expiry=url_stats["expiry"].isoformat() if url_stats["expiry"] else None
    )

@app.get("/{short_code}")
def redirect_url(short_code: str):
    """
    Redirect short URL to original long URL
    """
    try:
        long_url = url_service.redirect_url(short_code)
        return RedirectResponse(url=long_url, status_code=302)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

