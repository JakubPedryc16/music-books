from typing import List
import numpy as np
import asyncio
import torch
from app.utils.spotify_features_to_text import spotify_features_to_text
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingService:
    def __init__(
        self,
        tags: List[str],
        tag_embeddings: np.ndarray,
        embedding_model,
        emotion_model,
        emotion_tokenizer,
        emotion_labels,
        sentiment_model,
        sentiment_tokenizer,
    ): 
        self.tags = tags
        self.tag_embeddings = tag_embeddings
        self.embedding_model = embedding_model
        self.emotion_model = emotion_model
        self.emotion_tokenizer = emotion_tokenizer
        self.emotion_labels = list(emotion_labels.values())
        self.sentiment_model = sentiment_model
        self.sentiment_tokenizer = sentiment_tokenizer


    async def create_classic_embedding(self, text: str) -> np.ndarray:
        embedding_vector = await asyncio.to_thread(
            self.embedding_model.encode, text, convert_to_numpy=True, normalize_embeddings=True
        )
        return embedding_vector.astype(np.float32)

    async def create_tag_embedding(self, text: str, spotify_features: dict = None) -> dict[str, float]:
        full_text = text
        if spotify_features:
            spotify_desc = spotify_features_to_text(spotify_features)
            full_text = f"{text.strip()}\n\n{spotify_desc.strip()}"

        text_embedding = await self.create_classic_embedding(full_text)
        
        text_embedding_2d = text_embedding.reshape(1, -1)
        
        similarities_array = await asyncio.to_thread(cosine_similarity, text_embedding_2d, self.tag_embeddings)
        
        similarities = similarities_array.flatten()
        return dict(zip(self.tags, map(float, similarities)))


    async def predict_emotions(self, text: str) -> dict[str, float]:
        return await asyncio.to_thread(self._predict_emotions_sync, text)

    def _predict_emotions_sync(self, text: str):
        inputs = self.emotion_tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1).squeeze().tolist()
        return dict(zip(self.emotion_labels, map(float, probs)))
    
    async def predict_sentiment(self, text: str) -> float:
        if self.sentiment_model is None or self.sentiment_tokenizer is None:
            raise RuntimeError("Sentiment model not initialized")
        return await asyncio.to_thread(self._predict_sentiment_sync, text)

    def _predict_sentiment_sync(self, text: str) -> float:
        inputs = self.sentiment_tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = self.sentiment_model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)
            return scores[0,1].item() * 2 - 1
    