from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
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

# 创建MySQL异步引擎
engine = create_async_engine(settings.MYSQL_URL, echo=True, future=True)

# 创建Session工厂
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# 获取数据库Session
async def get_db():
    async with async_session() as session:
        yield session