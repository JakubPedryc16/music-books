
from app.dal.music_dal import MusicDAL
from app.models.music import Music
from app.services.matchers.embedding_matcher import EmbeddingMatcher
from app.services.matchers.emotions_matcher import EmotionsMatcher
from app.services.matchers.features_matcher import FeaturesMatcher
from app.matchers.matcher_logging import filter_matches, print_best_worst
from app.services.matchers.matcher import Matcher
from app.services.matchers.tag_matcher import TagsMatcher
from sqlalchemy.ext.asyncio import AsyncSession

class HybridCascadeMatcher(Matcher):
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
            
        min_spotify: int = 10000,
        max_spotify: int = 50000,
        min_spotify_score: float = 0.35,

        min_emotions: int = 5000,
        max_emotions: int = 25000,
        min_emotion_score: float = 0.6,

        min_tags: int = 2500,
        max_tags: int = 10000,
        min_tag_score: float = 0.8,

        min_embedding: int = 100,
        max_embedding: int = 1000,
        min_embedding_score: float = 0.35,

        musicDAL = MusicDAL(session)
        music_list = await musicDAL.get_music_columns(
            filter_not_none=[
                Music.spotify_features,
                Music.embedding_emotions,
                Music.embedding_tags,
                Music.embedding
            ]
        )

        spotify_matches = await self.features_matcher.match(text, amount=max_spotify, music_list_included=music_list)
        spotify_filtered = filter_matches(
            matches=spotify_matches,
            min_score=min_spotify_score,
            min_amount=min_spotify,
            max_amount=max_spotify
        )
        print_best_worst(spotify_filtered, min_spotify_score)
        spotify_ids = {id_ for id_, _ in spotify_filtered}
        music_list = [m for m in music_list if m.id in spotify_ids]

        emotion_matches = await self.emotions_matcher.match(text, amount=max_emotions, music_list_included=music_list)
        emotion_filtered = filter_matches(
            matches=emotion_matches,
            min_score=min_emotion_score,
            min_amount=min_emotions,
            max_amount=max_emotions
        )
        print_best_worst(emotion_filtered, min_emotion_score)
        emotion_ids = {id_ for id_, _ in emotion_filtered}
        music_list = [m for m in music_list if m.id in emotion_ids]

        tag_matches = await self.tags_matcher.match(text, amount=max_tags, music_list_included=music_list)
        tag_filtered = filter_matches(
            matches=tag_matches,
            min_score=min_tag_score,
            min_amount=min_tags,
            max_amount=max_tags
        )
        print_best_worst(tag_filtered, min_tag_score)
        tag_ids = {id_ for id_, _ in tag_filtered}
        music_list = [m for m in music_list if m.id in tag_ids]

        embedding_matches = await self.embedding_matcher.match(text, amount=max_embedding, music_list_included=music_list)
        embedding_filtered = filter_matches(
            matches=embedding_matches,
            min_score=min_embedding_score,
            min_amount=min_embedding,
            max_amount=max_embedding
        )
        print_best_worst(embedding_filtered, min_embedding_score)
        embedding_ids = {id_ for id_, _ in embedding_filtered}
        music_list = [m for m in music_list if m.id in embedding_ids]

        embedding_filtered.sort(key=lambda x: x[1], reverse=True)
        return embedding_filtered[:amount]
