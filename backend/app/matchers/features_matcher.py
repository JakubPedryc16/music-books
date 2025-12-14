from typing import override, List
from app.models.music import Music
from app.services.embedding_service import EmbeddingService
from app.matchers.matcher import Matcher


import numpy as np
from nltk import sent_tokenize, word_tokenize, pos_tag
from sklearn.preprocessing import StandardScaler
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.global_music_context import GlobalMusicContext
from app.utils.logger import logger

CALCULABLE_FEATURES = [
    "danceability",
    "energy",
    "valence",
    "tempo"
]

class FeaturesMatcher(Matcher):
    _scaler: StandardScaler = None

    def __init__(self, embeddingService: EmbeddingService, context: GlobalMusicContext):
        self.embeddingService = embeddingService
        
        if FeaturesMatcher._scaler is None:
            initial_music_list = context.get_full_music_list()
            self._initialize_scaler(initial_music_list)
        
        if FeaturesMatcher._scaler is None:
             logger.warning("FeaturesMatcher: Scaler nie został zainicjowany! Normalizacja może być niestabilna.")

    def _initialize_scaler(self, music_list: List[Music]):
        logger.info(f"FeaturesMatcher: Inicjalizacja Scalera na {len(music_list)} utworach.")
        
        music_features = []
        for m in music_list:
            features = m.spotify_features
            if features:
                music_features.append(
                    np.array([features.get(f, 0) for f in CALCULABLE_FEATURES], dtype=np.float32)
                )

        if not music_features:
            logger.error("FeaturesMatcher: Brak danych do inicjalizacji Scalera.")
            return

        music_matrix = np.vstack(music_features)
        
        FeaturesMatcher._scaler = StandardScaler()
        FeaturesMatcher._scaler.fit(music_matrix)
        logger.info("FeaturesMatcher: Scaler globalny wytrenowany pomyślnie.")
        
    @override
    async def match(
        self,
        session: AsyncSession,
        text: str,
        amount: int = 1,
        music_list_included:list[Music] = None
    ) -> list[tuple[int, float]]:
        
        if FeaturesMatcher._scaler is None:
            raise RuntimeError("FeaturesMatcher: Globalny scaler nie został zainicjowany. Proszę go zainicjować przed użyciem.")
            
        try:
            weights = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)

            sentiment_score = await self.embeddingService.predict_sentiment(text)
            emotion_map = await self.embeddingService.predict_emotions(text)

            feature_vector = self._compute_feature_vector(text, sentiment_score, emotion_map)
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise e
            raise RuntimeError(f"Feature calculation or ML service call failed: {e}")
        
        music_list = music_list_included
        if music_list is None:
            context = GlobalMusicContext()
            music_list = context.get_full_music_list()
            
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

            scaler = FeaturesMatcher._scaler 
            
            music_matrix_std = scaler.transform(music_matrix)
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

        action_dynamism = (dynamism + verb_ratio) / 2

        return np.array([
            action_dynamism,
            0.7*energy + 0.3*action_dynamism,
            valence,
            60 + action_dynamism*100
        ], dtype=np.float32)