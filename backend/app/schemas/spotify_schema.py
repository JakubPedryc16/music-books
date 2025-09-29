from pydantic import BaseModel

from app.schemas.api_response import APIResponse

class PlayResponseData(BaseModel):
    tracks_count: int
    played_tracks: list[str]
    
class PlayResponse(APIResponse):
    data: PlayResponseData

    