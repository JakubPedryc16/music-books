import asyncio
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import select
from langdetect import detect, DetectorFactory
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music

load_dotenv()
DetectorFactory.seed = 0 

MUSIC_DIR = "data/music/spotify_songs2.csv"
MAX_SONGS = 100000

async def load_music_metadata():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Music.title))
        existing_titles = set(r[0] for r in res.all())

    df = pd.read_csv(MUSIC_DIR)

    music_list = []

    for _, row in df.iterrows():
        if len(existing_titles) >= MAX_SONGS:
            break

        title = row["name"]
        author = row["artists"]

        if title in existing_titles:
            continue

        lyrics = row.get("lyrics", "")

        # Sprawdzenie języka tylko jeśli są teksty
        if lyrics:
            try:
                if detect(lyrics) != "en":
                    continue  # ignorujemy nieangielskie piosenki
            except:
                continue

        music = Music(
            title=title,
            author=author,
            lyrics=lyrics,

            spotify_id=row.get("id"),
            duration_ms=row.get("duration_ms"),
            popularity=row.get("track_popularity", ""),

            spotify_features={
                "danceability": row.get("danceability"),
                "energy": row.get("energy"),
                "valence": row.get("valence"),
                "tempo": row.get("tempo"),
                "acousticness": row.get("acousticness"),
                "instrumentalness": row.get("instrumentalness"),
                "liveness": row.get("liveness"),
                "speechiness": row.get("speechiness")
            }
        )

        music_list.append(music)
        existing_titles.add(title)

    async with AsyncSessionLocal() as session:
        session.add_all(music_list)
        await session.commit()
        print(f"Saved {len(music_list)} tracks to DB.")

if __name__ == "__main__":
    asyncio.run(load_music_metadata())
