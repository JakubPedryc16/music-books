from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import requests
from app.utils.logger import logger
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from spotipy.exceptions import SpotifyException

async def global_exception_handler(request: Request, exc: Exception):

    logger.exception(f"Unhandled error: {exc} | URL: {request.url}")

    if isinstance(exc, (RequestValidationError, ValidationError)):
        return JSONResponse(
            status_code=422,
            content={"success": False, "data": None, "error": str(exc)}
        )

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "data": None, "error": exc.detail}
        )
    
    if isinstance(exc, SpotifyException):
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": f"Spotify API error: {str(exc)}"}
        )
    
    if isinstance(exc, requests.RequestException):
        return JSONResponse(
            status_code=502,
            content={"success": False, "error": f"Network error: {str(exc)}"}
        )
    
    return JSONResponse(
        status_code=500,
        content={"success": False, "data": None, "error": str(exc)}
    )
