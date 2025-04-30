import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    # 应用设置
    APP_NAME: str = "Pictora"
    APP_DESCRIPTION: str = "AI图片生成应用"
    
    # MongoDB设置
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "pictora_db")
    
    # OpenAI设置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # JWT设置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 文件存储设置
    UPLOAD_DIR: str = "uploads"
    RESULTS_DIR: str = "results"

# 创建设置实例
settings = Settings()