from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.server.config import config
from app.server.models.user import User


async def init_db():
    client = AsyncIOMotorClient(config.DATABASE_URL)
    await init_beanie(database=client[config.DATABASE_NAME], document_models=[User])
