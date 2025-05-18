# 风格相关MySQL数据库操作
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models import Style, Task

async def get_styles(db: AsyncSession, category_id=None):
    stmt = select(Style).options(joinedload(Style.category)).order_by(desc(Style.popular))
    if category_id:
        stmt = stmt.where(Style.category_id == category_id)
    result = await db.execute(stmt)
    styles = result.scalars().all()
    return [{
        **style.__dict__,
        'category_id': style.category_id,
        'category_name': style.category.name if style.category else None
    } for style in styles]

async def get_user_recent_styles(db: AsyncSession, user_id: int, limit: int = 10):
    stmt = (
        select(Style)
        .join(Task)
        .where(Task.user_id == user_id)
        .options(joinedload(Style.category))
        .order_by(desc(Task.created_at))
        .distinct()
        .limit(limit)
    )
    result = await db.execute(stmt)
    styles = result.scalars().all()
    return [{
        **style.__dict__,
        'category_id': style.category_id,
        'category_name': style.category.name if style.category else None
    } for style in styles]

async def create_style(db: AsyncSession, style: Style):
    db.add(style)
    await db.commit()
    await db.refresh(style)
    return style