import json
from typing import override
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.models.music import Music
from app.services.embedding_service import EmbeddingService
from app.matchers.matcher import Matcher
from app.utils.tag_generator import TAGS
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.global_music_context import GlobalMusicContext # DODANY IMPORT


class TagsMatcher(Matcher):
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
        
        tag_vector_dict = await self.embeddingService.create_tag_embedding(text)
        tag_vector = np.array([tag_vector_dict[tag] for tag in TAGS], dtype=np.float32)
        
        music_list = music_list_included
        if music_list is None:
            context = GlobalMusicContext()
            music_list = context.get_full_music_list()
        
        music_list = [m for m in music_list if m.embedding_tags is not None]

        music_ids = [music.id for music in music_list]

        music_embeddings = []
        for m in music_list:
            current = json.loads(m.embedding_tags)
            music_embeddings.append(np.array([current.get(tag, 0) for tag in TAGS], dtype=np.float32))

        if not music_embeddings:
            return []
        
        try:
            music_matrix = np.vstack(music_embeddings)
            sims = cosine_similarity([tag_vector], music_matrix)[0]

            music_scored = list(zip(music_ids, sims))
            music_scored.sort(key=lambda x: x[1], reverse=True)
            return music_scored[:amount]
            
        except Exception as e:
            raise RuntimeError(f"Matching failed due to error in numerical calculation: {e}")