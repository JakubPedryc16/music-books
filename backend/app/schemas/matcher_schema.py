from typing import List, Optional, TypedDict
from pydantic import BaseModel

class SongResponse(BaseModel):
    title: str
    author: str
    spotify_id: str

class MatchedTracksResponse(BaseModel):
    success: bool
    tracks: List[SongResponse] 
    error: Optional[str] = None

class TranslationResult(TypedDict):
    success: bool
    text: str
    error: Optional[str]