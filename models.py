from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.dialects.mysql import JSON # 或者其他数据库对应的 JSON 类型
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=True, index=True)  # 允许为空，因为微信用户可能没有用户名
    hashed_password = Column(String(128), nullable=True)  # 允许为空，微信用户不需要密码
    email = Column(String(128), unique=True, nullable=True, index=True)  # 允许为空，微信用户可能没有邮箱
    openid = Column(String(64), unique=True, nullable=True, index=True)  # 微信用户的唯一标识
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    recently_used_styles = Column(JSON)
    tasks = relationship('Task', back_populates='user')
    credits = relationship('Credit', back_populates='user')
    is_new = Column(Boolean, default=True)  # 标记是否为新用户

    @classmethod
    def create_wechat_user(cls, openid: str):
        """创建微信用户"""
        return cls(
            openid=openid,
            username=f"wx_user_{openid[:8]}",  # 生成临时用户名
            is_new=True
        )

class StyleCategory(Base):
    __tablename__ = 'style_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)
    popular = Column(Integer, default=0)
    styles = relationship('Style', back_populates='category')

class Style(Base):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    description = Column(Text)
    prompt_template = Column(Text, nullable=False)
    preview_image = Column(String(256))
    category_id = Column(Integer, ForeignKey('style_categories.id'), nullable=True, index=True) # Changed to category_id
    popular = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    category = relationship('StyleCategory', back_populates='styles') # Relationship to StyleCategory
    tasks = relationship('Task', back_populates='style')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    style_id = Column(Integer, ForeignKey('styles.id'), nullable=False, index=True)
    input_image = Column(String(256), nullable=False)
    output_image = Column(String(256))
    custom_prompt = Column(Text)
    status = Column(String(32), nullable=False, index=True)
    progress = Column(Float, default=0.0)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    user = relationship('User', back_populates='tasks')
    style = relationship('Style', back_populates='tasks')

class Credit(Base):
    __tablename__ = 'credits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    amount = Column(Integer, default=0)
    is_vip = Column(Boolean, default=False)
    last_vip_credit_date = Column(DateTime)
    user = relationship('User', back_populates='credits')