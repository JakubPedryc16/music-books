from fastapi import HTTPException
from app.dal.music_dal import DataAccessException, MusicDAL
from app.matchers.matcher import Matcher
from app.schemas.matcher_schema import SongData
from app.matchers.matcher_constants import MatcherType
from app.services.translation_service import detect_and_translate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logger import logger
from app.api.dependencies import get_matcher
from typing import List
import traceback

async def get_matched_tracks(
    text: str,
    amount: int,
    matcher_type: MatcherType,
    session: AsyncSession
) -> List[SongData]:

    try:
        text_translated: str = await detect_and_translate(text)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception("Error calling translation service. Possible network issue.")
        raise HTTPException(
            status_code=502,
            detail="Failed to communicate with translation service."
        )

    matcher_class: Matcher = get_matcher(matcher_type)
    
    try:
        matches: list[tuple[int, float]] = await matcher_class.match(
            session=session,
            text=text_translated,
            amount=amount
        )
    except RuntimeError as e:
        logger.error(f"Matching failed due to internal ML error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal matching service error (ML model failure). Please try again."
        )
    
    try:
        music_ids = [music_id for music_id, _ in matches]
        music_dal = MusicDAL(session)
        music_list = await music_dal.get_all_by_ids(music_ids)

        tracks = [
            SongData(
                title=m.title,
                author=m.author,
                spotify_id=m.spotify_id
            )
            for m in music_list
        ]

    except DataAccessException as e:
        logger.error(f"Database error during track retrieval: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database connection error while retrieving tracks."
        )
    except Exception as e:
        logger.exception("An unexpected error occurred during track retrieval.")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during track retrieval."
        )

    return tracks
