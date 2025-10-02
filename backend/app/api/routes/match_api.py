from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_async_session
from app.services.match_service import get_matched_tracks
from app.schemas.matcher_schema import MatchedTracksResponse

from app.matchers.matcher_constants import MatcherType

router = APIRouter(prefix="/match")

@router.get("/text")
async def match_hybrid_cascade_api(
    text: str,
    amount: int = 5,
    matcher_type: MatcherType = MatcherType.hybrid_cascade,
    session: AsyncSession = Depends(get_async_session)
) -> MatchedTracksResponse:
    return await get_matched_tracks(text=text, amount=amount, matcher_type=matcher_type, session=session)
