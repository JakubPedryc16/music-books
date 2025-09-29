from app.dal.music_dal import MusicDAL
from app.matchers.matcher import Matcher
from app.schemas.matcher_schema import MatchedTracksResponse, SongData, TranslationResponse
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
    
    translation_result: TranslationResponse = await detect_and_translate(text)
    if not translation_result.success:
        logger.warning(f"Skipping matching due to translation error: {translation_result['error']}")
        return MatchedTracksResponse(
            success=False,
            data=[],
            error=translation_result.error
        )

    text_translated = translation_result.data
    matcher_class: Matcher = get_matcher(matcher_type)
    matches: list[tuple[int, float]] = await matcher_class.match(
        session=session,
        text=text_translated,
        amount=amount
        )

    tracks: list[SongData] = []
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
    except Exception as e:
        logger.error("Exception occured while retrieving songs from db: %s", e)
        return MatchedTracksResponse(
            success=False,
            error=f"Exception occured while retrieving songs from db:{e}"
        )

    return MatchedTracksResponse(
        success=True,
        data=tracks
    )
