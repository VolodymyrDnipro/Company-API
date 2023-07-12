import asyncio_redis
import asyncpg

from config import settings


async def open_redis_connection():
    connection = await asyncio_redis.Connection.create(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return connection


async def close_redis_connection(connection):
    connection.close()
    await connection.wait_closed()


async def open_postgres_connection():
    connection = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    return connection


async def close_postgres_connection(connection):
    await connection.close()

