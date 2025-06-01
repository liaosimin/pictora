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
    MYSQL_URL: str = os.getenv("MYSQL_URL", "mysql+aiomysql://root@localhost:3306/pictora")
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

    WECHAT_APP_ID: str = "wx3edc988f119b34e4"
    WECHAT_APP_SECRET: str = "0486663f13cf35de49a6edc289d156f2"

settings = Settings()