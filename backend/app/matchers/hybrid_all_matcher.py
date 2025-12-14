from app.models.music import Music
from app.matchers.embedding_matcher import EmbeddingMatcher
from app.matchers.emotions_matcher import EmotionsMatcher
from app.matchers.features_matcher import FeaturesMatcher
from app.matchers.matcher import Matcher
from app.matchers.tag_matcher import TagsMatcher
from app.matchers.multi_modal_evaluator import MultiModalEvaluator 
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.global_music_context import GlobalMusicContext
from typing import List, Tuple
from app.utils.logger import logger

class HybridAllMatcher(Matcher):
    def __init__(
        self,
        embedding_matcher: EmbeddingMatcher,
        emotions_matcher: EmotionsMatcher,
        features_matcher: FeaturesMatcher,
        tags_matcher: TagsMatcher,
        multimodal_evaluator: MultiModalEvaluator 
    ):
        self.embedding_matcher = embedding_matcher
        self.emotions_matcher = emotions_matcher
        self.features_matcher = features_matcher
        self.tags_matcher = tags_matcher
        self.multimodal_evaluator = multimodal_evaluator

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
        final_ranking = music_scored[:amount]

        final_ids = [id_ for id_, _ in final_ranking]
        
        if final_ids:
            context = GlobalMusicContext()
            
            all_music_map = {music.id: music for music in context.get_full_music_list()}
            tracks_to_evaluate = [all_music_map[id_] for id_ in final_ids if id_ in all_music_map]
            
            final_detailed_scores = await self.multimodal_evaluator.match(
                session=session, 
                text=text, 
                tracks_to_evaluate=tracks_to_evaluate,
                log_results=True
            )
            
            if final_detailed_scores:
                avg_scores = {}
                count = len(final_detailed_scores)
                
                sum_embedding = sum_tags = sum_features = sum_emotions = 0.0
                
                for scores in final_detailed_scores.values():
                    sum_embedding += scores.get("embedding_score", 0.0)
                    sum_tags += scores.get("tags_score", 0.0)
                    sum_features += scores.get("features_score", 0.0)
                    sum_emotions += scores.get("emotions_score", 0.0)

                if count > 0:
                    avg_scores['embedding_score'] = sum_embedding / count
                    avg_scores['tags_score'] = sum_tags / count
                    avg_scores['features_score'] = sum_features / count
                    avg_scores['emotions_score'] = sum_emotions / count

                    logger.info(f"Hybrid All Matcher: Average scores for final {count} tracks: {avg_scores}")
            
        return final_ranking