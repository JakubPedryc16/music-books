import asyncio
import pandas as pd
from dotenv import load_dotenv

from sqlalchemy import select
from src.db.db_async import AsyncSessionLocal
from src.models.music import Music

load_dotenv()

MUSIC_DIR = "data/music/spotify_songs.csv"
MAX_SONGS = 100

async def load_music_metadata():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Music.title))
        existing_titles = set(r[0] for r in res.all())

    df = pd.read_csv(MUSIC_DIR)

    df = df.head(MAX_SONGS)

    music_list = []

    for _, row in df.iterrows():
        title = row["track_name"]
        author = row["track_artist"]

        if title in existing_titles:
            continue

        music = Music(
            title=title,
            author=author,
            lyrics=row.get("lyrics", ""),

            spotify_id=row.get("track_id"),
            duration_ms=row.get("duration_ms"),
            popularity=row.get("track_popularity"),

            danceability=row.get("danceability"),
            energy=row.get("energy"),
            valence=row.get("valence"),
            tempo=row.get("tempo"),
            acousticness=row.get("acousticness"),
            instrumentalness=row.get("instrumentalness"),
            liveness=row.get("liveness"),
            speechiness=row.get("speechiness"),
        )

        music_list.append(music)
        existing_titles.add(title)

    async with AsyncSessionLocal() as session:
        session.add_all(music_list)
        await session.commit()
        print(f"Saved {len(music_list)} tracks to DB.")

if __name__ == "__main__":
    asyncio.run(load_music_metadata())
