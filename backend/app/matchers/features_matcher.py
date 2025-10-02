from typing import override
from app.dal.music_dal import MusicDAL
from app.models.music import Music

import numpy as np

from nltk import sent_tokenize, word_tokenize, pos_tag
from sklearn.preprocessing import StandardScaler

from app.services.embedding_service import EmbeddingService
from app.matchers.matcher import Matcher

from sqlalchemy.ext.asyncio import AsyncSession

CALCULABLE_FEATURES = [
    "danceability",
    "energy",
    "valence",
    "tempo"
]

class FeaturesMatcher(Matcher):
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
        
        try:
            weights = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)

            sentiment_score = await self.embeddingService.predict_sentiment(text)
            emotion_map = await self.embeddingService.predict_emotions(text)

            feature_vector = self._compute_feature_vector(text, sentiment_score, emotion_map)
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise e
            raise RuntimeError(f"Feature calculation or ML service call failed: {e}")
        
        music_list = []
        
        if music_list_included is None:
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

        if not music_features:
            return []
        
        try:
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
        except Exception as e:
            raise RuntimeError(f"Matching failed due to error in numerical calculation: {e}")


    def _compute_feature_vector(self, text: str, sentiment_score: float, emotion_map: dict) -> np.ndarray:
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

            return np.array([
                dynamism,
                0.7*energy + 0.3*verb_ratio,
                valence,
                60 + dynamism*100
            ], dtype=np.float32)