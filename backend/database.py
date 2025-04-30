from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# 数据库连接客户端
client = None

# 获取数据库连接
async def get_database():
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    db = client[settings.DATABASE_NAME]
    return db