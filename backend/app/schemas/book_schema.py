
from typing import Optional
from pydantic import BaseModel


from app.schemas.api_response import APIResponse

class BookData(BaseModel):
    id: int
    title: str
    author: str

class BookPageData(BaseModel):
    id: int
    page: int
    text: str
    
class BookResponse(APIResponse):
    data: Optional[list[BookData]]

class UploadBookResponse(APIResponse):
    data: Optional[int]

class BookPageResponse(APIResponse):
    data: Optional[BookPageData]