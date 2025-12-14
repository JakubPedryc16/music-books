import json
from typing import override
import numpy as np
from app.models.music import Music
from app.services.embedding_service import EmbeddingService
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession
from app.matchers.matcher import Matcher
from app.services.global_music_context import GlobalMusicContext


class EmotionsMatcher(Matcher):
    def __init__(self, embeddingService: EmbeddingService):
        self.embeddingService = embeddingService

    @override
    async def match(
        self,
        session: AsyncSession,
        text: str,
        amount: int = 1,
        music_list_included:list[Music] = None
    ) -> list[tuple[int, float]]:
        
        emotion_scores = await self.embeddingService.predict_emotions(text)
        text_emotion_vector = np.array([emotion_scores[label] for label in emotion_scores], dtype=np.float32)
        
        music_list = music_list_included
        
        if music_list is None:
            context = GlobalMusicContext()
            music_list = context.get_full_music_list()
        
        music_list = [m for m in music_list if m.embedding_emotions is not None]

        music_ids = []
        music_embeddings = []
        for m in music_list:
            current = json.loads(m.embedding_emotions)
            music_embeddings.append(np.array(
                [current.get(label, 0.0) for label in emotion_scores],
                dtype=np.float32
            ))

            music_ids.append(m.id)

        if not music_embeddings:
            return []
        
        try:
            music_matrix = np.vstack(music_embeddings)
            sims = cosine_similarity([text_emotion_vector], music_matrix)[0]
            music_scored = list(zip(music_ids, sims))
            music_scored.sort(key=lambda x: x[1], reverse=True)
            return music_scored[:amount]
        except Exception as e:
            raise RuntimeError(f"Matching failed due to error in numerical calculation: {e}")