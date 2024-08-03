from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreateSchema


class UserRepository:

    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        stmt = select(User).where(email == User.email)
        user = await db.execute(stmt)
        return user.scalars().first()

    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> User:
        stmt = select(User).where(user_id == User.id)
        user = await db.execute(stmt)
        return user.scalars().first()

    async def create_user(self, user: UserCreateSchema, db: AsyncSession) -> User:
        stmt = insert(User).values(**user)
        await db.execute(stmt)
        stmt = select(User).where(user.email == User.email)
        user = await db.execute(stmt)
        return user.scalars().first()
