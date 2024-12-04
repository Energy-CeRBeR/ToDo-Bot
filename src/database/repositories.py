from typing import Optional
from sqlalchemy import select, insert, update

from .database import async_session
from .models import User


class UserRepository:
    async def create_user(self, user_id: int, username: str, first_name: str, last_name: str) -> Optional[User]:
        async with async_session() as session:
            stmt = insert(User).values(id=user_id, username=username, first_name=first_name, last_name=last_name)
            await session.execute(stmt)
            await session.commit()

            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()

        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()

        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalars().first()

        return user

    async def refresh_tokens(self, user_id: int, access_token: str, refresh_token: str) -> Optional[User]:
        async with async_session() as session:
            query = update(User).where(User.id == user_id).values(
                access_token=access_token, refresh_token=refresh_token
            )
            await session.execute(query)
            await session.commit()

            user = await self.get_user_by_id(user_id)

        return user
