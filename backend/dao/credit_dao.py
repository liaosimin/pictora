# 积分相关MySQL数据库操作
from sqlalchemy.orm import Session
from models import Credit

def get_credit_by_user_id(db: Session, user_id: int):
    return db.query(Credit).filter(Credit.user_id == user_id).first()

def create_credit(db: Session, credit: Credit):
    db.add(credit)
    db.commit()
    db.refresh(credit)
    return credit

def update_credit_amount(db: Session, user_id: int, amount: int):
    credit = db.query(Credit).filter(Credit.user_id == user_id).first()
    if credit:
        credit.amount = amount
        db.commit()
        db.refresh(credit)
    return credit