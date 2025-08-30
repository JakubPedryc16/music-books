import os
import numpy as np
import json
import asyncio
import torch
from scripts.spotify_features import spotify_features_to_text
from app.db.db_async import AsyncSessionLocal
from sqlalchemy import or_, select, update
from app.models.music import Music

from scripts.ml_models.models import model, model_emotions, tokenizer, emotion_labels

CONFIG_DIR = "backend/data/tags/"
os.makedirs(CONFIG_DIR, exist_ok=True)

TAGS_FILE = os.path.join(CONFIG_DIR, "tags.json")
EMBEDDINGS_FILE = os.path.join(CONFIG_DIR, "tag_embeddings.npy")

with open(TAGS_FILE, "r") as f:
    TAGS = json.load(f)

tag_embeddings = np.load(EMBEDDINGS_FILE)

async def create_classic_embedding_async(text: str) -> np.ndarray:
    embedding_vector = await asyncio.to_thread(
        model.encode, text, convert_to_numpy=True, normalize_embeddings=True
    )
    return embedding_vector.astype(np.float32)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

async def create_tag_embedding_from_embeddings_async(text: str, spotify_features: dict = None) -> dict:
    full_text = text
    if spotify_features:
        spotify_desc = spotify_features_to_text(spotify_features)
        full_text = f"{text.strip()}\n\n{spotify_desc.strip()}"
    
    text_embedding = await create_classic_embedding_async(full_text)
    
    similarities = [float(cosine_similarity(text_embedding, t)) for t in tag_embeddings]
    return dict(zip(TAGS, similarities))

async def predict_emotions_async(text: str) -> dict:
    """Tworzy embedding emocji dla tekstu piosenki."""
    inputs = await asyncio.to_thread(tokenizer, text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = await asyncio.to_thread(model_emotions, **inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1).squeeze().tolist()
    
    return {emotion_labels[i]: float(probs[i]) for i in range(len(probs))}
    

async def process_music(music: Music, session):
    if not music.lyrics:
        return 

    update_values = {}

    # --- klasyczny embedding ---
    if music.embedding is None:
        loaded_embedding = await create_classic_embedding_async(music.lyrics)
        update_values["embedding"] = loaded_embedding.tobytes()

    # --- tagowe embedding ---
    if music.embedding_tags is None:
        loaded_tag_embedding = await create_tag_embedding_from_embeddings_async(
            music.lyrics, music.spotify_features
        )
        update_values["embedding_tags"] = json.dumps(loaded_tag_embedding)

    # --- embedding emocji ---
    if music.embedding_emotions is None:
        loaded_emotion_embedding = await predict_emotions_async(music.lyrics)
        update_values["embedding_emotions"] = json.dumps(loaded_emotion_embedding)

    # --- aktualizacja tylko brakujących pól ---
    if update_values:
        await session.execute(
            update(Music)
            .where(Music.id == music.id)
            .values(**update_values)
        )



async def load_music_embeddings(batch_size: int = 50):
    async with AsyncSessionLocal() as session:
        while True:
            music_batch = (
                await session.scalars(
                    select(Music)
                    .where(
                        or_(
                            Music.embedding.is_(None),
                            Music.embedding_tags.is_(None),
                            Music.embedding_emotions.is_(None)
                        )
                    )
                    .limit(batch_size)
                )
            ).all()

            if not music_batch:
                break 

            await asyncio.gather(*(process_music(m, session) for m in music_batch))
            await session.commit()


if __name__ == "__main__":
    asyncio.run(load_music_embeddings(1000))
