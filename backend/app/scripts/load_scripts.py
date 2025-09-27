import asyncio
import json
from sqlalchemy import select, update, or_

from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from app.api.dependencies import get_embedding_service, init_embedding_service

async def process_music(service, music: Music, session):
    if not music.lyrics:
        return 

    update_values = {}

    if music.embedding is None:
        loaded_embedding = await service.create_classic_embedding(music.lyrics)
        update_values["embedding"] = loaded_embedding.tobytes()

    if music.embedding_tags is None:
        loaded_tag_embedding = await service.create_tag_embedding(
            music.lyrics, music.spotify_features
        )
        update_values["embedding_tags"] = json.dumps(loaded_tag_embedding)

    if music.embedding_emotions is None:
        loaded_emotion_embedding = await service.predict_emotions(music.lyrics)
        update_values["embedding_emotions"] = json.dumps(loaded_emotion_embedding)

    if update_values:
        await session.execute(
            update(Music)
            .where(Music.id == music.id)
            .values(**update_values)
        )

async def load_music_embeddings(service, batch_size: int = 50):
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

            await asyncio.gather(*(process_music(service, m, session) for m in music_batch))
            await session.commit()

if __name__ == "__main__":
    init_embedding_service()
    embedding_service = get_embedding_service()
    asyncio.run(load_music_embeddings(embedding_service, batch_size=1000))
