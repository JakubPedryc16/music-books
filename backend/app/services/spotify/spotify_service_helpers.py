import os
from datetime import datetime, timedelta, timezone
from typing import List
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from app.db.db_async import AsyncSession
from app.models.user import User
from app.schemas.spotify_schema import PlayResponse, PlayResponseData
from app.utils.logger import logger

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = os.getenv("SCOPE")

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
)

def get_auth_url() -> str:
    return sp_oauth.get_authorize_url()

def exchange_code_for_token(code: str) -> dict:
    return sp_oauth.get_access_token(code, as_dict=True)

def play_songs(access_token: str, song_uris: List[str]) -> PlayResponse:
    sp = Spotify(auth=access_token)
    try:
        devices = sp.devices().get("devices", [])
        if not devices:
            return PlayResponse(
                success=False,
                error="no_active_device"
            )
        device_id = devices[0]["id"]
        sp.start_playback(device_id=device_id, uris=song_uris)
    except SpotifyException as e:
        logger.exception(f"Spotify API error: {e}")
        return PlayResponse(
            success=False,
            error=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error while playing songs: {e}")
        return PlayResponse(
            success=False,
            error=str(e)
        )

    return PlayResponse(
        success=True,
        data=PlayResponseData(
            tracks_count=len(song_uris),
            played_tracks=song_uris
        )
    )

def refresh_spotify_token(refresh_token: str) -> dict:
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()

async def get_valid_access_token(user: User, session: AsyncSession) -> str:
    now = datetime.now(timezone.utc)
    token_expires_at = user.token_expires_at
    if token_expires_at.tzinfo is None:
        token_expires_at = token_expires_at.replace(tzinfo=timezone.utc)

    if token_expires_at > now:
        return user.access_token

    token_info = refresh_spotify_token(user.refresh_token)
    user.access_token = token_info["access_token"]
    user.token_expires_at = now + timedelta(seconds=token_info["expires_in"])
    await session.commit()
    return user.access_token
