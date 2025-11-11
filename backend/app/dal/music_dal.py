from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.DataAccessException import DataAccessException
from app.models.music import Music
from app.utils.logger import logger 

class MusicDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_music_columns(
        self,
        columns: Optional[List[ColumnElement]] = None,
        filter_not_none: Optional[List[ColumnElement]] = None
    ) -> List[Music]:
        try:
            query = select(Music)

            if columns is not None:
                query = query.options(load_only(*columns))

            if filter_not_none is not None:
                for col in filter_not_none:
                    query = query.where(col != None)

            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_music_columns: {e}")
            raise DataAccessException(f"Failed to fetch music columns: {e}")

    async def get_all_by_ids(self, ids: list[int]) -> list[Music]:
        try:
            query = select(Music).where(Music.id.in_(ids))
            result = await self.session.scalars(query)
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_all_by_ids: {e}")
            raise DataAccessException(f"Failed to fetch music by IDs: {e}")
