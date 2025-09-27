from datetime import datetime, timedelta, timezone
import os
from typing import List
from spotipy import Spotify
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.dal.user_dal import UserDAL
from app.models.user import User
from app.schemas.spotify_schema import PlayResponse
from app.services.spotify.spotify_service_helpers import get_valid_access_token, play_songs, exchange_code_for_token, get_auth_url

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_SECONDS = 3600

class SpotifyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_dal = UserDAL(session)

    def create_app_jwt(self, user_id: int, spotify_id: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "spotify_id": spotify_id,
            "iat": now.timestamp(),
            "exp": (now + timedelta(seconds=JWT_EXPIRES_SECONDS)).timestamp()
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def decode_app_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="JWT expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid JWT token")

    async def get_user_from_jwt(self, app_jwt: str) -> User:
        payload = self.decode_app_jwt(app_jwt)
        spotify_id = payload.get("spotify_id")
        if not spotify_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await self.user_dal.get_by_spotify_id(spotify_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def play_tracks(self, app_jwt: str, tracks_ids: List[str]) -> PlayResponse:
        user = await self.get_user_from_jwt(app_jwt)
        valid_access_token = await get_valid_access_token(user, self.session)
        response = play_songs(valid_access_token, tracks_ids)
        return response

    async def handle_callback(self, code: str, frontend_url: str) -> tuple[str, str]:
        token_info = exchange_code_for_token(code)
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]
        expires_in = int(token_info["expires_in"])

        sp = Spotify(auth=access_token)
        me = sp.me()

        user = await self.user_dal.create_or_update(
            spotify_id=me["id"],
            display_name=me.get("display_name"),
            email=me.get("email"),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )

        jwt_token = self.create_app_jwt(user.id, user.spotify_id)
        redirect_url = f"{frontend_url}/spotify-callback"
        return jwt_token, redirect_url
