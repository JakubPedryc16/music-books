import json
from typing import List
import numpy as np
from sqlalchemy import select
from sklearn.metrics.pairwise import cosine_similarity
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from app.dal.music_dal import MusicDAL
from scripts.embedding import create_tag_embedding_from_embeddings_async
from scripts.tag import TAGS

async def match_by_tags(text: str, amount: int = 1, music_list_included:List[Music] =None):
    tag_vector_dict = await create_tag_embedding_from_embeddings_async(text)
    tag_vector = np.array([tag_vector_dict[tag] for tag in TAGS], dtype=np.float32)
    music_list = []
    if (music_list_included == None):
        async with AsyncSessionLocal() as session:
            musicDAL = MusicDAL(session)
            music_list = musicDAL.get_music_columns(
                columns=[Music.id, Music.embedding_tags],
                filter_not_none=[Music.embedding_tags]
            )
    else:
        music_list = music_list_included

    music_ids = [music.id for music in music_list]

    music_embeddings = []
    for m in music_list:
        current = json.loads(m.embedding_tags)
        music_embeddings.append(np.array([current.get(tag, 0) for tag in TAGS], dtype=np.float32))

    music_matrix = np.vstack(music_embeddings)
    sims = cosine_similarity([tag_vector], music_matrix)[0]

    music_scored = list(zip(music_ids, sims))
    music_scored.sort(key=lambda x: x[1], reverse=True)
    return music_scored[:amount]