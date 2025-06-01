# 风格相关MySQL数据库操作
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models import Style, Task, StyleCategory

async def get_styles(db: AsyncSession, category_id=None, limit: int = 10, offset: int = 0):
    stmt = select(Style).options(joinedload(Style.category)).order_by(desc(Style.popular))
    if category_id:
        stmt = stmt.where(Style.category_id == category_id)
    stmt = stmt.limit(limit).offset(offset)
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

async def get_style_categories(db: AsyncSession, limit: int = 10, offset: int = 0):
    stmt = select(StyleCategory).order_by(desc(StyleCategory.popular)).limit(limit).offset(offset)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return [{
        **category.__dict__,
        'id': category.id,
        'name': category.name,
        'popular': category.popular
    } for category in categories]