from fastapi import APIRouter, Body, Cookie, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_async_session
from app.schemas.spotify_schema import PlayResponse, SpotifyRequest
from app.services.spotify.spotify_service_helpers import get_auth_url
from app.services.spotify.spotify_service import SpotifyService
import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
router = APIRouter(prefix="/spotify")


@router.get("/login")
def login() -> RedirectResponse:
    return RedirectResponse(get_auth_url())


@router.get("/callback")
async def callback(code: str, session: AsyncSession = Depends(get_async_session)):

    service = SpotifyService(session)
    jwt_token, redirect_url = await service.handle_callback(code, FRONTEND_URL)
    response = RedirectResponse(redirect_url)
    response.set_cookie(
        key="app_jwt",
        value=jwt_token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False
    )
    return response


@router.post("/play", response_model=PlayResponse)
async def play_endpoint(
    tracks_ids: SpotifyRequest = Body(...),
    app_jwt: str = Cookie(None),
    session: AsyncSession = Depends(get_async_session)
):
    if not app_jwt:
        raise HTTPException(status_code=401, detail="User not logged in")

    service = SpotifyService(session)
    response: PlayResponse = await service.play_tracks(app_jwt, tracks_ids)
    return response
