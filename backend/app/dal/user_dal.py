from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_spotify_id(self, spotify_id: str) -> Optional[User]:
        query = select(User).where(User.spotify_id == spotify_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_or_update(
        self,
        spotify_id: str,
        display_name: Optional[str],
        email: Optional[str],
        access_token: str,
        refresh_token: str,
        expires_in: int
    ) -> User:
        user = await self.get_by_spotify_id(spotify_id)
        token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        if not user:
            user = User(
                spotify_id=spotify_id,
                display_name=display_name,
                email=email,
                access_token=access_token,
                refresh_token=refresh_token,
                token_expires_at=token_expires_at
            )
            self.session.add(user)
        else:
            user.display_name = display_name
            user.email = email
            user.access_token = access_token
            user.refresh_token = refresh_token
            user.token_expires_at = token_expires_at

        await self.session.commit()
        await self.session.refresh(user)
        return user
