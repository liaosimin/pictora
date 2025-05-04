# 积分相关MySQL数据库操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Credit

async def get_credit_by_user_id(db: AsyncSession, user_id: int):
    stmt = select(Credit).where(Credit.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_credit(db: AsyncSession, credit: Credit):
    db.add(credit)
    await db.commit()
    await db.refresh(credit)
    return credit

async def update_credit_amount(db: AsyncSession, user_id: int, amount: int):
    stmt = select(Credit).where(Credit.user_id == user_id)
    result = await db.execute(stmt)
    credit = result.scalar_one_or_none()
    if credit:
        credit.amount = amount
        await db.commit()
        await db.refresh(credit)
    return credit