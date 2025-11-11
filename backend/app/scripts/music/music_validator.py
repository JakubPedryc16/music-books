
import asyncio
from app.dal.music_dal import MusicDAL
from app.db.db_async import AsyncSessionLocal
from app.models.music import Music
from sqlalchemy.ext.asyncio import AsyncSession

signs_to_remove = "{}[]'\"<>./ -+!"
BATCH_SIZE = 1000

async def validate_track(music: Music, session: AsyncSession):

    modified_title: str = (music.title or "").strip(signs_to_remove).replace("\"", "")
    modified_author: str = (music.author or "").strip(signs_to_remove).replace(";", ", ").replace("\"", "")

    if not modified_title or not modified_author or not music.lyrics:
        await session.delete(music)
        return
    
    if modified_title == music.title and modified_author == music.author:
        return

    music.author = modified_author
    music.title = modified_title


async def validate_all():
    async with AsyncSessionLocal() as session:
        musicDAL = MusicDAL(session=session)
        musicList: list[Music] = await musicDAL.get_music_columns()
        tracks_count = len(musicList)

        for i in range(0, tracks_count, BATCH_SIZE):
            print(f"{i} / {tracks_count}")

            batch = musicList[i: i + BATCH_SIZE]

            for music in batch:
                await validate_track(music, session)
            
            await session.commit()


if __name__ == "__main__":
    asyncio.run(validate_all())

