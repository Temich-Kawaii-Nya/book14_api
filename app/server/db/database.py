from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.server.config import config
from app.server.models.book import Book
from app.server.models.collection import Collection
from app.server.models.description import Description
from app.server.models.quote import Quote
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.server.models.user import User


async def init_db():
    client = AsyncIOMotorClient(config.DATABASE_URL)
    await init_beanie(database=client[config.DATABASE_NAME], document_models=[Quote, Collection, User])
