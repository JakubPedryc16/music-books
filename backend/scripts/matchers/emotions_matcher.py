import json
from typing import List
import numpy as np
from sqlalchemy import select
from app.dal.music_dal import MusicDAL
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from scripts.embedding import predict_emotions_async
from sklearn.metrics.pairwise import cosine_similarity

async def match_by_emotions(text: str, amount: int = 5, music_list_included:List[Music] = None):

    emotion_scores = await predict_emotions_async(text)
    text_emotion_vector = np.array([emotion_scores[label] for label in emotion_scores], dtype=np.float32)
    music_list = []
    
    if music_list_included == None:
        async with AsyncSessionLocal() as session:
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

    music_matrix = np.vstack(music_embeddings)

    sims = cosine_similarity([text_emotion_vector], music_matrix)[0]
    music_scored = list(zip(music_ids, sims))
    music_scored.sort(key=lambda x: x[1], reverse=True)

    return music_scored[:amount]
