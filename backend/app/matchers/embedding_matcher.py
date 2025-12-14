from typing import override
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.dal.music_dal import MusicDAL
from app.models.music import Music
from app.services.embedding_service import EmbeddingService
from app.matchers.matcher import Matcher
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.global_music_context import GlobalMusicContext # NOWY IMPORT

class EmbeddingMatcher(Matcher):
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
        
        book_embedding = await self.embeddingService.create_classic_embedding(text)
        music_list = []
        
        if music_list_included is None:
            context = GlobalMusicContext()
            music_list = context.get_full_music_list()
        else:
            music_list = music_list_included

        music_list = [m for m in music_list if m.embedding is not None]

        music_ids = [music.id for music in music_list]
        music_embeddings = [np.frombuffer(m.embedding, dtype=np.float32) for m in music_list]
        if not music_embeddings:
            return []
        
        try:
            music_matrix = np.vstack(music_embeddings)
            sims = cosine_similarity([book_embedding], music_matrix)[0]
            music_scored = list(zip(music_ids, sims))
            music_scored.sort(key=lambda x: x[1], reverse=True)

            return music_scored[:amount]
        except Exception as e:
            raise RuntimeError(f"Matching failed due to error in numerical calculation: {e}")