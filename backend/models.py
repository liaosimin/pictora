from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    hashed_password = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False, index=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    tasks = relationship('Task', back_populates='user')
    credits = relationship('Credit', back_populates='user')

class Style(Base):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    description = Column(Text)
    prompt_template = Column(Text, nullable=False)
    preview_image = Column(String(256))
    category = Column(String(64))
    is_popular = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
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