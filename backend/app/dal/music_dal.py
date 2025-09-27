from typing import List, Optional
from sqlalchemy import ColumnElement, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from app.models.music import Music

class MusicDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_music_columns(
        self,
        columns: Optional[List[ColumnElement]] = None,
        filter_not_none: Optional[List[ColumnElement]] = None
    ) -> List[Music]:
        query = select(Music)

        if columns is not None:
            query = query.options(load_only(*columns))

        if filter_not_none is not None:
            for col in filter_not_none:
                query = query.where(col != None)

        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_all_by_ids(self, ids: list[int]) -> list[Music]:
        query = select(Music).where(Music.id.in_(ids))
        result = await self.session.scalars(query)
        return result.all()
