import asyncio_redis
import config
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData
from fastapi import Depends


async def create_redis_connection():
    # Параметри підключення до Redis
    redis_host = config.settings.REDIS_HOST
    redis_port = config.settings.REDIS_PORT

    redis_connection = await asyncio_redis.Connection.create(host=redis_host, port=redis_port)
    return redis_connection


metadata = MetaData()

# create async engine for interaction with database
engine = create_async_engine(
    config.REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def get_session(db: Session = Depends(get_db)):
    return db
