from typing import List
from pydantic import BaseModel

class PlayRequest(BaseModel):
    access_token: str
    tracks_ids: List[str]

class PlayResponse(BaseModel):
    status: str
    tracks_count: int
    played_tracks: List[str]
    
    