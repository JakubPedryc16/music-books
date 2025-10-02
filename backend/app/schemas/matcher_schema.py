from typing import Optional
from pydantic import BaseModel

from app.schemas.api_response import APIResponse

class SongData(BaseModel):
    title: str
    author: str
    spotify_id: str

class MatchedTracksResponse(APIResponse):
    data: Optional[list[SongData]]

class TranslationResponse(APIResponse):
    data: Optional[str]