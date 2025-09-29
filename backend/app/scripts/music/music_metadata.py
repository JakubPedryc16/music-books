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
SKIP_ROWS = 2_000_000
ADD_COUNT = 100_000_000
BATCH_SIZE = 1_000


async def is_english(lyrics: str) -> bool:
    lyrics = str(lyrics or "")
    if len(lyrics) < 20:
        return False
    try:
        return await asyncio.to_thread(detect, lyrics) == "en"
    except:
        return False


async def process_music_row(row) -> Music | None:
    lyrics = row.get("lyrics", "")
    if not await is_english(lyrics):
        return None

    return Music(
        title=row["name"],
        author=row["artists"],
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
            "speechiness": row.get("speechiness"),
        }
    )


async def process_batch(df_batch: pd.DataFrame, session) -> int:
    tasks = [process_music_row(row) for _, row in df_batch.iterrows()]
    music_objects = await asyncio.gather(*tasks)
    music_list = [m for m in music_objects if m is not None]

    if music_list:
        session.add_all(music_list)
        await session.commit()
        print(f"Saved {len(music_list)} tracks to DB.")

    return len(music_list)


async def load_music_metadata():
    df: pd.DataFrame = pd.read_csv(MUSIC_DIR)

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Music.title))
        existing_titles = set(r[0] for r in res.all())

        df_new = df.iloc[SKIP_ROWS:].reset_index(drop=True)
        df_new = df_new[~df_new["name"].isin(existing_titles)].reset_index(drop=True)
        if df_new.empty:
            print("No new tracks to add.")
            return

        total_saved = 0
        for start in range(0, min(len(df_new), ADD_COUNT), BATCH_SIZE):
            end = start + BATCH_SIZE
            df_batch = df_new.iloc[start:end]
            saved = await process_batch(df_batch, session)
            total_saved += saved

        print(f"Total saved tracks: {total_saved}")


if __name__ == "__main__":
    asyncio.run(load_music_metadata())
