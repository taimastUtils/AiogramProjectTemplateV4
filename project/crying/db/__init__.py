from asyncpg import ConnectionDoesNotExistError
from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

from ..config import TIME_ZONE
from ..config.db import PostgresDB, SqliteDB

__all__ = (
    "init_db",
    "close_db",
    "models",

)


async def close_db():
    await Tortoise.close_connections()
    logger.info(f"Database closed")


async def init_db(db: PostgresDB | SqliteDB):
    logger.debug(f"Initializing Database {db}...")
    MODELS_DIR = "crying.db.models"
    data = {
        "db_url": db.tortoise_url,
        "modules": {"models": [MODELS_DIR]},
        "timezone": str(TIME_ZONE),
    }
    try:
        await Tortoise.init(**data)
        await Tortoise.generate_schemas()
    except (ConnectionDoesNotExistError, DBConnectionError) as e:
        logger.warning(e)
        logger.info("Creating a new database ...")
        await Tortoise.init(**data, _create_db=True)
        await Tortoise.generate_schemas()
        logger.success(f"New database {db.database} created")

    logger.debug(f"Database {db} initialized")
