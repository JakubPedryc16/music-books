import json
import numpy as np
from sqlalchemy import select
from app.dal.music_dal import MusicDAL
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from scripts.embedding import cosine_similarity, create_classic_embedding_async, create_tag_embedding_from_embeddings_async
from scripts.matchers.embedding_matcher import match_by_embedding
from scripts.matchers.emotions_matcher import match_by_emotions
from scripts.matchers.features_matcher import match_by_spotify_features
from scripts.matchers.matchers_utils import filter_matches, print_best_worst
from scripts.matchers.tag_matcher import match_by_tags
from scripts.tag import TAGS


async def match_hybrid_cascade(
    text: str,
    amount: int = 5,

    min_spotify: int = 1000,
    max_spotify: int = 10000,
    min_spotify_score: float = 0.5,

    min_emotions: int = 500,
    max_emotions: int = 5000,
    min_emotion_score: float = 0.75,

    min_tags: int = 100,
    max_tags: int = 1000,
    min_tag_score: float = 0.9,

    min_embedding: int = 10,
    max_embedding: int = 100,
    min_embedding_score: float = 0.45,
):
    music_list = []  
    async with AsyncSessionLocal() as session:
            musicDAL = MusicDAL(session)
            music_list = await musicDAL.get_music_columns(
                filter_not_none=[Music.spotify_features, Music.embedding_emotions, Music.embedding_tags, Music.embedding]
            )

    spotify_matches = await match_by_spotify_features(text, amount=max_spotify, music_list_included=music_list)
    spotify_ids = {id_ for id_, _ in spotify_matches}
    music_list = [m for m in music_list if m.id in spotify_ids]
    
    spotify_filtered = filter_matches(
        matches=spotify_matches,
        min_score=min_spotify_score,
        min_amount=min_spotify,
        max_amount=max_spotify
    )
    print_best_worst(spotify_filtered, min_spotify_score)

    emotion_matches = await match_by_emotions(text, amount=max_emotions, music_list_included=music_list)
    emotion_filtered = filter_matches(
        matches=emotion_matches,
        min_score=min_emotion_score,
        min_amount=min_emotions,
        max_amount=max_emotions
    )
    print_best_worst(emotion_filtered, min_emotion_score)

    tag_matches = await match_by_tags(text, amount=max_tags, music_list_included=music_list)
    tag_ids = {id_ for id_, _ in tag_matches}
    music_list = [m for m in music_list if m.id in tag_ids]

    tag_filtered = filter_matches(
        matches=tag_matches,
        min_score=min_tag_score,
        min_amount=min_tags,
        max_amount=max_tags
    )
    print_best_worst(tag_filtered, min_tag_score)

    embedding_matches = await match_by_embedding(text, amount=max_embedding, music_list_included=music_list)
    embedding_ids = {id_ for id_, _ in embedding_matches}
    music_list = [m for m in music_list if m.id in embedding_ids]
    embedding_filtered = filter_matches(
        matches=embedding_matches,
        min_score=min_embedding_score,
        min_amount=min_embedding,
        max_amount=max_embedding
    )
    print_best_worst(embedding_filtered, min_embedding_score)


    embedding_matches.sort(key=lambda x: x[1], reverse=True)
    return embedding_matches[:amount]

