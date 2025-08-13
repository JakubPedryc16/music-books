from app.db.database import Base
from app.db.db_async import engine
from app.models import Book, Music, Tag, book_tag_association, music_tag_association

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
