from src.db.database import Base
from src.db.db_async import engine
from src.models import Book, Music, Tag, book_tag_association, music_tag_association

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
