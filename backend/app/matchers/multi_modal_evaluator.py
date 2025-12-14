from app.models.music import Music
from app.matchers.embedding_matcher import EmbeddingMatcher
from app.matchers.emotions_matcher import EmotionsMatcher
from app.matchers.features_matcher import FeaturesMatcher
from app.matchers.matcher import Matcher
from app.matchers.tag_matcher import TagsMatcher
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from app.utils.logger import logger 

class MultiModalEvaluator(Matcher): 
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
        tracks_to_evaluate: List[Music],
        log_results: bool = True 
    ) -> Dict[int, Dict[str, float]]:
        
        if not tracks_to_evaluate:
            return {}

        num_tracks = len(tracks_to_evaluate)

        fm_matches = await self.features_matcher.match(session=session, text=text, amount=num_tracks, music_list_included=tracks_to_evaluate)
        emo_matches = await self.emotions_matcher.match(session=session, text=text, amount=num_tracks, music_list_included=tracks_to_evaluate)
        tm_matches = await self.tags_matcher.match(session=session, text=text, amount=num_tracks, music_list_included=tracks_to_evaluate)
        em_matches = await self.embedding_matcher.match(session=session, text=text, amount=num_tracks, music_list_included=tracks_to_evaluate)

        fm_dict = dict(fm_matches)
        emo_dict = dict(emo_matches)
        tm_dict = dict(tm_matches)
        em_dict = dict(em_matches)
        
        final_results = {}

        if log_results:
            logger.info("--- START MULTIMODAL EVALUATOR REPORT ---")
            logger.info(f"Query text: '{text[:50]}...'")

        for music in tracks_to_evaluate:
            music_id = music.id
            
            results = {
                "features_score": fm_dict.get(music_id, 0.0),
                "emotions_score": emo_dict.get(music_id, 0.0),
                "tags_score": tm_dict.get(music_id, 0.0),
                "embedding_score": em_dict.get(music_id, 0.0)
            }
            final_results[music_id] = results
            
            if log_results:
                title = music.title if hasattr(music, 'title') else 'Unknown Title'
                logger.info(
                    f"Track ID {music_id} ({title}): "
                    f"FM={results['features_score']:.4f}, "
                    f"EMO={results['emotions_score']:.4f}, "
                    f"TM={results['tags_score']:.4f}, "
                    f"EM={results['embedding_score']:.4f}"
                )
        
        if log_results:
            logger.info("--- END MULTIMODAL EVALUATOR REPORT ---")
            
        return final_results