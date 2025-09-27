import json
from typing import override
import numpy as np
from app.dal.music_dal import MusicDAL
from app.models.music import Music
from app.services.embedding_service import EmbeddingService
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession
from app.matchers.matcher import Matcher


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
        music_list = []
        
        if music_list_included is None:
            musicDAL = MusicDAL(session)
            music_list = await musicDAL.get_music_columns(
                columns=[Music.id, Music.embedding_emotions],
                filter_not_none=[Music.embedding_emotions]
            )
        else:
            music_list = music_list_included

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
        
        music_matrix = np.vstack(music_embeddings)

        sims = cosine_similarity([text_emotion_vector], music_matrix)[0]
        music_scored = list(zip(music_ids, sims))
        music_scored.sort(key=lambda x: x[1], reverse=True)

        return music_scored[:amount]
