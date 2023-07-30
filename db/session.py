import asyncio_redis
import config
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData
from fastapi import Depends


async def get_redis_client() -> asyncio_redis.Connection:
    """Dependency for getting Redis client"""
    connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
    try:
        yield connection
    finally:
        connection.close()
        await connection.wait_closed()

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
