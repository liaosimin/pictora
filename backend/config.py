import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    # 应用设置
    APP_NAME: str = "Pictora"
    APP_DESCRIPTION: str = "AI图片生成应用"
    
    # MySQL设置
    MYSQL_URL: str = os.getenv("MYSQL_URL", "mysql+aiomysql://root:password@localhost:3306/pictora")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "pictora")
    
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