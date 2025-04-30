from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    hashed_password: str
    email: str
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, username: str, password: str, email: str):
        """创建新用户，并对密码进行哈希处理"""
        hashed_password = pwd_context.hash(password)
        return cls(
            username=username,
            hashed_password=hashed_password,
            email=email
        )
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

class Style(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_template: str
    preview_image: Optional[str] = None
    category: Optional[str] = None
    is_popular: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

class Task(BaseModel):
    user_id: str
    style_id: str
    input_image: str  # 输入图片路径
    output_image: Optional[str] = None  # 输出图片路径
    custom_prompt: Optional[str] = None
    status: str  # pending, processing, completed, failed
    progress: Optional[float] = 0.0
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

class Credit(BaseModel):
    user_id: str
    amount: int = 0
    is_vip: bool = False
    last_vip_credit_date: Optional[datetime] = None