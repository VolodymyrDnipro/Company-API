import asyncio
import asyncio_redis
import config
import json


async def qsave_data_to_redis():
    redis_connection = await create_redis_connection()

    quiz_results_with_company2 = [{
        "user_id": 3,
        "quiz_id": 8,
        "question_id": 14,
        "user_answer_id": 1,
        "result": 2,
        "company_id": 1
    }, {
        "user_id": 3,
        "quiz_id": 8,
        "question_id": 15,
        "user_answer_id": 2,
        "result": 2,
        "company_id": 1
    }]

    # Перетворюємо список у JSON-рядок
    quiz_results_json = json.dumps(quiz_results_with_company2)

    # Зберігаємо дані у Redis з ключем user_id на 48 годин (172800 секунд)
    await redis_connection.set(str(3), quiz_results_json)

    redis_connection.close()


async def create_redis_connection():
    # Параметри підключення до Redis
    redis_host = config.settings.REDIS_HOST
    redis_port = config.settings.REDIS_PORT

    redis_connection = await asyncio_redis.Connection.create(host=redis_host, port=redis_port)
    return redis_connection


if __name__ == "__main__":
    asyncio.run(save_data_to_redis())
