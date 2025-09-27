
from app.models.music import Music

from app.matchers.embedding_matcher import EmbeddingMatcher
from app.matchers.emotions_matcher import EmotionsMatcher
from app.matchers.features_matcher import FeaturesMatcher
from app.matchers.matcher import Matcher
from sqlalchemy.ext.asyncio import AsyncSession

from app.matchers.tag_matcher import TagsMatcher

class HybridAllMatcher(Matcher):
    def __init__(
        self,
        embedding_matcher: EmbeddingMatcher,
        emotions_matcher: EmotionsMatcher,
        features_matcher: FeaturesMatcher,
        tags_matcher: TagsMatcher

    ):
        self.embedding_matcher = embedding_matcher
        self.emotions_matcher = emotions_matcher
        self.features_matcher = features_matcher
        self.tags_matcher = tags_matcher

    async def match(
        self,
        session: AsyncSession,
        text: str,
        amount: int = 1,
        music_list_included:list[Music] = []
    ) -> list[tuple[int, float]]:
        

        w_embedding: float = 0.25
        w_tags: float = 0.25
        w_spotify: float = 0.25
        w_emotions: float = 0.25

        
        classic = await self.embedding_matcher.match(session=session, text=text, amount=None)
        tags = await self.tags_matcher.match(session=session, text=text, amount=None)
        spotify = await self.features_matcher.match(session=session,text=text, amount=None)
        emotions = await self.emotions_matcher.match(session=session,text=text, amount=None)

        scores = {}
        for music_id, score in classic:
            scores[music_id] = w_embedding * score
        for music_id, score in tags:
            scores[music_id] = scores.get(music_id, 0) + w_tags * score
        for music_id, score in spotify:
            scores[music_id] = scores.get(music_id, 0) + w_spotify * score
        for music_id, score in emotions:
            scores[music_id] = scores.get(music_id, 0) + w_emotions * score

        music_scored = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return music_scored[:amount]
