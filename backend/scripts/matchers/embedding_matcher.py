from typing import List
import numpy as np
from sqlalchemy import Row
from sklearn.metrics.pairwise import cosine_similarity
from app.dal.music_dal import MusicDAL
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from scripts.embedding import create_classic_embedding_async


async def match_by_embedding(text: str, amount: int = 1, music_list_included:List[Music] = None):
    book_embedding = await create_classic_embedding_async(text)
    music_list = []
    
    if music_list_included == None:
        async with AsyncSessionLocal() as session:
            music_dal = MusicDAL(session)
            music_list = await music_dal.get_music_columns(
                columns=[Music.id, Music.embedding],
                filter_not_none= [Music.embedding]
            )
    else:
        music_list = music_list_included

    music_ids = [music.id for music in music_list]
    music_embeddings = [np.frombuffer(m.embedding, dtype=np.float32) for m in music_list]

    music_matrix = np.vstack(music_embeddings)

    sims = cosine_similarity([book_embedding], music_matrix)[0]
    music_scored = list(zip(music_ids, sims))
    music_scored.sort(key=lambda x: x[1], reverse=True)

    return music_scored[:amount]
