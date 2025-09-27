from app.dal.music_dal import MusicDAL
from app.schemas.matcher_schema import MatchedTracksResponse, SongResponse
from app.matchers.matcher_constants import MatcherType
from app.services.translation_service import detect_and_translate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logger import logger
from app.api.dependencies import get_matcher

async def get_matched_tracks(
    text: str,
    amount: int,
    matcher_type: MatcherType,
    session: AsyncSession
) -> MatchedTracksResponse:
    
    translation_result = await detect_and_translate(text)
    if not translation_result["success"]:
        logger.warning(f"Skipping matching due to translation error: {translation_result['error']}")
        return {
            "success": False,
            "tracks": [],
            "error": translation_result["error"]
        }

    text_translated = translation_result["text"]
    matcher_class = get_matcher(matcher_type)
    matches = await matcher_class.match(session=session, text=text_translated, amount=amount)

    tracks: list[SongResponse] = []
    try:
        music_ids = [music_id for music_id, _ in matches]
        music_dal = MusicDAL(session)
        music_list = await music_dal.get_all_by_ids(music_ids)

        tracks = [
            SongResponse(
                title=m.title,
                author=m.author,
                spotify_id=m.spotify_id
            )
            for m in music_list
        ]
    except Exception as err:
        logger.error("Exception occured while retrieving songs from db: %s", err)
        return {
            "success": False,
            "tracks": [],
            "error": "Błąd podczas pobierania piosenek z bazy danych"
        }

    return {
        "success": True,
        "tracks": tracks,
        "error": None
    }
