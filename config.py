from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()

REAL_DATABASE_URL = env.str("REAL_DATABASE_URL", default="postgresql+asyncpg://postgres:postgres@postgres:5432/db")
TEST_DATABASE_URL = env.str("TEST_DATABASE_URL", default="postgresql+asyncpg://postgres:postgres@postgres_test:5433/db_test")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=3000)
SECRET_KEY: str = env.str("SECRET_KEY", default="cAtwa1kkEy")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    LOG_LEVEL: str = "DEBUG"

    SERVER_PORT: int
    SERVER_HOST: str

    # database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # database_test
    DB_TEST_USER: str
    DB_TEST_PASSWORD: str
    DB_TEST_HOST: str
    DB_TEST_PORT: int
    DB_TEST_NAME: str

    DATABASE_MAX_CONNECTIONS: int
    DATABASE_CONNECTION_RECYCLE: int

    # redis
    REDIS_HOST: str
    REDIS_PORT: int

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


settings = Settings()
