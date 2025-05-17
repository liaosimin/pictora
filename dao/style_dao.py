# 风格相关MySQL数据库操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Style

async def get_styles(db: AsyncSession, category=None, popular=None):
    stmt = select(Style)
    if category:
        stmt = stmt.where(Style.category == category)
    if popular is not None:
        stmt = stmt.where(Style.is_popular == popular)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_style(db: AsyncSession, style: Style):
    db.add(style)
    await db.commit()
    await db.refresh(style)
    return style