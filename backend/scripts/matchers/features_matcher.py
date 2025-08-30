from typing import List
from app.dal.music_dal import MusicDAL
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from scripts.embedding import predict_emotions_async

import numpy as np
import torch
from nltk import sent_tokenize, word_tokenize, pos_tag
from sklearn.preprocessing import StandardScaler

from scripts.ml_models.models import sentiment_model, sentiment_tokenizer

CALCULABLE_FEATURES = [
    "danceability",
    "energy",
    "valence",
    "tempo"
]

async def match_by_spotify_features(text: str, amount: int = 1, weights=None, music_list_included:List[Music] =None):
    if weights is None:
        weights = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)

    inputs = sentiment_tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = sentiment_model(**inputs)
        scores = torch.softmax(outputs.logits, dim=1)
        sentiment_score = scores[0,1].item() * 2 - 1

    emotion_map = await predict_emotions_async(text)
    valence = (emotion_map.get("joy",0) + 0.5*(1-emotion_map.get("sadness",0)))
    valence = (valence + (sentiment_score + 1)/2) / 2
    energy = emotion_map.get("anger",0) + emotion_map.get("fear",0) + 0.5*emotion_map.get("surprise",0)
    valence = min(max(valence,0),1)
    energy = min(max(energy,0),1)

    sentences = [s.strip() for s in sent_tokenize(text) if s.strip()]
    avg_sentence_len = np.mean([len(s.split()) for s in sentences]) if sentences else 1
    dynamism = min(max(1 - avg_sentence_len / 20, 0), 1.0)

    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    verb_count = sum(1 for _, pos in pos_tags if pos.startswith("VB"))
    verb_ratio = min(verb_count / max(len(tokens),1), 1.0)

    feature_vector = np.array([
        dynamism,                     # danceability
        0.7*energy + 0.3*verb_ratio,  # energy
        valence,                       # valence
        60 + dynamism*100              # tempo
    ], dtype=np.float32)

    print(f"[FEATURES] Fragment '{text[:50]}...' ma cechy:")
    print(f"  danceability: {feature_vector[0]:.4f}")
    print(f"  energy:       {feature_vector[1]:.4f}")
    print(f"  valence:      {feature_vector[2]:.4f}")
    print(f"  tempo:        {feature_vector[3]:.2f}")



    music_list = []
    
    if music_list_included == None:
        async with AsyncSessionLocal() as session:
            musicDAL = MusicDAL(session)
            music_list = await musicDAL.get_music_columns(
                columns=[Music.id, Music.spotify_features],
                filter_not_none=[Music.spotify_features]
            )
    else:
        music_list = music_list_included

    music_ids = [m.id for m in music_list]
    music_features = []
    for m in music_list:
        features = m.spotify_features
        music_features.append(
            np.array([features.get(f, 0) for f in CALCULABLE_FEATURES], dtype=np.float32)
        )
    music_matrix = np.vstack(music_features)

    scaler = StandardScaler()
    music_matrix_std = scaler.fit_transform(music_matrix)
    feature_vector_std = scaler.transform(feature_vector.reshape(1, -1))

    weighted_diff = weights * (music_matrix_std - feature_vector_std)
    distances = np.linalg.norm(weighted_diff, axis=1)
    scores = 1 / (1 + distances) 

    music_scored = list(zip(music_ids, scores))
    music_scored.sort(key=lambda x: x[1], reverse=True)

    return music_scored[:amount]
