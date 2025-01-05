import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ..config.config import Config
from ..models.user import User


async def init_db(cfg: Config):
    logging.info(cfg.DATABASE_URL)
    client = AsyncIOMotorClient(cfg.DATABASE_URL)
    await init_beanie(database=client[cfg.DATABASE_NAME], document_models=[User])
