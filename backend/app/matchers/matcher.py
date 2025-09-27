from app.models.music import Music
from sqlalchemy.ext.asyncio import AsyncSession

class Matcher:
    async def match(
        self,
        session: AsyncSession,
        text: str,
        amount: int = 5,
        music_list_included:list[Music] = []
    ) -> list[tuple[int, float]]:
        raise NotImplementedError
        return []
