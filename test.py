import asyncio

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Замініть <connection_string> на вашу реальну рядок підключення до бази даних PostgreSQL
database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/db"

# Створюємо асинхронний engine
engine = create_async_engine(database_url, echo=True)

# Створюємо асинхронний сесійний фабрик
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Створюємо асинхронну сесію
async def create_async_session():
    async with async_session() as session:
        # Ваш код для роботи з асинхронною сесією
        # Наприклад, виконання запитів до бази даних
        query = text("SELECT * FROM your_table")
        result = await session.execute(query)
        records = result.fetchall()
        for record in records:
            print(record)

# Запускаємо асинхронну сесію
asyncio.run(create_async_session())
