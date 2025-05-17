# 用户相关MySQL数据库操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

class UserDAO:
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: User):
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user