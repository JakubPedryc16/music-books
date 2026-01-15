import time
from app.models.music import Music
from app.matchers.embedding_matcher import EmbeddingMatcher
from app.matchers.emotions_matcher import EmotionsMatcher
from app.matchers.features_matcher import FeaturesMatcher
from app.matchers.matcher_logging import filter_matches, print_best_worst
from app.matchers.matcher import Matcher
from app.matchers.tag_matcher import TagsMatcher
from sqlalchemy.ext.asyncio import AsyncSession
from app.matchers.multi_modal_evaluator import MultiModalEvaluator 
from app.services.global_music_context import GlobalMusicContext
from typing import List, Tuple
from app.utils.logger import logger

class HybridCascadeMatcher(Matcher):
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
        music_list_included: list[Music] = []
    ) -> list[tuple[int, float]]:
        
        times = {}
        start_total = time.perf_counter()
        
        w_embedding: float = 0.25
        w_tags: float = 0.25
        w_spotify: float = 0.25
        w_emotions: float = 0.25
        
        min_spotify: int = 1000
        max_spotify: int = 50000
        min_spotify_score: float = 0.35

        min_emotions: int = 500
        max_emotions: int = 25000
        min_emotion_score: float = 0.6

        min_tags: int = 250
        max_tags: int = 10000
        min_tag_score: float = 0.8
        
        context = GlobalMusicContext()
        music_list = context.get_full_music_list()

        s1 = time.perf_counter()
        spotify_matches = await self.features_matcher.match(session=session, text=text, amount=max_spotify, music_list_included=music_list)
        spotify_filtered = filter_matches(
            matches=spotify_matches,
            min_score=min_spotify_score,
            min_amount=min_spotify,
            max_amount=max_spotify
        )
        times['S1(Feat)'] = time.perf_counter() - s1

        print_best_worst(spotify_filtered, min_spotify_score, "FEATURES")
        spotify_ids = {id_ for id_, _ in spotify_filtered}
        music_list = [m for m in music_list if m.id in spotify_ids]

        s2 = time.perf_counter()
        emotion_matches = await self.emotions_matcher.match(session=session, text=text, amount=max_emotions, music_list_included=music_list)
        emotion_filtered = filter_matches(
            matches=emotion_matches,
            min_score=min_emotion_score,
            min_amount=min_emotions,
            max_amount=max_emotions
        )
        times['S2(Emot)'] = time.perf_counter() - s2

        print_best_worst(emotion_filtered, min_emotion_score, "EMOTION")
        emotion_ids = {id_ for id_, _ in emotion_filtered}
        music_list = [m for m in music_list if m.id in emotion_ids]

        s3 = time.perf_counter()
        tag_matches = await self.tags_matcher.match(session=session, text=text, amount=max_tags, music_list_included=music_list)
        tag_filtered = filter_matches(
            matches=tag_matches,
            min_score=min_tag_score,
            min_amount=min_tags,
            max_amount=max_tags
        )
        times['S3(Tags)'] = time.perf_counter() - s3

        print_best_worst(tag_filtered, min_tag_score, "TAGS")
        tag_ids = {id_ for id_, _ in tag_filtered}
        tracks_for_evaluation = [m for m in music_list if m.id in tag_ids]

        if not tracks_for_evaluation:
            return []
            
        s4 = time.perf_counter()
        detailed_scores = await self.multimodal_evaluator.match(
            session=session, 
            text=text, 
            tracks_to_evaluate=tracks_for_evaluation,
            log_results=False
        )
        times['S4(Eval)'] = time.perf_counter() - s4

        fused_scores = []
        for music_id, scores in detailed_scores.items():
            avg_score = (
                scores.get("embedding_score", 0.0) * w_embedding + 
                scores.get("tags_score", 0.0) * w_tags +
                scores.get("features_score", 0.0) * w_spotify +
                scores.get("emotions_score", 0.0) * w_emotions
            )
            fused_scores.append((music_id, avg_score))

        fused_scores.sort(key=lambda x: x[1], reverse=True)
        final_ranking = fused_scores[:amount]
        
        final_ids = [id_ for id_, _ in final_ranking]
        
        if final_ids:
            tracks_to_evaluate_final = [t for t in tracks_for_evaluation if t.id in final_ids]
            
            s5 = time.perf_counter()
            final_detailed_scores = await self.multimodal_evaluator.match(
                session=session, 
                text=text, 
                tracks_to_evaluate=tracks_to_evaluate_final,
                log_results=True
            )
            times['S5(Final)'] = time.perf_counter() - s5

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
                    logger.info(f"Hybrid Cascade Matcher: Average scores for final {count} tracks: {avg_scores}")
            
        times['Total'] = time.perf_counter() - start_total
        report = " | ".join([f"{k}: {v:.4f}s" for k, v in times.items()])
        logger.info(f"CASCADE PERFORMANCE: {report}")
        
        return final_ranking