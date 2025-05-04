# 用户相关MySQL数据库操作
from sqlalchemy.orm import Session
from models import User

class UserDAO:
    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user